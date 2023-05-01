from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mehmberprofile.models import PaymentHistory, MehmbershipHistory
from mehmberprofile.views import mehmbership_due
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mehmberportal:dashboard')
    else:
        form = LoginForm()
    return render(request, 'conpan/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'conpan/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('mehmberportal:login')

@login_required
def payment_history(request):
    payments = PaymentHistory.objects.filter(user=request.user)
    membership_history = MehmbershipHistory.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'conpan/payment_history.html', {'payments': payments, 'amount_due_str': amount_due_string(request), 'membership_history': membership_history})


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

@login_required
def unlock(request):
    amount_due = mehmbership_due(request.user)
    active_member = is_active_member
    membership_in_good_standing = amount_due >= (-1*30*3) and active_member
    access_granted = membership_in_good_standing
    if(access_granted):
        pass
        # TODO make MQTT pub to door/access topic.

    return render(request, 'conpan/unlock.html', {'amount_due_str': amount_due_string(request), })