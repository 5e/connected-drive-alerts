import asyncio
from bimmer_connected.account import MyBMWAccount
from bimmer_connected.vehicle.doors_windows import Window, Lid
from bimmer_connected.api.regions import Regions
import discord
from discord.ext import tasks
import json
import utils
from geoapify import Geoapify


file = open('config.json')
config = json.load(file)

channel:discord.TextChannel = None
intents = discord.Intents.default()
client = discord.Client(intents=intents)

account = MyBMWAccount(config['email'], config['password'], Regions.REST_OF_WORLD)
geoapify = Geoapify(config['geoapify_api_key'])

alert_sent = False
last_lock = None
last_timestamp = None
counter = 0
from datetime import datetime
@client.event
async def on_ready():
    global channel
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(config['channel_id'])
    if not update_vehicles.is_running():
        update_vehicles.start() 

async def get_vehicles():
    await account.get_vehicles()

@tasks.loop(seconds=40)
async def update_vehicles():
    global alert_sent
    global last_lock
    global last_timestamp
    global counter
    try:
        await get_vehicles()
        counter += 1
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        vehicle = account.vehicles[0] #currently only supports tracking of 1 car
        if last_lock != vehicle.doors_and_windows.door_lock_state:
            if last_lock != None:
                embed=discord.Embed(title=f"{vehicle.brand.upper()} {vehicle.name}", description=f"Car lock from {last_lock} to {vehicle.doors_and_windows.door_lock_state}", color=0xff0000)
                embed.set_image(url=geoapify.get_static_map_url(vehicle))
                embed.add_field(name="Status", value=f"[Location]({utils.create_google_maps_link(vehicle)})", inline=False)
                embed.set_footer(text="connected-drive-alerts", icon_url="https://cdn-icons-png.flaticon.com/512/25/25231.png")
                message = await channel.send(embed=embed)
            last_lock = vehicle.doors_and_windows.door_lock_state

        if last_timestamp != vehicle.data['state']['lastUpdatedAt']:
            #experimental, if data has updated then car is being driven or has been locked/unlocked
            if last_timestamp == None:
                last_timestamp = vehicle.data['state']['lastUpdatedAt']
            else:
                alert_sent = False
                last_timestamp = vehicle.data['state']['lastUpdatedAt']
                return

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
            embed=discord.Embed(title=f"{vehicle.brand.upper()} {vehicle.name}", description=f"Windows/door open: {total_output[:-2]}", color=0xff0000)
            embed.set_image(url=geoapify.get_static_map_url(vehicle))
            embed.add_field(name="Status", value=f"[Location]({utils.create_google_maps_link(vehicle)})", inline=False)
            embed.set_footer(text="connected-drive-alerts", icon_url="https://cdn-icons-png.flaticon.com/512/25/25231.png")
            message = await channel.send(embed=embed)
            alert_sent = True

    except Exception as e:
        import jsonpickle
        import random
        import traceback
        message = await channel.send(str(e) + str(counter))
        message = await channel.send(traceback.format_exc())
        print(traceback.format_exc())
        randomnumber = random.randint(0,100000)
        jsonstr = jsonpickle.encode(account.vehicles[0])

        f = open(f"demofile{randomnumber}.txt", "w")
        f.write(jsonstr)
        f.close()
        
        print(str(e) + str(counter))






# asyncio.run(main())
client.run(config['discord_token'])
