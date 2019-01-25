from flask import Blueprint
from flask import request
from flask_sse import sse

channel = Blueprint('channel', __name__)


@channel.route("/send/<channel_name>/<massage_type>", methods=['POST'])
def send(channel_name, massage_type):
    print("Hello channel send!")
    print("request data:")
    print(request.data)
    print(type(request.data))
    print("massage_type:")
    print(massage_type)
    print(type(massage_type))
    print("channel_name:")
    print(channel_name)
    print(type(channel_name))
    # sse.publish({"message": str(request.data)[2:-1]}, type=massage_type, channel=channel_name)
    sse.publish({"message": request.data.decode("utf-8")}, type=massage_type, channel=channel_name)
    return "send" + massage_type + "to" + channel_name
