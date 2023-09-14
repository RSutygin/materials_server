from connect_sql import connect_to_database
import os
from dotenv import load_dotenv


load_dotenv('config.env')
table = os.getenv('TABLE_SQL')


def get_list_material():  # get all material names for combobox in client program
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            material_list = ''
            cursor.execute(f"SELECT name "
                           f"FROM {table}")
            temp = cursor.fetchall()
            for i in temp:
                material_list += str(i[0]) + ' '
        conn.close()

        return material_list

    else:
        return 'Нет соединения, невозможно получить список материалов'


def remains():  # get all remains
    conn = connect_to_database()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT name, lot "
                           f"FROM {table}")
            remain_list = cursor.fetchall()
            answer = ''
            for remain in remain_list:
                answer += str(remain[0]) + ': ' + str(remain[1]) + '\n'
            print(answer)
        conn.close()

        return answer

    else:
        return 'Нет соединения, невозможно узнать остатки!'


class Actions:  # this class contains all the actions with one material name
    def __init__(self, name, lot, action):
        self.material_name = name
        self.material_lot = lot
        self.action = action
        self.conn = connect_to_database()

        self.methods = {'Expenses': ExpensesClass.expenses,
                        'Coming': ComingClass.coming,
                        'Remain': RemainClass.remain,
                        'Add_material': AddMaterialClass.add_material,
                        'Delete_material': DeleteMaterialClass.delete_material}

    def run_method(self):  # launching the required action
        return self.methods[self.action](self)


class ExpensesClass(Actions):
    def expenses(self):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(f"SELECT lot "
                                   f"FROM {table} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    lot = cursor.fetchall()
                    new_lot = lot[0][0] - float(self.material_lot)
                    cursor.execute(f"UPDATE {table} SET lot = {new_lot} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    self.conn.commit()

                return f'Материал {self.material_name} расходован в количестве {self.material_lot} единиц.\n' \
                       f'Остаток: {new_lot} единиц'

            except IndexError:
                return 'Выберите материал!'

        else:
            return f'Нет соединения, материал {self.material_name} не расходован'


class ComingClass(Actions):
    def coming(self):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(f"SELECT lot "
                                   f"FROM {table} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    lot = cursor.fetchall()
                    new_lot = lot[0][0] + float(self.material_lot)
                    cursor.execute(f"UPDATE {table} SET lot = {new_lot} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    self.conn.commit()

                return f'Материал {self.material_name} оприходован в количестве {self.material_lot} единиц.\n' \
                       f'Остаток: {new_lot} единиц'

            except IndexError:
                return 'Выберите материал!'

        else:
            return f'Нет соединения, материал {self.material_name} не оприходован'


class RemainClass(Actions):
    def remain(self):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(f"SELECT lot "
                                   f"FROM {table} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    lot = cursor.fetchall()

                return f"Остаток материала {self.material_name} составляет:\n{lot[0][0]} единиц"

            except IndexError:
                return 'Выберите материал!'

        else:
            return f'Нет соединения, невозможно узнать остаток материала {self.material_name}!'


class AddMaterialClass(Actions):
    def add_material(self):
        if self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(f"INSERT INTO {table} (name, lot) "
                               f"VALUES ('{str(self.material_name)}', {float(self.material_lot)})")
                self.conn.commit()

            return f'Материал {self.material_name} добавлен!'

        else:
            return 'Нет соединения, материал не добавлен!'


class DeleteMaterialClass(Actions):
    def delete_material(self):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(f"DELETE "
                                   f"FROM {table} "
                                   f"WHERE name = '{str(self.material_name)}'")
                    self.conn.commit()

                return f'Материал {self.material_name} удален!'

            except IndexError:
                return 'Выберите материал!'

        else:
            return 'Нет соединения, материал не удален!'
