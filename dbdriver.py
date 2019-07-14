import psycopg2
import matplotlib as mpl
import matplotlib.pyplot as plt

class Db_driver:

    def __init__(self):
        pass

    def get_connect(self):
        return psycopg2.connect(
            host='109.194.141.162',
            port='5432',
            database='vk_bot',
            user='postgres',
            password='123456')

    def update_jkh(self):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute('select jkh_id, avg(rating) from first_rating group by jkh_id')
        first_rating = cursor.fetchall()
        cursor.execute('select jkh, avg(rating) from response join orders on orders.order_id = response.order_id')
        job_rating = cursor.fetchall()
        jkh = {}
        for item in first_rating:
            jkh[item[0]] = item[1]
        for item in job_rating:
            jkh[item[0]] = (item[0] + item[1])/ 2
        for key in jkh.keys():
            cursor.execute(f'update jkh set rating = {jkh[key]} where jkh = {key}')
        cursor.commit()
        cursor.close()
        conn.close()

    def get_rating(self):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute('select id, name, rating from jkh order by rating desc')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_jobs(self,jkh):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id, name from orders o join jobs j on o.job = j.id where jkh=0')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_jkh_by_id(self, id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id from jkh where id_person=\'{id}\'')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list[0]

    def get_jkh(self):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute('select *, name from jkh ')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_last_work_for_user(self,id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select job, date, order_id from orders o join users u on o.address= u.adress where u.id ={id} limit 5')
        jobs = cursor.fetchall()
        list = []
        for job in jobs:
            cursor.execute(f'select name from jobs where id = {job[0]}')
            name = cursor.fetchall()
            list.add({'name': name, 'date': job[1], 'order_id':job[2] })
        for item in list:
            id = item['order_id']
            cursor.execute(f'select avg(rating) from response group where order_id ={id}')
            avg=cursor.fetchall()
            item.update({'rating:',avg[0][0]})
        cursor.close()
        conn.close()
        return list

    def get_addr_from_jkh(self, jkh_id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute('select adress from jkh_and_adress where jkh_id=' + str(jkh_id))
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_jkh_from_addr(self, addr):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select * from jkh_and_adress where adress=\'{addr}\'')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_user(self, id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select * from users where id = {id}')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def check_user(self, id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id from users where id = {id}')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(rows) == 0:
            return False
        else:
            return True

    def check_key(self,key):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id from jkh where key = {key}')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(rows) == 0:
            return False
        else:
            return True



    def get_keys(self):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select key from jkh')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def write_user(self, id, id_jkh, address):
        conn = self.get_connect()
        cursor = conn.cursor()
        values = f"values ('{id}','{id_jkh}','{address}')"
        cursor.execute('insert into users(id, id_jkh, adress) ' + values)
        conn.commit()
        cursor.close()
        conn.close()
        self.update_jkh_and_address(id_jkh,address)

    def get_jobs(self):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute('select id, name from jobs')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def write_first_rating(self,user_id,jkh_id,rating):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'insert into first_rating(jkh_id,user_id,rating) values ({jkh_id},{user_id},{rating})')
        conn.commit()
        cursor.close()
        conn.close()

    def update_jkh_and_address(self,jkh_id,addres):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f"insert into jkh_and_adress(jkh_id,adress) values ({jkh_id},'{addres}')")
        conn.commit()
        cursor.close()
        conn.close()

    def write_order(self,jkh, job, address,date):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f"insert into orders(jkh,job,address,date) values ({jkh},\'{job}\','{address}','{date}')")
        conn.commit()
        cursor.close()
        conn.close()

    def get_job(self, name):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id from jobs where name={name}')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def write_response(self,user, order, rating):
        conn = self.get_connect()
        cursor = conn.cursor()
        # cursor.execute(f"select weight from jobs j join order o on j.order_id = o.id")
        cursor.execute(f"insert into response(user_id,order_id,rating) values ({user},{order},{rating})")
        conn.commit()
        cursor.close()
        conn.close()

    def write_person_id(self, key, person_id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'update jkh set id_person = \'{person_id}\' where key =\'{key}\'')
        conn.commit()
        cursor.close()
        conn.close()

    def check_jkh(self, id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select * from jkh where id_person=\'{id}\'')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(list) == 0:
            return False
        else:
            return True

    def get_jkh_by_name(self, name):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id from jkh where name=\'{name}\'')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_orders_from_jkh(self, jkh_id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select * from orders where jkh=\'{jkh_id}\'')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

    def get_job_by_name(self, name):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'select id from jobs where name=\'{name}\'')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list


