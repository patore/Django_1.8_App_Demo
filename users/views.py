from django.db import connection
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication, get_authorization_header
)
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
)
from .serializers import (
    TransactionsCreateSerializer,
    TransactionsUpdateSerializer,
    TransactionsSerializer,
    ReferralRewardCreateSerializer,
    UserPreferencesCreateSerializer,
    UserPreferencesSerializer,
    UserFavoritesSerializer,
    UserPointsSerializer,
    PointsUpdateSerializer,
    PointsCreateSerializer
)
from .models import Transactions, Preferences, ReferralRewards, Points

from dummy_app.utils import *


@api_view(['GET'])
def Get_User_APIView(request):
    if request.user.id != None:
        return Response({'user_id': request.user.id, 'username' : request.user.username})
    token = str(get_authorization_header(request)).split('JWT  ')[1].replace("'", "")
    return Response(jwt_decode_handler(token))


class Transaction_Create_APIView(CreateAPIView):
    """
        In this call, when a user saves a deal for redemption, the transaction is posted here
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionsCreateSerializer
    queryset = Transactions.objects.all()


class Transaction_Update_APIView(UpdateAPIView):
    """
        the transaction is updated here to record the earned points
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = TransactionsUpdateSerializer

    def update(self, request, *args, **kwargs):
        transaction = Transactions.objects.get(id=kwargs['id'])
        transaction.redeemed = True
        transaction.save()
        return Response()


class Get_Transaction_By_User_APIView(ListAPIView):
    """
        Returns transactions by the user
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionsSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        return Transactions.objects.filter(user__exact=user, redeemed=False)


class Referral_Reward_Create_APIView(CreateAPIView):
    """
       # In this call, when a user refers a deal to different outlets e.g facebook, email, text e.t.c, the transaction is posted here
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReferralRewardCreateSerializer
    queryset = ReferralRewards.objects.all()


class Add_Points_APIView(UpdateAPIView):
    """
        #In this call, when a referred user redeems or purchases a deal, the transaction is updated here to record the earned points
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PointsCreateSerializer
    queryset = Points.objects.all()


class Deduct_Points__APIView(UpdateAPIView):
    """
        #In this call, when a referred user redeems or purchases a deal, the transaction is updated here to record the earned points
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = PointsUpdateSerializer

    def update(self, request, *args, **kwargs):
        points = Points.objects.get(id=kwargs['id'], businessLocation=kwargs['locationid'])

        if kwargs['points'] > points.points:
            points = points.points - kwargs['points']
            points.save()
            return Response()
        else:
            return Response('points entered must be greater than available points')


class Get_Points_By_User_APIView(ListAPIView):
    """
        #Returns rewards by the user
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserPointsSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        return Points.objects.filter(user__exact=user)


class Preferences_Create_APIView(CreateAPIView):
    """
        This is a call for recording user favorites as far as categories that they would like to get notified on from the learned deals they favorite
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserPreferencesCreateSerializer
    queryset = Preferences.objects.all()


class Preferences_Delete_APIView(DestroyAPIView):
    """
        This is a call for recording user favorites as far as categories that they would like to get notified on from the learned deals they favorite
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        instance = Preferences.objects.get(id=id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class Get_Preference_By_User_APIView(ListAPIView):
    """
        Returns the preferences by the user
    """
    serializer_class = UserPreferencesSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Preferences.objects.filter(user=user_id)


class Get_Favorites_By_User_APIView(ListAPIView):
    """
        Returns the favorites by the user
    """
    serializer_class = UserFavoritesSerializer

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        with connection.cursor() as c:
            c.execute('SELECT P.id, P.businesslocationid_id AS locationid FROM users_preferences AS P INNER JOIN businesslocations_businesslocation AS D ON P.businesslocationid_id = D.id WHERE P.user_id = %s AND D.active', [user_id])
            return Response(dictfetchall(c))




