import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
############################################################################################################################################################
class UserModel(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(default="example@example.com")

class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }
############################################################################################################################################################
#改进建议提取
class NameModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要")
    detail = models.CharField(max_length=5000, verbose_name="详细描述")
    current_process = models.CharField(max_length=5000, verbose_name="处理进展",default="##由改进实施人填写##")
    #viewer_advice = models.CharField(max_length=5000, verbose_name="评审人意见",default="##由评审人填写##")
    value = models.CharField(max_length=200, default="0", verbose_name="改进价值评估")
    reviewer = models.CharField(max_length=200, default="#提交人填写#", verbose_name="改进建议评审人")
    executor = models.CharField(max_length=200, default="#由建议评审人指派#", verbose_name="改进建议实施人")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class NameForm(ModelForm):
    class Meta:
        model = NameModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':79}),
            'value' : forms.TextInput(attrs={'cols': 80, 'rows': 1}),
            'current_process' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'detail' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
############################################################################################################################################################
#实验室设备使用
class DeviceCardModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="设备描述")
    device_info = models.CharField(max_length=2000, verbose_name="设备信息", default="【归属小组】:")
    current_process = models.CharField(max_length=200, verbose_name="当前使用状态",default="##闲置OR使用##")
    occupied_by = models.CharField(max_length=200, default="#使用人更新#", verbose_name="设备使用人")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="分配给(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class DeviceCardForm(ModelForm):
    class Meta:
        model = DeviceCardModel
        fields = '__all__'
        exclude = []#['curent_state','created_by']
        widgets = {
            'summary' : forms.TextInput(attrs={'size':50}),
            'device_info':forms.Textarea(attrs={'cols': 52, 'rows': 5}),
            'current_process' : forms.TextInput(attrs={'readonly': True,'size':20}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
############################################################################################################################################################
#上市保障问题跟踪
CHOICE_CUSTOMER_TYPE = (
    ('jinrong','金融'),
    ('dianli','电力'),
    ('nengyuan','能源'),
    ('guangdian','广电'),
    ('meizi','媒资'),
)
class IssueTrackModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要", default="【20170101】XX局点XX设备发生XX问题")
    detail = models.CharField(max_length=5000, verbose_name="详细描述")
    current_process = models.CharField(max_length=5000, verbose_name="处理进展",default="##由维护处理人填写##")
    #viewer_advice = models.CharField(max_length=5000, verbose_name="评审人意见",default="##由评审人填写##")
    customer_type = models.CharField(max_length=200,  verbose_name="客户类别", choices=CHOICE_CUSTOMER_TYPE)  #default="#金融/电力/能源/广电/媒资#", verbose_name="客户类别")
    class_1 = models.CharField(max_length=200, default="#软件/硬件/结构/操作/配置#", verbose_name="问题大类")
    class_2 = models.CharField(max_length=200, default="#/驱动/集群/缓存#", verbose_name="问题小类")
    class_3 = models.CharField(max_length=200, default="#/FC/SAS/ETH/内存/板卡(硬件)/#", verbose_name="问题模块")
    buglist_url = models.CharField(max_length=200, default="0", verbose_name="Buglist链接")
    improvement_url = models.CharField(max_length=200, default="0", verbose_name="改进项链接")
    issue_processor = models.CharField(max_length=200, default="#提交人填写#", verbose_name="维护处理人")
    issue_checkor = models.CharField(max_length=200, default="#维护处理人指定#", verbose_name="维护代表")
    issue_se = models.CharField(max_length=200, default="#维护代表指定#", verbose_name="改进提取SE")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class IssueTrackForm(ModelForm):
    class Meta:
        model = IssueTrackModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':79}),
            'current_process' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'detail' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }

############################################################################################################################################################
FormAndModelDict = {
    'improvement':{'PrjNameZh':'改进建议','PrjModelClass':NameModel,'PrjFormClass':NameForm},
    'device_card':{'PrjNameZh':'设备档案','PrjModelClass':DeviceCardModel,'PrjFormClass':DeviceCardForm},
    'issue_track':{'PrjNameZh':'网上问题处理','PrjModelClass':IssueTrackModel,'PrjFormClass':IssueTrackForm}
}
