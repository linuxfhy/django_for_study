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

class NameModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要")
    detail = models.CharField(max_length=5000, verbose_name="详细描述")
    current_process = models.CharField(max_length=5000, verbose_name="处理进展",default="##由改进实施人填写##")
    #viewer_advice = models.CharField(max_length=5000, verbose_name="评审人意见",default="##由评审人填写##")
    value = models.CharField(max_length=200, verbose_name="改进价值评估")
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

class DeviceCardModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="设备描述")
    own_group = models.CharField(max_length=5000, verbose_name="归属小组")
    current_process = models.CharField(max_length=5000, verbose_name="当前使用状态",default="##闲置OR使用##")
    occupied_by = models.CharField(max_length=200, default="#使用人更新#", verbose_name="当前使用人")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class DeviceCardForm(ModelForm):
    class Meta:
        model = DeviceCardModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':79}),
            'current_process' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }

FormAndModelDict = {
    'improvement':{'PrjNameZh':'改进建议','PrjModelClass':NameModel,'PrjFormClass':NameForm},
    'device_card':{'PrjNameZh':'设备档案','PrjModelClass':DeviceCardModel,'PrjFormClass':DeviceCardForm},
}