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
