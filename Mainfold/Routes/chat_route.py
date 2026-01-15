from flask import Blueprint,request
from Mainfold.controllers.ChatController import intiate_chat
from Mainfold.controllers.chatStream import chat_stream
chat_route=Blueprint("chat_route",__name__)
@chat_route.route("/sendchat", methods=["POST"])
def chat():
    data=request.json
    return intiate_chat(data)
@chat_route.route("/streamchat", methods=["POST"])
def stream_chat():
    return chat_stream()