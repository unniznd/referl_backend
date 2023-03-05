from django.contrib import admin

from payment.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['amount','status','provider_order_id','payment_id','signature_id']

    def get_user(self,obj):
        return obj.user.name