from django.contrib import admin
from .models import LikeModel,LikeRecord

# Register your models here.

@admin.register(LikeModel)
class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('id','content_type','object_id','liked_num')
    ordering = ('id',)

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id','content_type','object_id','user','liked_time')
    ordering = ('id',)


