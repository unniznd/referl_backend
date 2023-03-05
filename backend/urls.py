
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from payment import views as payment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('', include('referal.urls')),
    path("payment/order/", payment_views.OrderPayment.as_view(), name="payment"),
    path("payment/callback/", payment_views.CallBack.as_view(), name="callback"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
