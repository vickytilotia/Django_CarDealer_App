# This file is needed for  passing variable to base.html
from .models import Car, Privacy, Ads


def ad_processor(request):
    popup_ad = Ads.objects.all()
    return {
        'ad' : popup_ad[0]
    }