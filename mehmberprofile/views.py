from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from mehmberprofile.models import PaymentHistory, MembershipHistory


def membership_due(user):
    today = date.today()
    due_date = today + relativedelta(months=1)
    rolloff_date = today - relativedelta(years=5)  # don't charge memberships that are 5 years old
    payments = PaymentHistory.objects.filter(user=user, date__range=(rolloff_date, due_date))
    memberships = MembershipHistory.objects.filter(user=user, start_date__range=(rolloff_date, due_date))
    total_paid = payments.aggregate(Sum('amount')).get('amount__sum') or 0
    total_charged = 0
    num_memberships = len(memberships)
    for index, membership in enumerate(memberships):
        difference = relativedelta(membership.end_date or today, membership.start_date)
        months_of_membership = difference.years * 12 + difference.months
        total_charged += months_of_membership * membership.monthly_price
        if index == num_memberships - 1:
            total_charged += membership.monthly_price
    return total_charged - total_paid
