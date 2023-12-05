from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer(required=False)

#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email', 'password', 'profile')  
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         user = CustomUser.objects.create_user(**validated_data)
        
#         if profile_data:
#             UserProfile.objects.create(user=user, **profile_data)

#         return user
    
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
