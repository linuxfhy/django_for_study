from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, NameModel, UserModel
from .models import NameForm, UserForm, FormAndModelDict
from .FSM import WorkFlowFSM
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


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
    obj_list = GenericModel.objects.filter( Q(assigned_to=request.user) | Q(assigned_to='anyone')).order_by('id')[:] 
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
        namemodel = get_object_or_404(GenericModel, pk=model_id)
        form = GenericForm(instance=namemodel)
        #Done:Add code for state trans here
        triggerlist = []
        if namemodel.assigned_to in [request.user.username ,'anyone']:
            triggerlist = workflowfsm.FSM_get_trigger(namemodel.curent_state) #TODO:delete those trigger which doesn't match trans condition
            triggerlist_cpy = triggerlist[:]
            for trigger_tmp in triggerlist:
                trans_condition = workflowfsm.FSM_get_triger_and_desstate(namemodel.curent_state)[trigger_tmp]['condition']
                if check_trans_condition(request, namemodel, trans_condition) == False:
                    triggerlist_cpy.remove(trigger_tmp)
            triggerlist = triggerlist_cpy
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
            form.save()
            #return HttpResponse("Hello, world. Thanks for submit.")
            return HttpResponseRedirect(reverse('polls:PrjIndexForCurUser', kwargs={'prj_name':prj_name}))
    # if a GET (or any other method) we'll create a blank form
    else:
        workflowfsm = WorkFlowFSM(prj_name=prj_name)
        init_state = workflowfsm.FSM_get_init_state() 
        current_user = request.user.username
        #根据项目不同，产生不同的NameForm，学习为下拉框类型字段添加内容，用于增加项目
        GenericForm = FormAndModelDict[prj_name]['PrjFormClass']
        #print('GET method ,ZH project name is %s'%FormAndModelDict[prj_name]['PrjNameZh'])
        #print('project name is %s'%FormAndModelDict[prj_name]['prjname'])
        form = GenericForm(initial={'curent_state':init_state, 'created_by':current_user, 'assigned_to':'anyone'})
        PrjNameZh = FormAndModelDict[prj_name]['PrjNameZh']
    return render(request, 'polls/name.html', {'form':form,'prj_name':prj_name, 'PrjNameZh':PrjNameZh})

def myflowprocess(request):
    return HttpResponse("Hello, world. This is form processing result.")

def flowregist(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            email = userform.cleaned_data['email']
            password = userform.cleaned_data['password']

            userinfo = User.objects.filter(username=username)
            if userinfo:
                return HttpResponse('User name %s has been occupied, please change another usename.'%username)

            user = User.objects.create_user(username, email, password)
            user.save()
            #return HttpResponse('regist success!!!')
            return HttpResponseRedirect(reverse('polls:flowlogin'))
    else:
        userform = UserForm()
    return render(request, 'polls/flowregist.html',{'form':userform})

def flowlogin(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
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
        userform = UserForm()
    return render(request, 'polls/flowlogin.html',{'form':userform})

def flowlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:flowhome'))

def flowhome(request):
    #TODO:添加当前登录用户显示。让项目名称显示更为灵活
    if request.user.is_authenticated():
        class PrjInfo(object):
            def __init__(self, prj_name, prj_name_zh, assigned_count):
                self.prj_name = prj_name
                self.prj_name_zh = prj_name_zh
                self.assigned_count = assigned_count
        prj_list = []
        for prj_instance in FormAndModelDict:
            GenericModel = FormAndModelDict[prj_instance]['PrjModelClass']
            assigned_count = GenericModel.objects.filter(assigned_to=request.user.username).count()
            prj_info_node = PrjInfo(prj_name = prj_instance, prj_name_zh = FormAndModelDict[prj_instance]['PrjNameZh'], assigned_count = assigned_count)
            prj_list.append(prj_info_node)
        username = request.user.username
        return render(request, 'polls/flowhome.html', {'prj_list':prj_list,'username':username})
    else:
        return render(request, 'polls/flowhome.html')

def flowprjhome(request, prj_name):
    prj_name_zh = FormAndModelDict[prj_name]['PrjNameZh']
    GenericModel = FormAndModelDict[prj_name]['PrjModelClass']
    obj_list = GenericModel.objects.filter(Q(assigned_to=request.user.username)|Q(assigned_to='anyone')).order_by('id')[:]
    return render(request, 'polls/flowprjhome.html',{'prj_name':prj_name,'prj_name_zh':prj_name_zh, 'obj_list':obj_list})

