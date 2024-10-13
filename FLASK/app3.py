import json, os
from flask import Flask, render_template, request  # request - глобальный словарь
from database.select import select_list, select_dict
from database.sql_provider import SQLProvider
from model_route import model_route


app = Flask(__name__)

#  f = open('../data/db_config.json')  # .. - поднялись на 2 дериктории выше
#  db_config = f.read()
#  print(db_config)
#  f.close()

with open('../data/db_config.json') as f:
    app.config['db_config'] = json.load(f)


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql')) # соединяем путь к текущей дериктории и sql шаблон


@app.route('/', methods=['GET'])
def product_handle():
    return render_template('input_category.html')


@app.route('/', methods=['POST'])
def product_result_handle():
    user_input_data = request.form
    user_info_result = model_route(app.config['db_config'], user_input_data, provider)  # содержит result error_mas status
    if user_info_result.status:
        products = user_info_result.result
        prod_title = 'Результат'
        return render_template('dynamic.html', prod_title=prod_title, products=products)
    else:
        return f"Что-то пошло не так: {user_info_result.error_massage}"


# @app.route('/', methods=['GET', 'POST'])  # в явном виде объявляем методы, т.к. по умолчанию только GET
# def product_index():
#     if request.method == 'GET':
#         return render_template('input_category.html')
#     else:
#         print(f"Received form data: {request.form}")
#         prod_category = request.form.get('prod_category')  # в request есть словать form, достаем из словаря prod_category
#         _sql = provider.get('product.sql', prod_category=prod_category)
#         products = select_dict(app.config['db_config'], _sql)
#         if products:
#             prod_title = 'Результат из БД'
#             return render_template('dynamic.html', prod_title=prod_title, products=products)
#         else:
#             return 'Результат не получен'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
