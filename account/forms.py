from django import forms
from django.contrib.auth.models import User
from .models import Profile
# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# 注册表单
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='密码')
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='再次输入密码')
    class Meta:
        model = User
        fields = ('username','first_name','email')

    # 检查两次输入的密码是否一致
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']

# 上传文件表单
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile     # 变量名一定要为model,否则无法获取到模型用户实例
        fields = ('date_of_birth','photo')

# 修改资料表单
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name','first_name','email')