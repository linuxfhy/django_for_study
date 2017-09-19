import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
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

class NameModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要")
    priority = models.CharField(max_length=200, verbose_name="重要性")
    urgency = models.CharField(max_length=200, verbose_name="紧急性")
    current_process = models.CharField(max_length=200, verbose_name="处理进展")
    deadline = models.CharField(max_length=200, verbose_name="截止时间")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态")
    processer_1st = models.CharField(max_length=200, default="", verbose_name="当前环节处理人")
    processer_2nd = models.CharField(max_length=200, default="", verbose_name="第二环节处理人")
    processer_3rd = models.CharField(max_length=200, default="", verbose_name="第三环节处理人")


class NameForm(ModelForm):
    class Meta:
        model = NameModel
        fields = '__all__'#['summary','priority','urgency','current_process','deadline','curent_state']
