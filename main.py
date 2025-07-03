import os
from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
)
import datetime

def processFitFiles(credentials, activities):
    try:
        ACTIVITIES_COUNT = os.getenv("ACTIVITIES_COUNT")

        email = credentials[1]
        password = credentials[2]
        path = credentials[3]
        client = Garmin(email, password)
        client.login()
        activities = client.get_activities(0, ACTIVITIES_COUNT)    # Get last ACTIVITIES_COUNT activities
        write = False
        
        if os.path.exists('activityIdList.txt'):
            with open('activityIdList.txt') as f:
                downloadedIds = [line.strip() for line in f if line.strip()]
        else:
            downloadedIds = []
        
        for activity in activities:
            activityId = str(activity["activityId"])

            if activityId in downloadedIds : continue
            
            write = True

            filename = f"{activityId}.fit"

            # Get .FIT file
            data = client.download_activity(activityId, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
                       
            # Do not owerwrite
            if os.path.exists(f"{path/filename}") : raise Exception("Activity exist!")

            # Write
            with open(f"{path}/{filename}", "wb") as f:
                f.write(data)
            downloadedIds.append(str(activityId))
        
        # At least one new item
        if write:
            with open('activityIdList.txt', 'w') as f:
                f.write("".join(f"{id}\n" for id in downloadedIds))

    except (GarminConnectConnectionError, GarminConnectAuthenticationError) as e:
        print(f"Chyba připojení: {e}")

# Přihlašovací údaje
EMAILS = os.getenv("GARMIN_EMAILS")             
PASSWORDS = os.getenv("GARMIN_PASSWORDS")
NEXTCLOUD_USER_PATHS = os.getenv("NEXTCLOUD_USER_PATHS")    #docker volume paths

today = datetime.date.today()

for credentials in (EMAILS.split(';'), PASSWORDS.split(';'), NEXTCLOUD_USER_PATHS.split(';')):
    processFitFiles(credentials)