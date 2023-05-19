from bimmer_connected.vehicle.vehicle import MyBMWVehicle

class Geoapify:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_static_map_url(self, vehicle: MyBMWVehicle) -> str:
        if self.api_key != "":
            url = "https://maps.geoapify.com/v1/staticmap?style=osm-bright&width=600&height=256&"
            url += f"&marker=lonlat:{vehicle.vehicle_location.location.longitude},{vehicle.vehicle_location.location.latitude};color:%23ff0000;size:small&zoom=16&apiKey={self.api_key}"
            return url
        else:
            return ""