include $(TOPDIR)/rules.mk

PKG_NAME:=meshrc
PKG_VERSION:=0.5
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/meshrc-web
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-web
  PKGARCH:=all
  DEPENDS:=+uhttpd-mod-ubus
endef

define Package/meshrc-web/description
	Web interface to show a graph and a overview table with stats.
endef

define Package/meshrc-web/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/web/* $(1)/
endef

define Package/meshrc-client
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-client
  PKGARCH:=all
  DEPENDS:=bmx7 lime-system +bmx7-sms +inotifywait
endef

define Package/meshrc-client/description
	Checks for new config files and installs if sender is trusted
endef

define Package/meshrc-client/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/client/* $(1)/
endef

define Package/meshrc-initial
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-initial
  PKGARCH:=all
  DEPENDS:=lime-system
endef

define Package/meshrc-initial/description
	Checks for an initial configuration offered by directly connected nodes
endef

define Package/meshrc-initial/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/initial/* $(1)/
endef

define Package/meshrc-cli
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-cli
  PKGARCH:=all
  DEPENDS:=bmx7 lime-system +bmx7-sms
endef

define Package/meshrc-cli/description
	Set configurations for nodes of network 
endef

define Package/meshrc-cli/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/cli/* $(1)/
endef

define Build/Compile
endef

define Build/Configure
endef

$(eval $(call BuildPackage,meshrc-web))
$(eval $(call BuildPackage,meshrc-client))
$(eval $(call BuildPackage,meshrc-initial))
$(eval $(call BuildPackage,meshrc-cli))
