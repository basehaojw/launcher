#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import getpass
import platform
import subprocess
from BQt import QtCore, QtGui, QtWidgets
LAUNCHER_DIR =(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(LAUNCHER_DIR)

from dayu_widgets import MPushButton, MToolButton, dayu_theme
from dayu_widgets.mixin import hover_shadow_mixin

from ui.util import display_executing_indicator


class Line(QtWidgets.QLabel):
    def __init__(self):
        super(Line, self).__init__()

    def paintEvent(self, event):
        super(Line, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(100, 100, 100))
        painter.setPen(pen)

        if self.text() == '':
            start = 0
        else:
            font_metrics = QtGui.QFontMetrics(self.font())
            start = font_metrics.width(self.text() + '   ')

        painter.drawLine(
            QtCore.QPoint(start, self.height() / 2),
            QtCore.QPoint(self.width(), self.height() / 2)
        )

@hover_shadow_mixin
class CardWidget(QtWidgets.QFrame):
    open_clicked_signal = QtCore.pyqtSignal()

    def __init__(self,
                 parent=None,
                 app_list=None,
                 app_full_list=None,
                 context=None,
                 ):
        """
        :param parent:
        :param app_list: put how many app versions in this list
        :param app_full_list: include all apps information
        :param context: project environment
        """
        super(CardWidget, self).__init__(parent)

        self.app_icon = os.path.join(LAUNCHER_DIR, str(app_full_list[0]['icon_path']))
        self.app_name = str(app_full_list[0]['name'])
        self.app_label_name = str(app_full_list[0]['label_name'])
        self.app_version = str(app_full_list[0]['version'])
        self.app_list = app_list
        self.app_full_list = app_full_list
        self.context = context
        self.btn_parent = parent
        self.meta = {}
        # self.icon_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.icon_dir = LAUNCHER_DIR

        self.init_ui()
        self.set_signal()

    def init_ui(self):
        self.setObjectName('TsCardWidget')
        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.set_info_ui())
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.add_line())
        self.main_layout.addLayout(self.set_button_ui())

        self.setLayout(self.main_layout)

        self.setStyleSheet("""
        QWidget#TsCardWidget{
            border-radius:3px;
            border:1px solid rgb(70, 70, 70);
            background-color:rgb(60, 60, 60);
        }
        QLabel{
            background-color:transparent;
        }
        QToolButton#MoreButton::menu-indicator {
            image: None;
        }
        QPushButton#OpenButton{
            font-weight: 400;
            border-radius: 12%;
            padding: 1% 10%;
            outline:none;
        }
        """)
        self.setFixedWidth(250)
    def add_line(self):
        line_label = Line()
        line_label.setFixedHeight(2)

        return line_label
    
    def paintEvent(self, event):
        super(CardWidget, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(100, 100, 100))
        painter.setPen(pen)
        painter.drawLine(QtCore.QPoint(0, 200), QtCore.QPoint(250, 200))
    
    def set_info_ui(self):
        info_layout = QtWidgets.QHBoxLayout()

        icon = QtWidgets.QLabel()
        if os.path.exists(self.app_icon):
            pixmap = QtGui.QPixmap(self.app_icon)
            fitPixmap = pixmap.scaled(48, 48, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            icon.setPixmap(fitPixmap)
            icon.setStyleSheet("""
                margin-right: 8px;
            """
            )

        label_layout = QtWidgets.QVBoxLayout()
        self.name_label = QtWidgets.QLabel(self.app_label_name)
        self.version_label = QtWidgets.QLabel(self.app_version)

        self.name_label.setStyleSheet("""
        QLabel{
            font-size: 18px;
            font-weight:bold;
        }
        """)

        self.version_label.setStyleSheet("""
        QLabel{
            color:rgb(150, 150, 150, 255);
        }
        """)

        label_layout.addWidget(self.name_label)
        label_layout.addWidget(self.version_label)

        close_button_layout = QtWidgets.QVBoxLayout()
        self.close_button = MToolButton()
        svg_close_icon = os.path.join(self.icon_dir, 'icon/close_line.svg')
        self.close_button.set_dayu_svg(svg_close_icon)
        self.close_button.set_dayu_size(dayu_theme.tiny)

        close_button_layout.addWidget(self.close_button)
        close_button_layout.addStretch()

        info_layout.addWidget(icon)
        info_layout.addLayout(label_layout)
        info_layout.addStretch()

        return info_layout
    
    def set_button_ui(self):
        
        button_layout = QtWidgets.QHBoxLayout()

        self.help_button = MToolButton()
        self.help_button.setObjectName('HelpButton')
        svg_help_icon = os.path.join(self.icon_dir, 'icon/ic_school.svg')
        self.help_button.set_dayu_svg(svg_help_icon)
        self.help_button.setToolTip('Help document')
        self.help_button.setStyleSheet("""
        QToolTip{
            border: 1px solid #1E90FF;
            background:rgb(60, 60, 60);
        }            
        """)

        space_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.open_button = MPushButton()
        self.open_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.open_button.setObjectName('OpenButton')
        self.open_button.setText('Open')
        self.open_button.setMinimumSize(80, 30)

        self.more_version_button = MToolButton()
        self.more_version_button.setMinimumSize(20, 30)
        self.more_version_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.more_version_button.setObjectName('MoreButton')
        svg_more_icon = os.path.join(self.icon_dir, 'icon/ic_more_vert.svg')
        self.more_version_button.set_dayu_svg(svg_more_icon)

        self.refresh()

        button_layout.setSpacing(0)
        if self.get_wiki_url():
            button_layout.addWidget(self.help_button)
        button_layout.addItem(space_item)
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.more_version_button)

        return button_layout

    def refresh(self):
        showed_app_versions = self.set_app_menu()
        if len(showed_app_versions) > 0:
            self.version_label.setText(showed_app_versions[0])
        else:
            pass

    def set_app_menu(self):
        app_menu = QtWidgets.QMenu(self.more_version_button)
        showed_app_versions = []
        for app_version in self.app_list:
            act = QtWidgets.QMenu(app_version, self)
            app_menu.addMenu(act)
            open_act = QtWidgets.QAction('Open', self)
            setattr(open_act, 'version', app_version)
            act.addAction(open_act)
            act.addSeparator()

            open_act.triggered.connect(self.version_app_open_event)

            showed_app_versions.append(app_version)

        self.more_version_button.setMenu(app_menu)

        return showed_app_versions

    def set_signal(self):
        self.open_button.clicked.connect(self.main_open_event)
        self.help_button.clicked.connect(self.help_button_click)
        
    def help_button_click(self):
        # TODO: show help wiki
        # help_wiki_url = self.get_wiki_url() ## wiki_tab = QtWebEngineWidgets.QWebEngineView()
        # self.create_help_tab(help_wiki_url, app_name=self.app_label_name)
        print('{} help page~~~ 0.0'.format(self.app_name))
        pass
    
    def get_wiki_url(self):
        for current_app in self.app_full_list:
            current_wiki_url = current_app['wiki_url']
            return current_wiki_url

    #open default version
    def main_open_event(self):
        self.open_app(self.app_version)

    #open other version
    def version_app_open_event(self):
        app_version = str(self.sender().version)
        self.open_app(app_version)
    
    def get_cmd_list(self, app_version):

        cmd_list = []
        for current_app in self.app_full_list:
            if current_app['version'] == app_version:
                cmd_list.append(current_app['pre_exec'])
                break
        return cmd_list, current_app

    def exec_app(self, app_version):
        cmd_list, current_app = self.get_cmd_list(
            app_version=app_version,
        )
        cmd_list.append(current_app['exec_cmd'])
        if platform.system() == 'Windows':
            cmd = '&'.join(cmd_list).replace('\n', ' & ')
        else:
            cmd = ' && '.join(cmd_list)
        print('cmd--', cmd)
        subprocess.Popen(cmd, shell=True)
    
    @display_executing_indicator(text='app is loading...')
    def open_app(self, app_version):

        show = self.context.get_show_name()

        self.open_clicked_signal.emit()
        
        self.exec_app(app_version=app_version)
