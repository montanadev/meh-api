import paho.mqtt.client as mqtt
from django import forms
from django.forms import Widget
from django.utils.safestring import mark_safe

from mehmberprofile.models import UserProfile, PaymentHistory, MehmbershipHistory
from settings import SECRETS


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
            'led_number': '0 is the first LED on the wall, 1 is the second...(0 will auto select lowest available) '
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
                if new_bool is not old_bool \
                        and cleaned_data[out_all] is getattr(self.instance, out_all):
                    cleaned_data[out_all] = False

        client = mqtt.Client()
        client.connect(SECRETS['mqtt']['host'], SECRETS['mqtt']['port'], 60)
        # TODO get meh/meh-api/lightsstatus first to ensure we don't overwrite an LED that had dimmed during profile edit
        # above "TODO" would be a lot of work and little reward.
        client.publish('meh/meh-api/lights', payload="{:d},{:d},{:d},{:d}".format(int(cleaned_data['led_number'])
                                                                                  , int(cleaned_data['red_value']),
                                                                                  int(cleaned_data['green_value']),
                                                                                  int(cleaned_data['blue_value'])),
                       qos=0, retain=False)

        led_number = self.cleaned_data.get('led_number')
        if led_number == 0:
            available_led_light = self.find_lowest_available_LED_light()
            self.cleaned_data['led_number'] = available_led_light

        return cleaned_data

    def find_lowest_available_LED_light(self):
        existing_led_numbers = UserProfile.objects.all().values_list('led_number', flat=True)
        for i in range(0, 2001):  # assuming 2000 is the maximum number of LEDs
            if i not in existing_led_numbers:
                return i
        return 0  # all LED numbers are taken

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
