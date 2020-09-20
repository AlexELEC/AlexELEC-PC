# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2011-present AlexELEC (https://alexelec.tv)

import os
import re
import glob
import time
import xbmc
import xbmcgui
import oeWindows
import threading
import subprocess

class tvserver:

    ENABLED = False
    TVLINK_GET_SRC = None
    D_STREAMER = None
    D_TVH_DEBUG = None
    D_TVH_FEINIT = None
    D_TVH_TVLINK =None

    menu = {'91': {
        'name': 43000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 4300,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('tvserver::__init__', 'enter_function', 0)

            self.struct = {
                'oscam': {
                    'order': 1,
                    'name': 42020,
                    'not_supported': [],
                    'settings': {
                        'enable_oscam': {
                            'order': 1,
                            'name': 42021,
                            'value': '0',
                            'action': 'initialize_oscam',
                            'type': 'bool',
                            'InfoText': 4221,
                        },
                    },
                },
                'tvlink': {
                    'order': 2,
                    'name': 42025,
                    'not_supported': [],
                    'settings': {
                        'enable_tvlink': {
                            'order': 1,
                            'name': 42026,
                            'value': '0',
                            'action': 'initialize_tvlink',
                            'type': 'bool',
                            'InfoText': 4226,
                        },
                        'upd_tvlink': {
                            'order': 2,
                            'name': 42027,
                            'value': '0',
                            'action': 'update_tvlink',
                            'type': 'button',
                            'parent': {'entry': 'enable_tvlink','value': ['1']},
                            'InfoText': 4227,
                        },
                        'strm_tvlink': {
                            'order': 3,
                            'name': 42028,
                            'value': 'FFmpeg',
                            'values': ['FFmpeg', 'VLC'],
                            'action': 'initialize_tvlink',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_tvlink','value': ['1']},
                            'InfoText': 4228,
                        },
                    },
                },
                'tvheadend': {
                    'order': 3,
                    'name': 42030,
                    'not_supported': [],
                    'settings': {
                        'enable_tvheadend': {
                            'order': 1,
                            'name': 42031,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'InfoText': 4231,
                        },
                        'tvh_feinit': {
                            'order': 2,
                            'name': 42032,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 4232,
                        },
                        'tvh_tvlink': {
                            'order': 3,
                            'name': 42036,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 4236,
                        },
                        'tvh_debug': {
                            'order': 4,
                            'name': 42033,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 4233,
                        },
                        'tvh_xmltv': {
                            'order': 5,
                            'name': 42035,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 4235,
                        },
                    },
                },
            }

            self.oe = oeMain

            oeMain.dbg_log('tvserver::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('tvserver::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_oscam()
            self.initialize_tvlink()
            self.initialize_tvheadend()
            self.oe.dbg_log('tvserver::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('tvserver::stop_service', 'enter_function', 0)
            self.oe.dbg_log('tvserver::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('tvserver::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('tvserver::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('tvserver::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.oe.dbg_log('tvserver::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('tvserver::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('tvserver::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('tvserver::load_values', 'enter_function', 0)

            # OSCAM_DAEMON
            self.struct['oscam']['settings']['enable_oscam']['value'] = \
                    self.oe.get_service_state('oscam')

            # TVLINK
            self.struct['tvlink']['settings']['enable_tvlink']['value'] = \
                    self.oe.get_service_state('tvlink')

            self.struct['tvlink']['settings']['strm_tvlink']['value'] = \
            self.oe.get_service_option('tvlink', 'STREAMER', self.D_STREAMER).replace('"', '')

            # TVHEADEND
            self.struct['tvheadend']['settings']['enable_tvheadend']['value'] = \
                    self.oe.get_service_state('tvheadend')

            self.struct['tvheadend']['settings']['tvh_debug']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_DEBUG', self.D_TVH_DEBUG).replace('"', '')

            self.struct['tvheadend']['settings']['tvh_feinit']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_FEINIT', self.D_TVH_FEINIT).replace('"', '')

            self.struct['tvheadend']['settings']['tvh_tvlink']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_TVLINK', self.D_TVH_TVLINK).replace('"', '')

            self.oe.dbg_log('tvserver::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_oscam(self, **kwargs):
        try:
            self.oe.dbg_log('tvserver::initialize_oscam', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['oscam']['settings']['enable_oscam']['value'] == '1':
                state = 1
            self.oe.set_service('oscam', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('tvserver::initialize_oscam', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('tvserver::initialize_oscam', 'ERROR: (%s)' % repr(e), 4)

    def initialize_tvlink(self, **kwargs):
        try:
            self.oe.dbg_log('tvserver::initialize_tvlink', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['tvlink']['settings']['enable_tvlink']['value'] == '1':

                if not os.path.exists('/storage/.config/tvlink/tvlink.py'):
                    tvl_status = self.get_tvl_source()
                    if tvl_status == 'OK':
                        self.oe.notify(self.oe._(32363), 'Starting TVLINK...')
                    else:
                        self.struct['tvlink']['settings']['enable_tvlink']['value'] = '0'
                        self.oe.set_busy(0)
                        xbmcDialog = xbmcgui.Dialog()
                        answer = xbmcDialog.ok('Install TVLINK',
                            'Error: The program is not installed, try again.')
                        return
                options['STREAMER'] = '"%s"' % self.struct['tvlink']['settings']['strm_tvlink']['value']
                state = 1
            self.oe.set_service('tvlink', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('tvserver::initialize_tvlink', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('tvserver::initialize_tvlink', 'ERROR: (%s)' % repr(e), 4)

    def get_tvl_source(self, listItem=None, silent=False):
        try:
            self.oe.dbg_log('tvserver::get_tvl_source', 'enter_function', 0)
            tvl_url = self.oe.execute(self.TVLINK_GET_SRC + ' url', 1).strip()
            self.download_file = tvl_url
            self.oe.set_busy(0)
            if hasattr(self, 'download_file'):
                downloaded = self.oe.download_file(self.download_file, self.oe.TEMP + self.download_file.split('/')[-1], silent)
                if not downloaded is None:
                    self.oe.notify(self.oe._(32363), 'Install TVLINK...')
                    self.oe.set_busy(1)
                    self.oe.execute(self.TVLINK_GET_SRC + ' install', 0)
                    self.oe.set_busy(0)
                    self.oe.dbg_log('tvserver::get_tvl_source', 'exit_function', 0)
                    return 'OK'
            self.oe.dbg_log('tvserver::get_tvl_source', 'exit_function', 0)
            return 'ERROR'
        except Exception, e:
            self.oe.dbg_log('tvserver::get_tvl_source', 'ERROR: (%s)' % repr(e), 4)

    def update_tvlink(self, listItem=None):
        try:
            self.oe.dbg_log('tvserver::update_tvlink', 'enter_function', 0)
            if os.path.exists('/storage/.config/tvlink/tvlink.py'):
                self.oe.notify(self.oe._(32363), 'Check new version...')
                self.oe.set_busy(1)
                ver_update = self.oe.execute(self.TVLINK_GET_SRC + ' new', 1).strip()
                self.oe.set_busy(0)
                if not ver_update == 'NOT UPDATE':
                    self.oe.set_busy(1)
                    ver_current = self.oe.execute(self.TVLINK_GET_SRC + ' old', 1).strip()
                    self.oe.set_busy(0)
                    dialog = xbmcgui.Dialog()
                    ret = dialog.yesno('Update TVLINK?', ' ', 'Current version:  %s' % ver_current,
                                                              'Update  version:  %s' % ver_update)
                    if ret:
                        self.oe.set_busy(1)
                        self.oe.execute('systemctl stop tvlink.service', 0)
                        self.oe.execute(self.TVLINK_GET_SRC + ' backup', 0)
                        tvl_status = self.get_tvl_source()
                        self.oe.set_busy(0)
                        if tvl_status == 'OK':
                            self.oe.notify(self.oe._(32363), 'Run TVLINK version: %s ...' % ver_update)
                        else:
                            self.oe.notify(self.oe._(32363), 'Updates is not installed, try again.')
                        self.oe.execute(self.TVLINK_GET_SRC + ' restore', 0)
                        self.oe.execute('systemctl start tvlink.service', 0)
                else:
                    self.oe.notify(self.oe._(32363), 'No updates available.')

        except Exception, e:
            self.oe.dbg_log('tvserver::update_tvlink', 'ERROR: (' + repr(e) + ')')

    def initialize_tvheadend(self, **kwargs):
        try:
            self.oe.dbg_log('tvserver::initialize_tvheadend', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['tvheadend']['settings']['enable_tvheadend']['value'] == '1':
                state = 1
                options['TVH_DEBUG']    = '"%s"' % self.struct['tvheadend']['settings']['tvh_debug']['value']
                options['TVH_FEINIT'] = '"%s"' % self.struct['tvheadend']['settings']['tvh_feinit']['value']
                options['TVH_TVLINK'] = '"%s"' % self.struct['tvheadend']['settings']['tvh_tvlink']['value']
                if self.struct['tvheadend']['settings']['tvh_xmltv']['value'] == '1':
                    self.oe.execute('rm -f /storage/.config/tvheadend/xmltv.data/*.upload', 0)
                    self.struct['tvheadend']['settings']['tvh_xmltv']['value'] = '0'
            self.oe.set_service('tvheadend', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('tvserver::initialize_tvheadend', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('tvserver::initialize_tvheadend', 'ERROR: (%s)' % repr(e), 4)

    def exit(self):
        try:
            self.oe.dbg_log('tvserver::exit', 'enter_function', 0)
            self.oe.dbg_log('tvserver::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvserver::exit', 'ERROR: (%s)' % repr(e), 4)
