import sqlite3
from enum import Enum
from PyQt5.QtCore import QRect
import copy
from translate import Translator
from UserFunc import execute_user_func


class OperationCategory(Enum):
    ColumnOperation = 0
    CellOperation = 1
    OperationAsNewParam = 2


class ValueType(Enum):
    String = 0
    List = 1


class Operation:
    Type = 0
    SourceValueType = -1
    TargetValueType = -1

    def set_params(self, text, source_type, functional, target_type):
        self.text = text
        self.SourceValueType = source_type
        self.TargetValueType = target_type
        self.text_source = copy.copy(text)
        self.functional = functional
        self.ui = functional.ui

    def set_row(self, row_index):
        self.row_index = row_index

    def execute(self, value):
        pass

    # Set Condition Input Field interface
    @staticmethod
    def set_cif_interface(ui, typee, functional, last_zpo_operation_index):
        ui.conditionText.setEnabled(True)
        ui.comboBox_1.show()
        ui.conditionText.show()
        ui.conditionText.setGeometry(QRect(40, 100, 271, 200))
        ui.label_5.setGeometry(QRect(10, 10, 331, 81))
        ui.pushButton_10.setGeometry(QRect(40, 320, 120, 70))
        ui.comboBox_1.setGeometry(QRect(240, 347, 70, 22))
        ui.comboBox_1.setEnabled(True)
        ui.label_1.move(240, 325)
        source_type = 0 if last_zpo_operation_index < 0 else functional.zpo_order[last_zpo_operation_index].TargetValueType
        target_type = 0 if last_zpo_operation_index == len(functional.zpo_order) - 1 else \
            functional.zpo_order[last_zpo_operation_index + 1].TargetValueType
        if typee == 5:
            target_type = 0 if source_type == 1 else 1
        ui.label_1.setText(f'Исходный тип: {"String" if source_type == 0 else "List"}')
        ui.comboBox_1.setCurrentIndex(target_type)
        ui.label_4.move(240, 308)
        ui.label_4.setText(f'Тип операции: {typee}')
        ui.label_5.setText('')
        ui.conditionText.setText('')
        ui.pushButton_10.show()
        ui.pushButton_13.hide()
        text = '' if last_zpo_operation_index == len(functional.zpo_order) - 1 else functional.zpo_order[last_zpo_operation_index + 1].text
        text_exists = text != ''
        if text_exists:
            ui.conditionText.setEnabled(False)
        if typee == 1:
            ui.label_5.setText(
                'Введите sql-выражение. $value$ = значение ЗПО (без кавычек или как кортеж, элементы которого с кавычками. '
                'В зависимости от исходного типа значения).'
                '$row=this$ = индекс ряда без кавычек. Если ваше sql-выражение '
                'что-то возвращает, то это что-то будет преобразовано в List. Если ничего не возвращает, вернется текущее значение. '
                'Изменяя саму базу данных (UPDATE, SET, ALTER TABLE и т.д.), вы изменяйте ее)). '
                'Используйте оператор SELECT, чтобы вернуть новое значение ЗПО.')
            ui.conditionText.setText((f'SELECT * FROM {ui.comboBox.currentText()} WHERE title=' + "'$value$'") if not text_exists else text)
        elif typee == 2:
            ui.label_5.setText(
                'Напишите python-выражение. Ваш код выполняется в отдельной функции. Вам доступны все базовые модули python, включая random. '
                '$value$ = значение ЗПО в чистом виде. Если тип значения - строка, получите строку, иначе получите СПИСОК строк. '
                '$row=this$ = индекс ряда как int. $(первое число, второе число)$ = значение (str) элемента в таблице. '
                'Первое число - индекс ряда, второе - индекс колонны, они отсчитываются от нуля. Если ваше python-выражение '
                'что-то возвращает, то это что-то не будет преобразовано в String или List - вы должны сами написать '
                'преобразование значения в следующий тип. Если выражение ничего не возвращает или преобразованное '
                'значение не соответствует целевому типу, вернется текущее значение. '
                'Используйте оператор return, чтобы вернуть новое значение ЗПО.')
            ui.conditionText.setText('return $(3, 10)$' if not text_exists else text)
        elif typee == 3:
            ui.label_5.setText(
                'Напишите исходный язык значения ЗПО и язык, в который оно будет переведено, на английском языке. '
                'Названия языков писать полными, примеры приведены ниже. НЕ '
                'МЕНЯТЬ ПОРЯДОК НАПИСАНИЯ ИСХОДНОГО И ЦЕЛЕВОГО ЯЗЫКОВ (т.е. не менять слова Source и Target местами).'
                'Регулярные выражения отсутсвуют. Новое значение ЗПО отправляется автоматически.')
            ui.conditionText.setText('Source=English\nTarget=Russian' if not text_exists else text)
        elif typee == 4:
            ui.label_5.setText(
                'Напишите исходную систему счисления значения ЗПО и систему, в которую оно будет преобразовано.'
                'НЕ МЕНЯТЬ ПОРЯДОК НАПИСАНИЯ ИСХОДНОЙ И ЦЕЛЕВОЙ СИСТЕМ (т.е. не менять слова Source и Target местами).'
                'Регулярные выражения отсутсвуют. Новое значение ЗПО отправляется автоматически.')
            ui.conditionText.setText('Source=2\nTarget=16' if not text_exists else text)
        else:
            ui.label_5.setText(
                'Преобразует значение ЗПО в другой тип по-умолчанию: если исходный тип строковый, '
                'то значение преобразуется в список. Если же до этого тип были списком, '
                'то значение преобразуется в строку, элементы разделяются пробелами. '
                'Такое преобразование эквивалентно переводу значения из одного типа в другой в других операциях. '
                'Новое значение ЗПО отправляется автоматически.')
            ui.comboBox_1.setEnabled(False)
            ui.conditionText.hide()
            ui.pushButton_10.move(125, 150)

    @staticmethod
    def get_operation(typee):
        if typee == 1:
            return SQLExpression()
        elif typee == 2:
            return PythonExpression()
        elif typee == 3:
            return LanguageTranslation()
        elif typee == 4:
            return NotationEncoding()
        else:
            return TypeReplacement()


class SQLExpression(Operation):
    Type = 1

    def execute(self, value):
        con = sqlite3.connect(self.functional.path)
        res = con.cursor().execute(
            f"""
            {self.text.replace('$value$', (f'{value}' if self.SourceValueType == 0  else ('(' + ', '.join([f"'{i}'" for i in value]) + ')')))
                .replace('$row=this$', f'{self.row_index}')}
            """).fetchall()
        if res:
            con.close()
            print(f'sql{self.row_index}')
            if self.TargetValueType == 0:
                s = ' '.join(str(i[0]) for i in res)
                s1 = 6
                return s
            s = [str(i[0]) for i in res]
            s1 = str(res[0][0])
            s2 = res[0][0]
            return [str(i[0]) for i in res]
        else:
            con.commit()
            con.close()
        return value


class PythonExpression(Operation):
    Type = 2

    def execute(self, value):
        self.text = copy.copy(self.text_source)
        cell_defining = self.text.find('$(')
        while cell_defining != -1:
            cell = self.text[self.text.find('$('):self.text.index('$)') + 1]
            cell = [int(i) for i in cell.replace(' ', '').split(',')]
            self.text = self.text.replace(self.text[self.text.find('$('):self.text.index('$)') + 1],
                                          self.ui.tableWidget.item(cell[0], cell[1]).text())
            cell_defining = self.text.find('$(')
        self.text = 'import random\n\n\ndef execute_user_func():\n' + \
                    '\n'.join(['    ' + i for i in self.text.replace('$value$', f'{value}').replace('$row=this$', f'{self.row_index}').split('\n')])
        with open('UserFunc.py', 'w', encoding='utf8') as f:
            f.write(self.text)
        res = execute_user_func()
        print(f'py{self.row_index}')
        if res and ((self.TargetValueType == 0 and isinstance(res, str)) or (self.TargetValueType == 1 and isinstance(res, list))):
            return res
        return value


class LanguageTranslation(Operation):
    Type = 3

    def execute(self, value):
        self.text = copy.copy(self.text_source)
        self.text = self.text.replace(' ', '')\
            .lower()\
            .replace('source=', '')\
            .repalce('target=', '')\
            .split('\n')
        translator = Translator(from_lang=self.text[0], to_lang=self.text[1])
        if self.SourceValueType == 1 and self.TargetValueType == 1:
            return [translator.translate(i) for i in value]
        elif self.SourceValueType == 0 and self.TargetValueType == 1:
            return translator.translate(value).split()
        elif self.SourceValueType == 0 and self.TargetValueType == 0:
            return translator.translate(value)
        return ' '.join(translator.translate(i) for i in value)


class NotationEncoding(Operation):
    Type = 4

    def execute(self, value):
        self.text = copy.copy(self.text_source)
        self.text = [int(i) for i in self.text
            .replace(' ', '')
            .upper()
            .replace('SOURCE=', '')
            .replace('TARGET=', '')
            .split('\n')]
        if self.SourceValueType == 1 and self.TargetValueType == 1:
            return [self.convert_base(i, self.text[0], self.text[1]) for i in value]
        elif self.SourceValueType == 0 and self.TargetValueType == 1:
            return self.convert_base(value, self.text[0], self.text[1]).split()
        elif self.SourceValueType == 0 and self.TargetValueType == 0:
            return self.convert_base(value, self.text[0], self.text[1])
        return ' '.join(self.convert_base(i, self.text[0], self.text[1]) for i in value)

    def convert_base(self, num, from_base=10, to_base=10):
        # first convert to decimal number
        if isinstance(num, str):
            n = int(num, from_base)
        else:
            n = int(num)
        # now convert decimal to 'to_base' base
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < to_base:
            return alphabet[n]
        else:
            return self.convert_base(n // to_base, to_base) + alphabet[n % to_base]


class TypeReplacement(Operation):
    Type = 5

    def execute(self, value):
        if self.SourceValueType == 0:
            return value.split()
        return ' '.join(value)
