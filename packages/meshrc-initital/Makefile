include $(TOPDIR)/rules.mk

PKG_NAME:=meshrc-initial
PKG_VERSION:=0.1
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/meshrc-initial-client
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-initial-client
  MAINTAINER:=Paul Spooren <spooren@informatik.uni-leipzig.de>
#  DEPENDS:=
endef

define Package/meshrc-initial-server
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-initial-server
  MAINTAINER:=Paul Spooren <spooren@informatik.uni-leipzig.de>
  DEPENDS:=+inotifywait
endef

define Build/Compile
endef

define Build/Configure
endef

define Package/meshrc-initial-server/install
		$(INSTALL_DIR) $(1)/etc/init.d/
		$(CP) files/server.procd $(1)/etc/init.d/meshrc-initial-server

		$(INSTALL_DIR) $(1)/etc/uci-defaults
		$(CP) files/server.defaults $(1)/etc/uci-defaults/90-meshrc-initial

		$(INSTALL_DIR) $(1)/usr/bin
		$(CP) files/server.sh $(1)/usr/bin/meshrc-initial-server
endef

define Package/meshrc-initial-client/install
		$(INSTALL_DIR) $(1)/etc/init.d/
		$(CP) files/client.procd $(1)/etc/init.d/meshrc-initial-client

		$(INSTALL_DIR) $(1)/etc/uci-defaults
		$(CP) files/client.defaults $(1)/etc/uci-defaults/90-meshrc-initial

		$(INSTALL_DIR) $(1)/usr/bin
		$(CP) files/client.sh $(1)/usr/bin/meshrc-initial-client
endef

$(eval $(call BuildPackage,meshrc-initial-server))
$(eval $(call BuildPackage,meshrc-initial-client))
