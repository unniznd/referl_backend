from rest_framework import serializers
from users.models import( 
    ShopOwner as ShopOwnerModel, 
    Influencer as InfluencerModel,
    Shops as ShopModel
)

from referal.models import Connection

from datetime import date, timedelta

import ast

class ShopOwnerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="profile.id")
    username = serializers.CharField(source="profile.email")
    name = serializers.CharField(source="profile.name")
    email = serializers.EmailField(source="profile.email")
    auth_provider = serializers.CharField(source="profile.auth_provider")

    class Meta:
        model = ShopOwnerModel
        fields = ('id','username','name','email',
                 'auth_provider','balance','payout','validity', 'profile_pic')

class InfluencerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="profile.id")
    username = serializers.CharField(source="profile.username")
    name = serializers.CharField(source="profile.name")
    email = serializers.EmailField(source="profile.email")
    auth_provider = serializers.CharField(source="profile.auth_provider")
    social = serializers.SerializerMethodField()

    class Meta:
        model = InfluencerModel
        fields = ('id','username','name','email',
                 'auth_provider','balance','social', 'phone_number', 'profile_pic')

    def get_social(self, obj):
        return ast.literal_eval(obj.social)

class ShopOwnerPublicSerailizer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="profile.id")
    username = serializers.CharField(source="profile.username")
    name = serializers.CharField(source="profile.name")
    email = serializers.EmailField(source="profile.email")
    validity = serializers.SerializerMethodField()

    has_pending = serializers.SerializerMethodField()

    class Meta:
        model = ShopOwnerModel
        fields = ('id','username','name','email','payout','validity', 'has_pending', 'profile_pic')
    
    def get_validity(self, obj):
        return (date.today() + timedelta(days=obj.validity)).strftime("%d-%b-%Y")
    
    def get_has_pending(self, obj):
        request = self.context.get('request', None)
        influencer = InfluencerModel.objects.filter(profile=request.user).first()
        conncetion = Connection.objects.filter(
            shop_owner=obj,
            influencer=influencer, 
            current_status=0
        ).first()
        if conncetion:
            return True
        return False

class ShopSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="shop_owner.profile.id")
    owner_name = serializers.CharField(source="shop_owner.profile.name")
    owner_email = serializers.EmailField(source="shop_owner.profile.email")
    payout = serializers.IntegerField(source="shop_owner.payout")
    validity = serializers.SerializerMethodField()
    has_pending = serializers.SerializerMethodField()
    is_pinned = serializers.SerializerMethodField()


    class Meta:
        model = ShopModel
        fields = ('id','owner_name','owner_email','name','address',
                 'validity', 'has_pending', 'payout', 'shop_pic', 'is_pinned')

    def get_validity(self, obj):
        return (date.today() + timedelta(days=obj.shop_owner.validity)).strftime("%d-%b-%Y")
    
    def get_has_pending(self, obj):
        request = self.context.get('request', None)
        influencer = InfluencerModel.objects.filter(profile=request.user).first()
        conncetion = Connection.objects.filter(
            shop_owner=obj.shop_owner,
            influencer=influencer, 
            current_status=0
        ).first()
        if conncetion:
            return True
        return False
    
    def get_is_pinned(self, obj):
        request = self.context.get('request', None)
        influencer = InfluencerModel.objects.filter(profile=request.user).first()
        print(1 in ast.literal_eval(influencer.pinned_shops))
        if influencer:
            if obj.shop_owner.profile.id in ast.literal_eval(influencer.pinned_shops):
                return True
        return False
    
class PinnedShopsSerializer(serializers.ModelSerializer):
    pinned_shops = serializers.SerializerMethodField()

    class Meta:
        model = InfluencerModel
        fields = ('pinned_shops',)

    def get_pinned_shops(self, obj):
        shops = []
        request = self.context.get('request', None)
        
        for i in ast.literal_eval(obj.pinned_shops):
            shop = ShopModel.objects.filter(shop_owner__profile=i).first()
            influencer = InfluencerModel.objects.filter(profile=request.user).first()
            conncetion = Connection.objects.filter(
                shop_owner=shop.shop_owner,
                influencer=influencer, 
                current_status=0
            ).first()
            if shop:
                pic = None
                if shop.shop_pic:
                    pic = shop.shop_pic.url

                shops.append({
                    "id": shop.id,
                    "name": shop.name,
                    "address": shop.address,
                    "shop_pic": pic,
                    "payout":shop.shop_owner.payout,
                    "validity":(date.today() + timedelta(days=shop.shop_owner.validity)).strftime("%d-%b-%Y"),
                    "has_pending": True if conncetion else False
                })


        return shops