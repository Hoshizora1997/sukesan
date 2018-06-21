from django.db import models
from django.contrib.auth.models import User
import uuid, datetime
from django.utils import timezone


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('タイトル', max_length=255)
    description = models.TextField('説明', max_length=1400)
    place = models.CharField('場所', max_length=500,null=True,blank=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='管理者')
    hours = models.PositiveIntegerField('時間', default=4)
    startDate = models.DateField('はじめ', default=timezone.now)
    endDate = models.DateField('おわり', default=timezone.now)
    startTime = models.PositiveIntegerField('開始時間-時', default=72)
    endTime = models.PositiveIntegerField('終了時間-時', default=88)
    delete = models.BooleanField('削除フラグ', default=False)
    create = models.DateTimeField('更新日時', auto_now_add=True)
    update = models.DateTimeField('作成日時', auto_now=True)


class PlanDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan,on_delete=models.PROTECT, verbose_name='プラン')
    date = models.DateField('日付', default=datetime.date(year=2000,month=1,day=1))
    startTime = models.PositiveIntegerField('選択エリア開始時刻', default=0)
    endTime = models.PositiveIntegerField('選択エリア終了時刻', default=95)
    delete = models.BooleanField('削除フラグ', default=False)


class Mob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan,on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField('名前', default='null', max_length=30)


class UserData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    planDetail = models.ForeignKey(PlanDetail, on_delete=models.PROTECT,verbose_name='対象日')
    time = models.PositiveIntegerField('時間カウント', default=0)
    mob = models.ForeignKey(Mob, on_delete=models.PROTECT, verbose_name='モブ')
    STATUS_O = "O"
    STATUS_X = "X"
    STATUS_N = "N"
    STATUS_SET = (
        (STATUS_O, "◯"),
        (STATUS_X, "×"),
        (STATUS_N, "△"),
    )
    status = models.CharField(choices=STATUS_SET, default=STATUS_X, max_length=3)