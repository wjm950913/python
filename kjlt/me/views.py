import json
import random

from alipay import AliPay
from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views import View
from user.models import Order, Msg
from .models import Goods, User
import datetime


# Create your views here.
def ajaxme(request):
    return render(request, 'alipay.html')


def ajaxpost(request):
    goods = Goods.objects.filter(is_active=True)

    p = Paginator(goods, 3)  # 每次展示几个商品
    i = int(request.GET.get('id', 1))
    if i < 1:
        i = p.num_pages
    if i > p.num_pages:
        i = 1
    q = p.page(i)
    data = []
    for i in q:
        item = {}

        item['img'] = str(i.picture)
        item['title'] = i.name
        item['msg'] = i.introduce
        item['price'] = i.price
        item['page'] = p.num_pages
        item['GoodId'] = i.id
        data.append(item)

    # a = {'w': '123'}
    # a = json.dumps(a, separators=(',', ':'))
    return JsonResponse({'code': 200, 'data': data, "page": p.num_pages})


def kjlt(request):
    return render(request, 'index.html')


class Goods_good(View):

    def get(self, request):
        return render(request, 'goods.html')

    def post(self, request):
        base_dir = '/home/tarena/桌面/论坛/kjlt/static/images/thumb/'
        # id=request.POST.get('token','meiyou')
        token = request.POST.get('token', 'meiyou')  # 获取用户token
        user = User.objects.get(uname=token)
        id = user.id
        try:
            pic_obj = request.FILES['myfile']
        except:
            return render(request, 'goodspost404.html')

        title = request.POST.get('title')
        pic_name = pic_obj.name
        picture = "/static/images/thumb/" + pic_name
        price = request.POST.get('price')
        key = request.POST.get('key')
        introduce = request.POST.get('introduce')
        # number=request.POST.get('number')
        if not title or not price or not introduce:
            return render(request, 'goodspost404.html')

        with open(base_dir + pic_name, 'wb') as f:
            data = pic_obj.file.read()
            f.write(data)
        try:
            Goods.objects.create(name=title, price=price, introduce=introduce, picture=picture, user_id=id)
            return render(request, 'goodspost200.html')
        except Exception as e:

            return render(request, 'goodspost404.html')


class update_good(View):
    def get(self, request):

        return render(request, 'update_good.html')

    def post(self, request, *args, **kwargs):
        new_title = request.POST.get('title')
        new_price = request.POST.get('price')
        new_key = request.POST.get('key')
        new_introduce = request.POST.get('introduce')
        good_id = request.POST.get('GoodId')  # 获取商品id
        user_id = request.POST.get('token')  # 获取用户id
        good = Goods.objects.get(id=good_id)
        try:
            if new_title:
                good.name = new_title
            if new_price:
                good.price = float(new_price)
            if new_introduce:
                good.introduce = new_introduce
            good.save()
            return render(request, 'goodupdate200.html')
        except:
            return HttpResponse('error')


class Goods_buy(View):

    def get(self, request):
        return render(request, 'goodsbuy.html')


class goods_buy_view(View):
    def get(self, request, *args, **kwargs):
        good_id = int(request.GET.get('id'))
        username = request.GET.get('userid')  # 临时使用，后期通过token后去
        user = User.objects.get(uname=username)
        user_id1 = user.id
        print('=' * 50)
        print(user_id1)
        good = Goods.objects.get(id=good_id)
        user_id2 = good.user_id
        uesr = User.objects.get(id=user_id1)
        data = {}
        data['price'] = good.price
        data['msg'] = good.introduce
        data['img'] = str(good.picture)
        data['good'] = good.name
        data['address'] = uesr.address
        data['good_owner'] = user_id2
        print(data)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        good_id = int(request.POST.get('id'))
        # user_id1=int(request.POST.get('userid'))

        username = request.POST.get('userid')  # 临时使用，后期通过token后去
        print('+' * 50)
        print(username)
        user = User.objects.get(uname=username)
        user_id1 = user.id
        address = request.POST.get('address')
        good = Goods.objects.get(id=good_id, is_active=True)
        with transaction.atomic():
            sid = transaction.savepoint()
            price = good.price
            owner_id = int(good.user_id)
            now = datetime.datetime.now()
            order_id = now.strftime('%Y%m%d%H%M%S') + str(good_id)

            result = Goods.objects.filter(id=good_id, is_active=True).update(is_active=False)
            if result == 0:
                return JsonResponse({'code': 400, 'error': '服务器繁忙'})
            try:
                Order.objects.create(user_id=user_id1, good_id=good_id, user_id2=owner_id, price=price,
                                     order_id=order_id, address=address)
            except:

                transaction.savepoint_rollback(sid)
                return JsonResponse({'code': 400, 'error': '服务器繁忙'})
            user_by = User.objects.get(id=user_id1)
            user_owner = User.objects.get(id=owner_id)
            if user_by.money < price:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'code': 400, 'return_url': 'http://127.0.0.1:8000/me/kjlt#portfolio'})

            result_1 = User.objects.filter(id=user_id1).update(money=user_by.money - price)
            result_2 = User.objects.filter(id=owner_id).update(money=user_owner.money + price)

            transaction.savepoint_commit(sid)
        return JsonResponse({'code': 200, 'return_url': 'http://127.0.0.1:8000/me/kjlt#portfolio'})


# 支付包公私钥
app_private_key_string = open(settings.ALIPAY_KEY_DIRS +
                              'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIRS +
                                'alipay_public_key.pem').read()


class MyAliPay(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )

    def get_trade_url(self, order_id, amount):
        # pc网站支付地址'https://openapi.alipaydev.com/gateway.do?'+
        order_string = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amount,
            subject=order_id,
            notify_url=settings.ALIPAY_NOTIFY_URL,
            return_url=settings.ALIPAY_RETURN_URL
        )
        return "https://openapi.alipaydev.com/gateway.do?" + order_string

    def get_verify_result(self, data, sign):
        # 验证签名
        return self.alipay.verify(data, sign)

    def get_trade_result(self, order_id):

        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        print(result)
        if result.get('trade_status') == "TRADE_SUCCESS":
            return True
        else:
            return False


class ALIPAY(MyAliPay):
    def get(self, request):
        return render(request, 'alipay.html')

    def post(self, request, *args, **kwargs):
        # now = datetime.datetime.now()
        # order_id = now.strftime('%Y%m%d%H%M%S') + str(random.randint(1,10000))+str(random.randint(1,10000))
        username = request.POST.get('userid')
        print('=' * 50)
        print(username)
        now = datetime.datetime.now()
        order_id = username + '_' + str(now.strftime('%Y%m%d%H%M%S'))
        price = request.POST.get('price')
        pay_url = self.get_trade_url(order_id, price)
        return JsonResponse({"code": 200, "pay_url": pay_url})


class ALIPAY_result(MyAliPay):
    def get(self, request):
        print('=====================get========================')
        print(request.GET)
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        sign = request_data.pop('sign')
        i_verity = self.get_verify_result(request_data, sign)
        if i_verity:
            order_id = request_data.get('out_trade_no')
            username = order_id.split('_')[0]
            user = User.objects.get(uname=username)

            price = request_data.get('total_amount')
            older_money = float(user.money)
            new_money = older_money + float(price)
            user.money = new_money
            user.save()
            res = self.get_trade_result(order_id)
            if res:
                pass

                return render(request, 'index.html')
            else:
                return HttpResponse('get is error')
        else:
            return HttpResponse('非法访问')
