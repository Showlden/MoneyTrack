from rest_framework import serializers
from .models import User, Category, Transaction, Budget, Goal
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get('password')
        
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user': UserSerializer(self.user).data})
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('owner',)

class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='category.type', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('owner',)
    
    def validate_category(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("You don't have permission to use this category.")
        return value

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ('owner',)
    
    def validate_category(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("You don't have permission to use this category.")
        return value

class GoalSerializer(serializers.ModelSerializer):
    current_progress = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('owner', 'current_progress')