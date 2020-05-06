from django.db import models
from me.models import User


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题')
    msg = models.CharField(max_length=2000, verbose_name='内容')
    time = models.DateTimeField(auto_now_add=True, verbose_name='日期')
    user_id = models.ForeignKey(User)

    class Meta:
        db_table = 'forum_topic'
        verbose_name = '帖子信息'


class comment(models.Model):
    content = models.CharField(max_length=150, verbose_name='评论')
    topic_id = models.ForeignKey(Topic)
    user_id = models.ForeignKey(User)

    class Meta:
        db_table = 'forum_comment'
        verbose_name = '评论信息'
