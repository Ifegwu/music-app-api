from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasUserAdmin
from django.utils.translation import gettext as _

from .models import User, Subscriptions

class SubscriptionsInline(admin.StackedInline):
    model = Subscriptions
    max_num = 1
    can_delete = False

class UserAdmin(BasUserAdmin):
    ordering = ['id']
    list_display = ['email', 'username']
    inlines = [SubscriptionsInline]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username',)}),
        (
            _('Persmission'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': (
                                    'last_login', 
                                    'date_joined', 
                                    'is_verified',
                                    )}
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscriptions)
