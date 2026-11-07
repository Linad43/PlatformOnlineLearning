from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Payment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные данные', {
            'fields': ('phone', 'city', 'avatar'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные данные', {
            'fields': ('email', 'phone', 'city', 'avatar'),
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'payment_date', 'amount', 'payment_method'
    )
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('user__email',)
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc5MzU0OTQwMSwiaWF0IjoxNzkzNDYzMDAxLCJqdGkiOiI4ZDQ4MWYxYmMxYmI0NjU4YWIwMzg2OTg1Mjk2YmJiOCIsInVzZXJfaWQiOiIyIn0.B4T7ouHx1Z-DG8iPn8LMvlo8ad-Fef1SMUCOfeqoXfU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzNDYzMzAxLCJpYXQiOjE3OTM0NjMwMDEsImp0aSI6ImFiZjMxNmFkOTdkZDQ5NTY5ZjhiYTkyYTJjZWZmN2EyIiwidXNlcl9pZCI6IjIifQ.xLZhcQkKF9l7AKzgvw9mGTZW9cq3DUgdYbhLFCVedvA"
}