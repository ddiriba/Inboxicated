import base64
from email.mime import image
import flask
from flask_restful import Api, Resource
import os
import socket

app = flask.Flask(__name__) #this would be replaced with app = flask.Flask(Inboxicated.py)/ flask.Flask(Inboxicated)
api = Api(app)


class AddKeys(Resource):
    def put(self, command_type):
        if command_type == 'add_a_key':
            #print()
            #flask.request.form
            
            received_name = flask.request.form['Name']
            received_phone = flask.request.form['Phone']
            received_index = flask.request.form['Index']
            received_image = flask.request.form['Image']
            #turning the binary data column back to files
            
            #decode image from hex to byte array
            received_image = bytearray.fromhex(received_image)
            
            
            #write image bytes to file
            with open("meganreceived.png", 'wb') as file:
                file.write(received_image)
            print("File ready : " +  "meganreceived.png")
            

        elif command_type == 'add_a_keeper':
            print('you a keeper now')

        print(" this is one ", received_name, " this is two ", received_phone, " this is three ", received_index)
        
        return {"name": received_name, "phone" : received_phone, "index": received_index}
        
        #return flask.jsonify({"test_msg": "Your Key is Deposited"})

class AddKeeper(Resource):
    def put(self, keeper_packet):
        return {"test_msg": "Your Keeper is added"}

class ReturnKeys(Resource):
    def put(self, return_key_packet):
        return {"test_msg": "here are your keys"}


api.add_resource(AddKeys, "/deposit_key/<string:command_type>")
api.add_resource(ReturnKeys, "/retrieve_key")
api.add_resource(AddKeeper, "/add_keeper")


#turning the binary data column back to files
def writeTofile(self, data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("File ready : " +  filename)


#this starts the server
if __name__ == "__main__":
    #app.run(debug = True)
    host_val = "10.0.0.3"

    print (host_val)
    
    app.run(host = host_val, port = 10050, debug = True)
    #app.run(host = 'host_val', port = 10050) #this would be final implementation
