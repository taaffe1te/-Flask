from pymysql import connect
from pymysql.err import OperationalError  #объект куда mysql поместит сообщ об ошибке если возникнет

class DBContextManager:

    def __init__(self, db_config: dict):
        self.conn = None        #трибут для хранения подключения к базе данных
        self.cursor = None      #атрибут для хранения курсора базы данных
        self.config = db_config     #Сохраняет переданную конфигурацию базы данных в атрибут config

    def __enter__(self):        # спец. метод, кот-ый вызывается при входе в блок with; возвр. объект, кот-й будет исп-ся внутри блока with
        try:        #для перехвата исключений
            self.conn = connect(**self.config)  #** - разбор именованных параметров на отдельные части
            self.cursor = self.conn.cursor()    #
            return self.cursor
        except OperationalError as err:
            print(f"Ошибка подключения к базе данных: {err}")
            print(err.args)    # код ошибки + пояснение;  сам-но - обработка ошибок для каждой свой вывод?
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type: #тип исключения
            print(exc_type)
            print(exc_val)
        if self.cursor:
            if exc_type:       #обЪект исключения
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return True               # тк всё предусмотрели


#контекстный менеджер для управления соединением с базой данных