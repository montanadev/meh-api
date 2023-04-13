from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from .forms import MemberProfileForm
from .models import UserProfile, PaymentHistory, MehmbershipHistory
from .views import mehmbership_due


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    form = MemberProfileForm


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0


class MehmbershipHistoryInline(admin.TabularInline):
    model = MehmbershipHistory
    extra = 0


class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline, PaymentHistoryInline, MehmbershipHistoryInline]

    def mehmbership_due(self, obj):
        due = mehmbership_due(obj)
        str_due = "${:,.2f}".format(abs(due))
        return str_due + '(credit)' if due < 0 else str_due

    mehmbership_due.short_description = "Mehmbership Due as of Today"

    list_display = DefaultUserAdmin.list_display + ('mehmbership_due',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
