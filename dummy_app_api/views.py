from businesses.models import BusinessAccount, BusinessRating, BusinessLocations
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import (LocationSerializer,
                          AccountsSerializer,
                          RatingsandReviewsSerializer,
RatingsandReviewsCreateSerializer
                          )
from users.models import Transactions
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
)


class Locations_List(ListAPIView):
    """
        Returns a list of all business accounts from the database
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = BusinessLocations.objects.all()



class Ratings_And_Reviews_Create_APIView(CreateAPIView):
    """
        This is a call for recording user favorites as far as categories that they would like to get notified on from the learned deals they favorite
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RatingsandReviewsCreateSerializer
    queryset = BusinessRating.objects.all()


class Get_Ratings_and_Reviews_By_Location_List(ListAPIView):
    """
        Returns a list of all ratings and reviews of a particular business location
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RatingsandReviewsSerializer

    def get_queryset(self):
        businessId = self.kwargs['businessId']
        return BusinessRating.objects.filter(businessId__exact=businessId)


class Get_Ratings_and_Reviews_By_User(ListAPIView):
    """
        Returns a list of all ratings and reviews that a particular consumer has entered in their profile
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RatingsandReviewsSerializer

    def get_queryset(self):
        userId = self.kwargs['userId']
        return BusinessRating.objects.filter(userId__exact=userId)