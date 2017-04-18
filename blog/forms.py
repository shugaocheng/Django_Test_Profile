from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25,label='姓名')
    email = forms.EmailField(label='发件人')
    to = forms.EmailField(label='收件人')
    comments = forms.CharField(required=False,widget=forms.Textarea,label='邮件内容')