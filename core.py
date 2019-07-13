from dbdriver import Db_driver
from loader import Loader



db_driver = Db_driver()
print(db_driver.get_jkh())
user = {'id':123, 'first_name': 'abs', 'last_name':'last_name','id_jkh':0,'address': 'asdfasdga'}
db_driver.write_user_to_db(user)



