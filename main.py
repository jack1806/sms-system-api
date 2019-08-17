from flask import Flask
from firebase import firebase
from pyfcm import FCMNotification
import json

app = Flask(__name__)
db = firebase.FirebaseApplication("https://sms-system-tarp.firebaseio.com",None)
push_service = FCMNotification(api_key="AIzaSyAwAliC4SNaM_JvJdQoQic6nXhFb_wONwE")
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
	put_id = db.post('/data',put_data,{'print': 'pretty'},{'X_FANCY_HEADER': 'VERY FANCY'})
	if(put_id!=None):
		push()
		return "{'status':200}"
	return "{'status':500}"

def push():
	reg_id = ""
	title = "Send SMS"
	body = json.dumps(put_data)
	res = push_service.notify_single_device(registration_id=reg_id,message_title=title,message_body=body)
	print(res)

app.run()

