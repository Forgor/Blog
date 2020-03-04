import datetime
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from read_record.utils import get_seven_days_read_data, get_today_hot_data,get_yesterday_hot_date
from blog.models import Blog


def get_7_days_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date) \
                        .values('id','title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据方法
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blog()
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3600) 


    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_dat'] = get_today_hot_data(blog_content_type) 
    context['yesterday_hot_dat'] = get_yesterday_hot_date(blog_content_type) 
    context['hot_data_for_7_days'] = get_7_days_hot_blog() 
    return render(request,'home.html',context)


def boot(request):
    data = {}
    return render(request,'boot.html',data)
