import datetime
import string
import random
import time
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib import auth
# from django.contrib.auth.models import User
from django.urls import reverse
from read_record.utils import get_seven_days_read_data, get_today_hot_data,get_yesterday_hot_date
from blog.models import Blog
from .forms import LoginForm,RegForm,ChangeNicknameForm,BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile

User = get_user_model()



def login(request):
    # username = request.POST.get('username','')
    # password = request.POST.get('password','')
    # user = auth.authenticate(request,username=username,password=password)
    # referer = request.META.get('HTTP_REFERER',reverse('home'))  #  指向当前登录页面或者首页  reverse 反向解析home
    # if user is not None:
    #     auth.login(request,user)
    #     # redirect a succeed page
    #     return redirect(referer)
    # else:
    #     return render(request,'error.html',{'message':'用户名或密码不正确'})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()         
    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            print(username)
            user = User.objects.create_user(username,email,password)
            user.save()
            # 清楚 session
            del request.session['register_code']
            # 登陆用户
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
         reg_form = RegForm()
         print('erroe')       
    context = {}
    context['reg_form'] = reg_form
    return render(request,'register.html',context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request,'user_info.html', context)

def change_nickname(request):
    redirect_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user = request.user)
            profile.nickname = nickname_new
            profile.save()
            # 提交完名称  跳转
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request,'form.html',context)

def bond_email(request):
    redirect_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 提交完名称  跳转
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request,'bind_email.html',context)

def send_vertification_code(request):
    email = request.GET.get('email','')
    # 传入请求 此时请求只是一个参数名称而已， 
    send_for = request.GET.get('send_for','')
    data = {}
   
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits,4))
        print(code)
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)

        # 利用后端方式保证两次申请验证码的时间在30s 以上
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code 
            print(request.session['send_for']+'in code')
            request.session['send_code_time'] = now
            send_mail("这是一封验证邮件",
                        '验证码：%s' % code,
                        '846450275@qq.com',
                        [email],
                        fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    redirect_to = request.GET.get(reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            # 提交完名称  跳转
            return redirect(reverse('home'))
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request,'form.html',context)

def forgot_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        
        if form.is_valid():
            print(request.session['forgot_password_code'])
            emial = form.cleaned_data['email']
            print(emial)
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=emial)
            user.set_password(new_password)
            user.save()
            # 清楚session
            del request.session['forgot_password_code'] 
            # 提交完名称  跳转
            return redirect(redirect_to)
        else:
            print('Form erroe')
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request,'forgot_password.html',context)


def boot(request):
    data = {}
    return render(request,'boot.html',data)
