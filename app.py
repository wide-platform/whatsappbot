from flask import Flask,request, jsonify

app=Flask(__name__)

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
                message =body
                print(message)
            except:
                return jsonify({"status":"success"},200)
        else:
            return "something wron", 400
if __name__ == '__main__':
    app.run(port=5000,debug=True)
        
