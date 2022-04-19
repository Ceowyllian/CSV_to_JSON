import parser


"""
Схемы для связи csv строк и json объектов

Каждая пара "ключ-значение" в словаре описывает связь между
полем JSON-объекта и значением/значениями из таблицы.

Ключ словаря определяет название поля в JSON-объекте.
Допустимые ключи:
 *  строка - название одновременно для поля JSON-объекта и 
    для связанного столбца в таблице.
 *  кортеж - должен содержать две строки: первая - название
    столбца таблицы, вторая - тип данных.

Значением (value) ключа словаря может быть строка, список, 
словарь и кортеж.

value-строка (допустимый ключ - строка)
Если value - строка, то она определяет тип, к которому нужно
преобразовать данные из столбца таблицы.

value-список (допустимый ключ - строка)
Может быть двух видов:
 *  ['int'] - список содержит единственный элемент-строку,
    которая определяет тип данных значений списка. Значения
    должны быть перечислены в ячейке таблицы через запятую.
 *  [('name', 'str'), ('age', 'int')] - список содержит один
    или несколько кортежей (название столбца, тип данных).
    Данные будут взяты из соответствующих столбцов таблицы,
    преобразованы к указанным типам и помещены в список. 

value-кортеж (допустимый ключ - кортеж)
Тоже должен содержать 2 строки - название столбца и тип
данных. Пара "ключ-кортеж: строка-кортеж" связывает два 
столбца в таблице. Полем JSON-объекта будет значение из 
первого столбца таблицы, а значением JSON-объекта - значение
из второго столбца.

value-словарь (допустимый ключ - строка)
Служит для описания вложенного JSON-объекта. Ключи и значения
такого словаря должны соответствовать условиям, описанным выше.

"""


specialty = {
    'code': 'str',
    'name': 'str',
    'desc': 'str',
    'exams': {
        ('exam1', 'str'): ('mark1', 'int'),
        ('exam2', 'str'): ('mark2', 'int'),
        ('exam3', 'str'): ('mark3', 'int'),
    }
}

product = {
    'name': 'str',
    'category': 'str',
    'cost': 'float',
    'amount': 'int',
    'weight': 'int',
    'storage': 'int',
    'manufacturer': 'str'
}

film = {
    'name': 'str',
    'duration (min)': 'int',
    'date': 'str',
    'producer': 'str',
    'actors': ['str'],
    'price': 'float'
}

book = {
    'title': 'str',
    'amount': 'int',
    'price': 'float',
    'authors': ['str'],
    'ISBN': 'str',
    'publisher': 'str',
    'year': 'int'
}

deposit = {
    'id': 'int',
    'balance': 'float',  # так делать нельзя, но ладно
    'currency': 'str',
    'term': 'int',
    'interest rate': 'int'
}

tariff = {
    'name': 'str',
    'monthly cost': 'float',
    'traffic (Gb)': 'float',
    'minutes': 'int'
}

fitness = {
    'type': 'str',
    'cost': 'float',
    'number of visits': 'int',
    'starts': 'str',
    'ends': 'str'
}

apartment = {
    'address': 'str',
    'number of rooms': 'int',
    'area (sq. m)': 'float',
    'floor': 'int',
    'price': 'float',
    'balcony': 'bool',
    'lift': 'bool'
}

smartphone = {
    'model': 'str',
    'cost': 'float',
    'amount': 'int',
    'manufacturer': 'str',
    'memory size (Gb)': 'float',
    'diagonal (inch)': 'float',
    'camera (mpx)': 'float'
}

ticket = {
    'name': 'str',
    'type': 'str',
    'cost': 'float',
    'term (mon)': 'int'
}

# Здесь можно указать названия и расположение файлов, а также выбрать схему
jsonname = 'test.json'
csvname = 'test.csv'
schema = specialty

csvpath = fr'C:\myfiles\{csvname}'
jsonpath = fr'C:\myfiles\json\{jsonname}'

print(bool(-1))

# Преобразовать таблицу в список JSON-объектов
# parser.csv_to_json(csvpath, jsonpath, schema)

# Создать таблицу с нужным заголовком для для схемы
# parser.create_table(csvpath, schema)
