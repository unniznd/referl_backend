from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from users.models import ShopOwner, Influencer

STATUS = (
    (0, "Pending"),
    (1, "Active"),
    (2, "Expired"),
) 

PLATFORM = (
    (1, "Instagram"),
    (2, "WhatsApp"),
    (3, "Facebook"),
    (4, "Twitter"),
    (5, "Snapchat"),
    (6, "Other")
)


class Connection(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    current_status = models.IntegerField(choices=STATUS,default=0)
    referal_code = models.CharField(max_length=6,default=0)
    payout = models.IntegerField(default=0)
    validity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.shop_owner.profile.name + " " + self.influencer.profile.name
    
    class Meta:
        unique_together = ('shop_owner','influencer','created_at')

class ReferalEarning(models.Model):
    referal = models.ForeignKey(Connection, on_delete=models.CASCADE)
    phone_number =  models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(r'^\d{1,10}$')
        ]
    )
    platform = models.IntegerField( choices=PLATFORM)
    bill_amount = models.IntegerField(validators=[MinValueValidator(0)])
    payout = models.IntegerField(validators=[MinValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.referal.referal_code

    class Meta:
        unique_together = ('referal','phone_number')