import pymysql
import paho.mqtt.client as paho
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
from flask_jwt_extended import jwt_required
import time, json
from flask_jwt_extended import get_jwt_identity
from mqtt_connect import client

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="qa_hust", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.connect("broker.hivemq.com", 1883)
client.loop_start()
# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("/iot_project_nhom04", qos=1)

#API dieu khien thiet bi
@app.route('/device/<int:id>/control', methods=['PUT'], endpoint='controlDevice')
@jwt_required()
def controlDevice(id):
    content = None
    conn = None
    cursor = None
    current_user = get_jwt_identity()
    try:
        _json = request.json
        _is_active = _json['is_active']
        _param = _json['param']
        _json['id'] = id
        _json['userID'] = current_user
        sql = "UPDATE device_room SET is_active=%s, param=%s WHERE id=%s"
        data = (_is_active, _param, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        client.publish("/iot_project_nhom04", payload=json.dumps(_json))

        res = jsonify(_json)
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

