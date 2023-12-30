from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from medical_store_control.models import StoreModel


def home_view(request):
    stores = StoreModel.objects.order_by("?")

    context = {
        "stores": stores
    }
    return render(request, "pages/medical-store/store-home.html", context)


def store_detail_view(request, id):
    store = StoreModel.objects.get(id=id)

    name_list = store.name.split(" ")
    address_list = store.address.split(" ")
    location_link = 'https://maps.google.com/maps?width=100%25&amp;height=600&amp;hl=en&amp;q='
    address_part = ''
    name_part = ''
    for location in name_list:
        name_part += location + "%20"

    for location in address_list:
        address_part += location + "%20"

    # print(location_link)
    full_location = location_link + address_part + "(" + name_part + ")" + "&amp;ie=UTF8&amp;t=&amp;z=14&amp;iwloc=B&amp;output=embed"
    # print(full_location)
    context = {

        "store": store,
        "location_link": full_location
    }
    return render(request, "pages/medical-store/store-detail.html", context)
