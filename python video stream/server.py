'''
Client Features:
    Deposit Key
        ->name, phone, index, image,

    Retrieve Key
        ->image

    Add keeper
        ->name, phone, password?

    Summon Keeper
        ->?

    Submit Feedback
        -> long text


Server Features:
    Deposit Key
        <- 200 ok, confirm

    Retrieve Key
        <- name, index, drunk confidence

    Add Keeper
        <- 200 ok, confirm

    Submit Feedback
        <- 200 ok, confirm

'''


import base64
from email.mime import image
import flask
from flask_restful import Api, Resource
import time

app = flask.Flask(__name__) #this would be replaced with app = flask.Flask(Inboxicated.py)/ flask.Flask(Inboxicated)
api = Api(app)


class DataGet(Resource):
    def put(self, command_type):
        if command_type == 'add_a_key':
         
            received_name = flask.request.form['Name']
            received_phone = flask.request.form['Phone']
            received_index = flask.request.form['Index']
            received_image = flask.request.form['Image']            
            
            writeTofile(received_image, (received_name+received_phone+".png"))
            
            print(" this is one ", received_name, " this is two ", received_phone, " this is three ", received_index)
        
            return {"name": received_name, "phone" : received_phone, "index": received_index}
            
        elif command_type == 'retrieve_key':
            received_image = flask.request.form['Image']     
            
            t = time.localtime()
            currenttime = time.strftime("%m%d%Y%H%M%S", t)
            #print(currenttime)
            
            writeTofile(received_image, ("unknown" + currenttime + ".png"))

            
        elif command_type == 'add_keeper':
            received_name = flask.request.form['Name']
            received_phone = flask.request.form['Phone']
            received_index = flask.request.form['Password']
            print(received_name + ' you a keeper now')


        
        #return flask.jsonify({"test_msg": "Your Key is Deposited"})

        




'''class AddKeeper(Resource):
    def put(self, keeper_packet):
        return {"test_msg": "Your Keeper is added"}

class ReturnKeys(Resource):
    def put(self, return_key_packet):
        return {"test_msg": "here are your keys"}'''


api.add_resource(DataGet, "/inboxicated/<string:command_type>")
#api.add_resource(ReturnKeys, "/retrieve_key/<string:command_type>")
#api.add_resource(AddKeeper, "/add_keeper/<string:command_type>")


#turning the binary data column back to files
def writeTofile(byteimage, filename):
    #decode image from hex to byte array
    byteimage = bytearray.fromhex(byteimage)
                
    #write image bytes to file
    with open(filename, 'wb') as file:
        file.write(byteimage)
    print("File ready : " +  filename)


#this starts the server
if __name__ == "__main__":
    #app.run(debug = True)
    host_val = "10.0.0.3"

    print (host_val)
    
    app.run(host = host_val, port = 10050, debug = True)
    #app.run(host = 'host_val', port = 10050) #this would be final implementation
