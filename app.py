# -*- coding: UTF-8 -*-
import datetime
import json
import os

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from paho.mqtt import client as MQTT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    FrontDoor2706, BackDoor2706, FirstMeetingRoomFun, FirstMeetingRoom, SecondMeetingRoom, 
    PowerBox220V, ServerRoom, AirConditioner, ACSwitchLog, DL303
)


# Timezone setting
tz_delta = datetime.timedelta(hours=0)
tz = datetime.timezone(tz_delta)

# Load env variable
dotenv_path = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# DataBase
engine = create_engine(os.environ.get("SQL_SERVER"), echo=True)
Session = sessionmaker(bind=engine)

# MQTT
client = MQTT.Client()

# Scheduler
task = BackgroundScheduler(timezone="Asia/Taipei")

# Data Temporary Storage
front_door = {}
back_door = {}
first_meeting_room_fun = {}
first_meeting_room = {}
second_meeting_room = {}
power_box = {}
dl303 = {}
server_room = {}
air_condiction = {}


def time():
    return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")


# Data Storage
def add_front_door(data):
    print("Front Door: ", data)
    try:
        with Session.begin() as session:
            session.add(FrontDoor2706(
                timestamp = time(),
                temp = data["Temperature"],
                humi = data["Humidity"],
                co2 = data["CO2"],
                tvoc = data["TVOC"],
                fan3 = data["fan_0"],
                fan4 = data["fan_1"]
            ))
        global front_door
        front_door.clear()
    except Exception as e:
        print('ERROR:', e)


def add_back_door(data):
    print("Back Door: ", data)
    try:
        with Session.begin() as session:
            session.add(BackDoor2706(
                timestamp = time(),
                temp = data["Temperature"],
                humi = data["Humidity"],
                co2 = data["CO2"],
                tvoc = data["TVOC"],
                fan1 = data["fan_0"],
                fan2 = data["fan_1"]
            ))
        global back_door
        back_door.clear()
    except Exception as e:
        print('ERROR:', e)


def add_first_meeting_room_fun(data):
    print("First Meeting Room Fun: ", data)
    try:
        with Session.begin() as session:
            session.add(FirstMeetingRoomFun(
                timestamp = time(),
                fan0 = data["fan_0"]
            ))
        global first_meeting_room_fun
        first_meeting_room_fun.clear()
    except Exception as e:
        print("ERROR:", e)


def add_first_meeting_room(data):
    print("First Meeting Room: ", data)
    try:
        with Session.begin() as session:
            session.add(FirstMeetingRoom(
                timestamp = time(),
                temp = data["Temperature"],
                humi = data["Humidity"],
                co2 = data["CO2"] / 3.5,
                tvoc = data["TVOC"]
            ))
        global first_meeting_room
        first_meeting_room.clear()
    except Exception as e:
        print('ERROR:', e)


def add_second_meeting_room(data):
    print("Second Meeting Room: ", data)
    try:
        with Session.begin() as session:
            session.add(SecondMeetingRoom(
                timestamp = time(),
                temp = data["Temperature"],
                humi = data["Humidity"],
                co2 = data["CO2"] / 3.5,
                tvoc = data["TVOC"]
            ))
        global second_meeting_room
        second_meeting_room.clear()
    except Exception as e:
        print('ERROR:', e)


def add_power_box(data):
    print("Power Box: ", data)
    try:
        with Session.begin() as session:
            session.add(PowerBox220V(
                timestamp = time(),
                in_a = data['IN_A'],
                in_b = data['IN_B'],
                in_c = data['IN_C'],
                in_avg = data['IN_Avg'],
                kw_a = data['kW_A'],
                kw_b = data['kW_B'],
                kw_c = data['kW_C'],
                kw_tot = data['kW_tot']
            ))
        global power_box
        power_box.clear()
    except Exception as e:
        print('ERROR:', e)


def add_dl303(data):
    print("DL303: ", data)
    try:
        with Session.begin() as session:
            session.add(DL303(
                timestamp = time(),
                temp = data["TemperatureC"],
                humi = data["Humidity"],
                dew_point = data["DewPointC"],
                co2 = data["CO2"]
            ))
        global dl303
        dl303.clear()
    except Exception as e:
        print('ERROR:', e)


def add_server_room(data):
    print("Server Room: ", data)
    try:
        with Session.begin() as session:
            session.add(ServerRoom(
                timestamp = time(),
                temp = data["Temperature"],
                humi = data["Humidity"]
            ))
        global server_room
        server_room.clear()
    except Exception as e:
        print('ERROR:', e)


def add_air_condiction(data):
    print("Air Conditioner: ", data)
    try:
        with Session.begin() as session:
            session.add(AirConditioner(
                timestamp = time(),
                status = data["Status"]
            ))
        global air_condiction
        air_condiction.clear()
    except Exception as e:
        print('ERROR:', e)


# MQTT connect
@client.connect_callback()
def on_connect(client, userdata, flags, rresult):
    print(f"=============== {'Connect':^15} ===============")
    client.subscribe("DL303/Info")
    client.subscribe("2706/#")


# MQTT message
@client.message_callback()
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
    except: 
        data = {}
    # print(f"{msg.topic} - {data}")
    if msg.topic == "2706/IAQ/2":
        front_door["Temperature"] = data.get("Temperature")
        front_door["Humidity"] = data.get("Humidity")
        front_door["CO2"] = data.get("CO2")
        front_door["TVOC"] = data.get("TVOC")
        front_door["fan_0"] = data.get("fan_0")
        front_door["fan_1"] = data.get("fan_1")
    elif msg.topic == "2706/IAQ/1":
        back_door["Temperature"] = data.get("Temperature")
        back_door["Humidity"] = data.get("Humidity")
        back_door["CO2"] = data.get("CO2")
        back_door["TVOC"] = data.get("TVOC")
        back_door["fan_0"] = data.get("fan_0")
        back_door["fan_1"] = data.get("fan_1")
    elif msg.topic == "2706/IAQ/3":
        first_meeting_room_fun["fan_0"] = data.get("fan_0")
    elif msg.topic == "2706/MeetingRoom/1":
        first_meeting_room["Temperature"] = data.get("Temperature")
        first_meeting_room["Humidity"] = data.get("Humidity")
        first_meeting_room["CO2"] = data.get("CO2")
        first_meeting_room["TVOC"] = data.get("TVOC")
    elif msg.topic == "2706/MeetingRoom/2":
        second_meeting_room["Temperature"] = data.get("Temperature")
        second_meeting_room["Humidity"] = data.get("Humidity")
        second_meeting_room["CO2"] = data.get("CO2")
        second_meeting_room["TVOC"] = data.get("TVOC")
    elif msg.topic == "2706/PowerBox":
        power_box["IN_A"] = data.get("IN_A")
        power_box["IN_B"] = data.get("IN_B")
        power_box["IN_C"] = data.get("IN_C")
        power_box["IN_Avg"] = data.get("IN_Avg")
        power_box["kW_A"] = (data.get("IN_A") / 1.732) * 220 / 1000
        power_box["kW_B"] = (data.get("IN_B") / 1.732) * 220 / 1000
        power_box["kW_C"] = (data.get("IN_C") / 1.732) * 220 / 1000
        power_box["kW_tot"] =  power_box["kW_A"] + power_box["kW_B"] + power_box["kW_C"]
    elif msg.topic == "DL303/Info":
        dl303["TemperatureC"] = data.get("TemperatureC")
        dl303["Humidity"] = data.get("Humidity")
        dl303["DewPointC"] = data.get("DewPointC")
        dl303["CO2"] = data.get("CO2")
    elif msg.topic == "2706/Air_Condiction/A":
        server_room["Temperature"] = data.get("Temperature")
        server_room["Humidity"] = data.get("Humidity")
    elif msg.topic == "2706/Air_Condiction/A/switch":
        air_condiction["Status"] = True if data.get("Status") == "On" else False
    elif msg.topic == "2706/Air_Condiction/A/control":
        try:
            with Session.begin() as session:
                session.add(ACSwitchLog(
                    timestamp = time(),
                    status = True if data.get("Status") == "ON" else False
                ))
        except Exception as e:
            print('ERROR:', e)


if __name__ == "__main__":
    client.connect(os.environ.get("MQTT_IP"),
                   int(os.environ.get("MQTT_PORT")))
    task.add_job(add_front_door, 'interval', seconds=10, args=[front_door])
    task.add_job(add_back_door, 'interval', seconds=10, args=[back_door])
    task.add_job(add_first_meeting_room_fun, 'interval', seconds=10, args=[first_meeting_room_fun])
    task.add_job(add_first_meeting_room, 'interval', seconds=10, args=[first_meeting_room])
    task.add_job(add_second_meeting_room, 'interval', seconds=10, args=[second_meeting_room])
    task.add_job(add_power_box, 'interval', seconds=10, args=[power_box])
    task.add_job(add_dl303, 'interval', seconds=10, args=[dl303])
    task.add_job(add_server_room, 'interval', seconds=10, args=[server_room])
    task.add_job(add_air_condiction, 'interval', seconds=10, args=[air_condiction])
    task.start()
    client.loop_forever()
