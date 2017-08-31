from django import forms

class NameForm(forms.Form):
    summary = forms.CharField(max_length=100)
    priority = forms.CharField(max_length=100)
    urgency = forms.CharField(max_length=100)
    current_process = forms.CharField(widget=forms.Textarea)
    deadline = forms.CharField(max_length=100)
    curent_state = forms.CharField(max_length=100)
