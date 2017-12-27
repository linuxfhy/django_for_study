from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, NameModel, UserModel
from .models import NameForm, UserForm, FormAndModelDict, PRJ_NAME_LIST
from .FSM import WorkFlowFSM
from django.contrib.auth.models import User, Permission,Group
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django import forms

from django.http import HttpResponse
from xlwt import *
import os
from io import StringIO,BytesIO
AuthDict = {
    '管理权限':'ManageAuth',
    '使用权限':'ExecAuth',
    '访问权限':'VisitAuth'
}
GrpDict = {
    '注册用户群组':'RegisteredUserGrp',
    '用户群组':'UserGrp',
    '管理员群组':'AdminGrp',
}

class AuthGrpAdmin(forms.Form):
    group_key = forms.CharField(label='群组名称', max_length=100)
    auty_key = forms.CharField(label='权限', max_length=100)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class NameModelView(generic.ListView):
    template_name = 'polls/flowindex.html'
    context_object_name = 'latest_namemodel_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return NameModel.objects.filter(assigned_to=self.request.user).order_by('id')[:]
        #return NameModel.objects.order_by('id')[:]

def flowindex(request, prj_name='improvement'):
    GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
    obj_list = GenericModel.objects.order_by('id')[:]
    username = request.user.username
    return render(request, 'polls/flowindex.html', {'latest_namemodel_list':obj_list, 'prj_name':prj_name, 'username':username})

def flow_index_for_current_user(request, prj_name='improvement'):
    GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
    obj_list = GenericModel.objects.filter(
                                               Q(assigned_to=request.user) | Q(assigned_to='anyone'),
                                               ~Q(curent_state='关闭')
                                          ).order_by('id')[:]
    username = request.user.username
    return render(request, 'polls/flowindex.html', {'latest_namemodel_list':obj_list, 'prj_name':prj_name, 'username':username})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def get_attr_value(request, get_method):
    if get_method == 'get_current_user':
        return request.user.username
def check_trans_condition(request, model_instance, trans_condition):
    for field_name in trans_condition:
        for field_tmp in model_instance._meta.get_fields():
            if field_tmp.verbose_name == field_name:  #found field
                attr_value = getattr(model_instance, field_tmp.name)
                if trans_condition[field_name]['op'] == '!=':
                    if not attr_value != trans_condition[field_name]['value']:
                        return False
                elif trans_condition[field_name]['op'] == '==':
                    if not attr_value == trans_condition[field_name]['value']:
                        return False
    return True

def excute_trans_action(request, model_instance, after_trans_action):
    if 'assign_to' in after_trans_action:
        if after_trans_action['assign_to'] == 'anyone':
            model_instance.assigned_to = 'anyone'
        elif 'constant' in after_trans_action['assign_to']:
            user_name = after_trans_action['assign_to']['constant'] 
            userinfo = User.objects.filter(username=user_name)
            if not userinfo:
                return {'func_rc':False, 'error_message':'请给<\'assign_to\':\'constant\'>指定合适的人，系统中无此用户:'+user_name}
            model_instance.assigned_to = user_name 
        else:
            field_found = False
            for field in model_instance._meta.get_fields():
                if field.verbose_name == after_trans_action['assign_to']:
                    attr_value = getattr(model_instance, field.name)
                    model_instance.assigned_to = attr_value
                    field_found = True
            if field_found == False:
                return {'func_rc':False, 'error_message':'无法指派给<'+after_trans_action['assign_to']+'>，系统无此字段'}
            if attr_value != 'anyone':
                userinfo = User.objects.filter(username=attr_value)
                if not userinfo:
                    return {'func_rc':False, 'error_message':'请给<'+after_trans_action['assign_to']+'>指定合适的人，系统中无此用户:'+attr_value}
    if 'set_fields' in after_trans_action:
        for field_1 in after_trans_action['set_fields']:
            field_found = False
            for field_2 in model_instance._meta.get_fields():
                if field_2.verbose_name == field_1:
                    setattr(model_instance, field_2.name, after_trans_action['set_fields'][field_1])
                    field_found = True
            if field_found == False:
                return {'func_rc':False, 'error_message':'无法将<'+field_1+'>设置为:'+after_trans_action['set_fields'][field_1]+'，系统无此字段'}
    if 'set_field_nonconstant' in after_trans_action:
        for field_1 in after_trans_action['set_field_nonconstant']:
            field_found = False
            for field_2 in model_instance._meta.get_fields():
                if field_2.verbose_name == field_1:
                    get_method = after_trans_action['set_field_nonconstant'][field_1]
                    attr_value = get_attr_value(request, get_method)
                    setattr(model_instance, field_2.name, attr_value)
                    field_found = True
            if field_found == False:
                return {'func_rc':False, 'error_message':'无法将<'+field_1+'>设置为:'+attr_value+'，系统无此字段'}
    return{'func_rc':True}

def myflowdetail(request, model_id, prj_name='improvement'):
    if not request.user.is_authenticated():
        return render(request, 'polls/flowhome.html')
    else:
        workflowfsm = WorkFlowFSM(prj_name)
        GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
        GenericForm = FormAndModelDict[prj_name]['PrjFormClass']
        if request.method == 'POST':
            model_instance = GenericModel.objects.get(pk=model_id)
            form_instance = GenericForm(request.POST, instance=model_instance)
            #Done:Add code for state trans here
            form_instance.save()
            trigger = request.POST['trigger']
            after_trans_action = workflowfsm.FSM_get_trans_action(prj_name, model_instance.curent_state, trigger)
            func_rc_dict = excute_trans_action(request, model_instance, after_trans_action)
            if func_rc_dict['func_rc'] == False:
                return HttpResponse(func_rc_dict['error_message'])
            model_instance.curent_state = workflowfsm.FSM_get_triger_and_desstate(model_instance.curent_state)[trigger]['dest']
            model_instance.save()
            #return HttpResponseRedirect(reverse('polls:flowprjhome', kwargs={'prj_name':prj_name}))
            return HttpResponseRedirect(reverse('polls:flowdetail', kwargs={'prj_name':prj_name,'model_id':model_id}))
        else:
            visit_perm_str = 'polls.'+prj_name+'_'+AuthDict['访问权限']
            if not request.user.has_perm(visit_perm_str):
                return HttpResponse('您没有访问权限:%s'%visit_perm_str)

            namemodel = get_object_or_404(GenericModel, pk=model_id)
            form = GenericForm(instance=namemodel)

            if 'PrjAuth' in FormAndModelDict[prj_name]:
                 if 'visit' in FormAndModelDict[prj_name]['PrjAuth']:
                     if 'role' in FormAndModelDict[prj_name]['PrjAuth']['visit']:
                         can_visit = False
                         for elmt in FormAndModelDict[prj_name]['PrjAuth']['visit']['role']:
                             if elmt == 'Creator' and namemodel.created_by == request.user.username:
                                 can_visit = True
                             elif elmt == 'Processor' and namemodel.assigned_to == request.user.username:
                                 can_visit = True
                             elif elmt == 'Administrator' and request.user.has_perm('polls.'+prj_name+'_'+AuthDict['管理权限']):
                                 can_visit = True
                         if not can_visit:
                             return HttpResponse('您不能访问不是您创建的问题')
            #Done:Add code for state trans here
            triggerlist = []
            if namemodel.assigned_to in [request.user.username ,'anyone']:
                triggerlist = workflowfsm.FSM_get_trigger(namemodel.curent_state) #Delete those trigger which doesn't match trans condition
                if triggerlist:
                    triggerlist_cpy = triggerlist[:]
                    for trigger_tmp in triggerlist:
                        trans_condition = workflowfsm.FSM_get_triger_and_desstate(namemodel.curent_state)[trigger_tmp]['condition']
                        if check_trans_condition(request, namemodel, trans_condition) == False:
                            triggerlist_cpy.remove(trigger_tmp)
                    triggerlist = triggerlist_cpy
                else:
                    triggerlist = []
            PrjNameZh = FormAndModelDict[prj_name]['PrjNameZh']
            return render(request, 'polls/flowdetail.html', {'form':form, 'model_id':model_id,'trigger':triggerlist, 'prj_name':prj_name, 'PrjNameZh':PrjNameZh})
            #return HttpResponse("hello")

def flow_create_question(request, prj_name='improvement'):
    #print('enter my flow ,project name is %s'%prj_name)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        GenericForm = FormAndModelDict[prj_name]['PrjFormClass']
        form = GenericForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #TODO:check model field and database colum
            model_instance = form.save()
            #return HttpResponse("Hello, world. Thanks for submit.")
            #return HttpResponseRedirect(reverse('polls:PrjIndexForCurUser', kwargs={'prj_name':prj_name}))
            return HttpResponseRedirect(reverse('polls:flowdetail', kwargs={'prj_name':prj_name,'model_id':model_instance.id}))
    # if a GET (or any other method) we'll create a blank form
    else:
        cur_user = request.user
        if not cur_user.is_authenticated():
            return HttpResponse('无权限，请先注册登录')#DONE:return 403 error

        exec_perm_str = 'polls.'+prj_name+'_'+AuthDict['使用权限']

        if not cur_user.has_perm(exec_perm_str):
            return HttpResponse('没有创建权限%s，请联系该项目管理员'%exec_perm_str)

 
        workflowfsm = WorkFlowFSM(prj_name=prj_name)
        init_state = workflowfsm.FSM_get_init_state() 
        current_user = request.user.username
        #根据项目不同，产生不同的NameForm，学习为下拉框类型字段添加内容，用于增加项目
        GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
        GenericForm = FormAndModelDict[prj_name]['PrjFormClass']
        #print('GET method ,ZH project name is %s'%FormAndModelDict[prj_name]['PrjNameZh'])
        #print('project name is %s'%FormAndModelDict[prj_name]['prjname'])
        model_instance = GenericModel()
        if model_instance.assigned_to == 'anyone':
            assigned_to = 'anyone'
        else:
            assigned_to = current_user
        form = GenericForm(initial={'curent_state':init_state, 'created_by':current_user, 'assigned_to':assigned_to})
        #if form.fields['assigned_to'] != 'anyone':
        #    form.fields['assigned_to'] = current_user
        PrjNameZh = FormAndModelDict[prj_name]['PrjNameZh']
    return render(request, 'polls/name.html', {'form':form,'prj_name':prj_name, 'PrjNameZh':PrjNameZh})

def myflowprocess(request):
    return HttpResponse("Hello, world. This is form processing result.")


def flowlogin(request):
    class LoginForm(forms.Form):
        username = forms.CharField(label='用户名')
        password = forms.CharField(label='密码', widget = forms.PasswordInput)
    if request.method == 'POST':
        userform = LoginForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('polls:flowhome'))# A backend authenticated the credentials
            else:
                # No backend authenticated the credentials
                return HttpResponse('login fail!!!')
    else:
        userform = LoginForm()
    return render(request, 'polls/flowlogin.html',{'form':userform})

def flowlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:flowhome'))

def flowhome(request):
    #DONE:添加当前登录用户显示。让项目名称显示更为灵活
    #TODO:增加项目名检查，保证项目名不重复
    #DONE:不登录也可以查看项目名称，将权限检查放到各个项目中
    class PrjInfo(object):
        def __init__(self, prj_name, prj_name_zh, assigned_count):
            self.prj_name = prj_name
            self.prj_name_zh = prj_name_zh
            self.assigned_count = assigned_count
    prj_list = []
    for prj_instance in PRJ_NAME_LIST:
        GenericModel = FormAndModelDict[prj_instance]['PrjModelClass']
        assigned_count = GenericModel.objects.filter(
                                                     Q(assigned_to=request.user.username),
                                                     ~Q(curent_state='关闭')
                                                    ).count()
        prj_info_node = PrjInfo(prj_name = prj_instance, prj_name_zh = FormAndModelDict[prj_instance]['PrjNameZh'], assigned_count = assigned_count)
        prj_list.append(prj_info_node)
    if request.user.is_authenticated():
        username = request.user.username
        return render(request, 'polls/flowhome.html', {'prj_list':prj_list,'username':username})
    else:
        return render(request, 'polls/flowhome.html', {'prj_list':prj_list})

def flowprjhome(request, prj_name):
    visit_perm = 'polls.'+prj_name+'_'+AuthDict['访问权限']
    if not request.user.has_perm(visit_perm):
        return HttpResponse('您没有权限访问该项目，所需权限%s'%visit_perm)#DONE:return 403 error
    if request.user.is_authenticated():
        prj_name_zh = FormAndModelDict[prj_name]['PrjNameZh']
        GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
        obj_list = GenericModel.objects.filter(
                                               Q(assigned_to=request.user.username)|Q(assigned_to='anyone'),
                                               ~Q(curent_state='关闭')
                                              ).order_by('id')[:]
        return render(request, 'polls/flowprjhome.html',{'prj_name':prj_name,'prj_name_zh':prj_name_zh, 'obj_list':obj_list})
    else:
        return render(request, 'polls/flowhome.html')

##############################For Auth Admin:Begin##############################
def add_auth_to_group(GenericModel, group, auth_str, op):
    content_type = ContentType.objects.get_for_model(GenericModel)
    try:
        permission = Permission.objects.get(
            codename = auth_str,
            content_type=content_type,
        )
    except Permission.DoesNotExist:
        permission = Permission.objects.create(
            codename=auth_str,
            name=auth_str,
            content_type=content_type,
        )
        permission.save()
    if op == 'add':
        group.permissions.add(permission)
    elif op == 'delete':
        group.permissions.remove(permission)
    group.save() #fix bug：Exception Value:"<Group: AdminGrp>" needs to have a value for field "id" before this many-to-many relationship can be used.

def add_prj_auth_to_group(prj_name, grp_key, auth_key, op='add'):
    GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
    group_name_EN = GrpDict[grp_key]
    grp_name = prj_name+'_'+group_name_EN
    try:
        group_obj = Group.objects.get(name=grp_name)
    except Group.DoesNotExist:
        group_obj = Group.objects.create(name=grp_name)
        group_obj.save()
    auth_val = prj_name+'_'+AuthDict[auth_key]
    add_auth_to_group(GenericModel, group_obj, auth_val, op)

def add_user_to_group(prj_name, grp_key, user_key, op):
    group_name_EN = GrpDict[grp_key]
    grp_name = prj_name+'_'+group_name_EN
    group_obj = Group.objects.get(name=grp_name)
    user_obj = User.objects.get(username=user_key)
    if op == 'add':
        user_obj.groups.add(group_obj)
    elif op == 'delete':
        user_obj.groups.remove(group_obj)

#DONE:这里应该增加权限控制，避免非管理员用户操作权限i
def flow_grp_auth_admin(request, prj_name):
    class AuthGrpAdmin(forms.Form):
        group_key = forms.ChoiceField(label='群组名称', choices=((key, key) for key in GrpDict))
        auth_key = forms.MultipleChoiceField(label='权限', choices=((key, key) for key in AuthDict)
                                            ,help_text='按住Ctrl可多选')
                                             # ,widget=forms.CheckboxSelectMultiple())

    group_name_EN = GrpDict['注册用户群组']
    grp_name = prj_name+'_'+group_name_EN

    try:
        group_obj = Group.objects.get(name=grp_name)
    except Group.DoesNotExist:
        group_obj = Group.objects.create(name=grp_name)
        group_obj.save()
    
    if request.user.username == 'superadmin':
        user_list = User.objects.all()
    else:
        user_list = User.objects.filter(groups__name=grp_name)

    manage_perm_str = 'polls.'+prj_name+'_'+AuthDict['管理权限']
    if not (request.user.username == 'superadmin' or request.user.has_perm(manage_perm_str)):
        return HttpResponse('您没有权限管理该项目')
 
    class AuthUsrAdmin(forms.Form):
        group_key = forms.ChoiceField(label='群组名称', choices=((key, key) for key in GrpDict))
        user_key = forms.MultipleChoiceField(label='用户名', choices=((key.username, key.username) for key in user_list))
    if request.method == 'POST':
        if request.POST['trigger'] == "为群组添加权限":
            authform = AuthGrpAdmin(request.POST)
            if authform.is_valid():
                grp_key = authform.cleaned_data['group_key']
                for auth_key in authform.cleaned_data['auth_key']:
                    add_prj_auth_to_group(prj_name, grp_key, auth_key, op='add')
        elif request.POST['trigger'] == "从群组删除权限":
            authform = AuthGrpAdmin(request.POST)
            if authform.is_valid():
                grp_key = authform.cleaned_data['group_key']
                for auth_key in authform.cleaned_data['auth_key']:
                    add_prj_auth_to_group(prj_name, grp_key, auth_key, op='delete')
        elif request.POST['trigger'] == "添加用户到群组":
            GrpUserForm = AuthUsrAdmin(request.POST)
            if GrpUserForm.is_valid():
                grp_key = GrpUserForm.cleaned_data['group_key']
                for user_key in GrpUserForm.cleaned_data['user_key']:
                    add_user_to_group(prj_name, grp_key, user_key, op='add')
        elif request.POST['trigger'] == "从群组移除用户":
            GrpUserForm = AuthUsrAdmin(request.POST)
            if GrpUserForm.is_valid():
                grp_key = GrpUserForm.cleaned_data['group_key']
                for user_key in GrpUserForm.cleaned_data['user_key']:
                    add_user_to_group(prj_name, grp_key, user_key, op='delete')
        return HttpResponseRedirect(reverse('polls:flowgrpauthadmin', kwargs={'prj_name':prj_name}))
    else:
        AddAuthToGrpForm = AuthGrpAdmin()
        AddUserToGrpForm = AuthUsrAdmin()
        return render(request, 'polls/flowgrpauthadmin.html',{'AddUserToGrpForm':AddUserToGrpForm,'AddAuthToGrpForm':AddAuthToGrpForm,'prj_name':prj_name})

def flowregist(request, prj_name='Null'):
    class UserRegForm(forms.Form):
        username = forms.CharField(label='用户名')
        password = forms.CharField(label='密码', widget = forms.PasswordInput)
        email = forms.CharField(label='邮箱')
    if request.method == 'POST':
        userform = UserRegForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            email = userform.cleaned_data['email']
            password = userform.cleaned_data['password']
            userinfo = User.objects.filter(username=username)
            if prj_name == 'Null':
                if userinfo:
                    return HttpResponse('User name %s has been occupied, please change another usename.'%username)
                user = User.objects.create_user(username, email, password)
                user.save()
                #return HttpResponse('regist success!!!')
                return HttpResponseRedirect(reverse('polls:flowlogin'))
            else:
                if userinfo:
                    return HttpResponse('User name %s has been occupied, please contact the project administrator for authority'%username)
                user = User.objects.create_user(username, email, password)
                user.save()
                group_name_EN = GrpDict['注册用户群组']
                grp_name = prj_name+'_'+group_name_EN
                try:
                    group_obj = Group.objects.get(name=grp_name)
                except Group.DoesNotExist:
                    group_obj = Group.objects.create(name=grp_name)
                user.groups.add(group_obj)
                #return HttpResponse('regist success!!!')
                return HttpResponseRedirect(reverse('polls:flowlogin'))
    else:
        userform = UserRegForm()
        if prj_name == 'Null':
            return render(request, 'polls/flowregist.html',{'form':userform})
        else:
            return render(request, 'polls/flowregist.html',{'form':userform,'prj_name':prj_name})

##############################For Auth Admin:End  ##############################

##############################For Data Import And Export:Begin##############################
#TODO:Process exception that model instance doesn't exist
def flow_export_excel(request, prj_name='improvement'):
    GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
    obj_list = GenericModel.objects.order_by('id')[:]
    if not obj_list:
        return HttpResponse('没有数据记录可以导出')
    ws = Workbook(encoding='utf-8')
    w = ws.add_sheet(u"数据报表第一页")
    col_number = 0
    for field in obj_list[0]._meta.get_fields():
        w.write(0, col_number, field.verbose_name)
        col_number = col_number + 1
    row_number = 1
    for obj in obj_list:
        col_number = 0
        for field in obj_list[0]._meta.get_fields():
            field_value = getattr(obj, field.name)
            w.write(row_number, col_number, field_value)
            col_number = col_number + 1
        row_number = row_number + 1
    filename = prj_name+'.xls'
    exist_file = os.path.exists(filename)
    if exist_file:
        os.remove(filename)
    ws.save(filename)
    ############################
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+filename
    response.write(sio.getvalue())
    return response
##############################For Data Import And Export:End##############################

##############################For Delete Item From Database:Begin##############################
def flow_muti_item_process(request, prj_name):
    admin_perm = 'polls.'+prj_name+'_'+AuthDict['管理权限']
    if not request.user.has_perm(admin_perm):
        return HttpResponse('您没有权限删除问题，请联系项目管理员')
    check_box_list = request.POST.getlist("check_box_list")
    GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
    if request.method == 'POST':
        for elmt in check_box_list:
           GenericModel.objects.get(id=elmt).delete()
        return HttpResponseRedirect(reverse('polls:myflowindex', kwargs={'prj_name':prj_name}))
    else:
        return HttpResponse('Get')
##############################For Delete Item From Database:Begin##############################





