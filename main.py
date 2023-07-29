# connected-drive-alerts v1.3
from bimmer_connected.account import MyBMWAccount
from bimmer_connected.vehicle.doors_windows import Window, Lid
from bimmer_connected.api.regions import Regions
from bimmer_connected.vehicle.vehicle import MyBMWVehicle

import json
import utils
from geoapify import Geoapify
import asyncio

file = open('config.json')
config = json.load(file)

account = MyBMWAccount(
    config['email'], config['password'], Regions.REST_OF_WORLD)
geoapify = Geoapify(config['geoapify_api_key'])
webhook = utils.Webhook(config['webhook_url'])

alert_sent = False
last_lock = None
last_timestamp = None


async def update_vehicles():
    global alert_sent
    global last_lock
    global last_timestamp
    try:
        await account.get_vehicles()
        # currently only supports tracking of 1 car
        vehicle: MyBMWVehicle = account.vehicles[0]
        if last_lock != vehicle.doors_and_windows.door_lock_state:
            if last_lock != None:
                title = f"{vehicle.brand.upper()} {vehicle.name}"
                description = f"Car lock from {last_lock} to {vehicle.doors_and_windows.door_lock_state}"
                image = geoapify.get_static_map_url(vehicle)
                status_field = f"[Location]({utils.create_google_maps_link(vehicle.vehicle_location.location.latitude, vehicle.vehicle_location.location.longitude)})"
                footer = vehicle.data['state']['lastUpdatedAt']
                webhook.send_webhook(title, description,
                                     image, status_field, footer)
            last_lock = vehicle.doors_and_windows.door_lock_state

        if last_timestamp != vehicle.data['state']['lastUpdatedAt']:
            # data from API is only updated when car is locked/unlocked, not during motion
            last_timestamp = vehicle.data['state']['lastUpdatedAt']
            if last_timestamp != None:
                alert_sent = False

        if alert_sent == True:
            return

        total_output = ""
        lid: Lid
        for lid in vehicle.doors_and_windows.open_lids:
            total_output += f"{lid.name} door, "
        window: Window
        for window in vehicle.doors_and_windows.open_windows:
            total_output += f"{window.name} window, "

        if total_output != "":
            title = f"{vehicle.brand.upper()} {vehicle.name}"
            description = f"Windows/door open: {total_output[:-2]}"
            image = geoapify.get_static_map_url(vehicle)
            status_field = f"[Location]({utils.create_google_maps_link(vehicle.vehicle_location.location.latitude, vehicle.vehicle_location.location.longitude)})"
            footer = vehicle.data['state']['lastUpdatedAt']
            webhook.send_webhook(title, description,
                                 image, status_field, footer)
            alert_sent = True

    except Exception as e:
        webhook.send_webhook_error(str(e))
        print(e)


async def start_loop():
    while True:
        await update_vehicles()
        await asyncio.sleep(43)

asyncio.run(start_loop())
