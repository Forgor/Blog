from django import forms
from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="用户名",required=True,widget=forms.TextInput(attrs={"class":"form-control",'placeholder':"请输入用户名或邮箱"}))
    password = forms.CharField(label="密码",widget=forms.PasswordInput(attrs = { "class" : "form-control",'placeholder':"请输入用户名" }))
    # 登录验证的方法 
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email,password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                # 用户存在
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username,password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError("用户名或者密码不正确")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label="用户名",
                                max_length=10,
                                min_length=3,
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入3-30位用户名'}))
    email = forms.CharField(label="邮箱",
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    veritication_code = forms.CharField(
                                label='验证码',
                                required=False,
                                widget=forms.TextInput(
                                    attrs = {'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}    ))
    password = forms.CharField(label="密码",
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again = forms.CharField(label="请在输入一次密码",
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'确认密码'}))
    
    # 将验证码数据传送过来
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
         # 判断验证码
        code = self.request.session.get('register_code','')
        veritication_code = self.cleaned_data.get('veritication_code','')
        # veritication_code = 'p289'
        print(code)
        print(veritication_code)
        if not (code !='' and code == veritication_code):
            raise forms.ValidationError('验证码不对，请重新输入')
        print(code !='' and code == veritication_code)
        return self.cleaned_data
    
    
    def clean_username(self):
        username = self.cleaned_data['username']                            
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已经存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        print(email)                            
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已经存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']                                   
        if password != password_again:
            raise forms.ValidationError("两次输入的密码不一致")
        return password_again

        # 验证验证码是否为空
    def clean_veritication_code(self):
        veritication_code = self.cleaned_data.get('veritication_code','').strip()
        if veritication_code == '':
            raise forms.ValidationError('验证码不能为空')
        return veritication_code

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label = '新的昵称',
        max_length=20,
        widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'请输入昵称'})
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
            print(self.user)
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     # 判断用户是否登录
    #     if self.user.is_authenticated:
    #         self.cleaned_data['user'] = self.user
    #     else:
    #         raise forms.ValidationError('用户尚未登陆')
    #     return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == "":
            raise forms.ValidationError("新的昵称不能为空")
        return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs = {'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    veritication_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
             attrs = {'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError("用户尚未登陆")

        # 怕买断用户是否已经绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email_code','')
        veritication_code = self.cleaned_data.get('veritication_code','')
        print(code)
        print(veritication_code)
        print(code == veritication_code)
        print(not(code == veritication_code))
        forms.ValidationError('验证码不对，请重新输入')
        if not (code !='' and code == veritication_code):
            raise forms.ValidationError('验证码不对，请重新输入')
        return self.cleaned_data



    # 验证邮箱是否已经绑定
    def email_clean(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经绑定')
        return email

    # 验证验证码是否为空
    def clean_veritication_code(self):
        veritication_code = self.cleaned_data.get('veritication_code','').strip()
        if veritication_code == '':
            raise forms.ValidationError('验证码不能为空')
        return veritication_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="密码",
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入旧的密码'}))
    new_password = forms.CharField(label="密码",
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新的密码'}))
    new_password_again = forms.CharField(label="密码",
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入新密码'}))

    # 将验证码数据传送过来
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.use = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    # 验证新的密码是否一致
    def clean(self):
        new_password = self.cleaned_data.get('new_password','')
        new_password_again = self.cleaned_data.get('new_password_again','')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    # 验证旧的密码是否正确
    def clean_old_password(self):
        # 方式一 传入密码
        # user.check_password('')
        old_password = self.cleaned_data.get('old_password','')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码不正确')
        return old_password

class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(label="邮箱",
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入绑定后的邮箱'}))
    veritication_code = forms.CharField(
                                label='验证码',
                                widget=forms.TextInput(
                                    attrs = {'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}    ))

    new_password = forms.CharField(label="密码",
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新的密码'}))
    
    # 将验证码数据传送过来
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email']                            
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱不存在")
        return email

    def clean_veritication_code(self):
        veritication_code = self.cleaned_data.get('veritication_code','').strip()
        if veritication_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('forgot_password_code','')
        veritication_code = self.cleaned_data.get('veritication_code','')
        print(code)
        print(veritication_code)
        if not (code !='' and code == veritication_code):
            raise forms.ValidationError('验证码不对，请重新输入')
        return veritication_code
