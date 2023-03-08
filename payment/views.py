from .models import Order
import razorpay
from .constants import PaymentStatus
from dotenv import load_dotenv
import os

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import permissions

from users.models import ShopOwner

load_dotenv()


RAZORPAY_KEY_ID = os.getenv("RZP_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RZP_SECREY_KEY")


class OrderPayment(ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        user = request.user
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
           shop_owner=user, amount=amount, provider_order_id=razorpay_order["id"], 
        )
        order.save()
        shop_owner = ShopOwner.objects.filter(profile=request.user).first()
        return Response(
            {
                "transaction_id":order.id,
                "key": RAZORPAY_KEY_ID,
                "order_id": razorpay_order["id"],
                "name":request.user.name,
                "email":request.user.email,
                "amount":razorpay_order["amount"],
                "description": "Add Money to Wallet",
            },
        )


class CallBack(ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    def verify_signature(self,response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    def post(self, request, *args, **kwargs):
        
        if "razorpay_signature" in request.data:
            payment_id = request.data.get("razorpay_payment_id", "")
            provider_order_id = request.data.get("razorpay_order_id", "")
            signature_id = request.data.get("razorpay_signature", "")
            try:
                order = Order.objects.get(provider_order_id=provider_order_id)
                order.payment_id = payment_id
                order.signature_id = signature_id
                order.save()
            except:
                return Response({"status": "FAILED"})

            
            try:
                isVerified = self.verify_signature(request.data)
            except:
                return Response({"status": "FAILED"})

            if isVerified:
                order.status = PaymentStatus.SUCCESS
                order.save()
                user = ShopOwner.objects.filter(profile=request.user)
                return Response({"status": order.status, "transaction_id":order.id})
            else:
                order.status = PaymentStatus.FAILURE
                order.save()
                user = ShopOwner.objects.filter(profile=request.user)
                user.balance = user.balance + order.amount
                return Response({"status": order.status, "transaction_id":order.id})
        else:
            payment_id = request.data.get("razorpay_payment_id")
            provider_order_id =request.data.get("razorpay_order_id")
            try:
                order = Order.objects.get(provider_order_id=provider_order_id)
                order.payment_id = payment_id
                order.status = PaymentStatus.FAILURE
                order.save()
            except:
                return Response({"status": "Failure"})
            return Response({"status": order.status, "transaction_id":order.id})


