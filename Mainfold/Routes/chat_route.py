from flask import Blueprint,request, jsonify
chat_route=Blueprint("chat_route",__name__)
@chat_route.route("/", methods=["POST"])
def chat():
    print("hello testing chat")