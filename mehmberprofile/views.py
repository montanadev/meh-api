from datetime import date, timedelta
from django.db.models import Sum
from mehmberprofile.models import PaymentHistory

def membership_due(user):
    today = date.today()
    due_date = today + timedelta(days=30)
    payments = PaymentHistory.objects.filter(user=user, date__range=(today, due_date))
    total_paid = payments.aggregate(Sum('amount')).get('amount__sum') or 0
    return 30 - total_paid