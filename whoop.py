#!/usr/bin/env python3
import os
import json
import requests
from pprint import pprint
from confluent_kafka import Producer
from datetime import datetime, timedelta

from credentials import WHOOP_API_TOKEN

KAFKA_IP = os.getenv("KAFKA_IP", "localhost")

def http_get(url, **kargs):
  try:
    res = requests.get(url, **kargs)
    return res.json()
  except requests.exceptions.RequestException as e:
    print("ERROR")
    print(e)
    return None

if __name__ == "__main__":
  headers = { "Authorization": "Bearer " + WHOOP_API_TOKEN }
  now = datetime.now()
  params = { "start": datetime.isoformat(now + timedelta(days=-1)) + "Z", "end": datetime.isoformat(now) + "Z" }

  workouts = http_get("https://api.prod.whoop.com/developer/v1/activity/workout", headers=headers, params=params)
  sleeps = http_get("https://api.prod.whoop.com/developer/v1/activity/sleep", headers=headers, params=params)
  # sleeps = {"records":[{"created_at":"2022-11-28T19:19:47.274Z","end":"2022-11-28T18:59:42.486Z","id":556393426,"score":{"altitude_change_meter":0.0,"altitude_gain_meter":0.0,"average_heart_rate":120,"distance_meter":0.0,"kilojoule":1611.9324,"max_heart_rate":155,"percent_recorded":100.0,"strain":8.8103,"zone_duration":{"zone_five_milli":0,"zone_four_milli":40374,"zone_one_milli":569131,"zone_three_milli":674836,"zone_two_milli":2004313,"zone_zero_milli":7690}},"score_state":"SCORED","sport_id":-1,"start":"2022-11-28T18:04:46.180Z","timezone_offset":"+01:00","updated_at":"2022-11-28T19:19:53.110Z","user_id":4365395}]}
  # workouts = {"records":[{"created_at":"2022-11-28T19:19:47.274Z","end":"2022-11-28T18:59:42.486Z","id":556393426,"score":{"altitude_change_meter":0,"altitude_gain_meter":0,"average_heart_rate":120,"distance_meter":0,"kilojoule":1611.9324,"max_heart_rate":155,"percent_recorded":100,"strain":8.8103,"zone_duration":{"zone_five_milli":0,"zone_four_milli":40374,"zone_one_milli":569131,"zone_three_milli":674836,"zone_two_milli":2004313,"zone_zero_milli":7690}},"score_state":"SCORED","sport_id":-1,"start":"2022-11-28T18:04:46.180Z","timezone_offset":"+01:00","updated_at":"2022-11-28T19:19:53.110Z","user_id":4365395}]}

  p = Producer({ "bootstrap.servers": KAFKA_IP + ":9092" })
  for r in sleeps["records"]:
    p.produce("sleeps", json.dumps(r).encode("utf-8"))

  for r in workouts["records"]:
    p.produce("workouts", json.dumps(r).encode("utf-8"))

  p.flush()