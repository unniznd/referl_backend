
from django.urls import path
from users.views import ShopOwnerView, InfluencerView, ShopOwnerPublicView
from rest_framework.authtoken import views

urlpatterns = [
   path('shopowner/profile/',ShopOwnerView.as_view(), name="shop-owner-profile"),
   path('influencer/profile/',InfluencerView.as_view(), name="influencer-profile"),
   path('shopowner/public/profile/',ShopOwnerPublicView.as_view(), name="shopowner-public-profile"),
   path('token/auth/', views.obtain_auth_token)
]
