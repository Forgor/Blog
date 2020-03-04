from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    # 以下可以认为是通用模板
    # 通过content_type 指向对应外键的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 记录对应模型的主键值
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Test():
        def get_read_num(self):
            try:
                ct = ContentType.objects.get_for_model(self)
                readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
                return readnum.read_num
            except ObjectDoesNotExist as e:
                return 0

# 如下增加统计博客访问数量的详细信息
class ReadDetail(models.Model):
    # 记录时间
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

