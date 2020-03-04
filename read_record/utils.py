import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_record_once_read(request,obj):
    """
    返回最近是不是度过这篇文章
    """
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read"%(ct.model,obj.pk)
     # 通过读取cookie信息，增加阅读计数
    if not request.COOKIES.get(key):

        # 总阅读数 +1
        # if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
        #     # 存在记录
        #     readnum = ReadNum.objects.get(content_type=ct,object_id=obj.pk)
        # else:
        #     # 不存在记录
        #     # 首先创建一条记录
        #     readnum = ReadNum(content_type=ct,object_id=obj.pk)
        # 替换如上代码 
        readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数 +1
        # date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=date).count():
        #     readDetail = ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=date)
        # else:
        #     readDetail = ReadDetail(content_type=ct,object_id=obj.pk,date=date)
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readDetail.read_num += 1
        readDetail.save()
    return key

# 获得连续七天的访问量
def get_seven_days_read_data(content_type,):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details  # 返回结果是ReadDetail


def get_yesterday_hot_date(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]  # 返回结果是ReadDetail

def get_7_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects \
                            .filter(content_type=content_type, date__lt=today,date__gte=date) \
                            .values('content_type','object_id') \
                            .annotate(read_num_sum = Sum('read_num')) \
                            .order_by('-read_num')
    return read_details[:7]