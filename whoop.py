#!/usr/bin/env python3
import requests
from datetime import datetime

from credentials import WHOOP_API_TOKEN

def get(url, **kargs):
  try:
    res = requests.get(url, **kargs)
    return res.json()
  except requests.exceptions.RequestException as e:
    print("ERROR")
    print(e)
    return None

if __name__ == "__main__":
  headers = { "Authorization": "Bearer " + WHOOP_API_TOKEN }
  params = {
    "start": datetime.isoformat(datetime(2022, 11, 24)) + "Z",
    "end": datetime.isoformat(datetime.now()) + "Z"
  }

  workouts = get("https://api.prod.whoop.com/developer/v1/activity/workout", headers=headers, params=params)
  print(workouts)

  print("="*20)

  sleeps = get("https://api.prod.whoop.com/developer/v1/activity/sleep", headers=headers, params=params)
  print(sleeps)
