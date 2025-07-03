import os
from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
)
import datetime
import requests

# Přihlašovací údaje
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")
NEXTCLOUD_URL = os.getenv("NEXTCLOUD_URL")  # např. https://cloud.example.com/remote.php/webdav/Garmin/
NEXTCLOUD_USER = os.getenv("NEXTCLOUD_USER")
NEXTCLOUD_PASS = os.getenv("NEXTCLOUD_PASS")

today = datetime.date.today()

try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()
    activities = client.get_activities(0, 5)  # Získá posledních 5 aktivit

    for activity in activities:
        activity_id = activity["activityId"]
        filename = f"{activity_id}.fit"

        # Stáhne aktivitu
        data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
        with open(filename, "wb") as f:
            f.write(data)

        # Nahraje do Nextcloudu
        with open(filename, "rb") as f:
            r = requests.put(
                f"{NEXTCLOUD_URL}/{filename}",
                auth=(NEXTCLOUD_USER, NEXTCLOUD_PASS),
                data=f
            )
            print(f"Upload {filename}: {r.status_code}")

except (GarminConnectConnectionError, GarminConnectAuthenticationError) as e:
    print(f"Chyba připojení: {e}")