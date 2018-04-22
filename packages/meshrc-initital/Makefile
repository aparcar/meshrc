include $(TOPDIR)/rules.mk

PKG_NAME:=meshrc-initital
PKG_VERSION:=0.1
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/meshrc-initial
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=meshrc-initial
  MAINTAINER:=Paul Spooren <spooren@informatik.uni-leipzig.de>
#  DEPENDS:=
endef

define Build/Compile
endef

define Build/Configure
endef

define Package/meshrc-initial-server/install
	$(CP) files/* $(1)/
endef

define Package/meshrc-initial-server/install
	$(CP) files/* $(1)/
endef

$(eval $(call BuildPackage,meshrc-initital-server))
$(eval $(call BuildPackage,meshrc-initital-client))
