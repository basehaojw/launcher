#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import os, sys
import getpass

from item import CardWidget
from dayu_widgets import MCollapse, MTabWidget
from dayu_widgets import dayu_theme, MTheme
from dayu_widgets.theme_switcher import ThemeSwitcher

from BQt import  QtCore, QtGui, QtWidgets
from ui.component import FlowLayout
from ui.util import display_executing_indicator, clear_layout, register_event
from core.core import get_show_app_data, should_app_show, get_approved_shows, get_user_recent_show, get_show_description

SHOW_CHOSSER = None
SHOW_INFO_WIDGET = None

LAUNCHER_ICON = os.path.join(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))), "app_icon/task.png")

class CardView(QtWidgets.QWidget):
    def __init__(
            self,
            parent=None,
            typ=None,
            hide_icons=None,
            show_level_icons=None,
            label=None
    ):
        super(CardView, self).__init__(parent)
        self.view_parent = parent
        self.hide_icons = hide_icons  # Preset data
        self.show_level_icons = show_level_icons  # Preset data

        self.button_list = []
        self.lines = []

        self.label = label
        self.apps = []
        self.app_widgets = []
        self.setui()

    def setui(self):
        self.apps_tools_layout = FlowLayout(margin=3, spacing=20)
        self.setLayout(self.apps_tools_layout)
    
    def set_col_row(self):
        if self.apps is not []:
            new_app_list = {}
            for app_data in self.apps:
                app_name = app_data['name']
                should_show = should_app_show(app_data)
                if not should_show:
                    print ('not show data', app_data)
                    continue
                if app_name not in new_app_list:
                    new_app_list[app_name] = []
                new_app_list[app_name].append(app_data)
            for name, apps in new_app_list.items():
                apps.sort(key=lambda apps:apps['version'], reverse=True)
                default_app = None
                for app in apps:
                    if re.match('default.*',app['version']):
                        default_app = app
                        break
                if default_app:
                    apps.remove(default_app)
                    apps.insert(0, default_app)

                app_versions = [i['version'] for i in apps]
                print('app_versions:', app_versions)
                btn_card = CardWidget(
                    self,
                    app_list=app_versions,
                    app_full_list=apps,
                    context=SHOW_CHOSSER,
                )
                btn_card.open_clicked_signal.connect(self.menu_widget_opened)
                
                self.button_list.append(btn_card)
                self.apps_tools_layout.addWidget(btn_card)
    
    def menu_widget_opened(self):
        # self.view_parent.refresh_recent_apps()
        pass

    def refresh_apps(self):
        if self.label == 'Software':
            self.apps = get_show_app_data('software', SHOW_CHOSSER.get_show_name())
        else:
            return

        clear_layout(self.apps_tools_layout)
        self.button_list = []

        self.set_col_row()


class ShowInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ShowInfoWidget, self).__init__(parent)
        self.main_layout = QtWidgets.QGridLayout()
        
        self.description_label = QtWidgets.QLabel('Description:')
        self.description_label.setAlignment(QtCore.Qt.AlignTop)
        self.description = QtWidgets.QLabel()

        self.description_label.setFixedWidth(97)
        self.description_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.description.setMinimumHeight(24)
        self.description.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        self.description.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.description.setWordWrap(True)

        self.main_layout.setColumnStretch(0, False)
        
        self.main_layout.addWidget(self.description_label, 1, 0)
        self.main_layout.addWidget(self.description, 1, 1)
        
        self.setLayout(self.main_layout)

    def clear_text(self):
        self.description.clear()


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        self.selectAll()

def spacer():
    return QtWidgets.QSpacerItem(420, 5)

class ShowChooser(QtWidgets.QWidget):
    show_changed_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(ShowChooser, self).__init__(parent)
        self.main_layout = QtWidgets.QGridLayout()
        self.show_label = QtWidgets.QLabel('Show')
        self.show_widget = QtWidgets.QComboBox()

        self.show_widget.setEditable(True)
        self.show_widget.setLineEdit(LineEdit())
        
        self.main_layout.addWidget(self.show_label, 0, 1)
        self.main_layout.addWidget(self.show_widget, 0, 2)
        self.main_layout.addItem(spacer(), 0, 3)
        self.setLayout(self.main_layout)

        # initial widgets
        show_list = list(get_approved_shows())
        show_list.sort()
        self.show_widget.addItems(show_list)

        # connects
        self.show_widget.currentIndexChanged.connect(self.show_changed)

    def show_changed(self):
        show = str(self.show_widget.currentText())
        if show:
            self.show_changed_signal.emit(show)

    def get_show_name(self):
        return str(self.show_widget.currentText())


class Window(QtWidgets.QMainWindow):
    """The main window of this software"""
    RESET_EVENT = register_event(1009)
    def __init__(self):
        super(Window, self).__init__()
        global MAIN_WINDOW
        MAIN_WINDOW = self

        self.setWindowIcon(QtGui.QIcon(LAUNCHER_ICON))

        self.setObjectName("launcher")

        self.central_widget = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QVBoxLayout()
        self.show_layout = QtWidgets.QHBoxLayout()
        self.show_chooser = ShowChooser(parent=self)
        self.show_info_widget = ShowInfoWidget()

        global SHOW_CHOSSER
        global SHOW_INFO_WIDGET

        SHOW_CHOSSER = self.show_chooser
        SHOW_INFO_WIDGET = self.show_info_widget

        self.app_chooser_layout = QtWidgets.QVBoxLayout()
        self.app_chooser_widget = MTabWidget(self)
        # self.app_chooser_widget.setTabsClosable(True)

        self.apps_widget_list = []

        self.setui()
        self.init_ui()

    @display_executing_indicator(text='show are loading...')
    def setui(self):
        self.setWindowTitle("Launcher")
        self.resize(520, 420)
        frame = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        self.show_layout.addWidget(self.show_chooser)
        self.app_chooser_layout.addWidget(self.app_chooser_widget)
        self.central_layout.addLayout(self.show_layout)
        self.central_layout.addWidget(self.show_info_widget)
        self.central_layout.addWidget(self.app_chooser_widget)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
    
    @display_executing_indicator(text='Launcher apps are loading...')
    def init_ui(self):
        section_list = []
        for title_label in ['Software']:
            apps_widget = CardView(label=title_label, parent=self)
            section_list.append({
                'title': title_label,
                'expand': True,
                'widget': apps_widget
            })
            self.apps_widget_list.append(apps_widget)
        
        self.collapse_widget = MCollapse()
        self.collapse_widget.add_section_list(section_list)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.collapse_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)

        self.app_chooser_widget.addTab(self.scroll_area, u'Apps')
        self.set_description()

        self.show_chooser.show_changed_signal.connect(self.show_changed)
        show = get_user_recent_show(getpass.getuser())
        if show:
            index = self.show_chooser.show_widget.findText(show)
            self.show_chooser.show_widget.setCurrentIndex(index)
            self.show_changed()

    def show_apps(self):
        for apps_widget in self.apps_widget_list:
            apps_widget.refresh_apps()

    @display_executing_indicator(text='loading...')
    def show_changed(self, *args):

        show = str(self.show_chooser.show_widget.currentText())
        if not show:
            return
        self.refresh_from_show()
        self.set_description()

    def refresh_from_show(self):
        show = str(self.show_chooser.show_widget.currentText())
        if not show:
            return
        for apps_widget in self.apps_widget_list:
            apps_widget.refresh_apps()

    def set_description(self):
        show = str(self.show_chooser.show_widget.currentText())
        description = get_show_description(show)
        if not description:
            description = ''
        self.show_info_widget.description.setText(description)

def main(args):
    app = QtWidgets.QApplication(args)
    win = Window()
    win.show()
    win.show_apps()
    dayu_theme.set_primary_color(MTheme.blue)
    dayu_theme.apply(win)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
