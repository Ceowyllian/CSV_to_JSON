class Mapping:

    def __init__(self, schema: dict):
        self.__validate_structure(schema)
        fields = self.__extract_fields(schema)
        if len(fields) != len(set(fields)):
            raise ValueError('Заголовок таблицы не может содержать одинаковые поля!')
        self.__struct = schema
        self.__table_fields = fields

    def __validate_structure(self, obj: dict):
        if not isinstance(obj, dict):
            raise TypeError('Неверный тип, ожидался словарь')

        for k, v in zip(obj.keys(), obj.values()):
            if not (isinstance(v, tuple) and isinstance(k, tuple)):
                if isinstance(v, tuple) or isinstance(k, tuple):
                    raise ValueError('Ключ и значение должны быть кортежами одновременно')
            self.__validate_key(k)
            self.__validate_value(v)

    @staticmethod
    def __validate_type(s: str):
        if not isinstance(s, str):
            raise TypeError('Название типа должно быть строкой')
        if s not in ('int', 'float', 'str', 'bool'):
            raise ValueError('Недопустимое название типа')

    @staticmethod
    def __validate_name(s: str):
        if not isinstance(s, str):
            raise TypeError('Название столбца должно быть строкой')
        if s == '' or s.isspace() or not s.isprintable():
            raise ValueError('Недопустимое название столбца')

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

    def __validate_tuple(self, t: tuple):
        if not isinstance(t, tuple):
            raise TypeError('Неверный тип, ожидался кортеж')
        name, type_of = t
        self.__validate_name(name)
        self.__validate_type(type_of)

    def __validate_key(self, k):
        if isinstance(k, str):
            self.__validate_name(k)
            return
        if isinstance(k, tuple):
            name, type_of = k
            self.__validate_name(name)
            self.__validate_type(type_of)
            return
        raise TypeError('Неверный тип, ожидалась строка или кортеж')

    def __validate_value(self, v):
        {
            str: self.__validate_type,
            list: self.__validate_list,
            tuple: self.__validate_tuple,
            dict: self.__validate_structure,
        }[type(v)](v)

    def __extract_fields(self, mapping: dict):
        fields = []
        for k, v in zip(mapping.keys(),
                        mapping.values()):
            if isinstance(k, str) and isinstance(v, str):
                fields.append(k)
                continue
            if isinstance(k, str) and isinstance(v, dict):
                fields.extend(self.__extract_fields(v))
                continue
            if isinstance(k, tuple) and isinstance(v, tuple):
                fields.append(k[0])
                fields.append(v[0])
                continue
            if isinstance(k, str) and isinstance(v, list):
                if len(v) == 1 and isinstance(v[0], str):
                    fields.append(k)
                    continue
                elif all([isinstance(x, tuple) for x in v]):
                    fields.extend([field[0] for field in v])
                    continue

        return fields

    def table_fields(self):
        return self.__table_fields

    def row_to_dict(self, row: dict):
        fields = list(row.keys())
        if set(self.__table_fields) != set(fields):
            raise ValueError('Поля не совпадают!')
        struct = self.__create_structure(self.__struct, row)
        return struct

    @staticmethod
    def __convert(to: str, val):
        return {
                'int': lambda x: int(x),
                'float': lambda x: float(str(x).replace(',', '.')),
                'str': lambda x: str(x),
                'bool': lambda x: bool(x)
                }[to](val)

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
