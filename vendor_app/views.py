from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count, Avg
from django.utils import timezone
from .models import Vendor, PurchaseOrder
from .serializers import *
from django.db import models
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token

class UserCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes=[AllowAny]
    
    def post(self, request, format=None):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                # Generate Token for the newly created vendor
                vendor = serializer.instance
                token, created = Token.objects.get_or_create(user=vendor)

                return Response({
                    'user': serializer.data,
                    'token': token.key  # Include the token in the response
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}','status':'Error','Status_code':400}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = CustomUser.objects.filter(username=username).first()

        if user is not None and user.password==password:
            # Vendor found, generate token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's token to log them out
            request.auth.delete()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}', 'status': 'Error', 'Status_code': 400},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# API - Create new vendor and view vendor list
class VendorListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API - View, Edit, Delete Vendor
class VendorRetrieveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response({"Error":"Vendor Deleted Successfully!"},status=status.HTTP_204_NO_CONTENT)

# API - Create purchase order and view list of PO
class PurchaseOrderListCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, format=None):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API - View, Edit, Delete PO
class PurchaseOrderRetrieveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# API - Vendor performance 
class VendorPerformanceView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)

        # Calculate performance metrics
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

        # On-Time Delivery Rate
        on_time_delivery_count = completed_orders.filter(delivery_date__lte=timezone.now()).count()
        total_completed_orders = completed_orders.count()
        on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate

        # Quality Rating Average
        quality_rating_avg = completed_orders.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg']
        vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg else 0

        # Save updated performance metrics
        vendor.save()

        return Response(serializer.data)

# API - to add aknowledge date
class AcknowledgePurchaseOrderView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            # Acknowledge the purchase order and update acknowledgment_date
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger recalculation of average_response_time
            vendor = purchase_order.vendor
            completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
            response_times = completed_orders.annotate(
                response_time=Count('acknowledgment_date', distinct=True, output_field=models.FloatField())
            ).aggregate(Avg('response_time'))['response_time__avg']
            vendor.average_response_time = response_times if response_times else 0
            vendor.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)