#pip install flask
#pip install flask-restful
#pip install requests

#this will be running on the server side

from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
import socket

app = Flask(__name__)
api = Api(app)


user_info = reqparse.RequestParser()
user_info.add_argument("name", type=str, help="Name of user is required", required=True)
user_info.add_argument("phone", type=str, help="Phone entry is required", required=True)
user_info.add_argument("face", type=str, help="visible face is required", required=True)

class Inboxicated_Server(Resource):
    def get(self):
        return {"data":"You are drunk", "identity": "dawit"}
        #output user info
    
    def post(self):
        return {"name": "dawit", "phone" : "phonenum", "face" : "image"}


api.add_resource(Inboxicated_Server, "/") #default url aka display and stuff
#api.add_resource(Inboxicated_server, "/mimic_video")#proto type I think?




if __name__ == "__main__":
    #need to initiate the db here
    host_ip = socket.gethostbyname("renoxdeception.duckdns.org")
    port_num = 10050
    app.run(host = host_ip, port = port_num, debug=True)