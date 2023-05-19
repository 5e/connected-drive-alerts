## connected-drive-alerts
Do you forget to close your windows in your car like me? This tool sends alerts to a Discord server to remind you to turn back and close them!

Uses the [bimmer_connected](https://github.com/bimmerconnected/bimmer_connected) library to query ConnectedDrive

<p float="left">
<img src="https://i.imgur.com/YfYem0p.jpg" width="500"/>
<img src="https://i.imgur.com/3dqwj4u.jpeg" width="500"/>
</p>

Current features:
- Alert if windows/doors have been left open
- Alerts when car has been locked/unlocked

Future features:
- Log locations of where you car has stopped
- Alert if your car has been started
- Support for multiple cars

## Config

|Field| Description |
|--|--|
| email | required, BMW Connected Drive email |
| password | required, BMW Connected Drive password |
| discord_token | required, discord bot token |
| channel_id | required, channel to post alerts in |
| geoapify_api_key | optional, use "" if don't want location thumbnails |
