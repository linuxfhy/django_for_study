from django import forms

class NameForm(forms.Form):
    summary = forms.CharField(label='事件概要', max_length=100)
    priority = forms.CharField(label='重要程度', max_length=100)
    urgency = forms.CharField(label='紧急程度', max_length=100)
    current_process = forms.CharField(label='当前进展', widget=forms.Textarea)
    deadline = forms.CharField(label='截止时间', max_length=100)
    curent_state = forms.CharField(label='当前状态', max_length=100)
