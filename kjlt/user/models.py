from django.db import models
import time
# Create your models here.
from me.models import User


class Order(models.Model):
    user_id=models.CharField(verbose_name='购买者',max_length=20)
    good_id=models.CharField(verbose_name='商品',max_length=20)
    user_id2=models.CharField(verbose_name='发布者',max_length=20)
    price=models.CharField(verbose_name='价格',max_length=20)
    create_time=models.DateTimeField(auto_now_add=True)
    order_id=models.CharField(verbose_name='订单号',max_length=30)
    address=models.CharField(verbose_name='地址',max_length=100)


class Msg(models.Model):
    user_id=models.CharField(verbose_name='接受者',max_length=10)
    user_id2 = models.CharField(verbose_name='发布者', max_length=20)
    msg=models.CharField(verbose_name='信息内容',max_length=50)
    create_time=models.DateTimeField(auto_now_add=True)



