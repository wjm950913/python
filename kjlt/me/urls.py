from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from me import views

# http://127.0.0.1:8000/me/kjlt#welcome

urlpatterns=[
    url(r'^$',views.ajaxme),
    url(r'^/jump$',views.ajaxpost),
    url(r'^/kjlt$',views.kjlt),
    url(r'^/update$',views.update_good.as_view()),
    url(r'^/goods$',views.Goods_good.as_view()),
    url(r'^/goodbuy$',views.Goods_buy.as_view()),
    url(r'^/goodbuyview$',views.goods_buy_view.as_view()),
    url(r'^/payment$', views.ALIPAY.as_view()),
    url(r'^/payment/result$', views.ALIPAY_result.as_view()),
    # url(r'^/putgoods',views.putgoods),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

