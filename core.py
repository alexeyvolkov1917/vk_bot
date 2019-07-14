from dbdriver import Db_driver



db_driver = Db_driver()
print(db_driver.get_jobs())
# user = {'id':123, 'first_name': 'abs', 'last_name':'last_name','id_jkh':0,'address': 'asdfasdga'}
# db_driver.write_user(user)
db_driver.write_order(0,0,'asd','10/07/2019')
# db_driver.write_response(123,0,10)
# db_driver.write_first_rating(123,0,8)



