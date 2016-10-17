from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from .models import Transactions, Preferences, ReferralRewards, Points
from rest_framework.serializers import (
    ModelSerializer,
)

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

from dummy_appapi.serializers import (
                                  LocationSerializer,
                                  AccountsSerializer,
                                  )
UserModel = get_user_model()
from django.contrib.auth.models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('email', 'id')
        read_only_fields = ('email', )


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        elif username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class TransactionsCreateSerializer(ModelSerializer):

    class Meta:
        model = Transactions
        fields = [
            'user',
            'businessLocation',
            'redeemed',
        ]

    def create(self, validated_data):
        print(validated_data)
        user = validated_data['user']
        businessLocation = validated_data['businessLocation']
        redeemed = validated_data['redeemed']
        transaction_obj = Transactions(
            user=user,
            businessLocation=businessLocation,
            redeemed=redeemed,
        )
        transaction_obj.save()
        return validated_data


class TransactionsSerializer(ModelSerializer):
    user = User()
    businessLocation = LocationSerializer()

    class Meta:
        model = Transactions
        fields = [
            'user',
            'businessLocation',
            'redeemed',
        ]


class TransactionsUpdateSerializer(ModelSerializer):

    class Meta:
        model = Transactions
        fields = [
            'id'
        ]


class ReferralRewardCreateSerializer(ModelSerializer):

    class Meta:
        model = ReferralRewards
        fields = [
            'user',
            'businessLocation',
            'redeemed',
            'referredto',
        ]

    def create(self, validated_data):
        print(validated_data)
        user = validated_data['user']
        businessLocation = validated_data['businessLocation']
        redeemed = validated_data['redeemed']
        referredto = validated_data['referredto']
        rewards_obj = ReferralRewards(
            user=user,
            businessLocation=businessLocation,
            redeemed=redeemed,
            referredto=referredto,
        )
        rewards_obj.save()
        return validated_data


class ReferralRewardSerializer(ModelSerializer):
    user = UserDetailsSerializer()
    referredto = UserDetailsSerializer()
    businessLocation = LocationSerializer()

    class Meta:
        model = ReferralRewards
        fields = [
            'id',
            'user',
            'businessLocation',
            'redeemed',
            'referredto',
        ]


class ReferralRewardUpdateSerializer(ModelSerializer):

    class Meta:
        model = ReferralRewards
        fields = [
            'id'
        ]


class UserPreferencesCreateSerializer(ModelSerializer):
    class Meta:
        model = Preferences
        fields = [
            'user',
            'businesslocationid',
        ]

    def create(self, validated_data):
        user = validated_data['user']
        businesslocationid = validated_data['businesslocationid']

        preferences_obj = Preferences(
            user=user,
            businesslocationid=businesslocationid,
        )
        preferences_obj.save()
        return preferences_obj


class UserPreferencesSerializer(ModelSerializer):
     class Meta:
        model = Preferences
        fields = [
            'id', 'businesslocationid'
        ]


class UserFavoritesSerializer(ModelSerializer):
    class Meta:
        model = Preferences
        fields = [
            'id', 'businesslocationid'
        ]


class UserPointsSerializer(ModelSerializer):

    class Meta:
        model = Points
        fields = [
            'user',
            'businessLocation',
            'points',
        ]


class PointsCreateSerializer(ModelSerializer):
    class Meta:
        model = Points
        fields = [
            'user',
            'businessLocation',
            'points'
        ]

    def create(self, validated_data):
        user = validated_data['user']
        businessLocation = validated_data['businessLocation']
        points = validated_data['points']

        points_obj = Preferences(
            user=user,
            businessLocation=businessLocation,
            points=points,
        )
        points_obj.save()
        return points_obj


class PointsUpdateSerializer(ModelSerializer):

    class Meta:
        model = Points
        fields = [
            'id',
            'points'
        ]