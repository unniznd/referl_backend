from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin
from django.core.validators import MinValueValidator

from users.manager import UserManager

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}
def user_directory_path(instance, filename):

    user = User.objects.filter(email=instance.profile.email).first()
    return '{0}/{1}'.format(user.id, filename)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

class ShopOwner(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    payout = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    validity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self) -> str:
        return self.profile.name +" - " + str(self.balance)

class Influencer(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    social = models.CharField(max_length=2048,)
    pinned_shops = models.CharField(max_length=1024, null=True, default='[]')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.profile.name} - {str(self.balance)}"

class Shops(models.Model):
    shop_owner = models.OneToOneField(ShopOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shop_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} -  {self.shop_owner.profile.name}"

