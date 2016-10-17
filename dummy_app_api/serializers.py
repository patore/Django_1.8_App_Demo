from rest_framework import serializers
from businesses.models import (BusinessAccount,
                               BusinessLocations,
                               BusinessRating
                               )
from django.contrib.auth.models import User


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAccount
        fields = ('id',
                  'legalbusinessname',
                  'businesslogo',
                  'address_line1',
                  'address_line2',
                  'city',
                  'state',
                  'zipcode',
                  'email',
                  'phone',
                  'websiteurl'
                  )


class LocationSerializer(serializers.ModelSerializer):
    business = AccountsSerializer()

    class Meta:
        model = BusinessLocations
        fields = ('id',
                  'business',
                  'locationname',
                  'address_line1',
                  'address_line2',
                  'waittimemapping',
                  'city',
                  'slug',
                  'state',
                  'zipcode',
                  'phone',
                  'websiteurl',
                  )


class RatingsandReviewsSerializer(serializers.ModelSerializer):
    businessId = LocationSerializer()

    class Meta:
        model = BusinessRating
        fields = (
            'businessId',
            'userId',
            'rating',
            'review',
        )


class RatingsandReviewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessRating
        fields = (
            'businessId',
            'userId',
            'rating',
            'review',
        )

    def create(self, validated_data):
        businessId = validated_data['businessId']
        userId = validated_data['userId']
        rating = validated_data['rating']
        review = validated_data['review']

        ratings_obj = BusinessRating(
            businessId=businessId,
            userId=userId,
            rating=rating,
            review=review,
        )
        ratings_obj.save()
        return validated_data








