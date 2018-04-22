include $(TOPDIR)/rules.mk

PKG_NAME:=meshrc
PKG_VERSION:=0.0.5
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/meshrc-client
  SECTION:=lime
  CATEGORY:=LiMe
  TITLE:=meshrc-client
  PKGARCH:=all
  DEPENDS:=bmx7 lime-system +bmx7-sms +inotifywait
endef

define Package/meshrc-client/description
	Checks for new config files and installs if sender is trusted
endef

define Build/Compile
endef

define Build/Configure
endef

define Package/meshrc-client/install
		$(INSTALL_DIR) $(1)/usr/bin
		$(CP) files/meshrc-client.sh $(1)/usr/bin/meshrc-client
		chmod +x $(1)/usr/bin/meshrc-client

		$(INSTALL_DIR) $(1)/etc/init.d
		$(CP) files/meshrc-client.procd $(1)/etc/init.d/meshrc-client
endef

define Package/meshrc-server
  SECTION:=lime
  CATEGORY:=LiMe
  TITLE:=meshrc-server
  PKGARCH:=all
  DEPENDS:=bmx7 lime-system +bmx7-sms
endef

define Package/meshrc-server/description
	Publishes installed lime-config to network and let other nodes use it
endef

define Build/Compile
endef

define Build/Configure
endef

define Package/meshrc-server/install
		$(INSTALL_DIR) $(1)/usr/bin
		$(CP) files/meshrc-cli.sh $(1)/usr/bin/meshrc-cli
endef

$(eval $(call BuildPackage,meshrc-client))
$(eval $(call BuildPackage,meshrc-server))
