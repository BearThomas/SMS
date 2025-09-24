# sms.en.py

# language English

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QTimer, Qt, QRectF
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QListWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QFrame, QLineEdit, QHBoxLayout, QDialog, QMessageBox, QLineEdit
from PyQt5.QtGui import QPainter, QPainterPath, QRegion, QColor, QPalette
import sys
import LibC
import os

print(os.getcwd())

Students = LibC.Lib(fr'{os.getcwd()}\main\Date\Students.xLib')
Other = LibC.Lib(fr'{os.getcwd()}\main\Date\Students.xLib')

def fill_zero(string : str):
    if not string: return "00"
    elif int(string) / 10 < 1 : return f"0{string}"
    else : return string 

class UI_MainWindow(QWidget):
    def __init__(self, parent = None):
        global MODE_LIST, MODE_WIDGET
        super().__init__(parent)

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.left_list_spacing = int(self.screen_height * 0.01)
        self.left_list_width = int(self.screen_width * 0.1)
        self.left_list_height = int(self.screen_height * 0.75)
        self.window_width = int(self.screen_width * 0.8)
        self.window_height = int(self.screen_height * 0.8)
        self.window_x = int((self.screen_width - self.window_width) / 2)
        self.window_y = int((self.screen_height - self.window_height) / 2)
        self.left_list_font_size = int(self.screen_height * 0.02)
        self.left_list_item_padding = int(self.screen_height * 0.01)
        self.break_button_height = int(self.screen_height * 0.03)
        self.break_button_font_size = int(self.screen_height * 0.015)

        # set style sheet
        self.setStyleSheet(
            f"""
            * {{
                outline: None;
                border-radius: 10px;
            }}
            QScrollBar {{
                width:0;height:0
            }}
            QListWidget {{
                border: None;
                background-color: #e0e0e0e0;
                color: #111;
                font-size: {self.left_list_font_size}px;
            }}
            QListWidget::item {{
                padding: {self.left_list_item_padding}px;
                border-bottom: None;
                background-color: #e0e0e0e0;
                border-radius: 10px;
            }}
            QListWidget::item:hover {{
                background-color: #DCDCDC;
            }}
            QListWidget::item:selected {{
                background-color: rgba(255,255,255,150);
                color: #000;
            }}
            QPushButton {{
                background-color: #ddd;
                height: {self.break_button_height}px;
                border: None;
                font-size: {self.break_button_font_size}px;
            }}
            """
            )

        # set the window size
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height)

        # set the window 
        self.setWindowFlag(Qt.FramelessWindowHint)

        # set layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # set the list
        self.left_list = QListWidget()
        self.left_list.setSpacing(self.left_list_spacing)
        self.left_list.setFixedWidth(self.left_list_width)
        self.left_list.setFixedHeight(self.left_list_height)
        self.left_list.addItems(MODE_LIST)
        self.left_list.setCurrentRow(0)
        self.layout.addWidget(self.left_list, 0, 0, 1, 2)
        self.left_list.currentRowChanged.connect(self.list_clicked)
        
        # set the break button
        self.break_button = QPushButton()
        self.break_button.setText("Exit")
        self.break_button.clicked.connect(self.break_button_clicked)
        self.layout.addWidget(self.break_button, 1, 0, 1, 1)

        # set the small button
        self.small_button = QPushButton()
        self.small_button.setText("Small")
        # self.small_button.clicked.connect()
        self.layout.addWidget(self.small_button, 1, 1, 1, 1)

        # set the widget in right
        self.right_widget = UI_RightWidget_Home()
        self.right_widget.setFixedWidth(self.window_width - self.left_list_width)
        self.layout.addWidget(self.right_widget, 0, 2, 2, 1)

        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def break_button_clicked(self):
        # quit the application
        Students.save()
        Other.save()
        QCoreApplication.instance().quit()
        
    def paintEvent(self, event):
        # paint the rounded rectangle background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 240)) # semi-transparent white
        rect = QRectF(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 15, 15)

    def list_clicked(self,event):
        if (event == -1):
            return
        else:
            self.layout.removeWidget(self.right_widget)
            self.right_widget = MODE_WIDGET[event]()
            self.right_widget.setFixedWidth(self.window_width - self.left_list_width)
            self.layout.addWidget(self.right_widget, 0, 2, 2, 1)

class UI_RightWidget_Home(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # set time card
        self.time_card = UI_RightWidget_Home_Card_Time()
        self.layout.addWidget(self.time_card, 0, 0, 1, 1)

        # set score card
        self.score_card = UI_RightWidget_Home_Card_Score()
        self.layout.addWidget(self.score_card, 0, 1, 1, 1)

        # set task card
        self.task_card = UI_RightWidget_Home_Card_Task()
        self.layout.addWidget(self.task_card, 1, 0, 1, 1)

class UI_RightWidget_Score(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.students = []

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        

        # set layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # set the style
        # self.setStyleSheet(f"""
        #                    QPushButton {{
                                
        #                    }}
        #                    """)
        
        # set the student
        self.students_button = []
        row = 1
        col = 1
        for student in Students.table("Students").data:
            self.students_button.append(QPushButton(student[0]))
            self.students_button[-1].setObjectName(str(student[4]))
            self.students_button[-1].clicked.connect(self.select_student)
            self.layout.addWidget(self.students_button[-1], row, col)
            col += 1
            if (col > 5):
                col = 1
                row += 1
        
        self.go = QPushButton("Go")
        self.go.clicked.connect(self.GO)
        self.layout.addWidget(self.go, row + 1, 1, 1, 5)

    def select_student(self):
        print(self.sender().text())
        if (self.sender().objectName()[0] == '!'):
            self.sender().setStyleSheet("background-color: #ddd")
            del self.students[self.students.index(self.sender().objectName()[1:])]
            self.sender().setObjectName(self.sender().objectName()[1:])
        else:
            self.sender().setStyleSheet("background-color: #bbb")
            self.students.append(self.sender().objectName())
            self.sender().setObjectName('!' + self.sender().objectName())
    
    def GO(self):
        if (not self.students):
            Message = QMessageBox()
            Message.setWindowTitle("Waring")
            Message.setText("Please select student(s)")
            Message.setInformativeText("You don't select student")
            Message.setStyleSheet("""font-size: 15px;""")
            Message.exec_()
            return
        print(self.students)
        self.ControlWindow = UI_RightWidget_Score_Control(self, self.students)
        self.ControlWindow.show()
        for student_button in self.students_button:
            if (student_button.objectName()[0] == '!'):
                student_button.setStyleSheet("background-color: #ddd")
                del self.students[self.students.index(student_button.objectName()[1:])]
                student_button.setObjectName(student_button.objectName()[1:])

class UI_RightWidget_Score_Control(QDialog):
    def __init__(self, parent, students):
        
        super().__init__(parent)
        print(students)
        self.students = students.copy()
        print(self.students)

        self.setModal(True)

        self.setWindowTitle("Control")
        print(self.students)
        self.UP = True

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.window_width = int(self.screen_width * 0.3)
        self.window_height = int(self.screen_height * 0.6)
        self.window_x = int((self.screen_width - self.window_width) / 2)
        self.window_y = int((self.screen_height - self.window_height) / 2)

        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height)

        # set style sheet
        print(self.students)

        # set layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.UpButton = QPushButton("Add")
        self.UpButton.setStyleSheet("background-color: #bbb;")
        self.UpButton.clicked.connect(self.Up_click)
        self.layout.addWidget(self.UpButton, 1, 1)

        self.DownButton = QPushButton("Down")
        self.DownButton.setStyleSheet("background-color: #ddd;")
        self.DownButton.clicked.connect(self.Down_click)
        self.layout.addWidget(self.DownButton, 1, 2)

        self.Score_Input = QLineEdit(self)
        self.Score_Input.setPlaceholderText("Input Score")
        self.Score_Input.setStyleSheet("height: 55px;font-size: 30px;border: 3px;border-color: #ddd;")
        self.layout.addWidget(self.Score_Input, 2, 1, 1, 2)

        self.GO = QPushButton('GO')
        self.GO.clicked.connect(self.Go_click)
        self.layout.addWidget(self.GO, 3, 1, 1, 2)

        print(self.students)

    def Up_click(self):
        print(self.students)
        if (not self.UP):
            self.UpButton.setStyleSheet("background-color: #bbb;")
            self.DownButton.setStyleSheet("background-color: #ddd;")
            self.UP = True
    
    def Down_click(self):
        print(self.students)
        if (self.UP):
            self.UpButton.setStyleSheet("background-color: #ddd;")
            self.DownButton.setStyleSheet("background-color: #bbb;")
            self.UP = False

    def Go_click(self):
        print(self.students)
        for num in self.students:
            fi = Students.table("Students").find(["Num"], [int(num)])
            print(fi)
            if (self.UP):
                try:
                    int(self.Score_Input.text())
                except:
                    Message = QMessageBox()
                    Message.setWindowTitle("Waring")
                    Message.setText("Please input number")
                    Message.setStyleSheet("""font-size: 15px;""")
                    Message.exec_()
                    return
                Students.table("Students").change(fi, "Score", Students.table("Students").at(fi, "Score") + int(self.Score_Input.text()))
                Students.save()
                print(Students.table("Students").at(fi, "Score") + int(self.Score_Input.text()))
            else:
                try:
                    int(self.Score_Input.text())
                except:
                    Message = QMessageBox()
                    Message.setWindowTitle("Waring")
                    Message.setText("Please input number")
                    Message.setStyleSheet("""font-size: 15px;""")
                    Message.exec_()
                    return
                Students.table("Students").change(fi, "Score", Students.table("Students").at(fi, "Score") - int(self.Score_Input.text()))
                Students.save()
                print(self.Score_Input.text())
    
            


class UI_RightWidget_Time(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.countdown_button_Width = int(self.screen_width * 0.2)
        self.countup_button_Width = int(self.screen_width * 0.2)
        self.time_button_Width = int(self.screen_width * 0.2)
        self.QLabel_font_size = int(self.screen_height * 0.2)
        self.start_button_width = int(self.countdown_button_Width * 0.3)
        self.reset_button_width = int(self.countdown_button_Width * 0.3)
        self.max_button_width = int(self.countdown_button_Width * 0.3)

        # set style sheet
        self.setStyleSheet(
            f"""
            #countdown_button {{
                background: #FFF;
            }}
            #countup_button {{
                background: #e0e0e0;
            }}
            #time_button {{
                background: #e0e0e0;
            }}
            #time_value_label {{
                font-size: {self.QLabel_font_size}px;
            }}
            """
        )

        self.max_window = UI_RightWidget_Time_MaxWindow()

        # set layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.timer = QTimer(self)

        # countdown button
        self.countdown_button = QPushButton("CountDown")
        self.countdown_button.setObjectName("countdown_button")
        self.countdown_button.setFixedWidth(self.countdown_button_Width)
        self.countdown_button.clicked.connect(self.clicked_countdown_button)
        self.layout.addWidget(self.countdown_button, 0, 0, 1, 1)

        # countup button
        self.countup_button = QPushButton("Stopwatch")
        self.countup_button.setObjectName("countup_button")
        self.countup_button.setFixedWidth(self.countup_button_Width)
        self.countup_button.clicked.connect(self.clicked_countup_button)
        self.layout.addWidget(self.countup_button, 0, 1, 1, 1)

        # clock
        self.time_button = QPushButton("Clock")
        self.time_button.setObjectName("time_button")
        self.time_button.setFixedWidth(self.time_button_Width)
        self.time_button.clicked.connect(self.clicked_time_button)
        self.layout.addWidget(self.time_button, 0, 2, 1, 1)

        # time value label
        self.time_value_label = QLabel("00:00:00")
        self.time_value_label.setObjectName("time_value_label")
        self.time_value_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_value_label, 1, 0, 1, 3)

        # self.clicked_countdown_button()

        self.time_input = UI_RightWidget_Time_Time_Input()
        self.layout.addWidget(self.time_input, 2, 0, 1, 3, alignment=Qt.AlignCenter)
        self.time_input.time_input_hour.setText("0")
        self.time_input.time_input_minute.setText("0")
        self.time_input.time_input_second.setText("0")

        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(self.start_button_width)
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)

        # reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(self.reset_button_width)
        self.layout.addWidget(self.reset_button, 3, 1, 1, 1, alignment=Qt.AlignCenter)
        self.reset_button.clicked.connect(self.stop)

        # max button
        self.max_button = QPushButton("Full")
        self.max_button.setFixedWidth(self.max_button_width)
        self.layout.addWidget(self.max_button, 3, 1, 1, 1, alignment=Qt.AlignRight)
        self.max_button.clicked.connect(self.max_window_clicked)
    
    def clicked_countdown_button(self):
        self.stop()
        try:
            self.layout.removeWidget(self.start_button)
            self.start_button.hide()
            self.start_button.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.reset_button)
            self.reset_button.hide()
            self.reset_button.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.max_button)
            self.max_button.hide()
            self.max_button.deleteLater()
        except:
            pass

        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(self.start_button_width)
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)

        # reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(self.reset_button_width)
        self.layout.addWidget(self.reset_button, 3, 1, 1, 1, alignment=Qt.AlignCenter)
        self.reset_button.clicked.connect(self.stop)

        # max button
        self.max_button = QPushButton("Full")
        self.max_button.setFixedWidth(self.max_button_width)
        self.layout.addWidget(self.max_button, 3, 1, 1, 1, alignment=Qt.AlignRight)
        self.max_button.clicked.connect(self.max_window_clicked)
        
        self.setStyleSheet(f"""
                      #countdown_button {{
                            background: #FFF;
                        }}
                        #countup_button {{
                            background: #e0e0e0;
                        }}
                        #time_button {{
                            background: #e0e0e0;
                        }}
                        #time_value_label {{
                            font-size: {self.QLabel_font_size}px;
                        }}
                      """)
        try:
            self.start_button.clicked.disconnect(self.start_countup)
        except:
            pass
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)

        # countdown input
        self.time_input = UI_RightWidget_Time_Time_Input()
        self.layout.addWidget(self.time_input, 2, 0, 1, 3, alignment=Qt.AlignCenter)
        self.time_input.time_input_hour.setText("0")
        self.time_input.time_input_minute.setText("0")
        self.time_input.time_input_second.setText("0")
    
    def clicked_countup_button(self):
        self.stop()
        try:
            self.layout.removeWidget(self.start_button)
            self.start_button.hide()
            self.start_button.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.reset_button)
            self.reset_button.hide()
            self.reset_button.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.max_button)
            self.max_button.hide()
            self.max_button.deleteLater()
        except:
            pass

        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(self.start_button_width)
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)

        # reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(self.reset_button_width)
        self.layout.addWidget(self.reset_button, 3, 1, 1, 1, alignment=Qt.AlignCenter)
        self.reset_button.clicked.connect(self.stop)

        # max button
        self.max_button = QPushButton("Full")
        self.max_button.setFixedWidth(self.max_button_width)
        self.layout.addWidget(self.max_button, 3, 1, 1, 1, alignment=Qt.AlignRight)
        self.max_button.clicked.connect(self.max_window_clicked)
        

        self.setStyleSheet(f"""
                      #countdown_button {{
                            background: #e0e0e0;
                        }}
                        #countup_button {{
                            background: #FFF;
                        }}
                        #time_button {{
                            background: #e0e0e0;
                        }}
                        #time_value_label {{
                            font-size: {self.QLabel_font_size}px;
                        }}  
                      """)
        try:
            self.start_button.clicked.disconnect(self.start_countdown)
        except:
            pass
        self.start_button.clicked.connect(self.start_countup)
        self.layout.addWidget(self.start_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)
        try:
            self.layout.removeWidget(self.time_input)
            self.time_input.hide()
            self.time_input.deleteLater()
        except:
            pass
    
    def clicked_time_button(self):
        self.stop()
        self.setStyleSheet(f"""
                        #countdown_button {{
                            background: #e0e0e0;
                        }}
                        #countup_button {{
                            background: #e0e0e0;
                        }}
                        #time_button {{
                            background: #FFF;
                        }}
                        #time_value_label {{
                            font-size: {self.QLabel_font_size}px;
                        }}
                      """)
        try:
            self.layout.removeWidget(self.time_input)
            self.time_input.hide()
            self.time_input.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.start_button)
            self.start_button.hide()
            self.start_button.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.reset_button)
            self.reset_button.hide()
            self.reset_button.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.max_button)
            self.max_button.hide()
            self.max_button.deleteLater()
        except:
            pass

        # max button
        self.max_button = QPushButton("Full")
        self.max_button.setFixedWidth(self.max_button_width)
        self.layout.addWidget(self.max_button, 3, 1, 1, 1, alignment=Qt.AlignCenter)
        self.max_button.clicked.connect(self.max_window_clicked)

        self.timer.timeout.connect(self.time_update)
        self.timer.start(50)

    def start_countdown(self):
        self.time_value_label.setText(f"{fill_zero(self.time_input.time_input_hour.text())}:{fill_zero(self.time_input.time_input_minute.text())}:{fill_zero(self.time_input.time_input_second.text())}")
        self.countdown_last = int(self.time_input.time_input_hour.text()) * 60 * 60 + int(self.time_input.time_input_minute.text()) * 60 + int(self.time_input.time_input_second.text())
        if self.countdown_last == 0 : return
        self.timer.timeout.connect(self.countdown_update)
        self.timer.start(1000)
        self.time_input.time_input_hour.setText("0")
        self.time_input.time_input_minute.setText("0")
        self.time_input.time_input_second.setText("0")

    def start_countup(self):
        self.time_value_label.setText(f"00:00:00")
        self.countup_last = 0
        self.timer.timeout.connect(self.countup_update)
        self.timer.start(1000)
    
    def countdown_update(self):
        self.countdown_last -= 1
        self.time_value_label.setText(f"{fill_zero(str(int(self.countdown_last / (60 * 60))))}:{fill_zero(str(int(self.countdown_last % (60 * 60) / 60)))}:{fill_zero(str(int(self.countdown_last % 60)))}")
        if self.countdown_last == 0:
            self.timer.stop()

    def countup_update(self):
        self.countup_last += 1
        self.time_value_label.setText(f"{fill_zero(str(int(self.countup_last / (60 * 60))))}:{fill_zero(str(int(self.countup_last % (60 * 60) / 60)))}:{fill_zero(str(int(self.countup_last % 60)))}")

    def stop(self):
        try:
            self.timer.stop()
        except:
            pass
        self.time_value_label.setText(f"00:00:00")
    
    def time_update(self):
        self.time_value_label.setText(QtCore.QTime.currentTime().toString("hh:mm:ss"))

    def max_window_clicked(self):
        self.max_window.start_time()
        self.max_window.show()

class UI_RightWidget_Time_Time_Input(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.Input_height = int(self.screen_height * 0.05)
        self.Input_width = int(self.screen_width * 0.4)
        self.colon_font_size = int(self.screen_height * 0.04)

        # set size
        self.setFixedHeight(self.Input_height)
        self.setFixedWidth(self.Input_width)

        # set style sheet
        self.setStyleSheet(f"""
                           * {{
                                height: {self.Input_height}px;
                                font-size: {self.colon_font_size}px;
                           }}
                           """)

        # set layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # colon
        self.colon1 = QLabel("H")
        self.colon2 = QLabel("M")
        self.colon3 = QLabel("S")
        self.colon1.setObjectName("colon")
        self.colon2.setObjectName("colon")
        self.colon3.setObjectName("colon")

        # hour input
        self.time_input_hour = QLineEdit()
        self.layout.addWidget(self.time_input_hour)

        self.layout.addWidget(self.colon1)

        # minute input
        self.time_input_minute = QLineEdit()
        self.layout.addWidget(self.time_input_minute)

        self.layout.addWidget(self.colon2)

        # second input
        self.time_input_second = QLineEdit()
        self.layout.addWidget(self.time_input_second)   

        self.layout.addWidget(self.colon3)     

class UI_RightWidget_Home_Card_Time(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("time_card")

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.card_width = int(self.screen_width * 0.2)
        self.card_height = int(self.screen_height * 0.2)
        self.time_label_font_size = int(self.screen_height * 0.02)
        self.time_value_font_size = int(self.time_label_font_size * 1.5)

        # set style sheet
        self.setStyleSheet(
            f"""
            #time_label {{
                font-size: {self.time_label_font_size}px;
            }}
            #time_value {{
                font-size: {self.time_value_font_size}px;
                border: 2px solid #ccc;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.8);
            }}
            #date_value {{
                font-size: {self.time_value_font_size}px;
                border: 2px solid #ccc;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.8);
            }}
            
            """
        )

        # set layout
        self.layout = QVBoxLayout()
        self.setFixedSize(self.card_width, self.card_height)
        self.setLayout(self.layout)

        # time label
        self.time_label = QLabel("Current Time")
        self.time_label.setObjectName("time_label")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        # separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(3)
        self.separator.setFixedHeight(2)
        self.separator.setStyleSheet("background-color: #ccc;")
        self.layout.addWidget(self.separator)

        # date value
        self.date_value = QLabel(QtCore.QDate.currentDate().toString("yyyy-MM-dd"))
        self.date_value.setObjectName("date_value")
        self.date_value.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.date_value)

        # time value
        self.time_value = QLabel()
        self.time_value.setObjectName("time_value")
        self.time_value.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_value)

        # date and time update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(50)

    def update_time(self):
        current_time = QtCore.QTime.currentTime()
        self.time_value.setText(current_time.toString("hh:mm:ss"))
        self.date_value.setText(QtCore.QDate.currentDate().toString("yyyy-MM-dd"))

class UI_RightWidget_Home_Card_Score(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.card_width = int(self.screen_width * 0.2)
        self.card_height = int(self.screen_height * 0.3)
        self.score_list_spacing = int(self.screen_height * 0.003)
        self.score_list_item_height = int(self.screen_height * 0.01)
        self.score_label_font_size = int(self.screen_height * 0.02)
        self.score_list_font_size = int(self.screen_height * 0.01)
        self.score_list_height = int(self.card_height * 0.75)

        # set style sheet
        self.setStyleSheet(
            f"""
            #score_label {{
                font-size: {self.score_label_font_size}px;
            }}
            QListWidget {{
                font-size: {self.score_list_font_size}px;
            }}
            QListWidget::item {{
                height: {self.score_list_item_height}px;
            }}
            """
        )

        # set layout
        self.layout = QVBoxLayout()
        self.setFixedSize(self.card_width, self.card_height)
        self.setLayout(self.layout)

        # score label
        self.score_label = QLabel("Current Score List")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setObjectName("score_label")
        self.layout.addWidget(self.score_label)

        # separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(3)
        self.separator.setFixedHeight(2)
        self.separator.setStyleSheet("background-color: #ccc;")
        self.layout.addWidget(self.separator)

        # set the list
        self.score_list = QListWidget()
        self.score_list.setSpacing(self.score_list_spacing)
        self.score_list.setFixedHeight(self.score_list_height)
        self.score_list.addItems([f"{name}  \t{score}" for name, score in _score_list_])
        self.layout.addWidget(self.score_list)

class UI_RightWidget_Home_Card_Task(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        # set some constant
        self.card_width = int(self.screen_width * 0.2)
        self.card_height = int(self.screen_height * 0.3)
        self.task_list_spacing = int(self.screen_height * 0.003)
        self.task_list_item_height = int(self.screen_height * 0.01)
        self.task_label_font_size = int(self.screen_height * 0.02)
        self.task_list_font_size = int(self.screen_height * 0.01)
        self.task_list_height = int(self.card_height * 0.75)

        # set style sheet
        self.setStyleSheet(
            f"""
            #task_label {{
                font-size: {self.task_label_font_size}px;
            }}
            QListWidget {{
                font-size: {self.task_list_font_size}px;
            }}
            QListWidget::item {{
                height: {self.task_list_item_height}px;
            }}
            """
        )

        # set layout
        self.layout = QVBoxLayout()
        self.setFixedSize(self.card_width, self.card_height)
        self.setLayout(self.layout)

        # score label
        self.task_label = QLabel("Bulletin Board")
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setObjectName("task_label")
        self.layout.addWidget(self.task_label)

        # separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(3)
        self.separator.setFixedHeight(2)
        self.separator.setStyleSheet("background-color: #ccc;")
        self.layout.addWidget(self.separator)

        # set the list
        self.task_list = QListWidget()
        self.task_list.setSpacing(self.task_list_spacing)
        self.task_list.setFixedHeight(self.task_list_height)
        self.task_list.addItems([f"{task}  \t{time}  \t{note}" for task, time, note in _task_list_])
        self.layout.addWidget(self.task_list)

class UI_RightWidget_Time_MaxWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # get screen geometry
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width() 
        self.screen_height = self.screen.height()

        self.QLabel_font_size = int(self.screen_height * 0.2)
        self.small_button_width = int((self.screen_width * 0.2) * 0.3)
        self.small_button_height = int(self.screen_height * 0.03)
        self.small_button_font_size = int(self.screen_height * 0.015)
        
        self.setStyleSheet(f"""
                        #time_value_label {{
                            font-size: {self.QLabel_font_size}px;
                        }}
                        #small_button {{
                            background-color: #ddd;
                            border: None;
                            border-radius: 10px;
                            font-size: {self.small_button_font_size}px;
                        }}
                      """)

        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # time label
        self.time_label = QLabel()
        self.time_label.setObjectName("time_value_label")
        self.layout.addWidget(self.time_label, alignment=Qt.AlignCenter)

        # small button
        self.small_button = QPushButton("Small")
        self.small_button.setFixedWidth(self.small_button_width)
        self.small_button.setFixedHeight(self.small_button_height)
        self.small_button.setObjectName("small_button")
        self.layout.addWidget(self.small_button, alignment=Qt.AlignCenter)
        self.small_button.clicked.connect(self.stop_time)

        self.timer = QTimer()
        self.timer.timeout.connect(self.time_update)
    
    def start_time(self):
        self.timer.start(50)

    def time_update(self):
        self.time_label.setText(main_window.right_widget.time_value_label.text())

    def stop_time(self):
        self.timer.stop()
        self.hide()

# set the modes list
MODE_LIST = [
    "Home",
    "Score",
    "Time"
]
MODE_WIDGET = [
    UI_RightWidget_Home,
    UI_RightWidget_Score,
    UI_RightWidget_Time
]

# set the score list
_score_list_ = [
    ("A",100),
    ("B",110),
    ("C",120),
    ("A",100),
    ("B",110),
    ("B", 100)
]

# set the task list
_task_list_ = [
    ("A", "10:00", "note"),
    ("A", "10:00", "note"),
    ("A", "10:00", "note"),
    ("b", "10:00", "note"),
    ("b", "10:00", "note"),
    ("b", "10:00", "note")
]   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = UI_MainWindow()
    main_window.show()
    sys.exit(app.exec_())