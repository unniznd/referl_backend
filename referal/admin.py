from django.contrib import admin

from referal.models import Connection, ReferalEarning

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['shop_owner_name','influencer_name','current_status',
                    'referal_code','payout','validity','updated_at','created_at']

    def shop_owner_name(self, obj):
        return obj.shop_owner.profile.name
    
    def influencer_name(self, obj):
        return obj.influencer.profile.name

@admin.register(ReferalEarning)
class ReferalEarningAdmin(admin.ModelAdmin):
    list_display = ['shop_owner_name','influencer_name','referal_code',
                'platform','phone_number','bill_amount' ,'created_at','payout']

    def referal_code(self, obj):
        return obj.referal.referal_code
        
    def shop_owner_name(self, obj):
        return obj.referal.shop_owner.profile.name
    
    def influencer_name(self, obj):
        return obj.referal.influencer.profile.name


    
