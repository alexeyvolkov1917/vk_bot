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
user_jkh = ''



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

        return kb.get_keyboard()

    def get_JKH_list(self):
        i = 0
        kb = keyboard.VkKeyboard(one_time=True)
        jkhs = dbdrive.get_jkh()
        for jkh in jkhs:
            if i > 3:
                kb.add_line()
            kb.add_button(jkh[1])
            i += 1
        return kb.get_keyboard()

    def get_addr_user(self, jkh):
        kb = keyboard.VkKeyboard(one_time=True)
        id = dbdrive.get_jkh_by_name(jkh)
        addrs = dbdrive.get_addr_from_jkh(id[0][0])
        i = 0
        if len(addrs) != 0:
            for addr in addrs:
                if i > 3:
                    kb.add_line()
                    i = 0
                kb.add_button(addr[0], color=VkKeyboardColor.PRIMARY)
                i += 1

            return kb.get_keyboard()
        else:
            return kb.get_empty_keyboard()

kb1 = keyboard.VkKeyboard(one_time=True)
kb1.add_button('ЖКХ', color=VkKeyboardColor.PRIMARY)
kb1.add_button('Житель', color=VkKeyboardColor.PRIMARY)


kb_prim = Keyboards()
kb_sec = Keyboards()
kb2 = kb_prim.firstKB()
job_done = ''
keys = dbdrive.get_keys()
for event in Longpoll.listen():
    randomid = random.randint(1, 9999999)
    Check_user = False
    Check_JKH = False
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # for job in jobs:
        #     if event.text == job:
        if dbdrive.check_user(event.user_id):
            Check_user = True
        if dbdrive.check_jkh(event.user_id):
            Check_JKH = True
        for key in keys:
            if event.text == key[0] and Check_JKH is False:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Теперь вы в группе ЖКХ',
                    random_id=randomid,
                    keyboard=kb_prim.JKH_KB_main()
                )
                dbdrive.write_person_id(key[0], event.user_id)
        jkhs = dbdrive.get_jkh()
        if Check_user is False:
            for jkh in jkhs:
                if event.text == jkh[1]:
                    user_jkh = jkh[1]
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Введите свой адрес',
                        keyboard=kb_prim.get_addr_user(user_jkh),
                        random_id=randomid
                    )
            if user_jkh != '':
                id = dbdrive.get_jkh_by_name(user_jkh)
                addrs = dbdrive.get_addr_from_jkh(id[0][0])
                for addr in addrs:
                    if event.text == addr[0] and user_jkh != '':
                        dbdrive.write_user(event.user_id, id[0][0], addr[0])
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Вы вступили в группу жителей вашего ЖКХ по вашему адресу.',
                            keyboard=kb_prim.Users_main(),
                            random_id=randomid
                        )


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
                vk.messages.send(
                    user_id=event.user_id,
                    message='Введите ключ!',
                    random_id=randomid,
                )
            elif Check_JKH == True or Check_user == True:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Вы уже вступили в одну из групп!',
                    random_id=randomid
                )
        if event.text == 'Житель':
            if Check_user == False and Check_JKH == False:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Введите свой ЖКХ',
                    random_id=randomid,
                    keyboard=kb_prim.get_JKH_list()
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
                messagereit += str(raits.index(rait)+1) +':'+ str(rait[1]) + ' с оценкой - ' + str(rait[2]) + '\n'
            vk.messages.send(
                user_id=event.user_id,
                message='Рейтинг:\n'
                        + messagereit,        #ДОПИЛИТЬ
                random_id=randomid
            )
        if event.text == 'Выполненные работы' and Check_JKH is True:
            id = dbdrive.get_jkh_by_id(event.user_id)
            id = id[0]
            mess = ''
            orders = dbdrive.get_orders_from_jkh(id)
            if len(orders) != 0:
                for ord in orders:
                    mess += f'{ord[0]} - {ord[1] - ord[2]}'
                vk.messages.send(
                    user_id=event.user_id,
                    message=mess,
                    random_id=randomid,
                    keyboard=kb_prim.JKH_KB_main()
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Ничего нет',
                    random_id=randomid,
                    keyboard=kb_prim.JKH_KB_main()
                )

        if event.text == 'Изменить оценку ЖКХ' and Check_user is True:
            vk.messages.send(
                user_id=event.user_id,
                message='Выберите новую оценку вашего ЖКХ',
                random_id=randomid
            )
        if event.text == 'Посмотреть последние выполненные работы' and Check_user is True:
            list = dbdrive.get_last_work_for_user(event.user_id)
            mass = ''
            for lis in list:
                mass += lis
            if mass == '':
                vk.messages.send(
                    user_id=event.user_id,
                    message='По вашему адресу не зарегистрировано работ',
                    random_id=randomid
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message=mass,
                    random_id=randomid
                )
        if event.text == 'Рейтинг ЖКХ' and Check_user is True:
            raits = dbdrive.get_rating()
            messagereit = ""
            for rait in raits:
                messagereit += str(raits.index(rait) + 1) + ':' + str(rait[1]) + ' с оценкой - ' + str(rait[2]) + '\n'
            vk.messages.send(
                user_id=event.user_id,
                message='Рейтинг:\n'
                        + messagereit,  # ДОПИЛИТЬ
                random_id=randomid
            )
        if event.text == ('1' or '2' or '3' or '4' or '5') and Check_user is True:
            addr = dbdrive.get_user(event.user_id)[0][3]
            jkh_id = dbdrive.get_jkh_from_addr(addr)
            dbdrive.write_first_rating(event.user_id, jkh_id[0][0], event.text)



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
                        job_id = dbdrive.get_job_by_name(job_done)
                        dbdrive.write_order(address=addr[0], jkh=event.user_id, job=job_id[0][0], date=date.today())
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




            else:
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