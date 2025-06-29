#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.2
# Email : muyanru345@163.com
###################################################################
"""
Custom Stylesheet for QSpinBox, QDoubleSpinBox, QDateTimeEdit, QDateEdit, QTimeEdit.
Only add size arg for their __init__.
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from PySide6 import QtCore
from PySide6 import QtWidgets

# Import local modules
from .mixin import cursor_mixin


@cursor_mixin
class MSpinBox(QtWidgets.QSpinBox):
    """
    MSpinBox just use stylesheet and add dayu_size. No more extend.
    Property:
        dayu_size: The height of MSpinBox
    """

    def __init__(self, parent=None):
        from . import dayu_theme

        super(MSpinBox, self).__init__(parent=parent)
        self._dayu_size = dayu_theme.default_size

    def get_dayu_size(self):
        """
        Get the MSpinBox height
        :return: integer
        """
        return self._dayu_size

    def set_dayu_size(self, value):
        """
        Set the MSpinBox size.
        :param value: integer
        :return: None
        """
        self._dayu_size = value
        self.style().polish(self)

    dayu_size = QtCore.Property(int, get_dayu_size, set_dayu_size)

    def huge(self):
        """Set MSpinBox to huge size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.huge)
        return self

    def large(self):
        """Set MSpinBox to large size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.large)
        return self

    def medium(self):
        """Set MSpinBox to  medium"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.medium)
        return self

    def small(self):
        """Set MSpinBox to small size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.small)
        return self

    def tiny(self):
        """Set MSpinBox to tiny size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.tiny)
        return self


@cursor_mixin
class MDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    """
    MDoubleSpinBox just use stylesheet and add dayu_size. No more extend.
    Property:
        dayu_size: The height of MDoubleSpinBox
    """

    def __init__(self, parent=None):
        from . import dayu_theme

        super(MDoubleSpinBox, self).__init__(parent=parent)
        self._dayu_size = dayu_theme.default_size

    def get_dayu_size(self):
        """
        Get the MDoubleSpinBox height
        :return: integer
        """
        return self._dayu_size

    def set_dayu_size(self, value):
        """
        Set the MDoubleSpinBox size.
        :param value: integer
        :return: None
        """
        self._dayu_size = value
        self.style().polish(self)

    dayu_size = QtCore.Property(int, get_dayu_size, set_dayu_size)

    def huge(self):
        """Set MDoubleSpinBox to huge size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.huge)
        return self

    def large(self):
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.large)
        return self

    def medium(self):
        """Set MDoubleSpinBox to  medium"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.medium)
        return self

    def small(self):
        """Set MDoubleSpinBox to small size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.small)
        return self

    def tiny(self):
        """Set MDoubleSpinBox to tiny size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.tiny)
        return self


@cursor_mixin
class MDateTimeEdit(QtWidgets.QDateTimeEdit):
    """
    MDateTimeEdit just use stylesheet and add dayu_size. No more extend.
    Property:
        dayu_size: The height of MDateTimeEdit
    """

    def __init__(self, datetime=None, parent=None):
        from . import dayu_theme

        if datetime is None:
            super(MDateTimeEdit, self).__init__(parent=parent)
        else:
            super(MDateTimeEdit, self).__init__(datetime, parent=parent)
        self._dayu_size = dayu_theme.default_size

    def get_dayu_size(self):
        """
        Get the MDateTimeEdit height
        :return: integer
        """
        return self._dayu_size

    def set_dayu_size(self, value):
        """
        Set the MDateTimeEdit size.
        :param value: integer
        :return: None
        """
        self._dayu_size = value
        self.style().polish(self)

    dayu_size = QtCore.Property(int, get_dayu_size, set_dayu_size)

    def huge(self):
        """Set MDateTimeEdit to huge size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.huge)
        return self

    def large(self):
        """Set MDateTimeEdit to large size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.large)
        return self

    def medium(self):
        """Set MDateTimeEdit to  medium"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.medium)
        return self

    def small(self):
        """Set MDateTimeEdit to small size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.small)
        return self

    def tiny(self):
        """Set MDateTimeEdit to tiny size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.tiny)
        return self


@cursor_mixin
class MDateEdit(QtWidgets.QDateEdit):
    """
    MDateEdit just use stylesheet and add dayu_size. No more extend.
    Property:
        dayu_size: The height of MDateEdit
    """

    def __init__(self, date=None, parent=None):
        from . import dayu_theme

        if date is None:
            super(MDateEdit, self).__init__(parent=parent)
        else:
            super(MDateEdit, self).__init__(date, parent=parent)
            
        self._dayu_size = dayu_theme.default_size

    def get_dayu_size(self):
        """
        Get the MDateEdit height
        :return: integer
        """
        return self._dayu_size

    def set_dayu_size(self, value):
        """
        Set the MDateEdit size.
        :param value: integer
        :return: None
        """
        self._dayu_size = value
        self.style().polish(self)

    dayu_size = QtCore.Property(int, get_dayu_size, set_dayu_size)

    def huge(self):
        """Set MDateEdit to huge size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.huge)
        return self

    def large(self):
        """Set MDateEdit to large size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.large)
        return self

    def medium(self):
        """Set MDateEdit to  medium"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.medium)
        return self

    def small(self):
        """Set MDateEdit to small size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.small)
        return self

    def tiny(self):
        """Set MDateEdit to tiny size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.tiny)
        return self


@cursor_mixin
class MTimeEdit(QtWidgets.QTimeEdit):
    """
    MTimeEdit just use stylesheet and add dayu_size. No more extend.
    Property:
        dayu_size: The height of MTimeEdit
    """

    def __init__(self, time=None, parent=None):
        from . import dayu_theme

        if time is None:
            super(MTimeEdit, self).__init__(parent=parent)
        else:
            super(MTimeEdit, self).__init__(time, parent=parent)
        self._dayu_size = dayu_theme.default_size

    def get_dayu_size(self):
        """
        Get the MTimeEdit height
        :return: integer
        """
        return self._dayu_size

    def set_dayu_size(self, value):
        """
        Set the MTimeEdit size.
        :param value: integer
        :return: None
        """
        self._dayu_size = value
        self.style().polish(self)

    dayu_size = QtCore.Property(int, get_dayu_size, set_dayu_size)

    def huge(self):
        """Set MTimeEdit to huge size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.huge)
        return self

    def large(self):
        """Set MTimeEdit to large size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.large)
        return self

    def medium(self):
        """Set MTimeEdit to  medium"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.medium)
        return self

    def small(self):
        """Set MTimeEdit to small size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.small)
        return self

    def tiny(self):
        """Set MTimeEdit to tiny size"""
        from . import dayu_theme

        self.set_dayu_size(dayu_theme.tiny)
        return self
