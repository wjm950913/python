from django.db import models


# Create your models here.

class User(models.Model):
    uname = models.CharField('用户名称：', max_length=20)
    password = models.CharField('密码', max_length=50)
    sex = models.CharField('性别', max_length=5, default='男')
    address = models.CharField('收件地址', max_length=50, default=" ")
    hobby = models.CharField('爱好', max_length=20, default=" ")
    money = models.DecimalField('余额', max_digits=10, decimal_places=2, default=0)
    age = models.IntegerField('年龄', default=18)


class Goods(models.Model):
    name = models.CharField('商品名称', max_length=20)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    introduce = models.CharField('商品简介', max_length=50)
    is_active = models.BooleanField(default=True)
    number = models.IntegerField('数量', default=1)
    createtime = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField('图片', upload_to='goods')
    key = models.CharField('关键字', max_length=20, default=' ')
    user = models.ForeignKey(User)

# class Topic(models.Model):
#     title = models.CharField(max_length=20, verbose_name='标题')
#     msg = models.CharField(max_length=2000, verbose_name='内容')
#     time = models.DateTimeField(auto_now_add=True, verbose_name='日期')
#     user_id = models.ForeignKey(User,related_name='uid')
#
#     class Meta:
#         db_table = 'forum_topic'
#         verbose_name = '帖子信息'
#
#
# class comment(models.Model):
#     content = models.CharField(max_length=150, verbose_name='评论')
#     topic_id = models.ForeignKey(Topic)
#     user_id = models.ForeignKey(User,related_name='uid')

# class Meta:
#     db_table = 'forum_comment'
#     verbose_name = '评论信息'
