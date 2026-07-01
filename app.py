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

def show_order(recipient_number):
    url = f'https://graph.facebook.com/v18.0/{phone_number_id}/messages'

    headers={
        "Authorization":f"Bearer {access_token}",
        "Content-Type":"application/json"
    }
    payload={
         "messaging_product":"whatsapp",
        "to":recipient_number,
        "type":"text",
        "intereactive":{
            "type":"list",
            "to":recipient_number,
            "body":{"text":"welcome to surge and accedd , please select the order:"},
            "footer":{"Tap the button below to select the order"},
            "action":{
                "button":"view menu",
                "sections":[
                    {
                        "title":"pads",
                        "rows":[
                            {
                                "id":"ultr_pads","title":"extra duration","description":"100"
                            },
                            {
                            "id":"premium_pads","title":"long lasting","description":"50"
                            }
                        ]
                    }
                ]
            }

        }
    }
    requests.post(url,headers=headers,json =payload)
def order_summary(recipient_number,item_name,price):
    url = f'https://graph.facebook.com/v18.0/{phone_number_id}/messages'

    headers={
        "Authorization":f"Bearer {access_token}",
        "Content-Type":"application/json"
    }
    payload={
         "messaging_product":"whatsapp",
        "to":recipient_number,
        "type":"interactive",
        "interactive":{
            "type":"button",
            "header":{"type":"text","text":"order_summary"},
            "body":{
                "text":f"your selected items \n : {item_name} - {price}\n Delivery fees : 50\n total_price : {price +5}\n proceed to checkout"
            },
            "action":{
                "buttons":[{
                    "type":"reply","reply":{"id":f"confirm_{item_name}","title":"confirm"}
                    
                },
                {
                    "type":"reply","reply":{"id":f"confirm_{item_name}","title":"cancel"}
                }]
            }
        }
    }
    requests.post(url,headers=headers,json =payload)
@app.route('/webhook',methods=['GET','POST'])
def webhook():
    print(request.method)
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
                if message =='text':
                    show_order(phone_number)
                elif message=="interactive":
                    interactive_type = message["interactive"]
                    if interactive_type=='list_reply':
                        selected_id = message["interactive"]['list_reply']['id']
                        selected_title = message["interactive"]['list_reply']['title']

                        prices ={"premium_pads": 50,"ultr_pads":100}
                        price  = prices.get(selected_id,0)
                        order_summary(phone_number,selected_title,price)
                        
                    elif interactive_type=='button_reply':
                        button_id=message['interactive']['button_reply']['id']
                        if button_id.startswith('confirm'):
                            item_bought=button_id.replace("confirm_","")
                            bill_text = f"order confirmed"
                            send_message(phone_number,"order confirmed")
                            print(phone_number,text)
                        if button_id.startswith('cancel'):
                            send_message(phone_number,"order cancelled")



            except Exception as e:
                print(e)
            return jsonify({"status":"success"},200)
        else:
            return "something wron", 400
if __name__ == '__main__':
    app.run(port=5000,debug=True)
        
