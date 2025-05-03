from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class Category(models.Model):
    class Type(models.TextChoices):
        INCOME = 'IN', _('Доход')
        EXPENSE = 'EX', _('Расход')
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=Type.choices, default='IN')
    color = models.CharField(max_length=7, default='#000000')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    
    class Meta:
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name_per_user')
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    @property
    def type(self):
        return self.category.type
    
    def __str__(self):
        return f"{self.date} - {self.amount} ({self.category.name})"

class Budget(models.Model):
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'month', 'year', 'category'], 
                name='unique_budget_per_category_per_month'
            )
        ]
    
    def __str__(self):
        return f"{self.month}/{self.year} - {self.limit} for {self.category.name}"

class Goal(models.Model):
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    deadline = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    
    @property
    def current_progress(self):
        from django.db.models import Sum
        return self.owner.transactions.filter(
            category__type=Category.Type.INCOME
        ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    def __str__(self):
        return f"{self.name} (Target: {self.target_amount})"