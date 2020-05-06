import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
# from django.views import View
from django.views import View

from forum.models import comment, Topic
from me.models import User, Goods
from . import my_token
import hashlib

# from .models import UserProfile, Address, WeiboProfile

# Create your views here.
from .models import Order, Msg


class Login(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        print(data)
        uname = data['username']
        pwd = data['password']
        m = hashlib.md5()
        m.update(pwd.encode())
        m_pwd = m.digest()
        try:
            user = User.objects.filter(uname=uname, password=str(m_pwd)).first()
            print(user)
            if user:
                token = my_token.make_token(uname)
                data = {'code': 200, 'data': {'uname': uname, 'token': token.decode()}}
            else:
                data = {'code': 2001, 'error': '用户名或密码错误!'}
        except Exception as e:
            data = {'code': 2002, 'error': '没有该账号,请前往注册!'}
        return JsonResponse(data)


class Register(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        print(data)
        uname = data['username']
        pwd = data['password']
        try:
            old_user = User.objects.filter(uname=uname).first()
            print(old_user)
            if old_user:
                data = {'code': 3001, 'error': '该用户名已存在!'}
            else:
                m = hashlib.md5()
                m.update(pwd.encode())
                m_pwd = m.digest()
                user = User.objects.create(uname=uname, password=str(m_pwd))
                token = my_token.make_token(uname)
                data = {'code': 200, 'data': {'uname': uname, 'token': token.decode()}}
        except Exception as e:
            print('---------')
            print(e)
            data = {'code': 3002, 'error': '该用户名已存在!'}
        return JsonResponse(data)


class Personal(View):
    def get(self, request):
        return render(request, 'user/personal.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        print(data)
        this = data.get('this')
        print(this)
        if this:
            uname = data.get('uname')
            print(uname)
            if uname:
                user = User.objects.filter(uname=uname).first()
                print(user)
                sex = user.sex
                age = user.age
                address = user.address
                hoby = user.hobby
                money = user.money
                data = {'code': 200,
                        'data': {'username': uname, 'sex': sex, 'age': age, 'address': address, 'hoby': hoby,
                                 'money': money}}
                print(data)
                return JsonResponse(data)
        else:
            username = data.get('username')
            old_uname = data['uname']
            if old_uname != username:
                old_user = User.objects.filter(uname=username)
                if old_user:
                    data = {'code': 4001, 'error': '用户名已存在!'}
            user = User.objects.filter(uname=old_uname).first()
            print(user)
            try:
                user.uname = username
                user.sex = data['sex']
                user.age = data['age']
                user.address = data['address']
                user.hobby = data['hoby']
                user.money = data['money']
                user.save()
                token = my_token.make_token(username)
                data = {'code': 200, 'data': {'uname': user.uname, 'token': token.decode()}}
            except Exception as e:
                data = {'code': 4002, 'error': '用户名已存在!'}
        return JsonResponse(data)


class News(View):
    def get(self, request):
        return render(request, 'user/news.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        uname = data['uname']
        # print(uname)
        lis = []
        try:
            user = User.objects.filter(uname=uname).first()
            # print(user.uname)
            if user:
                u_id = user.id
                # print(u_id)
                order_lis = Order.objects.filter(user_id=u_id).all()
                # print(order_lis)
                for i in order_lis:
                    dic = {}
                    dic['one'] = '您'
                    u_name = User.objects.filter(id=i.user_id2).first().uname
                    dic['con'] = '购买了' + u_name + '的商品'
                    lis.append(dic)
                order_lis = Order.objects.filter(user_id2=u_id).all()
                # print('2',order_lis)
                for i in order_lis:
                    # print(i)
                    dic = {}
                    u_name = User.objects.filter(id=i.user_id).first().uname
                    # print(u_name)
                    dic['one'] = u_name
                    dic['con'] = '购买了您的商品'
                    # print(dic)
                    lis.append(dic)
                toc = Topic.objects.filter(user_id=u_id).all()
                # print(toc)
                for i in toc:
                    message_lis = comment.objects.filter(topic_id=i.id).all()
                    for j in message_lis:
                        dic = {}
                        u_name = User.objects.filter(id=j.user_id.id).first().uname
                        dic['one'] = u_name
                        dic['con'] = '给您留下评论'
                        lis.append(dic)
                comment_lis = comment.objects.filter(user_id=u_id).all()
                print('1',comment_lis)
                for i in comment_lis:
                    # print('2',u_id,i.user_id.id,i.topic_id.user_id)
                    toc = Topic.objects.filter(user_id=i.topic_id.user_id.id).all()
                    # print('3',toc)
                    for j in toc:
                        dic = {}
                        # print('4',j.user_id.id)
                        u_name = User.objects.filter(id=j.user_id.id).first().uname
                        dic['one'] = '您评价了'
                        dic['con'] = u_name + '的文章'
                        lis.append(dic)
        except Exception as e:
            pass
        count = len(lis)
        data = {'code': 200, 'data': lis, 'count': count}
        return JsonResponse(data)
        # a_bs = pinglun.objects.filter(..)
        # r_list = []
        # for i in a_bs:


# http:127.0.0.1:8000/me/update?id=n
class Mygoods(View):
    def get(self, request):
        return render(request, 'user/mygoods.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        uname = data['uname']
        page = 1
        try:
            page = data.get('page')
        except Exception as e:
            print('---page---')
            print(e)
            page = 1
        user = User.objects.filter(uname=uname).first()
        u_good = Goods.objects.filter(user=user)
        paginator = Paginator(u_good, 9)  # Show 9 contacts per page
        try:
            u_good = paginator.page(page)
        except Exception as e:
            page = 1
            u_good = paginator.page(page)
        good_list = []
        for i in u_good:
            dic = {}
            print(i.picture)
            print(type(i.picture))
            print(str(i.picture))
            dic['pic'] = str(i.picture)
            dic['introduce'] = i.introduce
            dic['name'] = i.name
            good_list.append(dic)
        print('11')
        print(good_list)
        count = len(good_list)
        data = {'code': 200, 'data': good_list, 'count': count, 'page': page}
        return JsonResponse(data)


class Myact(View):
    def get(self, request):
        return render(request, 'user/myact.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        uname = data['uname']
        page = 1
        try:
            page = data.get('page')
        except Exception as e:
            print('---page---')
            print(e)
            page = 1
        user = User.objects.filter(uname=uname).first()
        print('1',user)
        u_toc = Topic.objects.filter(user_id=user)
        print('2', u_toc)
        paginator = Paginator(u_toc, 9)  # Show 9 contacts per page
        try:
            u_toc = paginator.page(page)
        except Exception as e:
            page = 1
            u_toc = paginator.page(page)
        toc_list = []
        for i in u_toc:
            dic = {}
            dic['time'] = str(i.time)[:10]
            dic['content'] = i.msg[:50]
            dic['name'] = i.title
            toc_list.append(dic)
        print('11')
        print(toc_list)
        count = len(toc_list)
        data = {'code': 200, 'data': toc_list, 'count': count, 'page': page}
        return JsonResponse(data)


class Myorder(View):
    def get(self, request):
        return render(request, 'user/myorder.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        uname = data['uname']
        r_list = []
        try:
            user = User.objects.filter(uname=uname).first()
            uid = user.id
            orders = Order.objects.filter(user_id=uid).all()
            for item in orders:
                lis = {}
                lis['id'] = item.order_id
                lis['name'] = uname
                lis['price'] = item.price
                lis['address'] = item.address
                r_list.append(lis)
        except Exception as e:
            pass
        count = len(r_list)
        data = {'code': 200, 'data': r_list,'count':count}
        return JsonResponse(data)


# 我的评论
class Myrelease(View):
    def get(self, request):
        return render(request, 'user/myreleases.html')

    def post(self, request, *args, **kwargs):
        json_str = request.body
        data = json.loads(json_str)
        uname = data['uname']
        # print(uname)
        lis = []
        try:
            user = User.objects.filter(uname=uname).first()
            # print(user.uname)
            if user:
                u_id = user.id
                # print(u_id)
                comment_lis = comment.objects.filter(user_id=u_id).all()
                print('1', comment_lis)
                for i in comment_lis:
                    # print('2',u_id,i.user_id.id,i.topic_id.user_id)
                    toc = Topic.objects.filter(user_id=i.topic_id.user_id.id).all()
                    # print('3',toc)
                    for j in toc:
                        dic = {}
                        # print('4',j.user_id.id)
                        u_name = User.objects.filter(id=j.user_id.id).first().uname
                        dic['one'] = '您评价了'
                        dic['con'] = u_name + '的文章'
                        lis.append(dic)
        except Exception as e:
            pass
        count = len(lis)
        data = {'code': 200, 'data': lis, 'count': count}
        return JsonResponse(data)

#
#
# def myact(request):
#     if request.method == 'GET':
#         json_str = request.body
#         data = json.loads(json_str)
#         uname = data['uname']
#         try:
#             page = data['page']
#         except Exception as e:
#             page = 1
#         u_act = Act.objects.filter(uname=uname)
#         act_list = []
#         for i in u_act:
#             act = {}
#             act['pic'] = i.pic
#             act['content'] = i.content
#             act['name'] = i.name
#             act_list.append(act)
#         paginator = Paginator(act_list, 9)  # Show 9 contacts per page
#         try:
#             lis = paginator.page(page)
#         except Exception as e:
#             page = 1
#             lis = paginator.page(page)
#         data = {'code': 200, 'data': lis, 'page': page}
#         return JsonResponse(data)
#
#
# def mygoods(request):
#     if request.method == 'GET':
#         json_str = request.body
#         data = json.loads(json_str)
#         uname = data['uname']
#         try:
#             page = data['page']
#         except Exception as e:
#             page = 1
#         u_good = Good.objects.filter(uname=uname)
#         act_list = []
#         for i in u_good:
#             act = {}
#             act['pic'] = i.pic
#             act['content'] = i.content
#             act['name'] = i.name
#             act_list.append(act)
#         paginator = Paginator(act_list, 9)  # Show 9 contacts per page
#         try:
#             lis = paginator.page(page)
#         except Exception as e:
#             page = 1
#             lis = paginator.page(page)
#         data = {'code': 200, 'data': lis, 'page': page}
#         return JsonResponse(data)
#
#
#
#
#
#
# def myreleases(request):
#     if request.method == 'GET':
#         json_str = request.bogy
#         data = json.loads(json_str)
#         uname = data['uname']
#         a_bs = pinglun.objects.filter(..)
#         r_list = []
#         for i in a_bs:
#
#
# def myorder(request):
#     if request.method == 'GET':
#         json_str = request.bogy
#         data = json.loads(json_str)
#         uname = data['uname']
#         orders = Myorder.objects.filter(username=uname)
#         r_list = []
#         for item in orders:
#             lis = {}
#             lis['id'] = item.id
#             lis['name'] = item.name
#             lis['price'] = item.price
#             lis['address'] = item.address
#             lis['phone'] = item.phone
#             lis['status'] = item.status
#             r_list.append(lis)
#         data = {'code': 200, 'data': r_list}
#         return JsonResponse(data)
