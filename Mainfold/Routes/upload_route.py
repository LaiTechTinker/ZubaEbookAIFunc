from flask import Blueprint,request, jsonify
from Mainfold.controllers.UploadController import process_upload,upload_to_pine
upload_route=Blueprint("upload_route",__name__)
@upload_route.route("/process", methods=["POST"])
def process_file():
    file=request.files["file"]
    user_id = request.form.get("user_id")
    book_id = request.form.get("book_id")
    book_title = request.form.get("book_title")
    return process_upload(file,user_id=user_id,book_id=book_id,book_title=book_title)


@upload_route.route("/uploadtopine",methods=["POST"])
def upload_pine():
    data=request.json()
    return upload_to_pine(data=data)

