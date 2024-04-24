import json
from .models import Device

class MysqlProcessor:
    def __init__(self):
        pass

    def add_device(self, device_info):
        if Device.objects.filter(station_id=device_info['station_id']).exists():
            return False
        else:
            device_mysql = Device(
                station_id=device_info['station_id'],
                address=device_info['address'],
                latitude=device_info['latitude'],
                longitude=device_info['longitude'],
                district=device_info['district'],
                hourlySpeed=device_info['hourlySpeed']
            )
            device_mysql.save()
            return True

    def update_device_info(self, device_info):
        if Device.objects.filter(index=device_info['index']).exists():
            device_mysql = Device.objects.get(index=device_info['index'])
            device_mysql.latitude = device_info['latitude']
            device_mysql.longitude = device_info['longitude']
            device_mysql.image_url = device_info['image_url']
            device_mysql.address = device_info['address']
            device_mysql.district = device_info['district']
            device_mysql.time = device_info['time']
            device_mysql.save()
        else:
            device_mysql = Device(index=device_info['index'], latitude=device_info['latitude'], longitude=device_info['longitude'], image_url=device_info['image_url'], address=device_info['address'], time=device_info['time'], district=device_info['district'])
            device_mysql.save()

    def get_device_info(self, request_index):
        if Device.objects.filter(index=request_index).exists():
            device = Device.objects.get(index=request_index)
            device_info = {
                'id': device.station_id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'freeway': device.freeway,
                'direction': device.direction,
                'district': device.district,
                # Parse hourlySpeed from string to list
                'hourlySpeed': json.loads(device.hourlySpeed),
            }
            return device_info
        else:
            return None
        
    def delete_device(self, id):
        print(id)
        if Device.objects.filter(station_id=id).exists():
            device_mysql = Device.objects.get(station_id=id)
            device_mysql.delete()
            return True
        else:
            return False
    
    def updateImage(self, request_index, image_url):
        if Device.objects.filter(index=request_index).exists():
            device_mysql = Device.objects.get(index=request_index)
            device_mysql.image_url = image_url
            device_mysql.save()
            return True
        else:
            return False
    
    def disable_or_enable_device(self, request_index):
        if Device.objects.filter(station_id=request_index).exists():
            device_mysql = Device.objects.get(station_id=request_index)
            device_mysql.enabled = not device_mysql.enabled
            device_mysql.save()
            return True
        else:
            return False
    
    def get_all_devices_of_district(self, district):
        devices = Device.objects.filter(district=district)
        device_info = []
        for device in devices:
            device_info.append({
                'latitude': device.latitude,
                'longitude': device.longitude,
                'index': device.index,
                'image_url': device.image_url,
                'address': device.address,
                'district': device.district,
                'time': str(device.time),
                'enabled': device.enabled
            })
        return device_info
    
    def get_all_devices(self):
        devices = Device.objects.all()
        device_info = []
        for device in devices:
            device_info.append({
                'id': device.station_id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'address': device.address,
                'district': device.district,
                'enabled': device.enabled,
                'hourlySpeed': json.loads(device.hourlySpeed),
            })
        return device_info

    # Search by station_id or address or district
    def get_searched_devices(self, search):
        devices = Device.objects.filter(station_id=search) | Device.objects.filter(address__icontains=search) | Device.objects.filter(district=search)
        device_info = []
        for device in devices:
            device_info.append({
                'id': device.station_id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'address': device.address,
                'district': device.district,
                'enabled': device.enabled,
                'hourlySpeed': json.loads(device.hourlySpeed),
            })
        return device_info

    