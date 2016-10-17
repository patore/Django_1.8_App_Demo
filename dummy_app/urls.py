from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^rest-auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
    url(r'^dummy_app_business/', views.dummy_appbusiness, name='dummy_app_business'),
    url(r'^new_business_form/', views.BusinessAccountCreateView.as_view(), name='new_business_form'),
    url(r'^profile/', views.businessProfile, name='deal_profile'),
    url(r'^authorized/sub/login/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^businesses/', include('businesses.urls')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^user-api/', include('users.urls')),
    url(r'^auth-api/api-dummy_app/', include('dummy_appapi.urls')),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


