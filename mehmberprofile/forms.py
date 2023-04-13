
from django import forms
from django.forms import Widget
from django.utils.safestring import mark_safe

from mehmberprofile.models import UserProfile, PaymentHistory, MehmbershipHistory

class displayText(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'<div style="font-weight:bold; font-size: 1.5em;">{value}</div>')

class MemberProfileForm(forms.ModelForm):
    opt_out_heading = forms.CharField(
        label="",
        initial="Opt-outs",
        required=False,
        widget=displayText()
    )
    led_heading = forms.CharField(
        label="",
        initial="LEDs",
        required=False,
        widget=displayText()
    )

    class Meta:
        model = UserProfile
        fields = (
            'opt_out_heading',
            'opt_out_all',
            'opt_out_led_wall',
            'opt_out_door_display',
            'opt_out_social_bot',
            'opt_out_accolade_display',
            'led_heading',
            'red_value',
            'green_value',
            'blue_value',
            'led_number',
        )

        help_texts = {
            'opt_out_all': 'opting out here effectively checks all current and future opt-outs',
            'red_value': '0-255 affect brightness, but you can have much greater numbers which slowly dwindle.',
            'green_value': '0-255 affect brightness, but you can have much greater numbers which slowly dwindle.',
            'blue_value': '0-255 affect brightness, but you can have much greater numbers which slowly dwindle.',
            'led_number':  '0 is the first LED on the wall, 1 is the second... '
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.payment_history = PaymentHistory.objects.filter(user=self.instance.user)
            self.membership_history = MehmbershipHistory.objects.filter(user=self.instance.user)
        else:
            self.payment_history = []
            self.membership_history = []

    def clean(self):
        cleaned_data = super().clean()
        out_all = "opt_out_all"
        for cd in cleaned_data:
            if hasattr(self.instance, cd) \
                    and 'opt_out' in cd \
                    and cd != out_all:
                new_bool = cleaned_data[cd]
                old_bool = getattr(self.instance, cd)
                # if an opt_out has changed, but the opt_out_all didn't change:
                if new_bool is not old_bool\
                        and  cleaned_data[out_all] is getattr(self.instance, out_all):
                    cleaned_data[out_all]  = False
        return cleaned_data

