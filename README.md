## connected-drive-alerts
Do you forget to close your windows in your car like me? This tool sends alerts to a Discord server to remind you to turn back and close them!

Uses the [bimmer_connected](https://github.com/bimmerconnected/bimmer_connected) library to query ConnectedDrive

Currently working on:
- Alert if windows have been left open (if after 1 minute of locking the car the windows are open, send alert)

Future features:
- Log locations of where you car has stopped
- Alert if your car has been unlocked/started

## Config

|Field| Description |
|--|--|
| email | required, BMW Connected Drive email |
| password | required, BMW Connected Drive password |
| discord_token | required, discord bot token |
| channel_id | required, channel to post alerts in |
| geoapify_api_key | optional, use "" if don't want location thumbnails |
