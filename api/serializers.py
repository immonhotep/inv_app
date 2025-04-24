
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Category,Distributor,Item,Company_Premises,Order
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse



class UserCreationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,style={'input_type': 'password'},validators=[validate_password])
    password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name' ,'password', 'password2')
        extra_kwargs = {"email": {"required": True, "allow_null": False},"first_name":{"required": True, "allow_null": False},"last_name":{"required": True, "allow_null": False}}
        read_only_fields = ('id',)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "two password fields didn't match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserUpdateSerializer(serializers.ModelSerializer):

    
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')
        read_only_fields = ('id',)
        extra_kwargs = {"email": {"required": True, "allow_null": False},"first_name":{"required": True, "allow_null": False},"last_name":{"required": True, "allow_null": False}}

class ManageUserSerializer(serializers.ModelSerializer):
  
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','is_active')
        read_only_fields = ('id',)
        extra_kwargs = {"email": {"required": True, "allow_null": False},"first_name":{"required": True, "allow_null": False},"last_name":{"required": True, "allow_null": False}}


class ResetPasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    new_password1 = serializers.CharField(write_only=True,style={'input_type': 'password'},validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "old password is wrong"})
        return value
    

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "two password fields didn't match"})
        return data
    

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        update_session_auth_hash(self.context['request'], user)
        return user


class CategorySerializer(serializers.ModelSerializer):

    description = serializers.CharField(max_length=3000)

    class Meta:
        model = Category
        fields=('id','slug','name','description')
        read_only_fields=('id','slug')


class DistributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Distributor
        fields=('id','slug','name','address','phone','email')
        read_only_fields=('id','slug')



class ItemSerializer(serializers.ModelSerializer):

    in_stock = serializers.IntegerField(min_value=1, max_value=100000)

    class Meta:
        model = Item
        fields=('id','slug','name','in_stock','category','distributor','worker')
        read_only_fields=('id','slug','worker','code')


class PremisesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company_Premises
        fields=('id','slug','name','address','phone','email')
        read_only_fields=('id','slug','contract_started')

class OrderSerializer(serializers.ModelSerializer):

    STATUS = (

    ('P','Placed'),
    ('T','In Transit'),
    ('D','Delivered'),
    ('C','Closed'),
    )

    amount = serializers.IntegerField(required=True,min_value=1, max_value=100000)
    status = serializers.ChoiceField(required=True,choices=STATUS)

    class Meta:
        model = Order
        fields = ('slug','worker','client','item','amount','status','date_placed','date_closed')
        read_only_fields = ('slug','worker','date_closed','date_placed',)

