import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api import keyboard
from vk_api.keyboard import *
from dbdriver import Db_driver

session = requests.Session()
vk_session = vk_api.VkApi(login='spaikywaiky@gmail.com', token='5aec034dde24a5d2c2c00214209e4dfaec92d0bc470c86055ecb1e86aed3928e1142821a6b39699dcf81d')

dbdrive = Db_driver()

jobs = dbdrive.get_jobs()

user_list = []
jkh_list = []
Check_user = False
Check_JKH = False
Longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

class Keyboards(object):
    def __init__(self):
        pass

    def JKH_KB_main(self):
        kb = keyboard.VkKeyboard(one_time=False)
        kb.get_empty_keyboard()
        kb.add_button('Добавить работу')
        kb.add_button('Посмотреть место в рейтинге')
        kb.add_button('Выполненные работы')
        return kb.get_keyboard()

    def firstKB(self):
        kb = keyboard.VkKeyboard(one_time=True)
        kb.add_button('ЖКХ', color=VkKeyboardColor.PRIMARY)
        kb.add_button('Житель', color=VkKeyboardColor.PRIMARY)
        return kb.get_keyboard()

    def Users_main(self):
        kb = keyboard.VkKeyboard(one_time=False)
        kb.add_button('Изменить оценку ЖКХ')
        kb.add_button('Посмотреть последние выполненные работы')
        kb.add_button('Рейтинг ЖКХ')
        return kb.get_keyboard()

    def JKH_jobs(self, jobs):
        kb = keyboard.VkKeyboard(one_time=True)
        i = 0
        for job in jobs:
            if i > 4:
                kb.add_line()
                i = 0
            kb.add_button(job[1], VkKeyboardColor.PRIMARY)
            i += 1
        return kb.get_keyboard()


kb1 = keyboard.VkKeyboard(one_time=True)
kb1.add_button('ЖКХ', color=VkKeyboardColor.PRIMARY)
kb1.add_button('Житель', color=VkKeyboardColor.PRIMARY)

kbtest = keyboard.VkKeyboard(one_time=True)
kbtest.add_button('Test')
kbtest.add_button('TestTest')

kb_prim = Keyboards()
kb_sec = Keyboards()
kb2 = kb_prim.firstKB()
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
                vk.messages.send(
                    user_id=event.user_id,
                    message='Здравствуйте. Вы хотите зарегестрироваться как житель или предстовитель ЖКХ?',
                    random_id=randomid,
                    keyboard=kb1.get_keyboard()
                )
            elif event.from_user and (Check_user == True or Check_JKH == True):
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы уже зарегистрированны!',
                    random_id=randomid
                )
        if event.text == 'ЖКХ':
            if Check_user == False and Check_JKH == False:
                jkh_list.append(event.user_id)
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы зарегистрированны как представитель ЖКХ!',
                    random_id=randomid,
                    keyboard=kb_prim.JKH_KB_main()
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
                    message='Вы зарегистрированны как Житель!',
                    random_id=randomid,
                    keyboard=kb_prim.Users_main()
                )
            elif Check_JKH == True or Check_user == True:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы уже вступили в одну из групп!',
                    random_id=randomid
                )
        if event.text == 'Добавить работу' and Check_JKH is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Выберите тип работы',
                keyboard=kb_sec.JKH_jobs(jobs),              #ДОПИЛИТЬ
                random_id=randomid
            )
        if event.text == 'Посмотреть место в рейтинге' and Check_JKH is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Вы занимаете ... место',        #ДОПИЛИТЬ
                random_id=randomid
            )
        if event.text == 'Выполненные работы' and Check_JKH is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Тут должны были быть ваши работы',
                random_id=randomid
            )
        if event.text == 'Изменить оценку ЖКХ' and Check_user is True:
            vk.messages.send(
                user_id=event.user_id,
                messages='Выберите новую оценку вашего ЖКХ',
                random_id=randomid
            )
        if event.text == 'Посмотреть последние выполненные работы' and Check_user is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Список последних 5 выполненных работ',
                random_id=randomid
            )
        if event.text == 'Рейтинг ЖКХ' and Check_user is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Рейтинг ЖКХ...',
                random_id=randomid
            )





