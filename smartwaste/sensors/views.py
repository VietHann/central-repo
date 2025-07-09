from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData
from bins.models import Bin

@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            bin_id = data['bin_id']
            level = data['level']

            bin = Bin.objects.get(pk=bin_id)

            sensor_data = SensorData(bin=bin, level=level)
            sensor_data.save()

            bin.current_level = level
            bin.save()

            return HttpResponse(status=200)
        except Exception as e:
            print(f"Error processing sensor data: {e}")
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)
