from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
import re
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Category,Item
from django.http import Http404
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import uuid




class ApiSummary(generics.GenericAPIView):

    permission_classes = (AllowAny,)

    def get(self,request):
        api_urls = {
            'API summary' :'/',      
            'List create users' : 'manage-user/',
            'Detail update delete users' : 'manage-user/<int:pk>/',
            'Session login' : 'api-auth/login/',
            'Session logout' : 'api-auth/logout/',
            'Update user' :'update-user/',
            'Change password' : ' change-password/',
            'Obtain JWT auth token' : 'token/',
            'Refresh JWT auth token' : 'token/refresh/',
            'List create categories' : 'category/',
            'Detail update delete categories' : 'category/<slug:slug>/',
            'List create distributors' : 'distributor/',
            'Detail update delete distributors' : 'distributor/<slug:slug>/',
            'List create items' : 'item/',
            'Detail update delete items' : 'item/<slug:slug>/',
            'List create premises':'premises',
            'Detail update delete premises' : 'premises/<slug:slug>/',
            'List create order' : 'order/',
            'Detail update delete odrder' : 'order/<slug:slug>',
            }
        
        return Response(api_urls)


class UserListCreateAPIView(generics.ListCreateAPIView):  
    
    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = UserCreationSerializer
    queryset = User.objects.all()


class ManageUserAPIView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ManageUserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        return obj

    def get(self, request):
        user = self.get_object()
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ChangePasswordAPIView(generics.UpdateAPIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ResetPasswordSerializer
 
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'success': 'Your password updated'}, status=200)

       


class CategoryListCreateAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    

class CategoryDetailUpdateDeleteAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def get(self,request,slug):
        try:
            category = Category.objects.get(slug=slug)
            serializer = CategorySerializer(category,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)


    def put(self,request,slug):
        try:
            category = Category.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
        
        serializer = CategorySerializer(category, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
   
        
    def delete(self,request,slug):
        try:
            category = Category.objects.get(slug=slug)
            category.delete()
            return Response({'success': 'category deleted'}, status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)


class DistributorListCreateAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DistributorSerializer

    def get(self, request):
        distributor = Distributor.objects.all()
        serializer = DistributorSerializer(distributor, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = DistributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    

class DistributorDetailUpdateDeleteAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DistributorSerializer

    def get(self,request,slug):
        try:
            distributor = Distributor.objects.get(slug=slug)
            serializer = DistributorSerializer(distributor,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)

    def put(self,request,slug):
        try:
            distributor = Distributor.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
        
        serializer = DistributorSerializer(distributor, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
         
    def delete(self,request,slug):
        try:
            distributor = Distributor.objects.get(slug=slug)
            distributor.delete()
            return Response({'success': 'distributor deleted'}, status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)


class ItemListCreateAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['worker'] = request.user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)


class ItemDetailUpdateDeleteAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self,request,slug):
        try:
            item = Item.objects.get(slug=slug)
            serializer = ItemSerializer(item,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
    
    def put(self,request,slug):
        try:
            item = Item.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
        
        serializer = ItemSerializer(item, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

         
    def delete(self,request,slug):
        try:
            item = Item.objects.get(slug=slug)
            item.delete()
            return Response({'success': 'item deleted'}, status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)


class ListCreatePremisesAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PremisesSerializer

    def get(self,request):

        premises = Company_Premises.objects.all()
        serializer = PremisesSerializer(premises, many=True)
        return Response(serializer.data)
    
    def post(self,request):

        serializer = PremisesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)



class PremisesDetailUpdateDeleteAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PremisesSerializer

    def get(self,request,slug):
        try:
            premises = Company_Premises.objects.get(slug=slug)
            serializer = PremisesSerializer(premises,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
    
    def put(self,request,slug):
        try:
            premises = Company_Premises.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
        
        serializer = PremisesSerializer(premises, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

         
    def delete(self,request,slug):
        try:
            premises = Company_Premises.objects.get(slug=slug)
            premises.delete()
            return Response({'success': 'premises deleted'}, status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)



class ListCreateOrderAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer


    def get(self,request):

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self,request):

        orders = Order.objects.all().exclude(status__iexact="C")

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():

            item = serializer.validated_data['item']
            available = item.in_stock
            status = serializer.validated_data['status']
            
            if available < serializer.validated_data['amount']:
                return Response({'error':'request unable to perform, because not enought item in stock'})
            if orders:
                summary = 0
                for order in orders:
                    summary += order.amount        
                if ( summary + serializer.validated_data['amount'] )  > available:
                    return Response({'error':'request unable to perform, too much order placed, and not enought item in stock'})
                
            serializer.validated_data['worker'] = request.user
            if status == "C":
                item.in_stock = ( item.in_stock - serializer.validated_data['amount'] )
                item.save()
                serializer.validated_data['date_closed'] = timezone.now()

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    


class OrderDetailUpdateDeleteAPIView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self,request,slug):
        try:
            order = Order.objects.get(slug=slug)              
            serializer = OrderSerializer(order,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
    
    def put(self,request,slug):
        
        orders = Order.objects.all().exclude(status__iexact="C").exclude(slug=slug)


        try:
            order = Order.objects.get(slug=slug)
            if order.status == "C":
                return Response({'error': 'closed orders unable to modify'}, status=200) 
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
        
        serializer = OrderSerializer(order, request.data)
        if serializer.is_valid():
            item = serializer.validated_data['item']
            available = item.in_stock
            status = serializer.validated_data['status']
            if available < serializer.validated_data['amount']:
                return Response({'error':'request unable to perform, because not enought item in stock'}) 
                     
            if orders:
                summary = 0
                for order in orders:
                    summary += order.amount        
                if ( summary + serializer.validated_data['amount'] )  > available:
                    return Response({'error':'request unable to perform, too much order placed, and not enought item in stock'})  

            
            serializer.validated_data['worker'] = request.user
           
            if status == "C":
                item.in_stock = ( item.in_stock - serializer.validated_data['amount'] )
                item.save()
                serializer.validated_data['date_closed'] = timezone.now()
                
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

         
    def delete(self,request,slug):
        try:
            order = Order.objects.get(slug=slug)
            if order.status == "C":
                return Response({'error': 'closed orders unable to delete'}, status=200) 
            order.delete()
            return Response({'success': 'order deleted'}, status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)