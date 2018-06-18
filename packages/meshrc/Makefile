include $(TOPDIR)/rules.mk

PKG_NAME:=meshrc
PKG_VERSION:=0.7
PKG_RELEASE:=1

PKG_MAINTAINER:=Paul Spooren <spooren@informatik.uni-leipzig.de>

include $(INCLUDE_DIR)/package.mk

define Package/meshrc/Default
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc
  PKGARCH:=all
endef

define Package/meshrc-initial
  $(call Package/meshrc/Default)
  TITLE+= initial
  DEPENDS:=+lime-system
endef

define Package/meshrc-client
  $(call Package/meshrc/Default)
  TITLE+= client
  DEPENDS:=bmx7 +lime-system +bmx7-sms +inotifywait
endef

define Package/meshrc-cli
  $(call Package/meshrc/Default)
  TITLE+= cli
  DEPENDS:=bmx7 +lime-system +bmx7-sms
endef

define Package/meshrc-web
  $(call Package/meshrc/Default)
  TITLE+= web
  DEPENDS:=+uhttpd-mod-ubus +python3-light +python3-email +python3-idna +python3-codecs
endef

Build/Compile=

define Package/meshrc-initial/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/initial/* $(1)/
endef

define Package/meshrc-client/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/client/* $(1)/
endef

define Package/meshrc-cli/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/cli/* $(1)/
endef

define Package/meshrc-web/install
		$(INSTALL_DIR) $(1)/
		$(CP) -r files/web/* $(1)/
endef

$(eval $(call BuildPackage,meshrc-initial))
$(eval $(call BuildPackage,meshrc-client))
$(eval $(call BuildPackage,meshrc-cli))
$(eval $(call BuildPackage,meshrc-web))
