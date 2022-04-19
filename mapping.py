class Mapping:
    """
    Конструктор принимает схему-словарь для связи csv строк
    и json объектов.

    Каждая пара "ключ-значение" в схеме описывает связь между
    полем JSON-объекта и значением/значениями из таблицы.

    Ключ словаря определяет название поля в JSON-объекте.
    Допустимые ключи:
     *  **строка** - название одновременно для поля JSON-объекта и
        для связанного столбца в таблице.
     *  **кортеж** - должен содержать две строки: первая - название
        столбца таблицы, вторая - тип данных.

    Значением (**value**) ключа словаря может быть **строка**, **список**,
    **словарь** и **кортеж**.

    **value**-**строка** (допустимый ключ - **строка**)
    Если **value** - строка, то она определяет тип, к которому нужно
    преобразовать данные из столбца таблицы.

    **value**-**список** (допустимый ключ - **строка**)
    Может быть двух видов:
     *  ['**int**'] - список содержит единственный элемент-строку,
        которая определяет тип данных значений списка. Значения
        должны быть перечислены в ячейке таблицы через запятую.
     *  [('name', '**str**'), ('age', '**int**')] - список содержит один
        или несколько кортежей (название столбца, тип данных).
        Данные будут взяты из соответствующих столбцов таблицы,
        преобразованы к указанным типам и помещены в список.

    **value**-**кортеж** (допустимый ключ - **кортеж**)
    Тоже должен содержать 2 строки - название столбца и тип
    данных. Пара "ключ-кортеж: строка-кортеж" связывает два
    столбца в таблице. Полем JSON-объекта будет значение из
    первого столбца таблицы, а значением JSON-объекта - значение
    из второго столбца.

    **value**-**словарь** (допустимый ключ - **строка**)
    Служит для описания вложенного JSON-объекта. Ключи и значения
    такого словаря должны соответствовать условиям, описанным выше.

    """

    def __init__(self, schema: dict):
        self.__validate_schema(schema)
        fields = self.__extract_fields(schema)
        if len(fields) != len(set(fields)):
            raise ValueError('Заголовок таблицы не может содержать одинаковые поля!')
        self.__schema = schema
        self.__table_fields = fields

    def __validate_schema(self, schema: dict):
        if not isinstance(schema, dict):
            raise TypeError('Неверный тип, ожидался словарь')

        for k, v in zip(schema.keys(), schema.values()):
            if isinstance(k, tuple) or isinstance(v, tuple):
                self.__validate_tuple(k)
                self.__validate_tuple(v)
                continue
            self.__validate_name(k)
            self.__validate_value(v)

    def __validate_value(self, v):
        {
            str: self.__validate_type,
            list: self.__validate_list,
            dict: self.__validate_schema,
        }[type(v)](v)

    @staticmethod
    def __validate_name(s: str):
        if not isinstance(s, str):
            raise TypeError('Название столбца должно быть строкой')
        if s == '' or s.isspace() or not s.isprintable():
            raise ValueError('Недопустимое название столбца')

    @staticmethod
    def __validate_type(s: str):
        if not isinstance(s, str):
            raise TypeError('Название типа должно быть строкой')
        if s not in ('int', 'float', 'str', 'bool'):
            raise ValueError('Недопустимое название типа')

    def __validate_tuple(self, t: tuple):
        if not isinstance(t, tuple):
            raise TypeError('Неверный тип, ожидался кортеж')
        name, type_of = t
        self.__validate_name(name)
        self.__validate_type(type_of)

    def __validate_list(self, lst: list):
        if not isinstance(lst, list):
            raise TypeError('Неверный тип, ожидался список')
        if len(lst) == 0:
            raise ValueError('Слишком короткий список')
        if len(lst) == 1 and isinstance(lst[0], str):
            self.__validate_type(lst[0])
            return
        if all([(isinstance(x, tuple) and len(x) == 2) for x in lst]):
            for tpl in lst:
                self.__validate_tuple(tpl)

    def __convert(self, to: str, val):

        def to_bool(x):
            try:
                return int(x) != 0
            except ValueError:
                return False

        self.__validate_type(to)
        return {
            'int': lambda x: int(x),
            'float': lambda x: float(x),
            'str': lambda x: str(x),
            'bool': lambda x: to_bool(x)
        }[to](val)

    def __extract_fields(self, schema: dict):
        fields = []
        for k, v in zip(schema.keys(),
                        schema.values()):

            if isinstance(k, tuple) and isinstance(v, tuple):
                fields.append(k[0])
                fields.append(v[0])
                continue

            if isinstance(v, str):
                fields.append(k)
                continue

            if isinstance(v, dict):
                fields.extend(self.__extract_fields(v))
                continue

            if isinstance(v, list):
                if len(v) == 1 and isinstance(v[0], str):
                    fields.append(k)
                    continue
                fields.extend([field[0] for field in v])
                continue

        return fields

    @property
    def table_fields(self):
        return self.__table_fields

    def row_to_dict(self, row: dict):
        fields = set(list(row.keys()))
        if set(self.__table_fields) != fields:
            raise ValueError('Поля не совпадают!')
        return self.__create_structure(self.__schema, row)

    def __create_structure(self, schema: dict,  row: dict):
        struct = dict()
        for k, v in zip(schema.keys(),
                        schema.values()):

            if isinstance(k, str) and isinstance(v, str):
                struct[k] = self.__convert(v, row[k])

            if isinstance(k, str) and isinstance(v, dict):
                struct[k] = self.__create_structure(v, row)

            if isinstance(k, tuple) and isinstance(v, tuple):
                left = self.__convert(k[1], row[k[0]])
                right = self.__convert(v[1], row[v[0]])
                struct[left] = right

            if isinstance(k, str) and isinstance(v, list):
                if len(v) == 1 and isinstance(v[0], str):
                    struct[k] = [self.__convert(v[0], x) for x in str(row[k]).split(',')]
                elif all([(isinstance(x, tuple) and len(x) == 2) for x in v]):
                    struct[k] = [self.__convert(x[1], row[x[0]]) for x in v]

        return struct
