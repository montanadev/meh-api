from django import forms
from mehmberprofile.models import UserProfile, PaymentHistory


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['date', 'amount']


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.payment_history = PaymentHistory.objects.filter(member_profile=self.instance)
        else:
            self.payment_history = []