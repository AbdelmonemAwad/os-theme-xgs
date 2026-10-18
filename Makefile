PLUGIN_NAME=		theme-xgs
PLUGIN_VERSION=		1.0
PLUGIN_COMMENT=		XGS Silicon: a light, a dark and an automatic theme for OPNsense on Sophos XGS appliances
PLUGIN_MAINTAINER=	eg2@live.com
PLUGIN_NO_ABI=		yes

# As OPNsense's own themes: everything under src/ is copied into ${LOCALBASE}. assets/ is the source
# of build/css (tools/build-css.sh) and is shipped as the theme plugins ship theirs. xgs-auto's css,
# fonts and images are the light theme's, linked by install/install.sh; a package build needs the
# same three links made in its staging tree.

.include "../../Mk/plugins.mk"
