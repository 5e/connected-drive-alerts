import requests


def create_google_maps_link(latitude, longitude) -> list:
    return f"http://www.google.com/maps/search/?api=1&query={latitude},{longitude}"


class Webhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_webhook(self, title, description, image, status_field, timestamp):
        data = {
            "username": "connected-drive-alerts",
            "embeds": [{
                "color": 0xff0000,
                "description": description,
                "title": title,
                "image": {
                    "url": image
                },
                "fields": [{
                    "name": "Status",
                    "value": status_field,
                    "inline": False
                }],
                "footer": {
                    "text": "connected-drive-alerts",
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/25/25231.png"
                },
                "timestamp": timestamp
            }]
        }
        r = requests.post(self.webhook_url, json=data)

    def send_webhook_error(self, debug_error):
        data = {
            "username": "connected-drive-alerts",
            "content": debug_error
        }
        r = requests.post(self.webhook_url, json=data)
