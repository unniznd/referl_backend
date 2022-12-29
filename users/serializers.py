from rest_framework import serializers

from users.models import( 
    ShopOwner as ShopOwnerModel, 
    Influencer as InfluencerModel
)

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
                 'auth_provider','balance','payout','validity')

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

    class Meta:
        model = ShopOwnerModel
        fields = ('id','username','name','email','payout','validity')
