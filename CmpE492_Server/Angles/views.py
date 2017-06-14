from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


class StoreClass:
    last_data_as_json = '{bos bos}'
    number = 0

def getData(request):
    return HttpResponse(StoreClass.last_data_as_json)

@csrf_exempt
def postData(request):
    StoreClass.number += 1
    if request.method == "POST":
        yaw = request.POST.get('Yaw', '????')
        pitch = request.POST.get('Pitch', '????')
        StoreClass.last_data_as_json = yaw + ',' + pitch
        if StoreClass.number == 100:
            print("100 OLDU !!!!!")
        return HttpResponse("Hello, world. You're at the polls index.")

#Kariyer.net