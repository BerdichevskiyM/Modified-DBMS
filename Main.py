import sys
import sqlite3
import copy
from Operations import OperationCategory, Operation, ValueType
from UI import UIC
from PyQt5.QtWidgets import QApplication, \
    QTableWidgetItem, QFileDialog, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class Functional:
    def __init__(self):
        self.ui = UIC(self)
        self.changingDBUISqlFieldIsEnabled = False
        self.ui.pushButton.clicked.connect(self.load_changing_dbui)
        self.ui.pushButton_3.clicked.connect(self.load_file)
        self.ui.pushButton_2.clicked.connect(self.change_changing_dbui)
        self.ui.pushButton_4.clicked.connect(self.enable_changing_dbui_sql_field)
        self.ui.comboBox.currentTextChanged.connect(lambda: self.change_table(True))
        self.ui.tableWidget.currentItemChanged.connect(lambda: self.ui.pushButton_2.setEnabled(True))
        self.ui.pushButton_9.clicked.connect(self.delete_new_params)
        self.ui.pushButton_10.clicked.connect(self.add_zpo_operation)
        self.ui.pushButton_13.clicked.connect(self.delete_zpo_operation)
        self.ui.pushButton_12.clicked.connect(self.select_zpo_items)
        self.ui.tableWidget.cellPressed.connect(self.select_param)
        self.ui.pushButton_1.clicked.connect(lambda: self.select_operation(OperationCategory.ColumnOperation))
        self.ui.pushButton_5.clicked.connect(lambda: self.select_operation(OperationCategory.CellOperation))
        self.ui.pushButton_8.clicked.connect(lambda: self.select_operation(OperationCategory.OperationAsNewParam))
        self.ui.pushButton_14.clicked.connect(self.execute_zpo)
        self.columns = []
        self.zpo_order = []
        self.zpo_buttons = []
        self.new_params = [3]
        self.showedZPOOperation = -1
        self.selectedZPOItems = []
        self.mayDeleteParams = False
        self.maySelectParams = False
        self.zpo_items_are_selected = False
        self.cur_operation_type = OperationCategory.ColumnOperation
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(1)
        self.ui.tableWidget.setHorizontalHeaderLabels(['tt'])
        self.default_header_background = self.ui.tableWidget.horizontalHeaderItem(0).background()
        self.ui.tableWidget.setColumnCount(0)
        self.ui.tableWidget.setRowCount(0)
        self.load_file()

    def load_file(self):
        self.path = QFileDialog.getOpenFileName(self.ui, 'Выберите БД', '', '(*.sqlite)')[0]
        self.fileName = self.path.split("/")[-1][:-len(self.path.split('.')[-1]) - 1]
        self.ui.disableUI()
        if self.path == '':
            self.ui.pushButton_4.setEnabled(False)
            self.ui.back.setEnabled(False)
            self.ui.forward.setEnabled(False)
            self.ui.pushButton_1.setEnabled(False)
            self.ui.pushButton_5.setEnabled(False)
            self.ui.pushButton_8.setEnabled(False)
        else:
            self.ui.enableUI()
            con = sqlite3.connect(self.path)
            [self.ui.comboBox.addItem(i[0]) for i in con.cursor().execute(
                """
                SELECT name FROM sqlite_master WHERE type = "table"
                """).fetchall()[1:]]
            self.change_table(True, con)

    def load_changing_dbui(self):
        con = sqlite3.connect(self.path)
        current_table_name = self.ui.comboBox.currentText()
        self.columns.insert(0, 'rowid')
        result = []
        if self.changingDBUISqlFieldIsEnabled:
            command = self.ui.commandToChange.toPlainText()
            if command[:6] == 'SELECT' and 'rowid' not in command[:command.index('FROM')]:
                command = command.lstrip('SELECT').lstrip()
                command = f'SELECT rowid, ' + command
            if command[:6] == 'SELECT':
                self.columns = command[7:command.index('FROM') - 1]\
                    .replace(' ', '')\
                    .split(',')
                if self.columns.count('*') > 0:
                    index = self.columns.index('*')
                    self.columns.remove('*')
                    for i in self.get_columns_from_sql_table(con, current_table_name):
                        self.columns.insert(index, i)
                        index += 1
            result = con.cursor().execute(f"""
                    {command}
                    """).fetchall()
            con.commit()
        else:
            result = con.cursor().execute(f"""
            SELECT rowid, * FROM {current_table_name}
            WHERE {self.ui.commandToChange.toPlainText()}""").fetchall()
        if len(result) != 0:
            self.ui.tableWidget.setColumnCount(len(self.columns))
            self.ui.tableWidget.setRowCount(len(result))
            self.ui.tableWidget.setHorizontalHeaderLabels(self.columns)
        for i in range(len(result)):
            for j in range(len(result[0])):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(f'{result[i][j]}'))
                if j == 0:
                    self.ui.tableWidget.item(i, j).setFlags(Qt.ItemIsEditable)
        self.ui.tableWidget.resizeColumnsToContents()
        self.columns = self.get_columns_from_sql_table(con, current_table_name)
        con.close()

    def change_changing_dbui(self):
        self.ui.pushButton_2.setEnabled(False)
        con = sqlite3.connect(self.path)
        columns = [i for i in range(self.ui.tableWidget.columnCount())][1:]
        for i in range(self.ui.tableWidget.rowCount()):
            changing_note = ', '.join([f"{self.ui.tableWidget.horizontalHeaderItem(i1).text()}"
                                       f"='{self.ui.tableWidget.item(i, i1).text()}'" for i1 in columns])
            con.cursor().execute(f"""
                            UPDATE {self.ui.comboBox.currentText()}
                            SET {changing_note}
                            WHERE rowid = {self.ui.tableWidget.item(i, 0).text()}
                            """)
            con.commit()
        con.close()

    @staticmethod
    def get_columns_from_sql_table(sql_connect, table_name):
        return [i[0] for i in sql_connect.cursor().execute(
                f"""
                SELECT name FROM PRAGMA_TABLE_INFO('{table_name}')
                """).fetchall()]

    def enable_changing_dbui_sql_field(self):
        if self.changingDBUISqlFieldIsEnabled:
            self.ui.pushButton_4.setText('Включить поле\nдля введения SQL-команд')
            self.ui.textEdit.setText('Введите SQL-условное выражение, чтобы найти соответствующие ему ряды:')
            self.changingDBUISqlFieldIsEnabled = False
            self.ui.commandToChange.setText('')
        else:
            self.ui.pushButton_4.setText('Включить поле\nдля введения условных SQL-выражений')
            self.ui.textEdit.setText('Введите SQL-команду для базы данных:')
            self.changingDBUISqlFieldIsEnabled = True
            self.ui.set_default_text(self.ui.commandToChange)

    def change_table(self, close_con, con=None):
        self.ui.set_default_text(self.ui.commandToChange)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        con = con if con else sqlite3.connect(self.path)
        self.columns = self.get_columns_from_sql_table(con, self.ui.comboBox.currentText())
        if close_con:
            con.close()

    def delete_new_params(self):
        if not self.mayDeleteParams:
            self.ui.comboBox.setEnabled(False)
            self.ui.pushButton_9.setText('Готово')
            self.ui.pushButton_9.resize(81, 31)
            for i in range(self.ui.tableWidget.columnCount()):
                if i not in self.new_params:
                    self.ui.tableWidget.horizontalHeaderItem(i).setBackground(QColor(0, 100, 50))
            self.mayDeleteParams = True
        else:
            self.ui.comboBox.setEnabled(True)
            self.ui.pushButton_9.setText('Удалить выбранные параметры')
            self.ui.pushButton_9.resize(self.ui.pushButton_9.sizeHint())
            self.ui.pushButton_9.resize(self.ui.pushButton_9.width(), self.ui.pushButton_9.height() + 8)
            deleted_params = []
            for i in range(self.ui.tableWidget.columnCount()):
                if i not in self.new_params:
                    self.ui.tableWidget.horizontalHeaderItem(i).setBackground(self.default_header_background)
                elif self.ui.tableWidget.horizontalHeaderItem(i).background().color() == QColor(255, 0, 0):
                    self.ui.tableWidget.removeColumn(i)
                    deleted_params.append(i)
            for i in deleted_params:
                self.new_params.remove(i)
            self.mayDeleteParams = False

    def select_param(self):
        col = self.ui.tableWidget.selectionModel().selectedColumns()
        if col and col[0].column() == 0:
            col = None
        if col and self.mayDeleteParams and col[0].column() in self.new_params:
            self.ui.tableWidget.horizontalHeaderItem(col[0].column()) \
                .setBackground(QColor(255, 0, 0) if self.ui.tableWidget.horizontalHeaderItem(col[0].column())
                               .background() == self.default_header_background else self.default_header_background)
        elif col and self.maySelectParams:
            def add_zpo_item(item, background_item, default_back):
                if background_item.background() == default_back:
                    self.selectedZPOItems.append(item)
                    background_item.setBackground(QColor(0, 255, 0))
                else:
                    self.selectedZPOItems.remove(item)
                    background_item.setBackground(default_back)

            if self.cur_operation_type.value == 0:
                add_zpo_item(col[0].column(), self.ui.tableWidget.horizontalHeaderItem(col[0].column()), self.default_header_background)
            elif col:
                add_zpo_item((col[0].row(), col[0].column()), self.ui.tableWidget.item(col[0].row(), col[0].column()), None)
        self.ui.tableWidget.selectionModel().clear()

    def select_operation(self, operation_type):
        self.ui.comboBox.setEnabled(False)
        self.zpo_items_are_selected = False
        if self.cur_operation_type.value == OperationCategory.ColumnOperation:
            for i in self.selectedZPOItems:
                self.ui.tableWidget.horizontalHeaderItem(i).setBackground(self.default_header_background)
        elif self.cur_operation_type.value == OperationCategory.CellOperation:
            for i in self.selectedZPOItems:
                self.ui.tableWidget.item(i[0], i[1]).setBackground(self.default_header_background)
        self.cur_operation_type = operation_type
        self.selectedZPOItems.clear()
        if operation_type.value == 0 or operation_type.value == 1:
            self.maySelectParams = True
        else:
            self.maySelectParams = False
            self.select_zpo_items()
        self.mayDeleteParams = False
        self.ui.pushButton_9.setText('Удалить выбранные параметры')
        self.ui.pushButton_9.resize(self.ui.pushButton_9.sizeHint())
        self.ui.pushButton_9.resize(self.ui.pushButton_9.width(), self.ui.pushButton_9.height() + 8)
        self.ui.pushButton_9.hide()
        self.ui.pushButton_12.show()

    def select_zpo_items(self):
        if len(self.selectedZPOItems) == 0:
            self.ui.pushButton_12.hide()
            self.ui.pushButton_9.show()
        else:
            if self.cur_operation_type == 2:
                self.ui.openCloseSettings()
            self.ui.openCloseWidget(self.ui.ConditionArea)
            self.zpo_items_are_selected = True
        self.mayDeleteParams = True
        self.ui.comboBox.setEnabled(True)

    def add_zpo_operation(self):
        source_zpo_type = 0
        if self.zpo_order:
            source_zpo_type = self.zpo_order[-1].TargetValueType
        operation = Operation.get_operation(int(self.ui.label_4.text()[-1]))
        operation.set_params(self.ui.conditionText.toPlainText(),
                                        source_zpo_type,
                                        self,
                                        self.get_zpo_type(self.ui.comboBox_1.currentText()))
        self.zpo_order.append(operation)
        zpo_button = QPushButton(self.ui.verticalLayoutWidget_3)
        zpo_button.resize(30, 30)
        zpo_button.setText(f'{self.ui.label_4.text()[-1]}')
        zpo_button.clicked.connect(lambda: self.show_zpo_operation(operation))
        self.ui.widgetLayout.addWidget(zpo_button)
        self.zpo_buttons.append(zpo_button)

    def show_zpo_operation(self, operation):
        self.showedZPOOperation = self.zpo_order.index(operation)
        Operation.set_cif_interface(self.ui, operation.Type, self, self.showedZPOOperation - 1)
        self.ui.pushButton_13.show()
        self.ui.pushButton_10.hide()
        self.ui.comboBox_1.setEnabled(False)
        self.ui.openCloseWidget(self.ui.ConditionInputField)

    def delete_zpo_operation(self):
        self.zpo_order.remove(self.zpo_order[self.showedZPOOperation])
        self.zpo_buttons.remove(self.zpo_buttons[self.showedZPOOperation])
        self.ui.widgetLayout.removeWidget(self.ui.widgetLayout.takeAt(self.showedZPOOperation).widget())
        self.ui.openCloseWidget(self.ui.ConditionArea)

    def execute_zpo(self):
        self.ui.openCloseWidget(self.ui.ChangingDBUI)
        self.zpo_buttons.clear()
        self.zpo_items_are_selected = False
        self.zpo_order[-1].TargetValueType = 0
        for i in self.selectedZPOItems:
            if self.cur_operation_type.value == 0:
                for i1 in range(self.ui.tableWidget.rowCount()):
                    item_value = copy.copy(self.ui.tableWidget.item(i1, i).text())
                    for operation in self.zpo_order:
                        operation.set_row(i1)
                        item_value = operation.execute(item_value)
                    self.ui.tableWidget.setItem(i1, i, QTableWidgetItem(item_value))
            else:
                item_value = self.ui.tableWidget.item(i[0], i[1]).text()
                for operation in self.zpo_order:
                    item_value = operation.execute(item_value)
                self.ui.tableWidget.setItem(i[0], i[1], QTableWidgetItem(item_value))

    @staticmethod
    def get_zpo_type(string):
        if string == 'String':
            return 0
        return 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_functional = Functional()
    main_functional.ui.show()
    sys.exit(app.exec())
