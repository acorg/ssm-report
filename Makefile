# -*- Makefile -*-
# Eugene Skepner 2017
# ----------------------------------------------------------------------

MAKEFLAGS = -w

# ----------------------------------------------------------------------

include $(ACMACSD_ROOT)/share/makefiles/Makefile.dist-build.vars

all: check-acmacsd-root install

install: check-acmacsd-root
	ln -sf $(abspath py)/ssm_report $(AD_PY)
	ln -sf $(abspath bin)/ssm-report $(AD_BIN)
	ln -sf $(abspath bin)/make-trees-on-albertine $(AD_BIN)
	ln -sf $(abspath bin)/gisaid-* $(AD_BIN)

test: install
	echo "WARNING: ssm-report test not implemented yet" >&2

# ----------------------------------------------------------------------

-include $(BUILD)/*.d
include $(ACMACSD_ROOT)/share/makefiles/Makefile.dist-build.rules

# ----------------------------------------------------------------------

clean:

rtags:

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
