from flask import Blueprint,request
from Mainfold.controllers.ChatController import intiate_chat
chat_route=Blueprint("chat_route",__name__)
@chat_route.route("/sendchat", methods=["POST"])
def chat():
    data=request.json
    return intiate_chat(data)