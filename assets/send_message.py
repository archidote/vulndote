from assets.controller import * 

def send_message(bot_token,chat_id,message) : 
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html"
    try: 
        return requests.get(url)
    except Exception as e :
        print ("Fatal error : "+str(e))