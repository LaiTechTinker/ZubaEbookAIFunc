from flask import Blueprint,request, jsonify
upload_route=Blueprint("upload_route",__name__)
@upload_route.route("/", methods=["POST"])
def upload_file():
    print("hello testing upload")