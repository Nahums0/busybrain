import json
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.mqtt import mqtt
from pydantic import BaseModel

APP_NAME = "Users Controller"
users_bp = Blueprint("users", __name__, url_prefix="/api")
messages = []

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "POST Not Implemented"

    return "GET Not Implemented"

# SAMPLE CODE - REMOVE!#
class User(BaseModel):
    username: str
    password: str
    tags: list = []


@users_bp.route("/invalid", methods=["GET", "POST"])
def create_invalid_user():
    u = User(username=1, password="test", tags=1)
    return u.model_dump()
 

@users_bp.route("/valid", methods=["GET", "POST"])
def create_valid_user():
    u = User(username="test", password="test", tags=["test"])
    return u.model_dump()

def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Received {payload} from {topic}")


@users_bp.route("/post", methods=["GET", "POST"])
def post_to_topics():
    import random
    i = random.randint(0, 100)
    mqtt.publish('my_topic', str(i))
    return f"PUBLISHED {i}"


@users_bp.route("/get", methods=["GET", "POST"])
def get_all_topic_messages():
    # get all messages for a topic
    return json.dumps(messages)
# End SAMPLE CODE - REMOVE!#
