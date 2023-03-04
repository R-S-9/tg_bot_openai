import os
import sqlite3


class SQLConnect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect(
            'db.sqlite', check_same_thread=False
        )
        self.cursor = self.sqlite_connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def db_information(self) -> None:
        """Информация о бд"""
        self.cursor.execute("select sqlite_version();")

        print("Версия базы данных SQLite: ", self.cursor.fetchall())

        return None

    def create_user_table(self) -> None:
        """Создание таблицы User"""

        try:
            cursor = self.sqlite_connection

            crete_table = ''' 
                CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL
                    );
            '''

            cursor.execute(crete_table)
            self.sqlite_connection.commit()
            print("Таблица User создана")
            cursor.close()
        except sqlite3.Error as _error:
            print("Ошибка при подключении к User SQL: ", _error)
        self.sqlite_connection.close()
        return None

    def create_key_table(self) -> None:
        """Создание таблицы Token"""

        try:
            cursor = self.sqlite_connection

            crete_table = '''
                CREATE TABLE IF NOT EXISTS Token (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    userid INTEGER NOT NULL,
                    number INTEGER DEFAULT 0, 
                    token TEXT NOT NULL UNIQUE,
                    FOREIGN KEY (userid)
                        REFERENCES User(id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                );
            '''

            cursor.execute(crete_table)
            self.sqlite_connection.commit()
            print("Таблица Token создана")

            cursor.close()
        except sqlite3.Error as _error:
            print("Ошибка при подключении к Token SQL: ", _error)
        self.sqlite_connection.close()
        return None

    def user_exists(self, user_name: str) -> bool:
        """Проверка на наличия пользователя с username"""

        try:
            cursor = self.sqlite_connection.cursor()

            if cursor.execute(
                    "SELECT 1 FROM User WHERE Username = ?", (user_name,)
            ).fetchone():
                cursor.close()
                return True
            cursor.close()
        except sqlite3.Error as _error:
            print("Ошибка при подключении к User SQL: ", _error)
        return False

    @staticmethod
    def get_user_id_by_username(cursor: sqlite3, user_name: str) -> int:
        """Получаем id пользователя"""
        get_user_id = cursor.execute(
            "SELECT id FROM User WHERE username=?",
            (user_name,)
        )

        for i in get_user_id:
            # Если пользователь существует, возвращаем его id
            return i[0]
        # Иначе это анонимный пользователь
        return 0

    @staticmethod
    def get_token_and_request_number_by_user_id(
            cursor: sqlite3, user_id: int
    ) -> tuple[str, int]:
        """Запрашиваем token и кол-во запросов пользователя"""

        user_token = cursor.execute(
            "SELECT token.token, token.number FROM User JOIN Token "
            "ON ? = Token.userid",
            (user_id,)
        )

        number, token = 0, ""

        for i in user_token:
            token = i[0]
            number = i[1]
            return token, number
        return token, number

    def increasing_number_requests(
            self, number: int, user_id: int
    ) -> bool:
        try:
            cursor = self.sqlite_connection

            cursor.execute(
                """Update Token set number = ? where id = ?""",
                (number, user_id)
            )

            self.sqlite_connection.commit()

            return True
        except Exception as _ex:
            print(f"Ошибка: {_ex}")
            return False

    def get_token_by_user_name(self, user_name: str) -> str:
        """Получаем Token пользователя"""
        cursor = self.sqlite_connection

        try:
            user_id: int = SQLConnect.get_user_id_by_username(
                cursor, user_name
            )

            if user_id == 0:
                user_id = SQLConnect.get_anonymous_id(cursor)

            token, number = SQLConnect.get_token_and_request_number_by_user_id(
                cursor, user_id
            )

            if SQLConnect().increasing_number_requests(number+1, user_id):
                return token
        except Exception as _ex:
            print(f"Ошибка: {_ex}")
        cursor.close()
        return str(os.getenv("API_KEY"))

    def close_sql_connection(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.sqlite_connection:
            self.sqlite_connection.close()

    @staticmethod
    def get_anonymous_id(cursor):
        try:
            anonymous_id = cursor.execute(
                "SELECT id FROM User WHERE username='anonymous'"
            )

            for i in anonymous_id:
                return i[0]
        except Exception as _ex:
            print(f"Ошибка: {_ex}")
        return 0

    def get_number_request_by_user_name(self, user_name: str):
        cursor = self.sqlite_connection

        try:
            user_id: int = SQLConnect.get_user_id_by_username(
                cursor, user_name
            )

            req_number = cursor.execute("""
                SELECT number FROM Token WHERE id = ?
            """, (user_id,)
            )

            for i in req_number:
                return i[0]
        except Exception as _ex:
            print(_ex)
        return 1
