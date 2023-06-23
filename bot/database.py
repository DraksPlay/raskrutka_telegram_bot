import pymysql
import pymysql.cursors


class Connector:

    def __init__(self, host, user, password, name, debug):
        self._connection = pymysql.connect(host=host, user=user, password=password, database=name, cursorclass=pymysql.cursors.DictCursor, unix_socket="/var/run/mysqld/mysqld.sock" if debug == 0 else None)  # Соединение с БД
        self._cursor = self._connection.cursor()


class Database(Connector):

    def __init__(self, host, user, password, name, debug=0):
        super().__init__(host, user, password, name, debug)
        self.users = Users(self._connection, self._cursor)
        self.form_payment = FormPayment(self._connection, self._cursor)
        self.orders = Orders(self._connection, self._cursor)
        self.tech_support = TechSupport(self._connection, self._cursor)
        self.free_view = FreeView(self._connection, self._cursor)


class Users:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    # Чтение данных пользователя из БД
    def user_read(self, search_value, search_to="id"):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
            SELECT *
            FROM users
            WHERE {search_to} = {search_value}
            ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchall()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        if len(results) != 0:
            return results[0]
        else:
            return False

    # Сохранение данных у пользователя в БД
    def user_save(self, column, value, search_value, search_to="id"):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''
            UPDATE users 
            SET {column} = {value if type(value) != str else f"'{value}'"}
            WHERE {search_to} = {search_value}
            ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения

    def user_add(self, user_id):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''
                    INSERT INTO users
                    (id) 
                    VALUES ({user_id});
                    ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения


class FormPayment:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    # Чтение данных пользователя из БД
    def all(self):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM form_payment
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchall()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def create_order(self, billId, user_id, amount, currency, comment, expirationDateTime,
                     creationDateTime, status, payUrl, recipientPhoneNumber):
        self.connection.begin()
        query = (f'''
                INSERT INTO `form_payment`
                (`billId`, `user_id`, `amount`, `currency`, `comment`, `expirationDateTime`, `creationDateTime`, `status`, `payUrl`, `recipientPhoneNumber`) 
                VALUES ('{billId}','{user_id}','{amount}','{currency}','{comment}',
                '{expirationDateTime}','{creationDateTime}','{status}','{payUrl}','{recipientPhoneNumber}')
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения

    def delete(self, billId):
        query = (f'''
                     DELETE FROM `form_payment` 
                     WHERE billId = {billId}
                     ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения


class Orders:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def all(self):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM orders
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchall()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def user_orders(self, user_id):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM orders
                WHERE user_id = {user_id}
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchall()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def create(self, order_id, user_id, name, link, price):
        self.connection.begin()
        query = (f'''
                INSERT INTO `orders`
                (`id`, `user_id`, `name`, `link`, `price`) 
                VALUES ({order_id}, {user_id}, '{name}', '{link}', {price})
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения

    def update(self, order_id, set_name, set_value):
        self.connection.begin()
        query = (f'''
                UPDATE `orders` 
                SET `{set_name}`= {f"'{set_value}'" if type(set_value) == str else set_value} 
                WHERE `id` = {order_id}
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения


class TechSupport:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def all(self):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM tech_support
                WHERE answered = '0'
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchall()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def create(self, user_id, message):
        self.connection.begin()
        query = (f'''
                INSERT INTO `tech_support`
                (`user_id`, `message`) 
                VALUES ({user_id}, '{message}')
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения

    def read(self, form_id):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM tech_support
                WHERE id = {form_id}
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchone()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def save(self, form_id, set_name, set_value):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''
                UPDATE `tech_support` 
                SET `{set_name}`= {f"'{set_value}'" if type(set_value) == str else set_value} 
                WHERE `id` = {form_id}
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchone()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results


class FreeView:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def all(self):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM free_view
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchall()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def create(self, user_id):
        self.connection.begin()
        query = (f'''
                INSERT INTO `free_view`
                (`user_id`, `last_take`, `link`, `order_id`) 
                VALUES ({user_id}, 0, '', 0)
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        self.connection.commit()  # Сохранить, занесённые изменения

    def read(self, user_id):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''        
                SELECT *
                FROM free_view
                WHERE user_id = {user_id}
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchone()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results

    def save(self, user_id, set_name, set_value):
        self.connection.begin()
        # Подготовить запрос в БД
        query = (f'''
                UPDATE `free_view` 
                SET `{set_name}`= {f"'{set_value}'" if type(set_value) == str else set_value} 
                WHERE `user_id` = {user_id}
                ''')
        self.cursor.execute(query)  # Выполнить запрос в БД
        results = self.cursor.fetchone()  # Результат из БД
        # Если данные есть, то выдать их, если нет, то вернуть None
        return results
