from rest_framework import serializers

from referal.models import Connection, ReferalEarning

import ast

class InfluencerRequestSerializer(serializers.ModelSerializer):
    influencer_name = serializers.CharField(source="influencer.profile.name")
    social = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()
    profile_pic = serializers.ImageField(source="influencer.profile_pic")

    def get_social(self, obj):
        return ast.literal_eval(obj.influencer.social)
    
    def get_current_status(self, obj):
        return obj.get_current_status_display()
    

    class Meta:
        model = Connection
        fields = ('id','influencer_name','referal_code','current_status','social','profile_pic')
    

class ReferalSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source="shop_owner.profile.name")
    no_of_referal = serializers.SerializerMethodField()
    earned_money = serializers.SerializerMethodField()
    referal_code = serializers.SerializerMethodField()

    def get_no_of_referal(self,obj):
        referal_earning = ReferalEarning.objects.filter(referal__referal_code=obj.referal_code)
        if referal_earning:
            return len(referal_earning)
        
        return 0;
    
    def get_earned_money(self, obj):
        referal_earning = ReferalEarning.objects.filter(referal__referal_code=obj.referal_code)
        if referal_earning:
            money = 0
            for referal in referal_earning:
                money = money + referal.bill_amount
            
            return money
        
        return 0

    def get_referal_code(self, obj):
        
        if obj.current_status == 0:
            return "Not Generated"
        elif obj.current_status == 2:
            return "Expired"
        
        return obj.referal_code
    class Meta:
        model = Connection
        fields = ('shop_name', 'referal_code','no_of_referal','earned_money')


class ActiveInfluencerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="influencer.profile.name")
    social = serializers.SerializerMethodField()
    total_referal = serializers.SerializerMethodField()
    total_earning = serializers.SerializerMethodField()
    profile_pic = serializers.ImageField(source="influencer.profile_pic")

    def get_social(self, obj):
        return ast.literal_eval(obj.influencer.social)
    
    def get_total_referal(self, obj):
        return len(ReferalEarning.objects.filter(referal=obj))
    
    def get_total_earning(self, obj):
        referals = ReferalEarning.objects.filter(referal=obj)
        earned = 0
        if referals:
            for referal in referals:
                earned = earned + referal.bill_amount
        return earned

    class Meta:
        model = Connection
        fields = ('id','name','social','total_earning','total_referal','profile_pic')
