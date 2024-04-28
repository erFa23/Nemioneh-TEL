import requests as req
from time import sleep
import pyautogui as os

token = '7073829955:AAEkFQVp4Ox0ImIlARdKvRMd26SJ1msPoq4'

# =============================================================================

tel_url = f'https://api.telegram.org/bot{token}/'

# =============================================================================

def run(command:str):
    res = req.get(tel_url + f'{command}')
    return res.json()
    
def update():
    update = run('getUpdates')

    new_message = []

    if update['result'] != [] :
        for i in update['result']:
            try:
                message_id = i['message']['message_id']
            except:
                try:
                    message_id = i["callback_query"]['message']['message_id']
                except:
                    message_id = None
                    
            try:
                chat_id = i['message']['chat']['id']
            except:
                try:
                    chat_id = i["callback_query"]['message']['chat']['id']
                except:
                    try:
                        chat_id = i['channel_post']['chat']['id']
                    except:
                        chat_id = None
            try:
                media_group_id = i['message']['media_group_id']
            except:
                try:
                    media_group_id = i['channel_post']['media_group_id']
                except:
                    media_group_id = None

            try:
                text = i['message']['text']
            except:
                try:
                    text = i['channel_post']['text']
                except:
                    text = i["callback_query"]['message']['text']

            try:
                data = i["callback_query"]['message']['data']
            except:
                data = None




            try:
                file = { 
                    'file_id3': {'file_id': i['message']['photo'][-3]['file_id'], 'file_unique_id': i['message']['photo'][-3]['file_unique_id'], 'type' : 'photo'},
                    'file_id2': {'file_id': i['message']['photo'][-2]['file_id'], 'file_unique_id': i['message']['photo'][-2]['file_unique_id'], 'type' : 'photo'},
                    'file_id': {'file_id': i['message']['photo'][-1]['file_id'], 'file_unique_id': i['message']['photo'][-1]['file_unique_id'], 'type' : 'photo'},
                }
            except:
                try:
                    file = { 
                    'file_id3': {'file_id': i['channel_post']['photo'][-3]['file_id'], 'file_unique_id': i['channel_post']['photo'][-3]['file_unique_id'], 'type' : 'photo'},
                    'file_id2': {'file_id': i['channel_post']['photo'][-2]['file_id'], 'file_unique_id': i['channel_post']['photo'][-2]['file_unique_id'], 'type' : 'photo'},
                    'file_id': {'file_id': i['channel_post']['photo'][-1]['file_id'], 'file_unique_id': i['channel_post']['photo'][-1]['file_unique_id'], 'type' : 'photo'},
                }
                except:  
                    file = None
            
            if file == None :
                try:
                    file = { 
                        'file_id': {'file_id': i['message']['video']['file_id'], 'file_unique_id': i['message']['video']['file_unique_id'], 'type' : 'video'},
                    }
                except:
                    try:
                        file = { 
                        'file_id': {'file_id': i['channel_post']['video']['file_id'], 'file_unique_id': i['channel_post']['video']['file_unique_id'], 'type' : 'video'},
                    }
                    except:  
                        file = None

            if file != None and text == None:
                try:
                    text = i['message']['caption']
                except:
                    try:
                        text = i['channel_post']['caption']
                    except:
                        text = None

            run('getUpdates?offset=' + str(i['update_id']+1))

            # others
            new_message.append({'chat_id': chat_id, 'message_id': message_id, 'file_ids': file, 'text': text, 'media_group_id' : media_group_id, 'data':data})
        
    return new_message # 'chat_id | message_id | 'file_ids : {file_id(1,2,3)} | text'

def send(chat_id:str, text:str, message_id=None, glass_buttons:dict=None):
    

    if glass_buttons:
        my_json = {
            "reply_markup": glass_buttons
        }
        if message_id:
            url = f'{tel_url}sendMessage?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}'
        else:
            url = f'{tel_url}sendMessage?chat_id={chat_id}&text={text}'
        req.post(url,None, my_json)
    else:
        if message_id:
            run(f'sendMessage?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}')
        else:
            run(f'sendMessage?chat_id={chat_id}&text={text}')
    ##### examples #######

    # glass_buttons = {
    #         "inline_keyboard": [
    #             [
    #                 {"text": "Button 1", "callback_data": "button1"},
    #                 {"text": "Button 2", "callback_data": "button2"}
    #             ]
    #         ]
    #     }


def send_media(chat_id:str, media_files:list):
    # media files = [ {'type' : 'photo/video' , 'media' : file_url , 'caption' : caption} , {'type' : 'photo/video' , 'media' : file_url2 , 'caption' : caption2} ]
    req.post(tel_url + 'sendMediaGroup', json={'media': media_files, 'chat_id': chat_id})

def file_url(file_id):
    json = run(f'getFile?file_id=' + str(file_id['file_ids']['file_id1']['file_id']))
    path = 'https://api.telegram.org/file/bot7073829955:AAEkFQVp4Ox0ImIlARdKvRMd26SJ1msPoq4/' + json['result']['file_path']
    return path

def send_media_by_file_id():
    pass

def list_buttons(buttons:list):
    pass
# =============================================================================
    
def bot(a):
    if a['text'] == '/start' :
        send(a['chat_id'], 'متن شروع', a['message_id'])
    elif a['text'] == '/help' :
        send(a['chat_id'], 'متن راهنما', a['message_id'])
    elif a['text'] == '/menu':
        send(a['chat_id'],
            'متن دلخواه',
            a['message_id']
            )
    elif a['text'] == '/buttons':
        send(
            a['chat_id'],
            'jgvgvkb',
            None,
            glass_buttons = {
            "inline_keyboard":[
                [
                    {"text": "Button 1", "callback_data": "button1"},
                    {"text": "Button 2", "callback_data": "button2"}
                ]
            ]
        }

    )
    elif a['data'] == 'button1':
        send(a['chat_id'], 'عملیات کلید 1')
# =============================================================================

while True:
    sleep(1)
    new_messages = update()
    if new_messages != []:
        for i in new_messages:
            bot(i)
