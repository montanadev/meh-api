from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, PaymentHistory
from .views import membership_due


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0


class UserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline, PaymentHistoryInline)

    def membership_due(self, obj):
        return membership_due(obj)

    membership_due.short_description = "Membership Due as of"

    list_display = DefaultUserAdmin.list_display + ('membership_due',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)