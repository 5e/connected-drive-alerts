## connected-drive-alerts
Do you forget to close your windows in your car like me? This tool sends alerts to a Discord server to remind you to turn back and close them!

Uses the [bimmer_connected](https://github.com/bimmerconnected/bimmer_connected) library to query ConnectedDrive

<p float="left">
<img src="https://i.imgur.com/qSwWL5V.png" width="500"/>
<img src="https://i.imgur.com/3dqwj4u.jpeg" width="500"/>
</p>

Current features:
- Alert if windows/doors have been left open
- Alerts when car has been locked/unlocked
- Location where above events happened

Future features:
- ~~Live location of vehicle~~ Not possible, location data not updated in-motion
- ~~Alert if your car has been started~~ Not possible
- Support for multiple cars

## Config

|Field| Description |
|--|--|
| email | required, BMW Connected Drive email |
| password | required, BMW Connected Drive password |
| webhook_url | required, webhook url to post updates |
| geoapify_api_key | optional, use "" if don't want location thumbnails |
