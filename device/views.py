from django.shortcuts import render, HttpResponse
from .models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mongodb import MongoDBProcessor
from .mysql import MysqlProcessor
import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse




@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        if user.password == password:
            user_data = {
                "token": "1234567890",
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "is_agent": user.is_agent,
            }
            return Response(json.dumps(user_data), status=200)
        else:
            return JsonResponse({'message': 'Invalid password'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)

@api_view(['POST'])
def addDevice(request):
    try:
        station_id = request.data.get('id')
        print(station_id)
        if not station_id:
            return Response({"error": "Station ID is required"}, status=400)

        # Add device info
        mongodb = MongoDBProcessor()
        mysql = MysqlProcessor()
        deviceInfo = mongodb.get_iot_info(station_id)
        if not deviceInfo:
            return Response({"error": "Device not found"}, status=404)
        # return Response(deviceInfo, status=200)
        if mysql.add_device(deviceInfo):
            return Response('Device added', status=status.HTTP_200_OK)
        else:
            return Response('Device already exists', status=status.HTTP_409_CONFLICT)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


def UpdateDeviceInfo(request):
    request_index = "1"
    # update device info
    mongodb = MongoDBProcessor()
    mysql = MysqlProcessor()
    deviceInfo = mongodb.get_iot_info(request_index)
    mysql.update_device_info(deviceInfo)
    
    return HttpResponse('Device info updated')

def getDeviceInfo(request):
    request_index = "1"
    # get device info
    db = MysqlProcessor()
    device_info = db.get_device_info(request_index)
    if device_info:
        json_data = json.dumps(device_info)
        return HttpResponse(json_data, content_type='application/json')
    else:
        return HttpResponse('Device not found', content_type='application/json')

@api_view(['GET'])
def GetALLDevices(request):
    # get all devices info
    db = MysqlProcessor()
    devices = db.get_all_devices()
    return Response(devices, status=status.HTTP_200_OK)

def GetSearchedDevices(request):
    try:
        search = request.GET.get('search')
        print(search)
        # get searched devices info
        mongodb = MongoDBProcessor()
        devices = mongodb.search_iot_info(search)

        return JsonResponse(devices, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['DELETE'])
def deleteDevice(request):
    id = int(request.query_params.get('id'))
    # delete device info
    db = MysqlProcessor()
    if db.delete_device(id):
        return Response('Device deleted', status=status.HTTP_200_OK)
    else:
        return Response('Device not found', status=status.HTTP_404_NOT_FOUND)

def updateImage(request):
    request_index = "1"
    # update image url
    mongodb = MongoDBProcessor()
    image_url = mongodb.get_image_url(request_index)
    db = MysqlProcessor()
    if db.updateImage(request_index, image_url):
        return HttpResponse('Image updated')
    else:
        return HttpResponse('Device not found')

@api_view(['POST', 'GET'])
def disableDevice(request):
    if request.method == 'POST':
        request_index = request.data.get('index')
        # disable device
        db = MysqlProcessor()
        if db.disable_or_enable_device(request_index):
            return Response('Status switched', status=status.HTTP_200_OK)
        else:
            return Response('Device not found', status=status.HTTP_404_NOT_FOUND)

def get_device_of_district(request):
    district = "1"
    # get device info of district
    db = MysqlProcessor()
    devices = db.get_all_devices_of_district(district)
    print(devices)
    return HttpResponse(devices)