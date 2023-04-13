# -*- coding: utf-8 -*-
import os
import six
from BQt import QtCore, QtGui, QtSvg, QtWidgets

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            if not item:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())


def display_executing_indicator(text=None):
    import functools
    from component.toast import ToastWidget

    def outer_wrapper(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            toast = None
            try:
                if text and isinstance(args[0], QtWidgets.QWidget):
                    toast = ToastWidget(parent=args[0])
                    toast.showText(text=text, duration=100000000)
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

                return func(*args, **kwargs)
            except Exception as e:
                # It prints out all the traceback in the console
                print(e)
                raise

            finally:
                if toast:
                    toast.deleteLater()
                QtWidgets.QApplication.restoreOverrideCursor()
        return wrapper

    return outer_wrapper

def register_event(event=-1):
    # type: (int) -> int
    event += QtCore.QEvent.User + 5000
    return QtCore.QEvent.registerEventType(event)

def get_icon(path, color="auto", size=None):
    """
    return QIcon from the given filename(supported image format and svg)

    :param path: icon file path(png, jpg, svg, etc...)
    :param color: QColor, color(int, str, list of rgb), widget, "auto", "src"
    :param size: QSize or list of width and height
    :return:
    """
    return QtGui.QIcon(get_pixmap(path, color, size))

def get_pixmap(path, color="auto", size=None):
    """
    return QPixmap from the given filename(supported image format and svg)

    :param path: icon file path(png, jpg, svg, etc...)
    :param color: QColor, color(int, str, list of rgb), widget, "auto"
    :param size: QSize or list of width and height
    :return:
    """

    if not os.path.isfile(path):
        raise ValueError(path)

    if isinstance(size, QtCore.QSize):
        pass
    elif isinstance(size, (list, tuple)):
        size = QtCore.QSize(size[0], size[1])

    if isinstance(color, QtGui.QColor):
        pass
    elif color == "auto":
        color = QtWidgets.QApplication.palette().text().color()
    elif isinstance(color, six.string_types):
        color = QtGui.QColor(color)
    elif isinstance(color, int):
        color = QtGui.QColor(color)
    elif isinstance(color, list):
        color = QtGui.QColor(color[0], color[1], color[2])
    elif isinstance(color, QtWidgets.QWidget):
        widget = color
        is_enabled = widget.isEnabled()
        if not is_enabled:
            widget.setEnabled(True)
        color = widget.palette().text().color()
        if not is_enabled:
            widget.setEnabled(is_enabled)

    if path.endswith("svg"):
        svg = QtSvg.QSvgRenderer(path)

        if not size:
            size = svg.defaultSize()

        img = QtGui.QImage(size, QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter()
        painter.begin(img)

        if not color:
            color = QtWidgets.QApplication.palette().text().color()

        if color:
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            painter.fillRect(img.rect(), color)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOut)
        svg.render(painter)
        if color:
            painter.fillRect(img.rect(), color)
        painter.end()
        pixmap = QtGui.QPixmap.fromImage(img)

    else:
        img = QtGui.QImage(path)
        if size:
            img = img.scaled(size)
        if color:
            img = img.convertToFormat(QtGui.QImage.Format_Indexed8)
            if img.depth() in [1, 8]:
                for index in range(img.colorCount()):
                    src_color = QtGui.QColor.fromRgba(img.color(index))
                    img.setColor(index, QtGui.QColor(color.red(), color.green(), color.blue(),
                                                     src_color.alpha()).rgba())
            else:
                for row in range(img.height()):
                    # print img.scanLine(row)
                    # print len(img.scanLine(row))
                    # help(img.scanLine(row))
                    # for pix in img.scanLine(row):
                    #     print pix
                    for col in range(img.width()):
                        src_color = QtGui.QColor.fromRgba(img.pixel(col, row))
                        if not src_color.alpha():
                            continue
                        img.setPixel(col, row, color.rgb())

        pixmap = QtGui.QPixmap.fromImage(img)

    return pixmap
