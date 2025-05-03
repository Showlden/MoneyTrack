from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.utils import timezone
from .models import User, Category, Transaction, Budget, Goal
from .serializers import (
    UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer,
    CategorySerializer, TransactionSerializer, BudgetSerializer, GoalSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user).select_related('category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=False, methods=['get'])
    def summary(self, request):
        time_period = request.query_params.get('period', 'month')
        now = timezone.now()
        
        if time_period == 'month':
            transactions = self.get_queryset().filter(
                date__month=now.month,
                date__year=now.year
            )
        elif time_period == 'year':
            transactions = self.get_queryset().filter(
                date__year=now.year
            )
        else:  # all time
            transactions = self.get_queryset()
        
        income = transactions.filter(category__type=Category.Type.INCOME).aggregate(
            Sum('amount'))['amount__sum'] or 0
        expense = transactions.filter(category__type=Category.Type.EXPENSE).aggregate(
            Sum('amount'))['amount__sum'] or 0
        
        by_category = transactions.values('category__name', 'category__type').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'income': income,
            'expense': expense,
            'balance': income - expense,
            'by_category': by_category
        })

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user).select_related('category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)