from django.shortcuts import render,get_object_or_404
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Count # 导入统计方法
from datetime import datetime
# contenttype package
from django.contrib.contenttypes.models import ContentType
from read_record.models import ReadNum
from read_record.utils import read_record_once_read
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.

each_page_blogs_number = settings.EACH_PAGE_BLOGS_NUMBER

def get_blog_list_common_data(request,blogs_all_list):
    # 分页设计
    paginator = Paginator(blogs_all_list,each_page_blogs_number) # 每10篇文章进行分页
    page_num = request.GET.get('page',1) # 获取页面参数 (GET请求)
    page_of_blogs = paginator.get_page(page_num)  # 错误字符返回1

    current_page_num = page_of_blogs.number #获取当前页
    # page_range = [current_page_num - 2, current_page_num - 1, current_page_num, current_page_num + 1, current_page_num + 2]
    # range(current_page_num - 2,current_page_num)
    # 获取当前页码前后两页
    page_range = [(current_page_num + i) for i in range(-3,3) if paginator.num_pages>=(current_page_num + i)>0]
    # 加上省略页
    if page_range[0] -1 > 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获得分类博客的数量 相关类的小写  以下最终解析为一条SQL语句，调用时候才会执行 其中的别名可以在 Model中的
    # 对应字段采用 related_name 进行设置
    BlogType.objects.annotate(blog_count = Count('blog'))
    '''blogs_type = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blogs_type:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)'''

    # 获取日期归档相关数据
    blog_dates = Blog.objects.dates('created_time','month', order="DESC") 

    blog_dates = Blog.objects.dates('created_time','month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    

    context = {}
    context['blogs'] =  page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # 方式二，通过传输长度
    context['blog_length'] = Blog.objects.all().count()
    # 将总的文章类别数目 传递至前端
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    return context

# show the blog list
def blog_list(request):

    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    return render(request,'blog_list.html',context)

# show the blog content
def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,id=blog_pk)
    read_cookie_key = read_record_once_read(request,blog)
    # # 通过读取cookie信息，增加阅读计数
    # if not request.COOKIES.get('blog_%s_read' % blog_pk):
    #     ct = ContentType.objects.get_for_model(Blog)
    #     if ReadNum.objects.filter(content_type=ct,object_id=blog.pk).count():
    #         # 存在记录
    #         readnum = ReadNum.objects.get(content_type=ct,object_id=blog.pk)
    #     else:
    #         # 不存在记录
    #         # 首先创建一条记录
    #         readnum = ReadNum(content_type=ct,object_id=blog.pk)
    #     readnum.read_num += 1
    #     readnum.save()

    blog_content_type = ContentType.objects.get_for_model(blog)
    comment = Comment.objects.filter(content_type = blog_content_type, object_id = blog.pk, parent=None)

    context = {}
    # 获取按照创建时间来说比较早的一条
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).first()
    context['blog'] = blog
    # context['comments'] = comment.order_by('-comment_time')
    # context['comment_count'] = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk).count()
    # 向blog_detail页面传递博客信息 初始化博客数据
    # context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk,'reply_comment_id':0})
    response =  render(request,'blog_detail.html',context)
    # django 会将cookie相关信息处理为字典
    response.set_cookie(read_cookie_key, 'true', max_age=10, )
    return response

def blogs_with_type(request,blogs_type_pk):
    
    blog_type = get_object_or_404(BlogType,pk=blogs_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    # blogs_all_list = Blog.objects.filter(blog_type__id = blog_type.pk) 博客分类外键拓展
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type 
    return render(request,'blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    context = {}
    # 分页设计
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_with_date'] =  '%s年%s月' % (year,month)
    return render(request,'blogs_with_date.html',context)
