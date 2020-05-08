from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Topic, comment
from me.models import User


# Create your views here.


def indexview(request):
    if request.method == 'GET':
        return render(request, 'forum/topic_index.html')
    elif request.method == 'POST':

        top_list = Topic.objects.filter().order_by('-id')[:5]
        title_list = []
        msg_list = []
        user_id_list = []
        topic_id_list = []

        for i in top_list:
            title_list.append(i.title)
            msg_list.append(i.msg)
            user_id_list.append(i.user_id_id)
            topic_id_list.append(i.id)
        title1 = title_list[0]
        title2 = title_list[1]
        title3 = title_list[2]
        title4 = title_list[3]
        title5 = title_list[4]
        msg1 = msg_list[0]
        msg2 = msg_list[1]
        msg3 = msg_list[2]
        msg4 = msg_list[3]
        msg5 = msg_list[4]
        id1 = user_id_list[0]
        id2 = user_id_list[1]
        id3 = user_id_list[2]
        id4 = user_id_list[3]
        id5 = user_id_list[4]
        uname1 = User.objects.filter(id=id1)[0].uname
        uname2 = User.objects.filter(id=id2)[0].uname
        uname3 = User.objects.filter(id=id3)[0].uname
        uname4 = User.objects.filter(id=id4)[0].uname
        uname5 = User.objects.filter(id=id5)[0].uname
        topic_id1 = topic_id_list[0]
        topic_id2 = topic_id_list[1]
        topic_id3 = topic_id_list[2]
        topic_id4 = topic_id_list[3]
        topic_id5 = topic_id_list[4]

        data_dict = {'title1': title1, 'title2': title2, 'title3': title3, 'title4': title4, 'title5': title5,
                     'msg1': msg1, 'msg2': msg2, 'msg3': msg3, 'msg4': msg4, 'msg5': msg5,
                     'uname1': uname1, 'uname2': uname2, 'uname3': uname3, 'uname4': uname4, 'uname5': uname5,
                     }

        comment1 = comment.objects.filter(topic_id_id=topic_id1)
        comment2 = comment.objects.filter(topic_id_id=topic_id2)
        comment3 = comment.objects.filter(topic_id_id=topic_id3)
        comment4 = comment.objects.filter(topic_id_id=topic_id4)
        comment5 = comment.objects.filter(topic_id_id=topic_id5)

        try:
            data_dict['comment1'] = comment1[0].content
        except:
            data_dict['comment1'] = '暂无评论'
        try:
            data_dict['comment2'] = comment2[0].content
        except:
            data_dict['comment2'] = '暂无评论'
        try:
            data_dict['comment3'] = comment3[0].content
        except:
            data_dict['comment3'] = '暂无评论'
        try:
            data_dict['comment4'] = comment4[0].content
        except:
            data_dict['comment4'] = '暂无评论'
        try:
            data_dict['comment5'] = comment5[0].content
        except:
            data_dict['comment5'] = '暂无评论'

        return JsonResponse(data_dict)


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
            title_pd = Topic.objects.filter(title=title)
            if not title_pd:
                user_id_id = User.objects.filter(uname=uname)[0].id
                Topic.objects.create(title=title, msg=topic, user_id_id=user_id_id)
                return JsonResponse({'code': 200})
        return JsonResponse({'code': 201})


def comment_send(request):
    # if request.method == 'GET':
    #     return render(request, 'forum/comment_send.html')
    # elif request.method == 'POST':
    # json_bytes = request.body
    # 将 bytes 类型转为 str
    # json_str = json_bytes.decode()
    # python3.6 及以上版本中, json.loads() 方法可以接收 str 和 bytes 类型
    # 但是 python3.5 以及以下版本中, json.loads() 方法只能接收 str,
    # 3.5 需要有上面的编码步骤.
    req_data = json.loads(request.body)
    content = req_data['comment']
    uname = req_data['uname']
    title = req_data['title']
    if comment:
        topic_id_id = Topic.objects.filter(title=title)[0].id
        user_id_id = User.objects.filter(uname=uname)[0].id
        comment.objects.create(content=content, topic_id_id=topic_id_id, user_id_id=user_id_id)
        return JsonResponse({'code': 200})
    return JsonResponse({'code': 201})
