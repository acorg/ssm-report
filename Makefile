# -*- Makefile -*-
# ----------------------------------------------------------------------

all: install

include $(ACMACSD_ROOT)/share/Makefile.config

install:
	$(call symbolic_link,$(abspath py)/ssm_report,$(AD_PY)/ssm_report)
	$(call symbolic_link_wildcard,$(abspath bin)/*,$(AD_BIN))
.PHONY: install

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
