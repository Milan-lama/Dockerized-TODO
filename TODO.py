import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

class TODO:
    engine = None
    connection = None
    database_name = os.getenv('DB_NAME', 'TODO')
    username = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'admin')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    result = []
    
    def __init__(self, id):
        self.id = id
    
    def db_connection(self):
        try:
            TODO.engine = create_engine(f"postgresql+psycopg2://{TODO.username}:{TODO.password}@{TODO.host}:{TODO.port}/{TODO.database_name}")
            TODO.connection = TODO.engine.connect()
            self.create()
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            exit(1)

    def create(self):
        try:
            if inspect(TODO.engine).has_table('todolist'):
                self.show()
            else:
                query = text(f'''CREATE TABLE todolist (
                                id SERIAL PRIMARY KEY,
                                username VARCHAR(30) NOT NULL,
                                list VARCHAR(300) NOT NULL)''')
                TODO.connection.execute(query)
                TODO.connection.commit()
                self.show()
        except SQLAlchemyError as e:
            print(f"Error creating table: {e}")
            TODO.connection.rollback()

    def show(self):
        try:
            query = text('SELECT * FROM todolist WHERE username = :username')
            TODO.result = TODO.connection.execute(query, {'username': self.id}).fetchall()
            TODO.result.sort(key=lambda x: x[0])
            if TODO.result:
                print(f"TODO List OF {self.id}")
                for sn in range(len(TODO.result)):
                    print('_______________________________________________')
                    print(f'{sn+1}. {TODO.result[sn][2]}')
            else:
                print('_______________________________________________')
                print("Add something to the list")
            print('_______________________________________________')
        except SQLAlchemyError as e:
            print(f"Error fetching data: {e}")

    def add(self, list_item):
        try:
            query = text('''INSERT INTO todolist (username, list) VALUES (:username, :list_item)''')
            TODO.connection.execute(query, {'list_item': list_item, 'username': self.id})
            TODO.connection.commit()
            self.show()
        except SQLAlchemyError as e:
            print(f"Error adding item: {e}")
            TODO.connection.rollback()

    def delete(self, list_id):
        try:
            if list_id < 1 or list_id > len(TODO.result):
                print("Invalid list ID.")
            else:
                query = text('''DELETE FROM todolist WHERE username = :username AND id = :list_id''')
                TODO.connection.execute(query, {'username': self.id, 'list_id': TODO.result[list_id - 1][0]})
                TODO.connection.commit()
            self.show()
        except SQLAlchemyError as e:
            print(f"Error deleting item: {e}")
            TODO.connection.rollback()

    def edit(self, update_item_list, list_id):
        try:
            if list_id < 1 or list_id > len(TODO.result):
                print("Invalid list ID.")
            else:
                query = text('''UPDATE todolist SET list = :new_value WHERE id = :list_id AND username = :username''')
                TODO.connection.execute(query, {'username': self.id, 'new_value': update_item_list, 'list_id': TODO.result[list_id - 1][0]})
                TODO.connection.commit()
            self.show()
        except SQLAlchemyError as e:
            print(f"Error updating item: {e}")
            TODO.connection.rollback()

    def disconnect(self):
        try:
            TODO.connection.close()
        except SQLAlchemyError as e:
            print(f"Error disconnecting: {e}")

    def __del__(self):
        print("LOG OUT")


while(True):
    user_input = input('1. log in \n2. exit\n')
    if user_input == '1':
        username = input("Enter username: ")
        todo = TODO(username)
        todo.db_connection()
        while(username):
            user_input = input('''\n1. Add to the list\n2. Delete item in the list\n3. Edit the list\n4. Log Out\n''')
            if user_input == '1':
                list_item = input('Enter what you wanna do: ')
                todo.add(list_item)
            elif user_input == '2':
                id = int(input('Enter the serial no of which you wanna delete: '))
                todo.delete(id)
            elif user_input == '3':
                list_id = int(input('Enter the sn you wanna edit: '))
                update_item_list = input('Enter what you wanna replace with: ')
                todo.edit(update_item_list,list_id)
            elif user_input == '4':
                todo.disconnect()
                del todo
                username = None
            else:
                print("Enter the right value")
            print('#####')
    elif user_input == '2':
        break
            

        

