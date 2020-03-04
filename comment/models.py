import threading
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your models here.

class SendMail(threading.Thread):

    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject, 
            '', 
            settings.EMAIL_HOST_USER, 
            [self.email], 
            fail_silently=self.fail_silently,
            html_message=self.text)
        
    

class Comment(models.Model):

    # 评论对象
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    # 评论内容
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='comments', on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.DO_NOTHING)
    # parent_id = models.IntegerField(default=0)
    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='replies',null=True,on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']


    def send_email(self):
        # 评论完成之后 发送邮件
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的内容'
            email = self.content_object.get_email()
        else:
            # 回复的其他用户的评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            # 反向解析 将get_url 和 get_email 设计成通用的方法
            # text = self.text + '\n' + self.content_object.get_url()
            # text = '%s\n<a href="%s">%s</a>' %(self.text, self.content_object.get_url(), '点击查看')
            context = {}
            context['comment_text'] = '巨头望明月，低头思故乡'
            context['url'] = 'http://127.0.0.1:8000' + self.content_object.get_url()
            text = render_to_string('email.html',context)
            send_mail = SendMail(subject, text, email)
            send_mail.start()

