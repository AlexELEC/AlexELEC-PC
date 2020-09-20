#!/bin/sh

# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2011-present Alex@ELEC (https://alexelec.tv)

URL_MAIN="https://github.com/AlexELEC/TVLINK-AE-PC/releases/download"
URL_LAST="https://github.com/AlexELEC/TVLINK-AE-PC/releases/latest"

TVL_DIR="/storage/.config/tvlink"
TEMP_DIR="/storage/.kodi/temp"

BACKUP_DIR="/tmp/tvlink"

################################ MAIN ##########################################

UPD_VER=`curl -s "$URL_LAST" | sed 's|.*tag\/||; s|">redirected.*||')`

# download URL
  if [ "$1" == "url" ] ; then
      if curl --output /dev/null --silent --head --fail "$URL_MAIN/$UPD_VER/TVLINK-$UPD_VER.tar.bz2"
      then
        echo "$URL_MAIN/$UPD_VER/TVLINK-$UPD_VER.tar.bz2"
      else
        echo "error"
      fi

# unpack to TVL_DIR
  elif [ "$1" == "install" ] ; then
      rm -fR $TVL_DIR
      mkdir -p $TVL_DIR
      tar -jxf $TEMP_DIR/TVLINK-$UPD_VER.tar.bz2 -C $TVL_DIR
      rm -f $TEMP_DIR/TVLINK-$UPD_VER.tar.bz2

# current version
  elif [ "$1" == "old" ] ; then
      CURRENT_VER=`curl -s 'http://127.0.0.1:2020/version'`
      [ "$CURRENT_VER" == "" ] && CURRENT_VER="Unknown"
      echo "$CURRENT_VER"

# update version
  elif [ "$1" == "new" ] ; then
      CURRENT_VER=`curl -s 'http://127.0.0.1:2020/version'`
      if [ "$CURRENT_VER" != "$UPD_VER" ]; then
        echo "$UPD_VER"
      else
        echo "NOT UPDATE"
      fi

# backup
  elif [ "$1" == "backup" ] ; then
      mkdir -p $BACKUP_DIR
      [ -d "$TVL_DIR/data" ] && cp -rf $TVL_DIR/data $BACKUP_DIR
      [ -d "$TVL_DIR/logos" ] && cp -rf $TVL_DIR/logos $BACKUP_DIR

# restore
  elif [ "$1" == "restore" ] ; then
      [ -e "$BACKUP_DIR/data/setup.db" ] && cp -f $BACKUP_DIR/data/setup.db $TVL_DIR/data
      [ -e "$BACKUP_DIR/data/channels.db" ] && cp -f $BACKUP_DIR/data/channels.db $TVL_DIR/data
      [ -d "$BACKUP_DIR/logos" ] && cp -rf $BACKUP_DIR/logos $TVL_DIR
      rm -fR $BACKUP_DIR

  fi

exit 0
