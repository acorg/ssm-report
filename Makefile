# -*- Makefile -*-
# ----------------------------------------------------------------------

all: install

NO_RTAGS_TARGET=1
include $(ACMACSD_ROOT)/share/Makefile.config

install:
	$(call install_all,$(AD_PACKAGE_NAME))
	$(call install_py,vr)
.PHONY: install

rtags:

test: install
	echo "WARNING: ssm-report test not implemented yet" >&2
.PHONY: test

# ----------------------------------------------------------------------

clean:

rtags:

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
