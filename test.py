from dbdriver import Db_driver
from datetime import date

import io
import vk_api
# from vk_api import keyboard
# kb = keyboard.VkKeyboard()
# db = Db_driver()
# jobs = db.get_jobs()
# for job in jobs:
#     kb.add_button(job[1])
#     if job[1] != jobs[-1:][0][1]:
#         kb.add_line()
# print(kb.get_keyboard())
# f = io.open('test.json', 'w')
# f.write(kb.get_keyboard())
# print(db.get_user('123')[0][3])
print(date.today())
db = Db_driver()
print(db.get_jkh_by_id(48650719))

print(db.get_last_work_for_user(48650719))