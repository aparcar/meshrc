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

define Package/meshrc-client/install
		$(INSTALL_DIR) $(1)/usr/bin
		$(CP) files/client.sh $(1)/usr/bin/meshrc-client
		chmod +x $(1)/usr/bin/meshrc-client

		$(INSTALL_DIR) $(1)/etc/init.d
		$(CP) files/client.procd $(1)/etc/init.d/meshrc-client
endef

define Package/meshrc-server
  SECTION:=lime
  CATEGORY:=LiMe
  TITLE:=meshrc-server
  PKGARCH:=all
  DEPENDS:=bmx7 lime-system +bmx7-sms
endef

define Package/meshrc-server/description
	Set configurations for nodes of network 
endef

define Package/meshrc-server/install
		$(INSTALL_DIR) $(1)/usr/bin
		$(CP) files/cli.sh $(1)/usr/bin/meshrc-cli
endef

define Build/Compile
endef

define Build/Configure
endef

$(eval $(call BuildPackage,meshrc-client))
$(eval $(call BuildPackage,meshrc-server))
