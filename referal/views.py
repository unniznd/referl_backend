from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError

from referal.models import Connection, ReferalEarning, PLATFORM
from referal.serializers import InfluencerRequestSerializer, ReferalSerializer, ActiveInfluencerSerializer
from referal.util import mark_expired, get_referalcode

from users.models import ShopOwner, Influencer, User

from datetime import datetime


class InfluencerRequestView(ListAPIView):
    queryset = Connection.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_request = Connection.objects.filter(
            shop_owner__profile=request.user, 
            current_status=0
        ).order_by('-created_at')
        connection_request_serial = InfluencerRequestSerializer(connection_request, many=True)
        return Response({
            "count":len(connection_request),
            "requests":connection_request_serial.data
        })


class PendingReferalView(ListAPIView):
    queryset = Connection.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_pending = Connection.objects.filter(
            influencer__profile=request.user,
            current_status=0,
        )
        connection_pending_serial = ReferalSerializer(connection_pending, many=True)
        return Response(connection_pending_serial.data)
    

class ActiveReferalView(ListAPIView):
    queryset = Connection.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_active = Connection.objects.filter(
            influencer__profile=request.user,
            current_status=1,
        )
        connection_active_serial = ReferalSerializer(connection_active, many=True)
        return Response(connection_active_serial.data)

class ExpiredReferalView(ListAPIView):
    queryset = Connection.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_expired = Connection.objects.filter(
            influencer__profile=request.user,
            current_status=2,
        )
        connection_expired_serial = ReferalSerializer(connection_expired, many=True)
        return Response(connection_expired_serial.data)

class InfluencerReferalSummaryView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    def get(self, request, *args, **kwargs):
        shopowner = Influencer.objects.filter(
            profile=request.user,
        ).first()
        total_earning = ReferalEarning.objects.filter(referal__influencer__profile=request.user)

        earned = 0

        for earning in total_earning:
            earned = earning.payout + earned
        

        return Response({
            "name":shopowner.profile.name,
            "referal":len(total_earning),
            "earned":earned
        })

class MonthlyReferalView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    def get(self, request, *args, **kwargs):
        month = datetime.now().month
        shopowner = ShopOwner.objects.filter(
            profile=request.user,
        ).first()

        total_earning = ReferalEarning.objects.filter(
            referal__shop_owner__profile=request.user,
            created_at__month = month
        )

        earned = 0

        for earning in total_earning:
            earned = earning.bill_amount + earned
        
        return Response({
            "balance":shopowner.balance,
            "referal":len(total_earning),
            "earned":earned,
            "payout":shopowner.payout,
            "validity":shopowner.validity
        })

class ActiveInfluencerView(ListAPIView):
    queryset = Connection.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_active = Connection.objects.filter(
            shop_owner__profile=request.user,
            current_status=1,
        )

        connection_active_serial = ActiveInfluencerSerializer(connection_active, many=True)
        return Response({
            "count":len(connection_active),
            "active":connection_active_serial.data
        })
    
    def post(self, request, id, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_active = Connection.objects.filter(
            shop_owner__profile=request.user,
            id = id
        ).first()

        if connection_active:
            connection_active.current_status = 1
            connection_active.payout = connection_active.shop_owner.payout
            connection_active.validity = connection_active.shop_owner.validity
            connection_active.referal_code = get_referalcode()
            connection_active.save()
            return Response({"status":"OK"})
        
        return Response({"status":"FAILED"})
    def delete(self, request,id, *args, **kwargs):
        mark_expired(Connection.objects.all())
        connection_active = Connection.objects.filter(
            shop_owner__profile=request.user,
            id = id
        ).first()

        if connection_active:
            
            connection_active.delete()
            return Response({"status":"OK"})
        
        return Response({"status":"FAILED"})

class ShopOwnerTotalReferalView(ListAPIView):
    queryset = ReferalEarning.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        total_earning = ReferalEarning.objects.filter(referal__shop_owner__profile=request.user)
        earned = 0

        for earning in total_earning:
            earned = earning.bill_amount + earned

        return Response({
            "total_customer":len(total_earning),
            "total_earning":earned
        })

class ShopOwnerReferal(ListAPIView):
    queryset = ReferalEarning.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        mark_expired(Connection.objects.all())
        try:
            connection = Connection.objects.filter(
                shop_owner__profile=request.user,
                current_status=1,
                referal_code=request.data.get('referal_code'),
            ).first()
            shop_owner = ShopOwner.objects.filter(profile=request.user,).first()
            influencer = Influencer.objects.filter(profile=connection.influencer.profile,).first()

            if connection:
                if shop_owner.balance - connection.payout>=0:
                    referal = ReferalEarning.objects.create(
                        referal = connection,
                        platform=request.data.get('platform'),
                        phone_number=request.data.get('phone_number'),
                        bill_amount=request.data.get('bill_amount'),
                        payout=connection.payout,
                    )
                    referal.save()
                    shop_owner.balance = shop_owner.balance - connection.payout
                    influencer.balance = influencer.balance + connection.payout
                    influencer.save()
                    shop_owner.save()
                    return Response({"id":referal.id})
                else:
                    return Response({"res":"Insufficient Balance"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
                
            else:
                return Response({"res":"Referal Expired or Invalid"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
            

        except IntegrityError:
            return Response({"res":"Referal Already Redeemed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        
        except:
            return Response({"res":"Unexcepted Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
    
class RequestReferal(ListAPIView):

    def post(self, request, *args, **kwagrs):
        try:
            user = User.objects.filter(id=request.data.get('id')).first()
            print(user)
            influencer = Influencer.objects.filter(
                profile=request.user,
            ).first()
            shop_owner = ShopOwner.objects.filter(
                profile=user
            ).first()
            if influencer and shop_owner:
                connection = Connection.objects.create(
                    influencer=influencer,
                    shop_owner=shop_owner,
                    current_status=0,
                )
                connection.save()
                return Response({"res":"OK"})
            else:
                return Response({"res":"Invalid Phone Number"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        except IntegrityError:
            return Response({"res":"Already Requested"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        
        except:
            return Response({"res":"Unexcepted Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
