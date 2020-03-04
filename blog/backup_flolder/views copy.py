from django.shortcuts import render,get_object_or_404
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.

each_page_blogs_number = settings.EACH_PAGE_BLOGS_NUMBER

# show the blog list
def blog_list(request):

    # 分页设计
    blogs_all_list = Blog.objects.all()
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
    context = {}
    context['blogs'] =  page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # 方式二，通过传输长度
    context['blog_length'] = Blog.objects.all().count()
    # 将总的文章类别数目 传递至前端
    context['blog_types'] = BlogType.objects.all();
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time','month', order="DESC")
    return render(request,'blog_list.html',context)

# show the blog content
def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,id=blog_pk)
    # 获取按照创建时间来说比较早的一条
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).first()
    context['blog'] = blog
    return render(request,'blog_detail.html',context)

def blogs_with_type(request,blogs_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blogs_type_pk)
    # context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    # context['blog_types'] = BlogType.objects.all();
    # 分页设计
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    # blogs_all_list = Blog.objects.filter(blog_type__id = blog_type.pk) 博客分类外键拓展
    paginator = Paginator(blogs_all_list,each_page_blogs_number) # 每10篇文章进行分页
    page_num = request.GET.get('page',1) # 获取页面参数 (GET请求)
    page_of_blogs = paginator.get_page(page_num)  # 错误字符返回1

    current_page_num = page_of_blogs.number #获取当前页
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
    

    context = {}
    context['blogs'] =  page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # 方式二，通过传输长度
    context['blog_length'] = Blog.objects.all().count()
    context['blog_type'] = blog_type 
    # 将总的文章类别数目 传递至前端
    context['blog_types'] = BlogType.objects.all();
    context['page_range'] = page_range
    return render(request,'blogs_with_type.html',context)


def blogs_with_date(request,year,month):
    context = {}
    # 分页设计
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    paginator = Paginator(blogs_all_list,each_page_blogs_number) # 每10篇文章进行分页
    page_num = request.GET.get('page',1) # 获取页面参数 (GET请求)
    page_of_blogs = paginator.get_page(page_num)  # 错误字符返回1

    current_page_num = page_of_blogs.number #获取当前页
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
    

    context = {}
    context['blog_with_date'] =  '%s年%s月' % (year,month)
    context['blogs'] =  page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # 将总的文章类别数目 传递至前端
    context['blog_types'] = BlogType.objects.all();
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time','month', order="DESC")
    return render(request,'blogs_with_date.html',context)
