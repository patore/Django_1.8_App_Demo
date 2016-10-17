from django.conf.urls import url
from .views import (
    Transaction_Create_APIView,
    Referral_Reward_Create_APIView,
    Preferences_Create_APIView,
    Preferences_Delete_APIView,
    Get_Transaction_By_User_APIView,
    Get_Preference_By_User_APIView,
    Get_Favorites_By_User_APIView,
    Get_User_APIView,
    Transaction_Update_APIView,
    Add_Points_APIView,
    Get_Points_By_User_APIView,
    Deduct_Points__APIView
)

urlpatterns = [
    url(r'^get_user/', Get_User_APIView, name='get_user'),
    url(r'^create_transaction/', Transaction_Create_APIView.as_view(), name='create_transaction'),
    url(r'^get_transaction/(?P<user>[\w-]+)/$', Get_Transaction_By_User_APIView.as_view(), name='get_transaction'),
    url(r'^update_transaction/(?P<id>[0-9]+)$', Transaction_Update_APIView.as_view(), name='update_transaction'),
    url(r'^create_rewards/', Referral_Reward_Create_APIView.as_view(), name='create_rewards'),
    url(r'^add_points/', Add_Points_APIView.as_view(), name='add_points'),
    url(r'^get_points/(?P<user_id>[0-9]+)$', Get_Points_By_User_APIView.as_view(), name='get_points'),
    url(r'^deduct_points/', Deduct_Points__APIView.as_view(), name='deduct_points'),
    url(r'^get_preferences/(?P<user_id>[0-9]+)$', Get_Preference_By_User_APIView.as_view(), name='get_preferences'),
    url(r'^get_favorites/(?P<user_id>[0-9]+)$', Get_Favorites_By_User_APIView.as_view(), name='get_favorites'),
    url(r'^create_preferences/', Preferences_Create_APIView.as_view(), name='create_preferences'),
    url(r'^delete_preferences/(?P<id>[0-9]+)$', Preferences_Delete_APIView.as_view(), name='delete_preferences'),
]