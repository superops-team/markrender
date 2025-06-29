# -*- coding: utf-8 -*-
# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .splitter import MSplitter
from .tool_button import MToolButton
from .toast import MToast
from .text_edit import MTextEdit
from .tab_widget import MTabWidget
from .switch import MSwitch
from .spin_box import MTimeEdit
from .spin_box import MSpinBox
from .spin_box import MDoubleSpinBox
from .spin_box import MDateTimeEdit
from .spin_box import MDateEdit
from .slider import MSlider
from .sequence_file import MSequenceFile
from .radio_button import MRadioButton
from .push_button import MPushButton
from .progress_circle import MProgressCircle
from .progress_bar import MProgressBar
from .page import MPage
from .message import MMessage
from .menu_tab_widget import MMenuTabWidget
from .menu import MMenu
from .loading import MLoadingWrapper
from .loading import MLoading
from .line_tab_widget import MLineTabWidget
from .line_edit import MLineEdit
from .label import MLabel
from .item_view_set import MItemViewSet
from .item_view_full_set import MItemViewFullSet
from .item_view import MTreeView
from .item_view import MTableView
from .item_view import MListView
from .item_view import MBigView
from .item_model import MTableModel
from .item_model import MSortFilterModel
from .flow_layout import MFlowLayout
from .field_mixin import MFieldMixin
from .divider import MDivider
from .combo_box import MComboBox
from .collapse import MCollapse
from .check_box import MCheckBox
from .carousel import MCarousel
from .card import MMeta
from .card import MCard
from .button_group import MToolButtonGroup
from .button_group import MRadioButtonGroup
from .button_group import MPushButtonGroup
from .button_group import MCheckBoxGroup
from .browser import MDragFolderButton
from .browser import MDragFileButton
from .browser import MClickBrowserFolderToolButton
from .browser import MClickBrowserFolderPushButton
from .browser import MClickBrowserFileToolButton
from .browser import MClickBrowserFilePushButton
from .breadcrumb import MBreadcrumb
from .badge import MBadge
from .avatar import MAvatar
from .alert import MAlert
from .theme import MTheme


# Import built-in modules
import os
import sys


DEFAULT_STATIC_FOLDER = os.path.join(
    sys.modules[__name__].__path__[0], "static")
CUSTOM_STATIC_FOLDERS = []
# Import local modules


dayu_theme = MTheme("light", primary_color=MTheme.cyan)
# dayu_theme.default_size = dayu_theme.small
# dayu_theme = MTheme('light')

# Import local modules


__all__ = [
    "MAlert",
    "MAvatar",
    "MBadge",
    "MBreadcrumb",
    "MClickBrowserFilePushButton",
    "MClickBrowserFileToolButton",
    "MClickBrowserFolderPushButton",
    "MClickBrowserFolderToolButton",
    "MDragFileButton",
    "MDragFolderButton",
    "MCheckBoxGroup",
    "MPushButtonGroup",
    "MRadioButtonGroup",
    "MToolButtonGroup",
    "MCard",
    "MMeta",
    "MCarousel",
    "MCheckBox",
    "MCollapse",
    "MComboBox",
    "MDivider",
    "MFieldMixin",
    "MFlowLayout",
    "MSortFilterModel",
    "MTableModel",
    "MBigView",
    "MListView",
    "MTableView",
    "MTreeView",
    "MItemViewFullSet",
    "MItemViewSet",
    "MLabel",
    "MLineEdit",
    "MLineTabWidget",
    "MLoading",
    "MLoadingWrapper",
    "MMenu",
    "MMenuTabWidget",
    "MMessage",
    "MPage",
    "MProgressBar",
    "MProgressCircle",
    "MPushButton",
    "MRadioButton",
    "MSequenceFile",
    "MSlider",
    "MDateEdit",
    "MDateTimeEdit",
    "MDoubleSpinBox",
    "MSpinBox",
    "MTimeEdit",
    "MSwitch",
    "MTabWidget",
    "MTextEdit",
    "MToast",
    "MToolButton",
    "MSplitter",
]
