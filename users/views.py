from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import permissions

from users.models import ShopOwner, Influencer
from users.pagination import ShopOwnerPagination
from users.serializers import InfluencerSerializer, ShopOwnerSerializer, ShopOwnerPublicSerailizer


class ShopOwnerView(ListAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def get(self, request, *args, **kwargs):
        shop_owner = ShopOwner.objects.filter(profile=request.user).first()
        shop_owner_serial = ShopOwnerSerializer(shop_owner)
        return Response(shop_owner_serial.data)

    def post(self, request,  *args, **kwargs):
        pass

    def patch(self, request,  *args, **kwargs):
        shop_owner = ShopOwner.objects.filter(profile=request.user).first()
        if shop_owner:
            shop_owner_serial = ShopOwnerSerializer(
                shop_owner,
                data=request.data,
                partial=True
            )
            if shop_owner_serial.is_valid():
                shop_owner_serial.save()
                return Response({"status":True})
            
            else:
                return Response({"status":False,"errors":shop_owner_serial.errors})
        
        else:
            return Response({
                "status":False,
                "error":'No such profile found!'
            })

class InfluencerView(ListAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def get(self, request, *args, **kwargs):
        influencer = Influencer.objects.filter(profile=request.user).first()
        influencer_serial = InfluencerSerializer(influencer)
        return Response(influencer_serial.data)
    
    def post(self, request, *args, **kwargs):
        pass

class ShopOwnerPublicView(ListAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    pagination_class = ShopOwnerPagination
    
    def get(self, request, *args, **kwargs):
        shop_owners = self.paginate_queryset(queryset=ShopOwner.objects.all())
        shop_owners_serial = ShopOwnerPublicSerailizer(shop_owners,many=True)
        return self.get_paginated_response(shop_owners_serial.data)


class GetToken(ListAPIView):
    def post(self, request, *args, **kwargs):
        pass