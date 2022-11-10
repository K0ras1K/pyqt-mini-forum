import sqlite3
import sys
from sqlite3 import IntegrityError

from PyQt5.QtCore import QStringListModel, QRect, QSize
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QLineEdit, QTextEdit, QTextBrowser, \
    QGridLayout, QListView


#Database work class
class DataBaseEntity:
    def __init__(self):
        with sqlite3.connect('./src/database.db') as db:
            cursor = db.cursor()
            query = """CREATE TABLE IF NOT EXISTS "forum" (
                    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'topic_name' TEXT,
                    'topic_text' TEXT,
                    'topic_section' TEXT
                    )"""
            cursor.execute(query)
            db.commit()

        self.cursor = db.cursor()

    #Add topic to database
    def addTopic(self, topic_name, topic_text, topic_section):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""INSERT INTO forum(topic_name, topic_text, topic_section) VALUES(?, ?, ?)"""
            self.cursor.execute(query, (topic_name, topic_text, topic_section))
            db.commit()

    #Update topic name in database
    def updateTopicName(self, id, topic_name, topic_text, topic_section):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""UPDATE forum 
            SET topic_name = ?
            WHERE id = ?"""
            print(query)
            self.cursor.execute(query, (topic_name, id))
            db.commit()

    #Update topic text in database
    def updateTopicText(self, id, topic_name, topic_text, topic_section):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""UPDATE forum 
            SET topic_text = ?
            WHERE id = ?"""
            print(query)
            self.cursor.execute(query, (topic_text, id))
            db.commit()

    #Update topic section in database
    def updateTopicSection(self, id, topic_name, topic_text, topic_section):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""UPDATE forum 
            SET topic_section = ?
            WHERE id = ?"""
            print(query)
            self.cursor.execute(query, (topic_section, id))
            db.commit()

    #Delete topic from database
    def deleteTopic(self, topic_name):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""DELETE FROM forum 
            WHERE topic_name = ?"""
            self.cursor.execute(query, (topic_name,))
            db.commit()

    #Return topic name, text, section from database
    def selectTopic(self, topic_name):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""SELECT * FROM forum 
            WHERE LOWER(topic_name) = ?"""
            result = self.cursor.execute(query, (topic_name.lower(),)).fetchall()
            return result

    #Return id of topic by topic name
    def getIdByTopicName(self, topic_name):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""SELECT id FROM forum
            WHERE topic_name = ?"""
            result = self.cursor.execute(query, (topic_name,)).fetchone()
            db.commit()
            return result

    #Return all list of topics
    def getTopicList(self):
        with sqlite3.connect('./src/database.db') as db:
            self.cursor = db.cursor()
            query = f"""SELECT topic_name FROM forum"""
            result = self.cursor.execute(query).fetchall()
            db.commit()
            return result


dataBaseEntity = DataBaseEntity()


#Missing elemet widget
class WindowMissingElemetError(QWidget):
    #Init def
    def __init__(self):
        super().__init__()

        self.label = QLabel(self)

        self.initUI()

    #Init UI
    def initUI(self):
        self.setGeometry(700, 500, 500, 200)
        self.setWindowTitle('Данной темы не существует.')
        self.label.setFont(QFont('Arial', 12))
        self.label.setText("Данной темы не существует.")
        self.label.move(30, 65)


#Existing element widget
class WindowExistingElementError(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 500, 500, 200)
        self.setWindowTitle('Название темы занято')
        self.label.setFont(QFont('Arial', 12))
        self.label.setText("Название темы занято")
        self.label.move(90, 65)


#Main window widget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



        self.background_label = QLabel()
        self.background_image = QPixmap("./src/background.png")
        self.background_label.setMinimumSize(QSize(1000, 200))
        self.background_label.setMaximumSize(QSize(2000, 200))
        self.background_label.setGeometry(QRect(0, 0, 2000, 300))
        self.background_label.setPixmap(self.background_image)

        self.grid = QGridLayout()

        self.button_topic_create = QPushButton('Создать тему', self)
        self.button_topic_remove = QPushButton('Удалить тему', self)
        self.button_topic_change = QPushButton('Редактировать тему', self)
        self.button_topic_view = QPushButton('Открыть тему', self)

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 960, 250)
        self.setWindowTitle('Forum by K0ras1K')
        text_font = QFont('Arial', 14)

        self.background_label.resize(960, 250)

        self.grid.addWidget(self.background_label, 1, 1)
        self.setLayout(self.grid)

        self.button_topic_create.resize(300, 75)
        self.button_topic_create.move(10, 20)
        self.button_topic_create.setFont(text_font)
        self.button_topic_create.clicked.connect(self.topicCreate)

        self.button_topic_remove.resize(300, 75)
        self.button_topic_remove.move(320, 20)
        self.button_topic_remove.setFont(text_font)
        self.button_topic_remove.clicked.connect(self.topicDelete)

        self.button_topic_change.resize(300, 75)
        self.button_topic_change.move(630, 20)
        self.button_topic_change.setFont(text_font)
        self.button_topic_change.clicked.connect(self.topicChange)

        self.button_topic_view.resize(400, 75)
        self.button_topic_view.move(270, 150)
        self.button_topic_view.setFont(text_font)
        self.button_topic_view.clicked.connect(self.check)

    #Open topic create widget
    def topicCreate(self):
        self.windowTopicCreate = WindowTopicCreate()
        self.windowTopicCreate.show()

    #Open topic delete widget
    def topicDelete(self):
        self.windowTopicDelete = WindowTopicDelete()
        self.windowTopicDelete.show()

    #Open Topic change(edit) widget
    def topicChange(self):
        self.windowTopicEdit = WindowTopicEdit()
        self.windowTopicEdit.show()

    #Open check(view) widget
    def check(self):
        self.windowViewTopic = WindowViewTopic()
        self.windowViewTopic.show()


#Topic create widget
class WindowTopicCreate(QWidget):
    def __init__(self):
        super().__init__()

        self.topic_name = QLineEdit(self)
        self.topic_text = QTextEdit(self)
        self.topic_section = QLineEdit(self)

        self.button_result = QPushButton('Подтвердить', self)

        self.window_error = WindowExistingElementError()

        self.initUI()

    def initUI(self):
        self.setGeometry(700, 400, 500, 550)
        self.setWindowTitle('Создание темы')
        text_font = QFont('Arial', 10)

        label_1 = QLabel(self)
        label_1.setFont(text_font)
        label_1.setText("Введите название темы")
        label_1.move(20, 20)

        self.topic_name.move(20, 50)
        self.topic_name.resize(450, 30)

        label_2 = QLabel(self)
        label_2.setFont(text_font)
        label_2.setText("Введите содержание темы")
        label_2.move(20, 110)

        self.topic_text.move(20, 140)
        self.topic_text.resize(450, 230)

        label_3 = QLabel(self)
        label_3.setFont(text_font)
        label_3.setText("Введите раздел форума")
        label_3.move(20, 400)

        self.topic_section.move(20, 430)
        self.topic_section.resize(450, 30)

        self.button_result.resize(150, 30)
        self.button_result.move(320, 500)
        self.button_result.setFont(QFont('Arial', 8))
        self.button_result.clicked.connect(self.handleResults)

    #Button handler
    def handleResults(self):
        topic_name = self.topic_name.text()
        topic_text = self.topic_text.toPlainText()
        topic_section = self.topic_section.text()
        try:
            #Add topic to database
            dataBaseEntity.addTopic(topic_name, topic_text, topic_section)
            self.close()
        except IntegrityError:
            #Show error window
            self.window_error.show()


#Topic delete widget
class WindowTopicDelete(QWidget):
    def __init__(self):
        super().__init__()

        self.name_input = QLineEdit(self)

        self.result_button = QPushButton('Подтвердить', self)

        self.window_error = WindowMissingElemetError()

        self.topic_list = []
        self.topic_list_label = QStringListModel()
        self.topic_list_view_label = QListView(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(700, 400, 500, 400)
        self.setWindowTitle('Удаление закона')
        text_font = QFont('Arial', 10)

        self.topic_list_view_label.move(20, 100)
        self.topic_list_view_label.resize(100, 200)

        self.topic_list = self.translateTopicList(dataBaseEntity.getTopicList())
        print(self.topic_list)

        self.topic_list_label.setStringList(self.topic_list)

        self.topic_list_view_label.setModel(self.topic_list_label)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название закона")
        label1.move(20, 20)

        self.name_input.move(20, 50)
        self.name_input.resize(450, 30)

        self.result_button.resize(150, 30)
        self.result_button.move(320, 150)
        self.result_button.setFont(QFont('Arial', 8))
        self.result_button.clicked.connect(self.handleResult)

    #Button handler
    def handleResult(self):
        name = self.name_input.text()
        try:
            dataBaseEntity.deleteTopic(name)
        except:
            self.window_error.show()
        self.close()

    #Return string list of topics from string tuple list of topics
    def translateTopicList(self, topic_list):
        new_topic_list = []
        for i in range(len(topic_list)):
            new_topic_list.append(topic_list[i][0])

        return new_topic_list


#Topic edit widget
class WindowTopicEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.old_topic_name = QLineEdit(self)

        self.topic_name = QLineEdit(self)
        self.topic_text = QTextEdit(self)
        self.topic_section = QLineEdit(self)

        self.button_result = QPushButton('Подтвердить', self)

        self.window_error = WindowMissingElemetError()

        self.is_update_topic_name = False
        self.is_update_topic_text = False
        self.is_update_topic_section = False

        self.topic_list = []
        self.topic_list_label = QStringListModel()
        self.topic_list_view_label = QListView(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(700, 400, 700, 650)
        self.setWindowTitle('Изменение формулы закона')
        text_font = QFont('Arial', 10)

        self.topic_list_view_label.move(550, 20)
        self.topic_list_view_label.resize(100, 200)

        self.topic_list = self.translateTopicList(dataBaseEntity.getTopicList())
        print(self.topic_list)

        self.topic_list_label.setStringList(self.topic_list)

        self.topic_list_view_label.setModel(self.topic_list_label)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите новое название темы")
        label1.move(20, 20)

        self.topic_name.move(20, 50)
        self.topic_name.resize(450, 30)

        label2 = QLabel(self)
        label2.setFont(text_font)
        label2.setText("Введите новый текст темы")
        label2.move(20, 110)

        self.topic_text.move(20, 140)
        self.topic_text.resize(450, 230)

        label_3 = QLabel(self)
        label_3.setFont(text_font)
        label_3.setText("Введите раздел форума")
        label_3.move(20, 400)

        self.topic_section.move(20, 430)
        self.topic_section.resize(450, 30)

        label_4 = QLabel(self)
        label_4.setFont(text_font)
        label_4.setText("Введите старое название")
        label_4.move(20, 480)
        self.old_topic_name.move(20, 510)
        self.old_topic_name.resize(450, 30)

        self.button_result.resize(150, 30)
        self.button_result.move(320, 560)
        self.button_result.setFont(QFont('Arial', 8))
        self.button_result.clicked.connect(self.handleResult)

    #Button handler
    def handleResult(self):
        old_topic_name = self.old_topic_name.text()
        topic_name = self.topic_name.text()
        topic_text = self.topic_text.toPlainText()
        topic_section = self.topic_section.text()

        if len(topic_name) != 0:
            self.is_update_topic_name = True

        if len(topic_text) != 0:
            self.is_update_topic_text = True

        if len(topic_section) != 0:
            self.is_update_topic_section = True

        id = int(dataBaseEntity.getIdByTopicName(old_topic_name)[0])
        print(id)
        try:
            #Update topic name, if QStringLine != null
            if self.is_update_topic_name:
                dataBaseEntity.updateTopicName(id, topic_name, topic_text, topic_section)

            #Update topic text, if QStringLine != null
            if self.is_update_topic_text:
                dataBaseEntity.updateTopicText(id, topic_name, topic_text, topic_section)

            #Update topic section, if QStringLine != null
            if self.is_update_topic_section:
                dataBaseEntity.updateTopicSection(id, topic_name, topic_text, topic_section)
        except:
            self.window_error.show()
        self.close()

    #Return string list from string tuple list
    def translateTopicList(self, topic_list):
        new_topic_list = []
        for i in range(len(topic_list)):
            new_topic_list.append(topic_list[i][0])

        return new_topic_list


#View topiv widget
class WindowViewTopic(QWidget):
    def __init__(self):
        super().__init__()

        self.topic_name = QLineEdit(self)

        self.button_result = QPushButton('Подтвердить', self)

        self.window_error = WindowMissingElemetError()

        self.topic_list = []
        self.topic_list_label = QStringListModel()
        self.topic_list_view_label = QListView(self)

        self.initUI()

    def initUI(self):
        self.setGeometry(700, 400, 500, 500)
        self.setWindowTitle('Просмотр темы')
        text_font = QFont('Arial', 10)

        self.topic_list_view_label.move(20, 100)
        self.topic_list_view_label.resize(100, 200)

        self.topic_list = self.translateTopicList(dataBaseEntity.getTopicList())
        print(self.topic_list)

        self.topic_list_label.setStringList(self.topic_list)

        self.topic_list_view_label.setModel(self.topic_list_label)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название темы")
        label1.move(20, 20)

        self.topic_name.move(20, 50)
        self.topic_name.resize(450, 30)

        self.button_result.resize(150, 30)
        self.button_result.move(320, 150)
        self.button_result.setFont(QFont('Arial', 8))
        self.button_result.clicked.connect(self.handleResult)

    #Button handler
    def handleResult(self):
        topic_name = self.topic_name.text()
        result = dataBaseEntity.selectTopic(topic_name)
        print(result)
        if len(result) != 0:
            topic_text = result[0][2]
            self.result_window = WindowResultViewTopic(topic_name, topic_text)
            self.result_window.show()
        else:
            self.window_error.show()

    #Return string list from string tuple list
    def translateTopicList(self, topic_list):
        new_topic_list = []
        for i in range(len(topic_list)):
            new_topic_list.append(topic_list[i][0])

        return new_topic_list


#Result ciew topic widget
class WindowResultViewTopic(QWidget):
    def __init__(self, topic_name, topic_text):
        super().__init__()

        self.topic_name = topic_name
        self.topic_text = topic_text

        self.window_error = WindowMissingElemetError()

        self.initUI()

    def initUI(self):
        self.setGeometry(600, 100, 850, 500)
        self.setWindowTitle('Просмотр темы')
        text_font = QFont('Arial', 10)

        label_1 = QLabel(self)
        label_1.setFont(text_font)
        label_1.setText(self.topic_name)
        label_1.move(20, 40)

        label_2 = QTextBrowser(self)
        label_2.setFont(text_font)
        label_2.setText(self.topic_text)
        label_2.move(20, 80)
        label_2.resize(600, 400)


#Main function to start application
def main():
    forum = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(forum.exec())


if __name__ == '__main__':
    main()
