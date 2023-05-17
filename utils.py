from bimmer_connected.vehicle.vehicle import MyBMWVehicle

def create_google_maps_link(vehicle: MyBMWVehicle) -> list:  
    return f"http://www.google.com/maps/search/?api=1&query={vehicle.vehicle_location.location.latitude},{vehicle.vehicle_location.location.longitude}"