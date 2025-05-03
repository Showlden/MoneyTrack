from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    UserViewSet,
    CategoryViewSet,
    TransactionViewSet,
    BudgetViewSet,
    GoalViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'budgets', BudgetViewSet, basename='budgets')
router.register(r'goals', GoalViewSet, basename='goals')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls