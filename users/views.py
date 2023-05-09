from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import filters
from users.models import ShopOwner, Influencer, Shops
from users.pagination import ShopOwnerPagination
from users.serializers import (
    InfluencerSerializer, ShopOwnerSerializer, 
    ShopSerializer, PinnedShopsSerializer

)

from cryptography.fernet import Fernet

import os
import ast

from dotenv import load_dotenv
load_dotenv()

fernet = Fernet(os.getenv('FERNET_KEY'))

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
    
    serializer_class = ShopSerializer
    pagination_class = ShopOwnerPagination
    search_fields = ['profile__name', 'profile__username']
    filter_backends = [ filters.SearchFilter, ]
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
        query_set = self.filter_queryset(Shops.objects.get_queryset())
        shop_owners = self.paginate_queryset(queryset=query_set)
        shop_owners_serial = ShopSerializer(
            shop_owners, many=True, 
            context = {
            'request':request
            }
        )
        return self.get_paginated_response(shop_owners_serial.data)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # request._mutable = True
        
        # request.data['password'] = fernet.decrypt((request.data['password']).encode()).decode()
        # request._mutable = False
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class PinShopsInfluencer(ListAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        influencer = Influencer.objects.filter(profile=request.user).first()
        pinned_shops = PinnedShopsSerializer(influencer, context={'request': request})
        return Response(pinned_shops.data)


        
    
    def post(self, request, id, *args, **kwargs):
        influencer = Influencer.objects.filter(profile=request.user).first()
        if influencer:
            if influencer.pinned_shops:
                pinned_shops = ast.literal_eval(influencer.pinned_shops)
            else:
                pinned_shops = []

            if id not in pinned_shops:
                pinned_shops.append(id)
                influencer.pinned_shops = str(pinned_shops)
                influencer.save()
                return Response({"status":True})
            return Response({"status":False,"error":"Shop already pinned!"})

        
        return Response({
            "status":False,
            "error":'No such profile found!'
        })

    def delete(self, request, id, *args, **kwargs):
        # unpin shop from the influencer
        influencer = Influencer.objects.filter(profile=request.user).first()
        if influencer:
            if influencer.pinned_shops:
                pinned_shops = ast.literal_eval(influencer.pinned_shops)
            else:
                pinned_shops = []
            
            if id in pinned_shops:
                pinned_shops.remove(id)
                influencer.pinned_shops = str(pinned_shops)
                influencer.save()
                return Response({"status":True})
            return Response({"status":False,"error":"Shop not pinned!"})
        
        return Response({
            "status":False,
            "error":'No such profile found!'
        })
