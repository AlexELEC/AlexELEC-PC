# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)

PKG_NAME="driverselect"
PKG_VERSION="b99f2d0"
PKG_SHA256="c06137b384bd149f006823daaadf311e8477ca56df54b30c13651c837509612d"
PKG_REV="1"
PKG_ARCH="any"
PKG_LICENSE="OSS"
PKG_SITE="https://github.com/AlexELEC/script.program.driverselect"
PKG_URL="$PKG_SITE/archive/$PKG_VERSION.tar.gz"
PKG_DEPENDS_TARGET="toolchain"
PKG_SECTION="script.program"
PKG_SHORTDESC="script.program.driverselect"
PKG_LONGDESC="script.program.driverselect"
PKG_TOOLCHAIN="manual"

PKG_IS_ADDON="embedded"
PKG_ADDON_NAME="Driver Select"
PKG_ADDON_TYPE="xbmc.python.script"

unpack() {
  mkdir -p $PKG_BUILD/addon
  tar --strip-components=1 -xf $SOURCES/$PKG_NAME/$PKG_NAME-$PKG_VERSION.tar.gz -C $PKG_BUILD/addon
}

make_target() {
  :
}

makeinstall_target() {
  mkdir -p $INSTALL/usr/share/kodi/addons/${PKG_SECTION}.${PKG_NAME}
  cp -rP $PKG_BUILD/addon/* $INSTALL/usr/share/kodi/addons/${PKG_SECTION}.${PKG_NAME}
}
