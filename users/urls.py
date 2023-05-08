
from django.urls import path
from users.views import (
    PinShopsInfluencer, ShopOwnerView, InfluencerView, 
    ShopOwnerPublicView, CustomAuthToken
)
from rest_framework.authtoken import views

urlpatterns = [
   path('shopowner/profile/',ShopOwnerView.as_view(), name="shop-owner-profile"),
   path('influencer/profile/',InfluencerView.as_view(), name="influencer-profile"),
   path('influencer/pinnedshops/', PinShopsInfluencer.as_view(), name="influencer-pinnedshops"),
   path('influencer/pinshop/<int:id>/', PinShopsInfluencer.as_view(), name="influencer-pin"),
   path('shopowner/public/profile/',ShopOwnerPublicView.as_view(), name="shopowner-public-profile"),
   path('account/login/', CustomAuthToken.as_view())
]
 