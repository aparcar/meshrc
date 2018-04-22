include $(TOPDIR)/rules.mk

PKG_NAME:=prometheus-bmx7-targets
PKG_VERSION:=0.1
PKG_RELEASE:=4

include $(INCLUDE_DIR)/package.mk

define Package/prometheus-bmx7-targets
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=prometheus-bmx7-targets
  MAINTAINER:=Paul Spooren <spooren@informatik.uni-leipzig.de>
  DEPENDS:=bmx7 +bmx7-json +inotifywait +jshn
endef

define Build/Compile
endef

define Build/Configure
endef

define Package/prometheus-bmx7-targets/install
	$(CP) files/* $(1)/
endef

$(eval $(call BuildPackage,prometheus-bmx7-targets))
