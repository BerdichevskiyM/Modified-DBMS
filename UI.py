from PyQt5.QtWidgets import QPushButton, QMenuBar, QWidget, \
    QToolButton, QLabel, QFrame, QLineEdit, QStatusBar, QTextEdit, \
    QTableWidgetItem, QTableWidget, QVBoxLayout, QAbstractItemView, \
    QScrollArea, QAbstractScrollArea, QComboBox
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from Operations import Operation


class UIC(QWidget):
    def __init__(self, functional):
        super().__init__()
        self.functional = functional
        self.resize(730, 472)
        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(QRect(0, 0, 730, 472))
        self.SettingButton = QToolButton(self.centralwidget)
        self.SettingButton.setGeometry(QRect(10, 10, 31, 41))
        font = QFont()
        font.setPointSize(8)
        font.setUnderline(False)
        self.SettingButton.setFont(font)
        icon = QIcon.fromTheme("=")
        self.SettingButton.setIcon(icon)
        self.SettingButton.setIconSize(QSize(16, 16))
        self.SettingButton.setCheckable(False)
        self.SettingButton.setPopupMode(QToolButton.DelayedPopup)
        self.SettingButton.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.SettingButton.setAutoRaise(False)
        self.SettingButton.setArrowType(Qt.NoArrow)
        self.back = QPushButton(self.centralwidget)
        self.back.setGeometry(QRect(50, 10, 50, 25))
        self.back.setText('Назад')
        self.back.clicked.connect(lambda: self.widget_back_forward(-1))
        self.forward = QPushButton(self.centralwidget)
        self.forward.setGeometry(QRect(109, 10, 50, 25))
        self.forward.setText('Вперёд')
        self.forward.clicked.connect(lambda: self.widget_back_forward(1))
        self.ChangingDBUI = QWidget(self.centralwidget)
        self.ChangingDBUI.setEnabled(True)
        self.ChangingDBUI.setGeometry(QRect(60, 50, 600, 371))
        self.ChangingDBUI.setAutoFillBackground(False)
        self.label = QLabel(self.ChangingDBUI)
        self.label.setGeometry(QRect(0, 310, 421, 61))
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setText("")
        self.label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.tableWidget = QTableWidget(self.ChangingDBUI)
        self.tableWidget.setGeometry(QRect(0, 100, 571, 192))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.commandToChange = QTextEdit(self.ChangingDBUI)
        self.commandToChange.setGeometry(QRect(0, 50, 201, 41))
        self.pushButton = QPushButton(self.ChangingDBUI)
        self.pushButton.setGeometry(QRect(205, 50, 81, 31))
        self.pushButton_2 = QPushButton(self.ChangingDBUI)
        self.pushButton_2.setGeometry(QRect(305, 50, 81, 31))
        self.pushButton_9 = QPushButton(self.ChangingDBUI)
        self.pushButton_9.setGeometry(QRect(405, 50, 33, 33))
        self.pushButton_9.setText("Удалить выбранные параметры")
        self.pushButton_9.resize(self.pushButton_9.sizeHint())
        self.pushButton_9.resize(self.pushButton_9.width(), self.pushButton_9.height() + 8)
        self.pushButton_12 = QPushButton(self.ChangingDBUI)
        self.pushButton_12.setGeometry(QRect(405, 50, 50, 50))
        self.pushButton_12.setText("Готово")
        self.pushButton_12.hide()
        self.textEdit = QTextEdit(self.ChangingDBUI)
        self.textEdit.setGeometry(QRect(0, 0, 301, 41))
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Sunken)
        self.textEdit.setLineWidth(1)
        self.textEdit.setUndoRedoEnabled(True)
        self.comboBox = QComboBox(self.ChangingDBUI)
        self.comboBox.setGeometry(QRect(430, 10, 111, 22))
        self.comboBox.setMaxVisibleItems(3)
        self.SettingsWidget = QWidget(self.centralwidget)
        self.SettingsWidget.setGeometry(QRect(10, 80, 261, 351))
        self.verticalLayoutWidget = QWidget(self.SettingsWidget)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 255, 351))
        self.Settings = QVBoxLayout(self.verticalLayoutWidget)
        self.Settings.setContentsMargins(0, 0, 0, 0)
        self.pushButton_4 = QPushButton(self.verticalLayoutWidget)
        font = QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setFlat(False)
        self.Settings.addWidget(self.pushButton_4)
        self.pushButton_1 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setText('Выполнить операцию над\nвыбранными столбцами')
        self.Settings.addWidget(self.pushButton_1)
        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setText('Выполнить операцию над\nвыбранными ячейками')
        self.Settings.addWidget(self.pushButton_5)
        self.pushButton_8 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setText('Добавить операцию\nв качестве параметра')
        self.Settings.addWidget(self.pushButton_8)
        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setFont(font)
        self.Settings.addWidget(self.pushButton_3)
        self.ConditionArea = QScrollArea(self.centralwidget)
        self.ConditionArea.setGeometry(QRect(60, 50, 650, 390))
        self.ConditionArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ConditionArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.ConditionArea.setWidgetResizable(True)
        self.ConditionArea.setFrameShape(QFrame().Box)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 16, 473))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(0, 473))
        self.verticalLayoutWidget_2 = QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget_2.setGeometry(QRect(220, 0, 250, 481))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QTextEdit(self.ConditionArea)
        self.label_2.setGeometry(QRect(10, 10, 180, 300))
        self.label_2.setText('\nВыберите операцию и настройте ее. Как только операция будет готова, '
                             'она появиться в списке ЗПО - Запросы Последовательных Операций. '
                             'Эти запросы (операции) выполняются по порядку. Они передают друг другу значение, '
                             'которое изначально равно элементу в ячейке таблицы. Взяв это значение '
                             'оно преобразуется либо в список (List. На SQL - кортеж, на Python - list), '
                             'либо в строку (String. На SQL - TEXT, на Python - str). В настройке операций '
                             'вы можете также использовать пока что только 2 регулярных выражения: $value$, $row=this$. '
                             'Первое обозначает то самое значение ЗПО. Второе обычно возвращает ряд ячейки таблицы (rowid), '
                             'над которой проводится данная операция. Также есть 3 выражение, которое можно использовать в '
                             'операции "Python-выражение". Чтобы принять все изменения после ЗПО и сохранить их в базу данных, '
                             'нажмите на кнопку "Изменить". Подробности в описаниях операций.')
        self.label_3 = QLabel(self.ConditionArea)
        self.label_3.move(500, 50)
        self.label_3.setText('Порядок ЗПО:')
        self.label_3.resize(self.label_3.sizeHint())
        self.pushButton_14 = QPushButton(self.ConditionArea)
        self.pushButton_14.setGeometry(QRect(500, 300, 100, 50))
        font = QFont()
        font.setPointSize(9)
        self.pushButton_14.setFont(font)
        self.pushButton_14.setText('ГОТОВО')
        self.scrollArea = QScrollArea(self.ConditionArea)
        self.scrollArea.setGeometry(QRect(500, 70, 90, 200))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.widget = QWidget()
        self.widget.setGeometry(QRect(0, 0, 95, 473))
        self.widget.setMinimumSize(QSize(0, 473))
        self.verticalLayoutWidget_3 = QWidget(self.widget)
        self.verticalLayoutWidget_3.setGeometry(QRect(0, 0, 80, 481))
        self.widgetLayout = QVBoxLayout(self.verticalLayoutWidget_3)
        self.scrollArea.setWidget(self.widget)
        self.operation1 = QPushButton(self.verticalLayoutWidget_2)
        font.setPointSize(11)
        self.operation1.setFont(font)
        self.verticalLayout.addWidget(self.operation1)
        self.operation2 = QPushButton(self.verticalLayoutWidget_2)
        font = QFont()
        font.setPointSize(11)
        self.operation2.setFont(font)
        self.verticalLayout.addWidget(self.operation2)
        self.operation3 = QPushButton(self.verticalLayoutWidget_2)
        font = QFont()
        font.setPointSize(11)
        self.operation3.setFont(font)
        self.verticalLayout.addWidget(self.operation3)
        self.operation4 = QPushButton(self.verticalLayoutWidget_2)
        font = QFont()
        font.setPointSize(11)
        self.operation4.setFont(font)
        self.verticalLayout.addWidget(self.operation4)
        self.operation5 = QPushButton(self.verticalLayoutWidget_2)
        font = QFont()
        font.setPointSize(11)
        self.operation5.setFont(font)
        self.verticalLayout.addWidget(self.operation5)
        self.pushButton_11 = QPushButton(self.verticalLayoutWidget_2)
        font = QFont()
        font.setPointSize(11)
        self.pushButton_11.setFont(font)
        self.verticalLayout.addWidget(self.pushButton_11)
        self.ConditionArea.setWidget(self.scrollAreaWidgetContents)
        self.ConditionInputField = QFrame(self.centralwidget)
        self.ConditionInputField.setGeometry(QRect(180, 20, 361, 401))
        self.ConditionInputField.setFrameShape(QFrame.Box)
        self.ConditionInputField.setFrameShadow(QFrame.Raised)
        self.conditionText = QTextEdit(self.ConditionInputField)
        self.conditionText.setGeometry(QRect(40, 100, 271, 200))
        self.label_5 = QLabel(self.ConditionInputField)
        self.label_5.setGeometry(QRect(10, 10, 331, 81))
        self.label_5.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.pushButton_10 = QPushButton(self.ConditionInputField)
        self.pushButton_10.setGeometry(QRect(40, 320, 120, 70))
        self.pushButton_10.setFont(font)
        self.pushButton_10.setText('Добавить\nоперацию')
        self.pushButton_13 = QPushButton(self.ConditionInputField)
        self.pushButton_13.setGeometry(QRect(40, 345, 150, 50))
        self.pushButton_13.setFont(font)
        self.pushButton_13.setText('Удалить\nоперацию')
        self.pushButton_13.hide()
        self.comboBox_1 = QComboBox(self.ConditionInputField)
        self.comboBox_1.setGeometry(QRect(290, 360, 70, 22))
        self.comboBox_1.setMaxVisibleItems(2)
        self.comboBox_1.addItem('String')
        self.comboBox_1.addItem('List')
        self.label_4 = QLabel('Тип операции: 0', self.ConditionInputField)
        self.label_4.move(240, 308)
        self.comboBox_1.addItem('List')
        self.label_1 = QLabel(self.ConditionInputField)
        self.label_1.move(290, 338)
        self.label_1.setText('Исходный тип: String')
        self.label_1.resize(self.label_1.sizeHint())
        self.ChangingDBUI.raise_()
        self.SettingButton.raise_()
        self.SettingsWidget.raise_()
        self.ConditionArea.raise_()
        self.ConditionInputField.raise_()
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 697, 21))
        self.statusbar = QStatusBar(self)
        self.SettingButton.setText("|||")
        self.pushButton.setText("Запуск")
        self.pushButton_2.setText("Изменить")
        self.pushButton_4.setText("Включить поле\nдля введения SQL- команд")
        self.pushButton_3.setText("Изменить путь")
        self.operation1.setText("SQL - выражение")
        self.operation1.clicked.connect(lambda: Operation.set_cif_interface(self, 1, self.functional, len(self.functional.zpo_order) - 1))
        self.operation2.setText("Python - выражение")
        self.operation2.clicked.connect(lambda: Operation.set_cif_interface(self, 2, self.functional, len(self.functional.zpo_order) - 1))
        self.operation3.setText("Перевод на другой язык")
        self.operation3.clicked.connect(lambda: Operation.set_cif_interface(self, 3, self.functional, len(self.functional.zpo_order) - 1))
        self.operation4.setText("Перевод в\nсистему счисления")
        self.operation4.clicked.connect(lambda: Operation.set_cif_interface(self, 4, self.functional, len(self.functional.zpo_order) - 1))
        self.operation5.setText("Быстрая замена типа")
        self.operation5.clicked.connect(lambda: Operation.set_cif_interface(self, 5, self.functional, len(self.functional.zpo_order) - 1))
        self.pushButton_11.setText('Удалить операцию по индексу')
        self.widgets = [(self.ChangingDBUI, self.ChangingDBUI.geometry().x()),
                        (self.ConditionArea, self.ConditionArea.geometry().x()),
                        (self.ConditionInputField, self.ConditionInputField.geometry().x())]
        for i in range(1, 6):
            getattr(self, f'operation{i}').clicked.connect(lambda: self.openCloseWidget(self.ConditionInputField))
        self.disableUI()
        self.boundsAreDefining = False
        self.SettingButton.clicked.connect(self.openCloseSettings)

    def enableUI(self):
        self.openCloseWidget(self.ChangingDBUI)
        self.SettingsWidget.hide()
        self.back.setEnabled(True)
        self.forward.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_1.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.label.setText(
            f'Сейчас вы изменяте файл {self.functional.fileName}\nВНИМАНИЕ! БУДЕТ ИЗМЕНЕН КОРНЕВОЙ ФАЙЛ! '
            f'Рекомендуем сделать его резервную копию.')
        self.functional.enable_changing_dbui_sql_field()

    def disableUI(self):
        for widget in self.widgets:
            widget[0].hide()

    def openCloseWidget(self, widget):
        if not widget.isVisible():
            self.disableUI()
            widget.show()
        else:
            widget.hide()

    def openCloseSettings(self):
        active_widget = [i for i in self.widgets if i[0].isVisible()]
        if active_widget:
            x_pos = active_widget[0][1]
            active_widget = active_widget[0][0]
            if not self.SettingsWidget.isVisible():
                x_needed_indent = 271 - x_pos + 50
                if x_needed_indent > 0:
                    active_widget.move(x_pos + x_needed_indent,
                                       active_widget.geometry().y())
                self.SettingsWidget.show()
                active_widget.setEnabled(False)
            else:
                active_widget.move(x_pos, active_widget.geometry().y())
                self.SettingsWidget.hide()
                active_widget.setEnabled(True)

    def set_default_text(self, widget):
        if widget == self.commandToChange and self.functional.changingDBUISqlFieldIsEnabled:
            self.commandToChange.setText(f'SELECT * FROM {self.comboBox.currentText()}')
        elif widget == self.commandToChange and not self.functional.changingDBUISqlFieldIsEnabled:
            self.commandToChange.setText('')

    def widget_back_forward(self, vector):
        active_widget = self.widgets.index([i for i in self.widgets if i[0].isVisible()][0])
        if (active_widget == 0 and vector == 1 and not self.functional.zpo_items_are_selected) or\
                (active_widget == 1 and vector == 1):
            vector = 5
        active_widget += vector
        for i in self.widgets:
            if self.widgets.index(i) == active_widget:
                self.openCloseWidget(i[0])