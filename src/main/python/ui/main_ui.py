"""
Module that implements the basic UI class
"""

# Third party imports
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QMovie, QColor

# Local application imports
from src.main.python.ui.map_ui import MapUI
from src.main.python.json_connector import JsonConnector
# Doesn't remove this, it's icons import
import src.main.python.ui.icons


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

        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.head = QtWidgets.QFrame(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.head)
        self.frame = QtWidgets.QFrame(self.head)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.find_name_line = QtWidgets.QLineEdit(self.frame)
        self.find_name_but = QtWidgets.QPushButton(self.frame)
        self.title = QtWidgets.QFrame(self.head)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.title)
        self.title_icon = QtWidgets.QLabel(self.title)
        self.title_name = QtWidgets.QLabel(self.title)
        self.service_butt = QtWidgets.QFrame(self.head)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.service_butt)
        self.minimize = QtWidgets.QPushButton(self.service_butt)
        self.maximaze = QtWidgets.QPushButton(self.service_butt)
        self.close = QtWidgets.QPushButton(self.service_butt)
        self.body = QtWidgets.QFrame(self.centralwidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.body)
        self.query_butt = QtWidgets.QFrame(self.body)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.query_butt)
        self.buttons = QtWidgets.QFrame(self.query_butt)
        self.gridLayout = QtWidgets.QGridLayout(self.buttons)
        self.cinema = QtWidgets.QPushButton(self.buttons)
        self.hotel = QtWidgets.QPushButton(self.buttons)
        self.restaurant = QtWidgets.QPushButton(self.buttons)
        self.meseum = QtWidgets.QPushButton(self.buttons)
        self.cafe = QtWidgets.QPushButton(self.buttons)
        self.electronic = QtWidgets.QPushButton(self.buttons)
        self.sup_market = QtWidgets.QPushButton(self.buttons)
        self.fitness = QtWidgets.QPushButton(self.buttons)
        self.fuel = QtWidgets.QPushButton(self.buttons)
        self.library = QtWidgets.QPushButton(self.buttons)
        self.bar = QtWidgets.QPushButton(self.buttons)
        self.pharmacy = QtWidgets.QPushButton(self.buttons)
        self.clothes = QtWidgets.QPushButton(self.buttons)
        self.fast_food = QtWidgets.QPushButton(self.buttons)
        self.hospital = QtWidgets.QPushButton(self.buttons)
        self.mall = QtWidgets.QPushButton(self.buttons)

        self._map = ui_map

        self.footer = QtWidgets.QFrame(self.body)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.footer)
        self.indicator = QtWidgets.QFrame(self.footer)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.indicator)
        self.busy_indicator = QtWidgets.QLabel(self.indicator)
        self.find_butt = QtWidgets.QPushButton(self.footer)
        self.clear_all = QtWidgets.QPushButton(self.footer)
        self.movie = QMovie(working_gif)

        self._setup_ui()
        self._init_slots()

    def _map_error(self, warning_text: str):
        """
        Output an error to the user screen
        :param warning_text: Error text
        :return: None
        """
        QMessageBox.warning(self, "Some warning", warning_text)

    def _map_by_name(self):
        """
        Emits a signal to install a new map through a UI text string
        :return: None
        """
        name = self.find_name_line.text()
        self.find_name_line.setText('')

        if name == '':
            self._map_error('Empty name')
            return

        self.search_objects.emit(name)

    def _show_indicator(self):
        """
        Display operating indicator
        :return: None
        """
        self.busy_indicator.setHidden(False)
        self.movie.start()

    def _hide_indicator(self):
        """
        Hide operating indicator
        :return: None
        """
        self.movie.stop()
        self.busy_indicator.setHidden(True)

    def _init_buttons(self):
        """
        Initialize slots for button press events
        :return: None
        """
        # Pressing these buttons (reserved requests) sends
        # a signal to set a new map, with found objects, in a limited area
        self.cafe.clicked.connect(lambda: self.search_objects.emit('cafe'))
        self.fast_food.clicked.connect(lambda: self.search_objects.emit('fast_food'))
        self.restaurant.clicked.connect(lambda: self.search_objects.emit('restaurant'))
        self.bar.clicked.connect(lambda: self.search_objects.emit('bar'))
        self.cinema.clicked.connect(lambda: self.search_objects.emit('cinema'))
        self.fitness.clicked.connect(lambda: self.search_objects.emit('fitness'))
        self.meseum.clicked.connect(lambda: self.search_objects.emit('museum'))
        self.library.clicked.connect(lambda: self.search_objects.emit('library'))
        self.sup_market.clicked.connect(lambda: self.search_objects.emit('supermarket'))
        self.clothes.clicked.connect(lambda: self.search_objects.emit('clothes'))
        self.mall.clicked.connect(lambda: self.search_objects.emit('mall'))
        self.electronic.clicked.connect(lambda: self.search_objects.emit('electronic'))
        self.hospital.clicked.connect(lambda: self.search_objects.emit('hospital'))
        self.fuel.clicked.connect(lambda: self.search_objects.emit('fuel'))
        self.hotel.clicked.connect(lambda: self.search_objects.emit('hotel'))
        self.pharmacy.clicked.connect(lambda: self.search_objects.emit('pharmacy'))

        # Search by query in input field
        self.find_name_but.clicked.connect(self._map_by_name)

    def _init_slots(self):
        """
        Initializing slots for service UI signals
        :return: None
        """
        self._init_buttons()

        self.clear_all.clicked.connect(self._map.request_pure_map)
        self.find_butt.clicked.connect(self._map.request_nearest_object)
        self._map.some_error.connect(self._map_error)

        self.search_objects.connect(self._show_indicator)
        self._map.search_done.connect(self._hide_indicator)
        self.search_objects.connect(self._map.request_objects)

    def _setup_ui(self):
        """
        Set up UI all elements
        :return: None
        """
        self.setObjectName("MainWindow")
        self.resize(1036, 730)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.head.setMinimumSize(QtCore.QSize(0, 60))
        self.head.setMaximumSize(QtCore.QSize(16777215, 60))
        self.head.setStyleSheet("background-color : #dcdcdd;")
        self.head.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.head.setFrameShadow(QtWidgets.QFrame.Raised)
        self.head.setObjectName("head")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame.setMinimumSize(QtCore.QSize(300, 35))
        self.frame.setMaximumSize(QtCore.QSize(300, 35))
        self.frame.setStyleSheet("QPushButton {\n"
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
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3.setContentsMargins(9, 0, 0, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.find_name_line.setMinimumSize(QtCore.QSize(0, 30))
        self.find_name_line.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.find_name_line.setFont(font)
        self.find_name_line.setInputMask("")
        self.find_name_line.setText("")
        self.find_name_line.setMaxLength(100)
        self.find_name_line.setAlignment(Qt.Qt.AlignCenter)
        self.find_name_line.setObjectName("find_name_line")
        self.horizontalLayout_3.addWidget(self.find_name_line, 0, Qt.Qt.AlignVCenter)
        self.find_name_but.setMinimumSize(QtCore.QSize(84, 30))
        self.find_name_but.setMaximumSize(QtCore.QSize(104, 25))
        self.find_name_but.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/map/target.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.find_name_but.setIcon(icon)
        self.find_name_but.setObjectName("find_name_but")
        self.horizontalLayout_3.addWidget(self.find_name_but)
        self.horizontalLayout.addWidget(self.frame, 0, Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
        self.title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title.setObjectName("title")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.title_icon.setText("")
        self.title_icon.setPixmap(QtGui.QPixmap(":/map/logo.png"))
        self.title_icon.setAlignment(Qt.Qt.AlignCenter)
        self.title_icon.setObjectName("title_icon")
        self.horizontalLayout_4.addWidget(self.title_icon, 0, Qt.Qt.AlignRight)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_name.setFont(font)
        self.title_name.setAlignment(Qt.Qt.AlignCenter)
        self.title_name.setObjectName("title_name")
        self.horizontalLayout_4.addWidget(self.title_name, 0, Qt.Qt.AlignRight)
        self.horizontalLayout.addWidget(self.title, 0, Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        self.service_butt.setMaximumSize(QtCore.QSize(100, 16777215))
        self.service_butt.setStyleSheet("QPushButton{\n"
                                        "        border-radius: 5;\n"
                                        "        background-color : #dcdcdd;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton::hover\n"
                                        "{\n"
                                        "        background-color : #fff;\n"
                                        "}")
        self.service_butt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.service_butt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.service_butt.setObjectName("service_butt")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.minimize.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self.minimize.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/map/min.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimize.setIcon(icon1)
        self.minimize.setIconSize(QtCore.QSize(24, 24))
        self.minimize.setObjectName("minimize")
        self.horizontalLayout_2.addWidget(self.minimize)
        self.maximaze.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self.maximaze.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/map/max.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.maximaze.setIcon(icon2)
        self.maximaze.setIconSize(QtCore.QSize(24, 24))
        self.maximaze.setObjectName("maximaze")
        self.horizontalLayout_2.addWidget(self.maximaze)
        self.close.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self.close.setStyleSheet("QPushButton{\n"
                                 "        border-radius: 5;\n"
                                 "        background-color : #dcdcdd;\n"
                                 "}\n"
                                 "QPushButton::hover\n"
                                 "{\n"
                                 "    background-color: rgb(255, 94, 91);\n"
                                 "}")
        self.close.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/map/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon3)
        self.close.setIconSize(QtCore.QSize(24, 24))
        self.close.setObjectName("close")
        self.horizontalLayout_2.addWidget(self.close)
        self.horizontalLayout.addWidget(self.service_butt, 0, Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.head)
        self.body.setStyleSheet("QPushButton{\n"
                                "    background-color: rgb(222, 226, 230);\n"
                                "    border-radius: 15;\n"
                                "\n"
                                "}\n"
                                "QPushButton::hover\n"
                                "{\n"
                                "    background-color: rgb(220, 220, 221);\n"
                                "}\n"
                                "")
        self.body.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.body.setObjectName("body")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.query_butt.setMinimumSize(QtCore.QSize(0, 80))
        self.query_butt.setMaximumSize(QtCore.QSize(16777215, 80))
        self.query_butt.setStyleSheet("QFrame {\n"
                                      "background-color: rgb(175, 182, 190);\n"
                                      "}")
        self.query_butt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.query_butt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.query_butt.setObjectName("query_butt")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.buttons.setMinimumSize(QtCore.QSize(0, 0))
        self.buttons.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.buttons.setStyleSheet("QPushButton {\n"
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
        self.buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttons.setObjectName("buttons")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(9)
        self.gridLayout.setObjectName("gridLayout")
        self.cinema.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/map/film.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cinema.setIcon(icon4)
        self.cinema.setObjectName("cinema")
        self.gridLayout.addWidget(self.cinema, 2, 2, 1, 1)
        self.hotel.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/map/hotel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hotel.setIcon(icon5)
        self.hotel.setObjectName("hotel")
        self.gridLayout.addWidget(self.hotel, 2, 7, 1, 1)
        self.restaurant.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/map/rest.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.restaurant.setIcon(icon6)
        self.restaurant.setObjectName("restaurant")
        self.gridLayout.addWidget(self.restaurant, 2, 1, 1, 1)
        self.meseum.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/map/museum.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.meseum.setIcon(icon7)
        self.meseum.setObjectName("meseum")
        self.gridLayout.addWidget(self.meseum, 2, 3, 1, 1)
        self.cafe.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/map/cafe.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cafe.setIcon(icon8)
        self.cafe.setObjectName("cafe")
        self.gridLayout.addWidget(self.cafe, 2, 0, 1, 1)
        self.electronic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/map/electro.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.electronic.setIcon(icon9)
        self.electronic.setObjectName("electronic")
        self.gridLayout.addWidget(self.electronic, 4, 5, 1, 1)
        self.sup_market.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/map/supermarket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sup_market.setIcon(icon10)
        self.sup_market.setObjectName("sup_market")
        self.gridLayout.addWidget(self.sup_market, 2, 4, 1, 1)
        self.fitness.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/map/gym.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fitness.setIcon(icon11)
        self.fitness.setObjectName("fitness")
        self.gridLayout.addWidget(self.fitness, 4, 2, 1, 1)
        self.fuel.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/map/gas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fuel.setIcon(icon12)
        self.fuel.setObjectName("fuel")
        self.gridLayout.addWidget(self.fuel, 4, 6, 1, 1)
        self.library.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/map/book.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.library.setIcon(icon13)
        self.library.setObjectName("library")
        self.gridLayout.addWidget(self.library, 4, 3, 1, 1)
        self.bar.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/map/bar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bar.setIcon(icon14)
        self.bar.setObjectName("bar")
        self.gridLayout.addWidget(self.bar, 4, 1, 1, 1)
        self.pharmacy.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/map/pharmacy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pharmacy.setIcon(icon15)
        self.pharmacy.setObjectName("pharmacy")
        self.gridLayout.addWidget(self.pharmacy, 4, 7, 1, 1)
        self.clothes.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/map/clothes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clothes.setIcon(icon16)
        self.clothes.setObjectName("clothes")
        self.gridLayout.addWidget(self.clothes, 4, 4, 1, 1)
        self.fast_food.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self.fast_food.setIcon(icon6)
        self.fast_food.setObjectName("fast_food")
        self.gridLayout.addWidget(self.fast_food, 4, 0, 1, 1)
        self.hospital.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/map/hospital.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hospital.setIcon(icon17)
        self.hospital.setObjectName("hospital")
        self.gridLayout.addWidget(self.hospital, 2, 6, 1, 1)
        self.mall.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/map/mall.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mall.setIcon(icon18)
        self.mall.setObjectName("mall")
        self.gridLayout.addWidget(self.mall, 2, 5, 1, 1)
        self.verticalLayout_3.addWidget(self.buttons)
        self.verticalLayout_2.addWidget(self.query_butt)

        self.verticalLayout_2.addWidget(self._map.get_view())

        self.footer.setMinimumSize(QtCore.QSize(0, 60))
        self.footer.setMaximumSize(QtCore.QSize(16777215, 60))
        self.footer.setStyleSheet("QPushButton {\n"
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
        self.footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout_5.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.indicator.setMinimumSize(QtCore.QSize(60, 0))
        self.indicator.setMaximumSize(QtCore.QSize(50, 16777215))
        self.indicator.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.indicator.setFrameShadow(QtWidgets.QFrame.Raised)
        self.indicator.setObjectName("indicator")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.busy_indicator.setText("")
        self.busy_indicator.setObjectName("busy_indicator")
        self.horizontalLayout_6.addWidget(self.busy_indicator)

        self.busy_indicator.setMovie(self.movie)
        self.busy_indicator.movie().setScaledSize(QtCore.QSize(55, 55))

        self.horizontalLayout_5.addWidget(self.indicator, 0, Qt.Qt.AlignLeft)
        self.find_butt.setMinimumSize(QtCore.QSize(84, 50))
        self.find_butt.setMaximumSize(QtCore.QSize(104, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.find_butt.setFont(font)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/map/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.find_butt.setIcon(icon19)
        self.find_butt.setIconSize(QtCore.QSize(24, 24))
        self.find_butt.setObjectName("find_butt")
        self.horizontalLayout_5.addWidget(self.find_butt, 0, Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        self.clear_all.setMinimumSize(QtCore.QSize(84, 50))
        self.clear_all.setMaximumSize(QtCore.QSize(104, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clear_all.setFont(font)
        self.clear_all.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/map/erase.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_all.setIcon(icon20)
        self.clear_all.setIconSize(QtCore.QSize(24, 24))
        self.clear_all.setObjectName("clear_all")
        self.horizontalLayout_5.addWidget(self.clear_all, 0, Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.footer)
        self.verticalLayout.addWidget(self.body)
        self.setCentralWidget(self.centralwidget)

        self._translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _translate_ui(self):
        """
        Set text in some UI elements
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.find_name_but.setText(_translate("MainWindow", "Find"))
        self.title_name.setText(_translate("MainWindow", "Map Target"))
        self.cinema.setText(_translate("MainWindow", "cinema"))
        self.hotel.setText(_translate("MainWindow", "hotel"))
        self.restaurant.setText(_translate("MainWindow", "restaurant"))
        self.meseum.setText(_translate("MainWindow", "museum"))
        self.cafe.setText(_translate("MainWindow", "cafe"))
        self.electronic.setText(_translate("MainWindow", "electronic"))
        self.sup_market.setText(_translate("MainWindow", "supermarket"))
        self.fitness.setText(_translate("MainWindow", "fitness"))
        self.fuel.setText(_translate("MainWindow", "fuel"))
        self.library.setText(_translate("MainWindow", "library"))
        self.bar.setText(_translate("MainWindow", "bar"))
        self.pharmacy.setText(_translate("MainWindow", "pharmacy"))
        self.clothes.setText(_translate("MainWindow", "clothes"))
        self.fast_food.setText(_translate("MainWindow", "fast food"))
        self.hospital.setText(_translate("MainWindow", "hospital"))
        self.mall.setText(_translate("MainWindow", "mall"))
        self.find_butt.setText(_translate("MainWindow", "Find"))
        self.clear_all.setText(_translate("MainWindow", "Clear All"))
