
from django.urls import path
from referal.views import (
    ActiveReferalView, ExpiredReferalView, InfluencerRequestView, PendingReferalView, 
    InfluencerReferalSummaryView, MonthlyReferalView, ActiveInfluencerView,
    ShopOwnerTotalReferalView, ShopOwnerReferal, RequestReferal
)

urlpatterns = [
    path('shopowner/influencer/pending/',InfluencerRequestView.as_view(), name="influencer-request"),
    path('shopowner/referal/monthly/summary/',MonthlyReferalView.as_view(), name="referal-monthly"),
    path('shopowner/influencer/active/',ActiveInfluencerView.as_view(), name="influencer-active"),
    path('shopowner/influencer/active/<int:id>/',ActiveInfluencerView.as_view(), name="influencer-active-id"),
    path('shopowner/referal/all/',ShopOwnerTotalReferalView.as_view(), name="influencer-active"),
    path('shopowner/influencer/referal/',ShopOwnerReferal.as_view(), name="influencer-referal"),

    path('influencer/referal/pending/', PendingReferalView.as_view(), name="influencer-pending-request"),
    path('influencer/referal/active/', ActiveReferalView.as_view(), name="influencer-active-request"),
    path('influencer/referal/expired/', ExpiredReferalView.as_view(), name="influencer-expired-request"),
    path('influencer/referal/summary/',InfluencerReferalSummaryView.as_view(), name="influencer-summary"),
    path('influencer/referal/request/', RequestReferal.as_view(), name="influencer-request-referal")
    
]
