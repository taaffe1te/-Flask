from dataclasses import dataclass  # Импорт декоратора dataclass для создания классов данных
from database.select import select_list  # Импорт функции select_list для выполнения SQL-запросов


# Определение класса данных ProductInfoResponse
@dataclass
class ProductInfoResponse:
    result: tuple  # Кортеж с данными, полученными из базы данных
    error_massage: str  # Строка с сообщением об ошибке, если она возникла
    status: bool  # Булево значение, указывающее на успешность выполнения операции


# Функция model_route, которая выполняет запрос к базе данных
def model_route(db_config, user_input_data, sql_provider):
    error_massage = ''  # Инициализация переменной для сообщения об ошибке

    # Проверка, определена ли категория
    if 'prod_category' not in user_input_data or user_input_data['prod_category'] == "":
        print('user_input_data=', user_input_data)  # Вывод данных пользователя в консоль
        error_massage = 'Категория не найдена'  # Установка сообщения об ошибке
        result = ()  # Инициализация пустого кортежа для результата
        return ProductInfoResponse(result, error_massage=error_massage, status=False)  # Возврат объекта с ошибкой

    # Проверка, является ли категория числом
    elif user_input_data['prod_category'].isdigit() == False:
        print('user_input_data=', user_input_data)  # Вывод данных пользователя в консоль
        error_massage = 'Категория должна быть натуральным числом'  # Установка сообщения об ошибке
        result = ()  # Инициализация пустого кортежа для результата
        return ProductInfoResponse(result, error_massage=error_massage, status=False)  # Возврат объекта с ошибкой

    # Получение SQL-запроса
    _sql = sql_provider.get('product.sql', prod_category=user_input_data['prod_category'])
    print('_sql=', _sql)  # Вывод SQL-запроса в консоль

    # Выполнение SQL-запроса и получение результата и схемы
    result, schema = select_list(db_config, _sql)

    # Проверка, найдены ли данные по категории
    if result == -1:
        error_massage = f"Курсор не создан"  # Установка сообщения об ошибке
        return ProductInfoResponse(result, error_massage=error_massage, status=False)  # Возврат объекта с ошибкой
    if len(result) == 0:
        error_massage = f"данные по категории {user_input_data['prod_category']} не найдены"  # Установка сообщения об ошибке
        return ProductInfoResponse(result, error_massage=error_massage, status=False)  # Возврат объекта с ошибкой

    print(result)  # Вывод результата в консоль
    print(schema)  # Вывод схемы в консоль

    # Возврат объекта с результатом
    return ProductInfoResponse(result=result, error_massage=error_massage, status=True)