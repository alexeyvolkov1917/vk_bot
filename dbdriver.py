import psycopg2

class Db_driver:

    def __init__(self):
        pass


    def get_connect(self):

        return psycopg2.connect(
            host='localhost',
            port='5432',
            database='vk_bot',
            user='postgres',
            password='admin')



    def write_user_to_db(self,user):
        conn = self.get_connect()
        cursor = conn.cursor()
        values = 'values'
        id = user['id']
        first_name = user['first_name']
        last_name = user['last_name']
        address = user['address']
        id_jkh = user['id_jkh']
        values += f" ('{id}', '{first_name}', '{last_name}','{id_jkh}','{address}'),"
        cursor.execute('insert into users(id, first_name, last_name,id_jkh, adress) ' + values)
        conn.commit()
        cursor.close()
        conn.close()

    def write_person_id_in_db(self,id, person_id):
        conn = self.get_connect()
        cursor = conn.cursor()
        cursor.execute(f'update jkh set person_id = {person_id} where id = {id}')
        conn.commit()
        cursor.close()
        conn.close()


    def clear_database(self):
        conn = self.get_connect()
        cur = conn.cursor()
        cur.execute('delete from friends')
        cur.execute('delete from users')
        cur.commit()
        cur.close()
        conn.close()


