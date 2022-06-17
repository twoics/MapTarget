"""
Module that implements the basic UI class
"""

# Third party imports
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QMovie

# Local application imports
from .map_ui import MapUI
from json_connect.json_connector import JsonConnector
# Doesn't remove this, it's icons import
from . import icons


class MainUI(QMainWindow):
    # Signal emitted to search for objects
    # Param: Query - cafe, cinema, ... (or name)
    search_objects = QtCore.pyqtSignal(str)

    def __init__(self, ui_map: MapUI):
        """
        Initializing the main UI of the application
        :param ui_map: UI maps
        """
        super().__init__()
        json_connector = JsonConnector()

        # The gif that is shown when the app is running
        working_gif = json_connector.get_data("loading.gif").name

        self._click_position = None
        self._map = ui_map

        self._central_widget = QtWidgets.QWidget(self)
        self._vertical_layout = QtWidgets.QVBoxLayout(self._central_widget)
        self._head = QtWidgets.QFrame(self._central_widget)
        self._horizontal_layout = QtWidgets.QHBoxLayout(self._head)
        self._frame = QtWidgets.QFrame(self._head)
        self._horizontal_layout_3 = QtWidgets.QHBoxLayout(self._frame)
        self._find_name_line = QtWidgets.QLineEdit(self._frame)
        self._find_name_but = QtWidgets.QPushButton(self._frame)
        self._title = QtWidgets.QFrame(self._head)
        self._horizontal_layout_4 = QtWidgets.QHBoxLayout(self._title)
        self._title_icon = QtWidgets.QLabel(self._title)
        self._title_name = QtWidgets.QLabel(self._title)
        self._service_butt = QtWidgets.QFrame(self._head)
        self._horizontal_layout_2 = QtWidgets.QHBoxLayout(self._service_butt)
        self._minimize = QtWidgets.QPushButton(self._service_butt)
        self._maximaze = QtWidgets.QPushButton(self._service_butt)
        self._close_button = QtWidgets.QPushButton(self._service_butt)
        self._body = QtWidgets.QFrame(self._central_widget)
        self._vertical_layout_2 = QtWidgets.QVBoxLayout(self._body)
        self._query_butt = QtWidgets.QFrame(self._body)
        self._vertical_layout_3 = QtWidgets.QVBoxLayout(self._query_butt)
        self._buttons = QtWidgets.QFrame(self._query_butt)
        self._gridLayout = QtWidgets.QGridLayout(self._buttons)
        self._cinema = QtWidgets.QPushButton(self._buttons)
        self._hotel = QtWidgets.QPushButton(self._buttons)
        self._restaurant = QtWidgets.QPushButton(self._buttons)
        self._meseum = QtWidgets.QPushButton(self._buttons)
        self._cafe = QtWidgets.QPushButton(self._buttons)
        self._electronic = QtWidgets.QPushButton(self._buttons)
        self._sup_market = QtWidgets.QPushButton(self._buttons)
        self._fitness = QtWidgets.QPushButton(self._buttons)
        self._fuel = QtWidgets.QPushButton(self._buttons)
        self._library = QtWidgets.QPushButton(self._buttons)
        self._bar = QtWidgets.QPushButton(self._buttons)
        self._pharmacy = QtWidgets.QPushButton(self._buttons)
        self._clothes = QtWidgets.QPushButton(self._buttons)
        self._fast_food = QtWidgets.QPushButton(self._buttons)
        self._hospital = QtWidgets.QPushButton(self._buttons)
        self._mall = QtWidgets.QPushButton(self._buttons)

        self._footer = QtWidgets.QFrame(self._body)
        self._horizontal_layout_5 = QtWidgets.QHBoxLayout(self._footer)
        self._indicator = QtWidgets.QFrame(self._footer)
        self._horizontal_layout_6 = QtWidgets.QHBoxLayout(self._indicator)
        self._busy_indicator = QtWidgets.QLabel(self._indicator)
        self._find_butt = QtWidgets.QPushButton(self._footer)
        self._clear_all = QtWidgets.QPushButton(self._footer)
        self._movie = QMovie(working_gif)

        self._setup_ui()
        self._init_slots()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Mouse click event, recording
        the coordinates of the click
        :param event: Click event
        :return: None
        """
        self._click_position = event.globalPos()

    @QtCore.pyqtSlot()
    def _map_by_name(self):
        """
        Emits a signal to install a new map through a UI text string
        :return: None
        """
        name = self._find_name_line.text()
        self._find_name_line.setText('')

        if name == '':
            self._map_error('Empty name')
            return

        self.search_objects.emit(name)

    @QtCore.pyqtSlot()
    def _show_indicator(self):
        """
        Display operating indicator
        :return: None
        """
        self._busy_indicator.setHidden(False)
        self._movie.start()

    @QtCore.pyqtSlot()
    def _hide_indicator(self):
        """
        Hide operating indicator
        :return: None
        """
        self._movie.stop()
        self._busy_indicator.setHidden(True)

    @QtCore.pyqtSlot()
    def _close_app(self):
        """
        Closes the application
        by pressing the button
        :return: None
        """
        self.close()

    @QtCore.pyqtSlot()
    def _minimize_app(self):
        """
        Minimizes the application
        by pressing the button
        :return: None
        """
        self.showMinimized()

    @QtCore.pyqtSlot()
    def _maximize_or_restore(self) -> None:
        """
        Event handler for pressing the
        "minimize" button
        Makes the window small
        or large relative to the current size
        :return: None
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    @QtCore.pyqtSlot(QtGui.QMouseEvent)
    def _move_window(self, event: QtGui.QMouseEvent) -> None:
        """
        Dragging the application window
        :param event: Dragging window event
        :return: None
        """
        self.move(self.pos() + event.globalPos() - self._click_position)
        self._click_position = event.globalPos()
        event.accept()

    def _map_error(self, warning_text: str):
        """
        Output an error to the user screen
        :param warning_text: Error text
        :return: None
        """
        QMessageBox.warning(self, "Some warning", warning_text)

    def _init_query_buttons(self):
        """
        Initialize slots for button press events
        :return: None
        """
        # Pressing these buttons (reserved requests) sends
        # a signal to set a new map, with found objects, in a limited area
        self._cafe.clicked.connect(lambda: self.search_objects.emit('cafe'))
        self._fast_food.clicked.connect(lambda: self.search_objects.emit('fast_food'))
        self._restaurant.clicked.connect(lambda: self.search_objects.emit('restaurant'))
        self._bar.clicked.connect(lambda: self.search_objects.emit('bar'))
        self._cinema.clicked.connect(lambda: self.search_objects.emit('cinema'))
        self._fitness.clicked.connect(lambda: self.search_objects.emit('fitness'))
        self._meseum.clicked.connect(lambda: self.search_objects.emit('museum'))
        self._library.clicked.connect(lambda: self.search_objects.emit('library'))
        self._sup_market.clicked.connect(lambda: self.search_objects.emit('supermarket'))
        self._clothes.clicked.connect(lambda: self.search_objects.emit('clothes'))
        self._mall.clicked.connect(lambda: self.search_objects.emit('mall'))
        self._electronic.clicked.connect(lambda: self.search_objects.emit('electronic'))
        self._hospital.clicked.connect(lambda: self.search_objects.emit('hospital'))
        self._fuel.clicked.connect(lambda: self.search_objects.emit('fuel'))
        self._hotel.clicked.connect(lambda: self.search_objects.emit('hotel'))
        self._pharmacy.clicked.connect(lambda: self.search_objects.emit('pharmacy'))

        # Search by query in input field
        self._find_name_but.clicked.connect(self._map_by_name)

    def _init_slots(self):
        """
        Initializing slots for service UI signals
        :return: None
        """
        self._init_query_buttons()

        self._clear_all.clicked.connect(self._map.request_pure_map)
        self._find_butt.clicked.connect(self._map.request_nearest_object)
        self._map.some_error.connect(self._map_error)

        self.search_objects.connect(self._show_indicator)
        self._map.search_done.connect(self._hide_indicator)
        self.search_objects.connect(self._map.request_objects)

        # Init top right buttons
        self._close_button.clicked.connect(self._close_app)
        self._minimize.clicked.connect(self._minimize_app)
        self._maximaze.clicked.connect(self._maximize_or_restore)

        # Init drag and drop app
        self._head.mouseMoveEvent = self._move_window

    def _setup_ui(self):
        """
        Set up UI all elements
        :return: None
        """
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setObjectName("MainWindow")
        self.resize(1036, 730)
        self._central_widget.setObjectName("centralwidget")
        self._vertical_layout.setContentsMargins(0, 0, 0, 0)
        self._vertical_layout.setSpacing(0)
        self._vertical_layout.setObjectName("verticalLayout")
        self._head.setMinimumSize(QtCore.QSize(0, 60))
        self._head.setMaximumSize(QtCore.QSize(16777215, 60))
        self._head.setStyleSheet("background-color : #dcdcdd;")
        self._head.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._head.setFrameShadow(QtWidgets.QFrame.Raised)
        self._head.setObjectName("head")
        self._horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self._horizontal_layout.setSpacing(15)
        self._horizontal_layout.setObjectName("horizontalLayout")
        self._frame.setMinimumSize(QtCore.QSize(300, 35))
        self._frame.setMaximumSize(QtCore.QSize(300, 35))
        self._frame.setStyleSheet("QPushButton {\n"
                                 "    border: 2px solid #8f8f91;\n"
                                 "    border-radius: 6px;\n"
                                 "    background-color: #fff;\n"
                                 "    min-width: 80px;\n"
                                 "     max-width: 100px;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton::hover\n"
                                 "{\n"
                                 "    background-color: rgb(251, 253, 255);\n"
                                 "    border: 0px;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit{\n"
                                 "    border-radius: 6px;\n"
                                 "    border: 2px solid #8f8f91;\n"
                                 "    background-color: #fff;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit::hover{\n"
                                 "    border: 0px;\n"
                                 "}")
        self._frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._frame.setObjectName("frame")
        self._horizontal_layout_3.setContentsMargins(9, 0, 0, -1)
        self._horizontal_layout_3.setObjectName("horizontalLayout_3")
        self._find_name_line.setMinimumSize(QtCore.QSize(0, 30))
        self._find_name_line.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self._find_name_line.setFont(font)
        self._find_name_line.setInputMask("")
        self._find_name_line.setText("")
        self._find_name_line.setMaxLength(100)
        self._find_name_line.setAlignment(Qt.Qt.AlignCenter)
        self._find_name_line.setObjectName("find_name_line")
        self._horizontal_layout_3.addWidget(self._find_name_line, 0, Qt.Qt.AlignVCenter)
        self._find_name_but.setMinimumSize(QtCore.QSize(84, 30))
        self._find_name_but.setMaximumSize(QtCore.QSize(104, 25))
        self._find_name_but.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/map/target.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._find_name_but.setIcon(icon)
        self._find_name_but.setObjectName("find_name_but")
        self._horizontal_layout_3.addWidget(self._find_name_but)
        self._horizontal_layout.addWidget(self._frame, 0, Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
        self._title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._title.setFrameShadow(QtWidgets.QFrame.Raised)
        self._title.setObjectName("title")
        self._horizontal_layout_4.setContentsMargins(0, 0, 0, 0)
        self._horizontal_layout_4.setObjectName("horizontalLayout_4")
        self._title_icon.setText("")
        self._title_icon.setPixmap(QtGui.QPixmap(":/map/logo.png"))
        self._title_icon.setAlignment(Qt.Qt.AlignCenter)
        self._title_icon.setObjectName("title_icon")
        self._horizontal_layout_4.addWidget(self._title_icon, 0, Qt.Qt.AlignRight)
        font = QtGui.QFont()
        font.setPointSize(14)
        self._title_name.setFont(font)
        self._title_name.setAlignment(Qt.Qt.AlignCenter)
        self._title_name.setObjectName("title_name")
        self._horizontal_layout_4.addWidget(self._title_name, 0, Qt.Qt.AlignRight)
        self._horizontal_layout.addWidget(self._title, 0, Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        self._service_butt.setMaximumSize(QtCore.QSize(100, 16777215))
        self._service_butt.setStyleSheet("QPushButton{\n"
                                        "        border-radius: 5;\n"
                                        "        background-color : #dcdcdd;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton::hover\n"
                                        "{\n"
                                        "        background-color : #fff;\n"
                                        "}")
        self._service_butt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._service_butt.setFrameShadow(QtWidgets.QFrame.Raised)
        self._service_butt.setObjectName("service_butt")
        self._horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self._horizontal_layout_2.setObjectName("horizontalLayout_2")
        self._minimize.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self._minimize.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/map/min.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._minimize.setIcon(icon1)
        self._minimize.setIconSize(QtCore.QSize(24, 24))
        self._minimize.setObjectName("minimize")
        self._horizontal_layout_2.addWidget(self._minimize)
        self._maximaze.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self._maximaze.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/map/max.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._maximaze.setIcon(icon2)
        self._maximaze.setIconSize(QtCore.QSize(24, 24))
        self._maximaze.setObjectName("maximaze")
        self._horizontal_layout_2.addWidget(self._maximaze)
        self._close_button.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self._close_button.setStyleSheet("QPushButton{\n"
                                        "        border-radius: 5;\n"
                                        "        background-color : #dcdcdd;\n"
                                        "}\n"
                                        "QPushButton::hover\n"
                                        "{\n"
                                        "    background-color: rgb(255, 94, 91);\n"
                                        "}")
        self._close_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/map/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._close_button.setIcon(icon3)
        self._close_button.setIconSize(QtCore.QSize(24, 24))
        self._close_button.setObjectName("close_button")
        self._horizontal_layout_2.addWidget(self._close_button)
        self._horizontal_layout.addWidget(self._service_butt, 0, Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        self._vertical_layout.addWidget(self._head)
        self._body.setStyleSheet("QPushButton{\n"
                                "    background-color: rgb(222, 226, 230);\n"
                                "    border-radius: 15;\n"
                                "\n"
                                "}\n"
                                "QPushButton::hover\n"
                                "{\n"
                                "    background-color: rgb(220, 220, 221);\n"
                                "}\n"
                                "")
        self._body.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._body.setFrameShadow(QtWidgets.QFrame.Raised)
        self._body.setObjectName("body")
        self._vertical_layout_2.setContentsMargins(0, 0, 0, 0)
        self._vertical_layout_2.setSpacing(0)
        self._vertical_layout_2.setObjectName("verticalLayout_2")
        self._query_butt.setMinimumSize(QtCore.QSize(0, 80))
        self._query_butt.setMaximumSize(QtCore.QSize(16777215, 80))
        self._query_butt.setStyleSheet("QFrame {\n"
                                      "background-color: rgb(175, 182, 190);\n"
                                      "}")
        self._query_butt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._query_butt.setFrameShadow(QtWidgets.QFrame.Raised)
        self._query_butt.setObjectName("query_butt")
        self._vertical_layout_3.setContentsMargins(0, 0, 0, 0)
        self._vertical_layout_3.setSpacing(0)
        self._vertical_layout_3.setObjectName("verticalLayout_3")
        self._buttons.setMinimumSize(QtCore.QSize(0, 0))
        self._buttons.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self._buttons.setStyleSheet("QPushButton {\n"
                                   "    border: 2px solid #8f8f91;\n"
                                   "    border-radius: 6px;\n"
                                   "    background-color: #fff;\n"
                                   "    min-width: 80px;\n"
                                   "     max-width: 100px;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton::hover\n"
                                   "{\n"
                                   "    \n"
                                   "    background-color: rgb(251, 253, 255);\n"
                                   "    border: 0px;\n"
                                   "}\n"
                                   "\n"
                                   "QLineEdit{\n"
                                   "    border-radius: 6px;\n"
                                   "    border: 2px solid #8f8f91;\n"
                                   "\n"
                                   "}\n"
                                   "\n"
                                   "QFrame {\n"
                                   "    background-color : #dcdcdd;\n"
                                   "}")
        self._buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self._buttons.setObjectName("buttons")
        self._gridLayout.setContentsMargins(0, 0, 0, 0)
        self._gridLayout.setSpacing(9)
        self._gridLayout.setObjectName("gridLayout")
        self._cinema.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/map/film.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._cinema.setIcon(icon4)
        self._cinema.setObjectName("cinema")
        self._gridLayout.addWidget(self._cinema, 2, 2, 1, 1)
        self._hotel.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/map/hotel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._hotel.setIcon(icon5)
        self._hotel.setObjectName("hotel")
        self._gridLayout.addWidget(self._hotel, 2, 7, 1, 1)
        self._restaurant.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/map/rest.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._restaurant.setIcon(icon6)
        self._restaurant.setObjectName("restaurant")
        self._gridLayout.addWidget(self._restaurant, 2, 1, 1, 1)
        self._meseum.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/map/museum.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._meseum.setIcon(icon7)
        self._meseum.setObjectName("meseum")
        self._gridLayout.addWidget(self._meseum, 2, 3, 1, 1)
        self._cafe.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/map/cafe.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._cafe.setIcon(icon8)
        self._cafe.setObjectName("cafe")
        self._gridLayout.addWidget(self._cafe, 2, 0, 1, 1)
        self._electronic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/map/electro.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._electronic.setIcon(icon9)
        self._electronic.setObjectName("electronic")
        self._gridLayout.addWidget(self._electronic, 4, 5, 1, 1)
        self._sup_market.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/map/supermarket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._sup_market.setIcon(icon10)
        self._sup_market.setObjectName("sup_market")
        self._gridLayout.addWidget(self._sup_market, 2, 4, 1, 1)
        self._fitness.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/map/gym.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._fitness.setIcon(icon11)
        self._fitness.setObjectName("fitness")
        self._gridLayout.addWidget(self._fitness, 4, 2, 1, 1)
        self._fuel.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/map/gas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._fuel.setIcon(icon12)
        self._fuel.setObjectName("fuel")
        self._gridLayout.addWidget(self._fuel, 4, 6, 1, 1)
        self._library.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/map/book.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._library.setIcon(icon13)
        self._library.setObjectName("library")
        self._gridLayout.addWidget(self._library, 4, 3, 1, 1)
        self._bar.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/map/bar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._bar.setIcon(icon14)
        self._bar.setObjectName("bar")
        self._gridLayout.addWidget(self._bar, 4, 1, 1, 1)
        self._pharmacy.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/map/pharmacy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._pharmacy.setIcon(icon15)
        self._pharmacy.setObjectName("pharmacy")
        self._gridLayout.addWidget(self._pharmacy, 4, 7, 1, 1)
        self._clothes.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/map/clothes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._clothes.setIcon(icon16)
        self._clothes.setObjectName("clothes")
        self._gridLayout.addWidget(self._clothes, 4, 4, 1, 1)
        self._fast_food.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self._fast_food.setIcon(icon6)
        self._fast_food.setObjectName("fast_food")
        self._gridLayout.addWidget(self._fast_food, 4, 0, 1, 1)
        self._hospital.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/map/hospital.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._hospital.setIcon(icon17)
        self._hospital.setObjectName("hospital")
        self._gridLayout.addWidget(self._hospital, 2, 6, 1, 1)
        self._mall.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/map/mall.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._mall.setIcon(icon18)
        self._mall.setObjectName("mall")
        self._gridLayout.addWidget(self._mall, 2, 5, 1, 1)
        self._vertical_layout_3.addWidget(self._buttons)
        self._vertical_layout_2.addWidget(self._query_butt)

        self._vertical_layout_2.addWidget(self._map.get_view())

        self._footer.setMinimumSize(QtCore.QSize(0, 60))
        self._footer.setMaximumSize(QtCore.QSize(16777215, 60))
        self._footer.setStyleSheet("QPushButton {\n"
                                  "    border: 2px solid #8f8f91;\n"
                                  "    border-radius: 6px;\n"
                                  "    background-color: #fff;\n"
                                  "    min-width: 80px;\n"
                                  "     max-width: 100px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::hover\n"
                                  "{\n"
                                  "    \n"
                                  "    background-color: rgb(251, 253, 255);\n"
                                  "    border: 0px;\n"
                                  "}\n"
                                  "\n"
                                  "QFrame {\n"
                                  "    background-color : #dcdcdd;\n"
                                  "}")
        self._footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self._footer.setObjectName("footer")
        self._horizontal_layout_5.setContentsMargins(9, 0, 9, 0)
        self._horizontal_layout_5.setSpacing(0)
        self._horizontal_layout_5.setObjectName("horizontalLayout_5")
        self._indicator.setMinimumSize(QtCore.QSize(60, 0))
        self._indicator.setMaximumSize(QtCore.QSize(50, 16777215))
        self._indicator.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._indicator.setFrameShadow(QtWidgets.QFrame.Raised)
        self._indicator.setObjectName("indicator")
        self._horizontal_layout_6.setContentsMargins(0, 0, 0, 0)
        self._horizontal_layout_6.setSpacing(0)
        self._horizontal_layout_6.setObjectName("horizontalLayout_6")
        self._busy_indicator.setText("")
        self._busy_indicator.setObjectName("busy_indicator")
        self._horizontal_layout_6.addWidget(self._busy_indicator)

        self._busy_indicator.setMovie(self._movie)
        self._busy_indicator.movie().setScaledSize(QtCore.QSize(55, 55))

        self._horizontal_layout_5.addWidget(self._indicator, 0, Qt.Qt.AlignLeft)
        self._find_butt.setMinimumSize(QtCore.QSize(84, 50))
        self._find_butt.setMaximumSize(QtCore.QSize(104, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self._find_butt.setFont(font)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/map/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._find_butt.setIcon(icon19)
        self._find_butt.setIconSize(QtCore.QSize(24, 24))
        self._find_butt.setObjectName("find_butt")
        self._horizontal_layout_5.addWidget(self._find_butt, 0, Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        self._clear_all.setMinimumSize(QtCore.QSize(84, 50))
        self._clear_all.setMaximumSize(QtCore.QSize(104, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self._clear_all.setFont(font)
        self._clear_all.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/map/erase.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._clear_all.setIcon(icon20)
        self._clear_all.setIconSize(QtCore.QSize(24, 24))
        self._clear_all.setObjectName("clear_all")
        self._horizontal_layout_5.addWidget(self._clear_all, 0, Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        self._vertical_layout_2.addWidget(self._footer)
        self._vertical_layout.addWidget(self._body)
        self.setCentralWidget(self._central_widget)

        self._translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _translate_ui(self):
        """
        Set text in some UI elements
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self._find_name_but.setText(_translate("MainWindow", "Find"))
        self._title_name.setText(_translate("MainWindow", "Map Target"))
        self._cinema.setText(_translate("MainWindow", "cinema"))
        self._hotel.setText(_translate("MainWindow", "hotel"))
        self._restaurant.setText(_translate("MainWindow", "restaurant"))
        self._meseum.setText(_translate("MainWindow", "museum"))
        self._cafe.setText(_translate("MainWindow", "cafe"))
        self._electronic.setText(_translate("MainWindow", "electronic"))
        self._sup_market.setText(_translate("MainWindow", "supermarket"))
        self._fitness.setText(_translate("MainWindow", "fitness"))
        self._fuel.setText(_translate("MainWindow", "fuel"))
        self._library.setText(_translate("MainWindow", "library"))
        self._bar.setText(_translate("MainWindow", "bar"))
        self._pharmacy.setText(_translate("MainWindow", "pharmacy"))
        self._clothes.setText(_translate("MainWindow", "clothes"))
        self._fast_food.setText(_translate("MainWindow", "fast food"))
        self._hospital.setText(_translate("MainWindow", "hospital"))
        self._mall.setText(_translate("MainWindow", "mall"))
        self._find_butt.setText(_translate("MainWindow", "Find"))
        self._clear_all.setText(_translate("MainWindow", "Clear All"))
