from django.db import models
# from django.db.models import exceptions
# import django user module
# from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.urls import reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from read_record.models import Test,ReadDetail
# Create your models here.
# Blog type
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
            return  self.type_name

# Blogdir
class Blog(models.Model,Test):
    title = models.CharField(max_length=50)

    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    # read_num = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)


    # def get_read_num(self):
    #     try:
    #         return self.readnum.read_num
    #     except ObjectDoesNotExist as e:
    #         return 0
    #     # return self.readnum.read_num

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk' : self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return '<Blog: %s>'%self.title

    class Meta:
        ordering = ['created_time']
'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog,on_delete=models.DO_NOTHING) #  选择一对一关系字段
'''

