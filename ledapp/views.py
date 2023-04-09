from django.shortcuts import render
from .models import LED
from .forms import LEDForm
from django.urls import get_resolver


def led_view(request):
    url_patterns = get_resolver().reverse_dict.keys()
    led, created = LED.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = LEDForm(request.POST, instance=led)
        if form.is_valid():
            form.save()
    else:
        form = LEDForm(instance=led)
    return render(request, 'led.html', {'form': form, 'url_patterns': url_patterns,})