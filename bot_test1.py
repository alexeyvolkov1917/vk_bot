import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api import keyboard
from vk_api.keyboard import *
from dbdriver import Db_driver
from datetime import date

session = requests.Session()
vk_session = vk_api.VkApi(token='5aec034dde24a5d2c2c00214209e4dfaec92d0bc470c86055ecb1e86aed3928e1142821a6b39699dcf81d')

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
        kb.add_button('Посмотреть рейтинг')
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
        i = 0
        kb = keyboard.VkKeyboard(one_time=True)
        for job in jobs:
            if i > 4:
                kb.add_line()
            kb.add_button(job[1], VkKeyboardColor.PRIMARY)
            i += 1
        return kb.get_keyboard()

    def JKH_rating(self):
        i = 1
        kb = keyboard.VkKeyboard(one_time=True)
        while i <= 5:
            if i > 4:
                kb.add_line()
            kb.add_button(i, color=VkKeyboardColor.PRIMARY)
            i += 1
        return kb.get_keyboard()

    def JKH_addr(self, id_per):
        id_jkh = dbdrive.get_jkh_by_id(id_per)
        addrs = dbdrive.get_addr_from_jkh(id_jkh[0])
        i = 0
        kb = keyboard.VkKeyboard(one_time=True)
        for addr in addrs:
            if i > 3:
                kb.add_line()
                i = 0
            kb.add_button(addr[0], color=VkKeyboardColor.PRIMARY)
        print(kb.get_keyboard())

        return kb.get_keyboard()


kb1 = keyboard.VkKeyboard(one_time=True)
kb1.add_button('ЖКХ', color=VkKeyboardColor.PRIMARY)
kb1.add_button('Житель', color=VkKeyboardColor.PRIMARY)


kb_prim = Keyboards()
kb_sec = Keyboards()
kb2 = kb_prim.firstKB()
job_done = ''
for event in Longpoll.listen():
    randomid = random.randint(1, 9999999)
    Check_user = False
    Check_JKH = False
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # for job in jobs:
        #     if event.text == job:

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

        if event.text == 'Посмотреть рейтинг' and Check_JKH is True:
            raits = dbdrive.get_rating()
            messagereit = ""
            for rait in raits:
                messagereit += str(raits.index(rait)+1) +':'+ str(rait[0]) + ' с оценкой - ' + str(rait[1]) + '\n'
            vk.messages.send(
                user_id=event.user_id,
                message='Рейтинг:\n'
                        + messagereit,        #ДОПИЛИТЬ
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
            list = dbdrive.get_last_work_for_user(event.user_id)
            vk.messages.send(
                user_id=event.user_id,
                message=list,
                random_id=randomid
            )
        if event.text == 'Рейтинг ЖКХ' and Check_user is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Рейтинг ЖКХ...',
                random_id=randomid
            )
        if event.text == ('1' or '2' or '3' or '4' or '5') and Check_user is True:
            addr = dbdrive.get_user(event.user_id)[0][3]
            jkh_id = dbdrive.get_jkh_from_addr(addr)
            dbdrive.write_first_rating(event.user_id, jkh_id, event.text)



        if Check_JKH is True:
            id = dbdrive.get_jkh_by_id(event.user_id)
            addr1 = dbdrive.get_addr_from_jkh(id[0])
            for addr in addr1:
                if event.text == addr[0]:
                    if job_done != '':
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Выполенная работа была добавлена',
                            random_id=randomid
                        )
                        dbdrive.write_order(address=addr, jkh=event.user_id, job=job_done, date=date.today())
                        job_done = ''
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Нечего добавлять',
                            random_id=randomid
                        )
            for job in jobs:
                if event.text == job[1] and Check_JKH is True:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Напишите адрес выполненной работы',
                        random_id=randomid,
                        keyboard=kb_prim.JKH_addr(event.user_id)
                    )
                    job_done = job[1]




        elif Check_JKH is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Я вас не понимаю',
                keyboard=kb_prim.JKH_KB_main(),
                random_id=randomid
            )
        elif Check_user is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Я вас не понимаю',
                keyboard=kb_prim.Users_main(),
                random_id=randomid
            )

        else:
            vk.messages.send(
                user_id=event.user_id,
                message='Я вас не понимаю. Вы хотите зарегестрироваться как житель или предстовитель ЖКХ?',
                keyboard=kb_prim.firstKB(),
                random_id=randomid
            )