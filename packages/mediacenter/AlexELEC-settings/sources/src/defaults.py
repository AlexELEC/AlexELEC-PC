# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2009-2013 Stephan Raue (stephan@openelec.tv)
# Copyright (C) 2013 Lutz Fiebach (lufie@openelec.tv)

import os

################################################################################
# Base
################################################################################

XBMC_USER_HOME = os.environ.get('XBMC_USER_HOME', '/storage/.kodi')
CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '/storage/.cache')
USER_CONFIG = os.environ.get('USER_CONFIG', '/storage/.config')

BIN_DIR_EXT = '%s/addons/service.alexelec.settings/resources/bin' % XBMC_USER_HOME
BIN_DIR_INT = '/usr/share/kodi/addons/service.alexelec.settings/resources/bin'
SCRIPT_DIR = lambda : (BIN_DIR_EXT if os.path.exists(BIN_DIR_EXT) else BIN_DIR_INT)

################################################################################
# Connamn Module
################################################################################

connman = {
    'CONNMAN_DAEMON': '/usr/sbin/connmand',
    'WAIT_CONF_FILE': '%s/libreelec/network_wait' % CONFIG_CACHE,
    'ENABLED': lambda : (True if os.path.exists(connman['CONNMAN_DAEMON']) and not os.path.exists('/dev/.kernel_ipconfig') else False),
    }
connman['ENABLED'] = connman['ENABLED']()

################################################################################
# Bluez Module
################################################################################

bluetooth = {
    'BLUETOOTH_DAEMON': '/usr/lib/bluetooth/bluetoothd',
    'OBEX_DAEMON': '/usr/lib/bluetooth/obexd',
    'ENABLED': lambda : (True if os.path.exists(bluetooth['BLUETOOTH_DAEMON']) else False),
    'D_OBEXD_ROOT': '/storage/downloads/',
    }
bluetooth['ENABLED'] = bluetooth['ENABLED']()

################################################################################
# Service Module
################################################################################

services = {
    'ENABLED': True,
    'KERNEL_CMD': '/proc/cmdline',
    'SAMBA_NMDB': '/usr/sbin/nmbd',
    'SAMBA_SMDB': '/usr/sbin/smbd',
    'D_SAMBA_WORKGROUP': 'WORKGROUP',
    'D_SAMBA_SECURE': '0',
    'D_SAMBA_USERNAME': 'alexelec',
    'D_SAMBA_PASSWORD': 'alexelec',
    'D_SAMBA_MINPROTOCOL': 'SMB1',
    'D_SAMBA_MAXPROTOCOL': 'SMB1',
    'D_SAMBA_AUTOSHARE': '1',
    'SSH_DAEMON': '/usr/sbin/sshd',
    'OPT_SSH_NOPASSWD': "-o 'PasswordAuthentication no'",
    'D_SSH_DISABLE_PW_AUTH': '0',
    'AVAHI_DAEMON': '/usr/sbin/avahi-daemon',
    'CRON_DAEMON': '/sbin/crond',
    }

system = {
    'ENABLED': True,
    'KERNEL_CMD': '/proc/cmdline',
    'SET_CLOCK_CMD': '/sbin/hwclock --systohc --utc',
    'XBMC_RESET_FILE': '%s/reset_xbmc' % CONFIG_CACHE,
    'LIBREELEC_RESET_FILE': '%s/reset_oe' % CONFIG_CACHE,
    'KEYBOARD_INFO': '/usr/share/X11/xkb/rules/base.xml',
    'UDEV_KEYBOARD_INFO': '%s/xkb/layout' % CONFIG_CACHE,
    'NOX_KEYBOARD_INFO': '/usr/lib/keymaps',
    'BACKUP_DIRS': [
        XBMC_USER_HOME,
        USER_CONFIG,
        CONFIG_CACHE,
        '/storage/.ssh',
        ],
    'BACKUP_DESTINATION': '/storage/backup/',
    'RESTORE_DIR': '/storage/.restore/',
    }

about = {'ENABLED': True}

xdbus = {'ENABLED': True}

tvserver = {
    'ENABLED'        : True,
    #TVHEADEND
    'D_TVH_DEBUG'    : '0',
    'D_TVH_FEINIT'   : '0',
    'D_TVH_TVLINK'   : '0',
    #TVLINK
    'TVLINK_GET_SRC' : "%s/tvlink-get.sh" % SCRIPT_DIR(),
    'D_STREAMER'     : 'FFmpeg',
    }

_services = {
    'sshd': ['sshd.service'],
    'avahi': ['avahi-daemon.service'],
    'samba': ['nmbd.service', 'smbd.service'],
    'bluez': ['bluetooth.service'],
    'obexd': ['obex.service'],
    'crond': ['cron.service'],
    'iptables': ['iptables.service'],
    'oscam': ['oscam.service'],
    'tvlink': ['tvlink.service'],
    'tvheadend': ['tvheadend.service'],
    }
