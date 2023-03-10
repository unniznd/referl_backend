from rest_framework import serializers
from users.models import( 
    ShopOwner as ShopOwnerModel, 
    Influencer as InfluencerModel
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
                 'auth_provider','balance','social')

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
        conncetion = Connection.objects.filter(shop_owner=obj,influencer=influencer, current_status=0)
        if conncetion:
            return True
        return False
