import parser

# Схемы

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
jsonname = 'specialty.json'
csvname = 'specialty.csv'
schema = specialty

csvpath = fr'C:\myfiles\{csvname}'
jsonpath = fr'C:\myfiles\json\{jsonname}'

# Преобразовать таблицу в список JSON-объектов
parser.csv_to_json(csvpath, jsonpath, schema)

# Создать таблицу с нужным заголовком для для схемы
# parser.create_table(csvpath, schema)
