from django.contrib import admin
from .models import User, ShopOwner, Influencer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','name','email','auth_provider','updated_at','created_at']

@admin.register(ShopOwner)
class ShopOwnerAdmin(admin.ModelAdmin):
    list_display = ['profile_name','balance','payout','validity', 'profile_pic']

    def profile_name(self,obj):
        return obj.profile.name

@admin.register(Influencer)
class InfluencersAdmin(admin.ModelAdmin):
    list_display = ['profile_name','balance','social','profile_pic']

    def profile_name(self,obj):
        return obj.profile.name