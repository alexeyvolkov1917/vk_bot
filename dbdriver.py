import psycopg2

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


    def get_jkh(self):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute('select id, name from jkh')
        list = cursor.fetchall()
        cursor.close()
        conn.close()
        return list

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

    def write_user(self,user):
        conn = self.get_connect()
        cursor = conn.cursor()
        id = user['id']
        first_name = user['first_name']
        last_name = user['last_name']
        address = user['address']
        id_jkh = user['id_jkh']
        values = f"values ('{id}', '{first_name}', '{last_name}','{id_jkh}','{address}')"
        cursor.execute('insert into users(id, first_name, last_name,id_jkh, adress) ' + values)
        conn.commit()
        cursor.close()
        conn.close()

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
        cursor.execute(f"insert into jkh_and_adress(jkh_id,adress) values ({jkh_id},'{addres})")
        conn.commit()
        cursor.close()
        conn.close()

    def write_person_id(self, id, person_id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'update jkh set person_id = {person_id} where id = {id}')
        conn.commit()
        cursor.close()
        conn.close()




