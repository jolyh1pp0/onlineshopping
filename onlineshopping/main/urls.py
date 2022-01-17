from django.urls import path
from django.contrib import admin
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('receipt/', views.receipt, name='receipt')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
