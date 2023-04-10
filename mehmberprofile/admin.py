from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, PaymentHistory, MembershipHistory
from .views import membership_due


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0


class MembershipHistoryInline(admin.TabularInline):
    model = MembershipHistory
    extra = 0


class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline, PaymentHistoryInline, MembershipHistoryInline]

    def membership_due(self, obj):
        due = membership_due(obj)
        str_due = "${:,.2f}".format(abs(due))
        return str_due + '(credit)' if due < 0 else str_due

    membership_due.short_description = "Membership Due as of"

    list_display = DefaultUserAdmin.list_display + ('membership_due',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
