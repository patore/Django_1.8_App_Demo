from django.conf.urls import url
from .views import (
    Locations_List,
                    Get_Ratings_and_Reviews_By_Location_List,
                    Get_Ratings_and_Reviews_By_User,
                    Ratings_And_Reviews_Create_APIView,
                    )

urlpatterns = [
    url(r'^locations_list/', Locations_List.as_view(), name='locations_list'),
    url(r'^create_ratings_by_user/(?P<userId>[\w-]+)/$', Ratings_And_Reviews_Create_APIView.as_view(), name='create_ratings_by_user'),
    url(r'^get_ratings_by_user/(?P<userId>[\w-]+)/$', Get_Ratings_and_Reviews_By_User.as_view(), name='get_ratings_by_user'),
    url(r'^get_ratings_by_business/(?P<businessId>[\w-]+)/$', Get_Ratings_and_Reviews_By_Location_List.as_view(), name='get_ratings_by_location'),

]