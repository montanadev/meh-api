from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from mehmberprofile.models import PaymentHistory, MehmbershipHistory


def mehmbership_due(user):
    today = date.today()
    due_date = today + relativedelta(months=1)
    rolloff_date = today - relativedelta(years=5)  # don't charge memberships that are 5 years old
    payments = PaymentHistory.objects.filter(user=user, date__range=(rolloff_date, due_date))
    mehmberships = MehmbershipHistory.objects.filter(user=user, start_date__range=(rolloff_date, due_date))
    total_paid = payments.aggregate(Sum('amount')).get('amount__sum') or 0
    total_charged = 0
    num_mehmberships = len(mehmberships)
    for index, mehmbership in enumerate(mehmberships):
        difference = relativedelta(mehmbership.end_date or today, mehmbership.start_date)
        months_of_mehmbership = difference.years * 12 + difference.months
        total_charged += months_of_mehmbership * mehmbership.monthly_price
        if index == num_mehmberships - 1 and num_mehmberships > 1:
            total_charged += mehmbership.monthly_price
    return total_charged - total_paid


def amount_due_string(request):
    amount_due = mehmbership_due(request.user)
    if amount_due < 0:
        amount_due_str = f"${abs(amount_due):,.2f} (credit)"
    else:
        amount_due_str = f"${amount_due:,.2f}"
    return amount_due_str


def is_active_member(user):
    memberships = MehmbershipHistory.objects.filter(user=user, end_date__isnull=True)
    return len(memberships) > 0
