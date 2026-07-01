from flask import Flask,request, jsonify
import requests

app=Flask(__name__)

verify_toekn='testtoken'
phone_number_id='1223995324127406'
access_token='EAAObTIE5ifYBRzX6tuzRxwg0hThGywzP6za65Q60MdhGBRHxmqHphdT9W8pgCX6xQvWBdcalWwafeTdEbgdwgfS0GR1IQzeUzI9rKiKQj0wvyRwMjFWTR1Qurw8bnRZAH2uMqi870yj7QFqmxLQ1eiqhRgqRUba18rM9Yc7NKKNbVJTcXukp97XUcW13kSMQBUrTjzOPNKbvLxvmhHCoxKae7mYqATW0WlFaDkUHMIZCVGUdvZAJZCrZCraIHRZCocZCcATWfDh6MLZCN9w1JXKX'

def send_message(recipient_number , message_text):
    url = f'https://graph.facebook.com/v18.0/{phone_number_id}/messages'

    headers={
        "Authorization":f"Bearer {access_token}",
        "Content-Type":"application/json"
    }

    payload = {
        "messaging_product":"whatsapp",
        "to":recipient_number,
        "type":"text",
        "text":{"body":message_text}
    }
    requests.post(url,headers=headers,json =payload)

@app.route('/webhook',methods=['GET','POST'])
def webhook():
    if request.method =='GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
    
        if mode and token:
            if mode == 'subscribe' and token=='testtoken':
                print("webhook verified")
                return challenge,200
        else:
            return "bad request",400

    if request.method =='POST': 
        body = request.get_json()

        if body.get('object'):
            try:
                message =body['entry'][0]['changes'][0]['value']['messages'][0]
                phone_number = message['from']
                text = message['text']['body']

                send_message(phone_number,"Thanks for message ,please don't except any reply after this")
                print(phone_number,text)
            except Exception as e:
                print(e)
            return jsonify({"status":"success"},200)
        else:
            return "something wron", 400
if __name__ == '__main__':
    app.run(port=5000,debug=True)
        
