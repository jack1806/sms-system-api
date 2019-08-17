from flask import Flask,request
from firebase import firebase
from pyfcm import FCMNotification
import json
import os

app = Flask(__name__)
db = firebase.FirebaseApplication("https://sms-system-tarp.firebaseio.com",None)
push_service = FCMNotification(api_key="AAAAdRC7uZ0:APA91bES_ElPLByHD-nlX6J9doi9OOObvGfmQ-SS_qYCuO4alEAbZXdnZjNejLuCez5z_Od1NLS8RmnEWVWA3JEU-799_m7iYD90JF8jaZMBddWSsXz5s__dKzc_klVsgLoRUEf2lgYh")
reg_id = db.get('/reg',None)

@app.route('/')
def index():
	return "Hello world!"

@app.route('/add-leave',methods=['POST'])
def add_leave_request():
	f_from = request.form.get('from')
	f_reason = request.form.get('reason')
	f_sender = request.form.get('sender_id')
	f_till = request.form.get('till')
	f_number = request.form.get('to_number')
	put_data = {'from':f_from,'reason':f_reason,'sender_id':f_sender,'status':0,'till':f_till,'to_number':f_number}
	put_id = db.post('/data',data=put_data,params={'print': 'pretty','X_FANCY_HEADER': 'VERY FANCY'})
	if(put_id!=None):
		push(put_data)
		return "{'status':200}"
	return "{'status':500}"

def push(put_data):
	title = "Send SMS"
	body = json.dumps(put_data)
	res = push_service.notify_single_device(registration_id=reg_id,message_title=title,message_body=body)
	print(res)

if __name__ == "__main__":
	port = int(os.environ.get("PORT",5000))
	app.run(host='0.0.0.0',port=port)
