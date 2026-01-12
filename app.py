import os
import flask
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from Mainfold.Routes.upload_route import upload_route
from Mainfold.Routes.chat_route import chat_route
load_dotenv()
Port=os.getenv("PORT")
#this creates our flask sever
app=Flask(__name__)
CORS(app)
app.register_blueprint(upload_route,url_prefix="api/upload")
# app.register_blueprint(chat_route,url_prefix="api/chat")

@app.route("/", methods=["GET"])
def home():
    return "hello boy"
if __name__=="__main__":
    app.run(host="0.0.0.0", port=Port, debug=True)
