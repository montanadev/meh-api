import paho.mqtt.client as mqtt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mehmberprofile.models import PaymentHistory, MehmbershipHistory
from mehmberprofile.views import mehmbership_due, amount_due_string, is_active_member, mehmber_accessed_hackspace
from settings import SECRETS
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
    return render(request, 'conpan/payment_history.html',
                  {'payments': payments, 'amount_due_str': amount_due_string(request),
                   'membership_history': membership_history})


@login_required
def unlock(request):
    amount_due = mehmbership_due(request.user)
    active_member = is_active_member(request.user)
    membership_in_good_standing = amount_due <= (30 * 3) and active_member
    access_granted = membership_in_good_standing
    if (access_granted):
        client = mqtt.Client()
        client.connect(SECRETS['mqtt']['host'], SECRETS['mqtt']['port'], 60)
        # TODO sign this.  Maybe use JWT... probably not because then I'd have to keep track of time securely... NTP FTL
        client.publish('meh/meh-api/door/access', payload="friend",
                       qos=0, retain=False)
        mehmber_accessed_hackspace(request)

    return render(request, 'conpan/unlock.html', {'amount_due_str': amount_due_string(request), })
