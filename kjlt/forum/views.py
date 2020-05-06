from django.shortcuts import render
import json
from django.http import JsonResponse
import pymysql
from .models import Topic
from me.models import User


# Create your views here.


def indexview(request):
    return render(request, 'forum/topic_index.html')






def topic_publish(request):
    if request.method == 'GET':
        return render(request, 'forum/topic_publish.html')
    elif request.method == 'POST':
        # json_bytes = request.body
        # 将 bytes 类型转为 str
        # json_str = json_bytes.decode()
        # python3.6 及以上版本中, json.loads() 方法可以接收 str 和 bytes 类型
        # 但是 python3.5 以及以下版本中, json.loads() 方法只能接收 str,
        # 3.5 需要有上面的编码步骤.
        req_data = json.loads(request.body)
        title = req_data['title']
        topic = req_data['topic']
        uname = req_data['uname']
        if title and topic:
            user_id_id = User.objects.filter(uname=uname)[0].id
            print(user_id_id)
            Topic.objects.create(title=title, msg=topic, user_id_id=user_id_id)
            return JsonResponse({'code': 200})
        return JsonResponse({'code': 201})


def comment_send(request):
    if request.method == 'GET':
        return render(request, 'forum/comment_send.html')
    elif request.method == 'POST':
        # json_bytes = request.body
        # 将 bytes 类型转为 str
        # json_str = json_bytes.decode()
        # python3.6 及以上版本中, json.loads() 方法可以接收 str 和 bytes 类型
        # 但是 python3.5 以及以下版本中, json.loads() 方法只能接收 str,
        # 3.5 需要有上面的编码步骤.
        req_data = json.loads(request.body)
        comment = req_data['comment']
        uname = req_data['uname']
        if comment:

            return JsonResponse({'code': 200})
        return JsonResponse({'code': 201})


