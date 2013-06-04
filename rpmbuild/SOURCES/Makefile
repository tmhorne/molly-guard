# Makefile - make script to build all supported distribution versions
#
# Copyright © Lazarus Long <lazarus.long@bigfoot.com>
# Released under the terms of the Artistic Licence 2.0
#

# RPM build executable
RPMBUILD:=rpmbuild

# Paths
BUILDDIR:=$(shell rpm --eval '%{_topdir}')

# Flags for rpmbuild
BINFLAGS:=-bb --clean
SRCFLAGS:=-bs
EL5FLAGS:=-D"dist .el5" -D"el5 1"
EL6FLAGS:=-D"dist .el6" -D"el6 1"

# Program specific
NAME=molly-guard
SPECFILE:=$(BUILDDIR)/SPECS/$(NAME).spec

help:
	@echo ""
	@echo "Usage:	$(MAKE) <el5|el6|binary|source|all|clean|distclean>"
	@echo ""
	@echo "	el5		- Compile for EL distribution's version 5"
	@echo "	el6		- Compile for EL distribution's version 6"
	@echo "	binary		- Compile for all supported distribution versions"
	@echo "	source		- Compile the source RPM"
	@echo "	all		- Compile all the binary and source RPMs"
	@echo "	clean		- Delete all $(NAME) binary RPMs from the $(BUILDDIR)"
	@echo "	dstclean	- Delete all $(NAME) binary and source RPMs from the $(BUILDDIR)"
	@echo ""

el5:
	$(RPMBUILD) $(BINFLAGS) $(EL5FLAGS) $(SPECFILE)

el6:
	$(RPMBUILD) $(BINFLAGS) $(EL6FLAGS) $(SPECFILE)

source:
	$(RPMBUILD) $(SRCFLAGS) $(SPECFILE)

binary: el5 el6

all: source binary

clean:
	rm -f $(BUILDDIR)/RPMS/noarch/$(NAME)*

distclean: clean
	rm -f $(BUILDDIR)/SRPMS/$(NAME)*

.PHONY: all binary source el6 el5 distclean clean help
