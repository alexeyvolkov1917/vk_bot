import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
import random

session = requests.Session()
vk_session = vk_api.VkApi(login='spaikywaiky@gmail.com', token='5aec034dde24a5d2c2c00214209e4dfaec92d0bc470c86055ecb1e86aed3928e1142821a6b39699dcf81d')

user_list = []
jkh_list = []
Check_user = False
Check_JKH = False
Longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in Longpoll.listen():
    randomid = random.randint(1, 9999999)
    Check_user = False
    Check_JKH = False
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        for user in user_list:
            if user == event.user_id:
                Check_user = True
        for jkh in jkh_list:
            if jkh == event.user_id:
                Check_JKH = True
        if event.text == 'Начать':
            if event.from_user and Check_JKH == False and Check_user == False:
                randomid = random.randint(1, 9999999)
                vk.messages.send(
                    user_id=event.user_id,
                    message='Hello, Житель или ЖКХ?',
                    random_id=randomid
                )
            elif event.from_user and (Check_user == True or Check_JKH == True):
                randomid = random.randint(1, 9999999)
                vk.messages.send(
                    user_id=event.user_id,
                    message='You already started the chat!',
                    random_id=randomid
                )
        if event.text == 'ЖКХ':
            if Check_user == False and Check_JKH == False:
                jkh_list.append(event.user_id)
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы вступили в группу ЖКХ!',
                    random_id=randomid
                )
            elif Check_JKH == True or Check_user == True:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы уже вступили в одну из групп!',
                    random_id=randomid
                )
        if event.text == 'Житель':
            if Check_user == False and Check_JKH == False:
                user_list.append(event.user_id)
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы вступили в группу Житель!',
                    random_id=randomid
                )
            elif Check_JKH == True or Check_user == True:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы уже вступили в одну из групп!',
                    random_id=randomid
                )





