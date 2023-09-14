from connect_sql import connect_to_database
from config import table_sql


def get_list_material():
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            material_list = ''
            cursor.execute(f"SELECT name "
                           f"FROM {table_sql}")
            temp = cursor.fetchall()
            for i in temp:
                material_list += str(i[0]) + ' '
            print('Список материалов: ', material_list)
        conn.close()
        return material_list
    else:
        print('Нет соединения, невозможно получить список материалов')
        return 'Нет соединения, невозможно получить список материалов'


def new_object(list_material):
    name, lot, act = list_material
    obj = MaterialsFunction(name, float(lot), act)
    if obj.action == 'add':
        return obj.add_material()
    elif obj.action == 'del':
        return obj.del_material()
    elif obj.action == 'remain_one':
        return obj.remain_material()
    elif obj.action == 'expenses':
        return obj.expenses()
    elif obj.action == 'coming':
        return obj.coming()


def remains():
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT name, lot "
                           f"FROM {table_sql}")
            remain_list = cursor.fetchall()
            answer = ''
            for remain in remain_list:
                answer += str(remain[0]) + ': ' + str(remain[1]) + '\n'
            print(answer)
        conn.close()
        return answer
    else:
        print('Нет соединения, невозможно узнать остатки!')
        return 'Нет соединения, невозможно узнать остатки!'


class MaterialsFunction:
    def __init__(self, material_name, material_lot, action):
        self.material_name = material_name
        self.material_lot = material_lot
        self.action = action

    def add_material(self):
        conn = connect_to_database()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute(f"INSERT INTO {table_sql} (name, lot) "
                               f"VALUES ('{str(self.material_name)}', {float(self.material_lot)})")
                conn.commit()

            conn.close()
            print(f'Материал {self.material_name} добавлен!')
            return f'Материал {self.material_name} добавлен!'
        else:
            print('Нет соединения, материал не добавлен!')
            return 'Нет соединения, материал не добавлен!'

    def del_material(self):
        conn = connect_to_database()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"DELETE "
                                   f"FROM {table_sql} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    conn.commit()
                    print(f'Материал {self.material_name} удален!')
                conn.close()
                return f'Материал {self.material_name} удален!'
            except:
                print('Материал не выбран')
                return 'Выберите материал!'
        else:
            print('Нет соединения, материал не удален!')
            return 'Нет соединения, материал не удален!'

    def remain_material(self):
        conn = connect_to_database()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT lot "
                                   f"FROM {table_sql} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    lot = cursor.fetchall()
                    print(f"Остаток материала {self.material_name} составляет:\n"
                          f"{lot[0][0]} единиц")
                conn.close()
                return f"Остаток материала {self.material_name} составляет:\n{lot[0][0]} единиц"
            except:
                print('Материал не выбран')
                return 'Выберите материал!'
        else:
            print(f'Нет соединения, невозможно узнать остаток материала {self.material_name}!')
            return f'Нет соединения, невозможно узнать остаток материала {self.material_name}!'

    def expenses(self):
        conn = connect_to_database()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT lot "
                                   f"FROM {table_sql} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    lot = cursor.fetchall()
                    new_lot = lot[0][0] - self.material_lot
                    cursor.execute(f"UPDATE {table_sql} SET lot = {new_lot} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    conn.commit()
                    print(f'Материал {self.material_name} расходован в количестве '
                          f'{self.material_lot} единиц. Остаток: {new_lot} единиц')
                conn.close()
                return f'Материал {self.material_name} расходован в количестве {self.material_lot} единиц.\n' \
                       f'Остаток: {new_lot} единиц'
            except:
                print('Материал не выбран')
                return 'Выберите материал!'
        else:
            print(f'Нет соединения, материал {self.material_name} не расходован')
            return f'Нет соединения, материал {self.material_name} не расходован'

    def coming(self):
        conn = connect_to_database()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT lot "
                                   f"FROM {table_sql} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    lot = cursor.fetchall()
                    new_lot = lot[0][0] + self.material_lot
                    cursor.execute(f"UPDATE {table_sql} SET lot = {new_lot} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    conn.commit()
                    print(f'Материал {self.material_name} оприходован в количестве '
                          f'{self.material_lot} единиц. Остаток: {new_lot} единиц')
                conn.close()
                return f'Материал {self.material_name} оприходован в количестве {self.material_lot} единиц.\n' \
                       f'Остаток: {new_lot} единиц'
            except:
                print('Материал не выбран')
                return 'Выберите материал!'
        else:
            print(f'Нет соединения, материал {self.material_name} не оприходован')
            return f'Нет соединения, материал {self.material_name} не оприходован'
