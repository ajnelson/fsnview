#!/usr/bin/make -f

#Usage: ./nversion.mk IMAGE=full_path_to_image_file

#This really should be over-ridden.
PREFIX?=/usr/local
PYTHON?=$(shell which python)
PACKAGE?=fsnview
PKGDATADIR?=$(PREFIX)/share/$(PACKAGE)

IDIFFERENCE_PY=$(PKGDATADIR)/python3/idifference.py
IDIFFERENCE_CMD=python3 $(IDIFFERENCE_PY)
FIWALK?=$(PREFIX)/bin/fiwalk
PY360_REPORT360_PY?=$(PKGDATADIR)/python2/report360.py
PY360_PARTITION360_PY=$(PKGDATADIR)/python2/py360/partition.py
PY360_PYS=$(PY360_PARTITION_PY) $(PY360_REPORT360_PY)
PY360_CMD=$(PYTHON) $(PY360_REPORT360_PY) -x
UXTAF?=$(PREFIX)/bin/uxtaf

FIWALK_MAYBE_ALLOC_ONLY?=

TARGETS = \
  fiwalk_to_py360.diffs.txt \
  fiwalk_to_uxtaf.diffs.txt \
  py360_to_fiwalk.diffs.txt \
  py360_to_uxtaf.diffs.txt \
  uxtaf_to_fiwalk.diffs.txt \
  uxtaf_to_py360.diffs.txt 

all: report

#report: Fake-file rule, should move to calling Bash script
report: $(TARGETS)
	@echo "Exit statuses of all the DFXML-generating programs (should be 0's):"
	@grep '^' *.status.log | cat
	@echo ""
	@echo "Review these files:"
	@ls *.diffs.txt

fiwalk_to_py360.diffs.txt: $(IDIFFERENCE_PY) fiwalk.dfxml py360.dfxml
	$(IDIFFERENCE_CMD) fiwalk.dfxml py360.dfxml >$@

fiwalk_to_uxtaf.diffs.txt: $(IDIFFERENCE_PY) fiwalk.dfxml uxtaf.dfxml
	$(IDIFFERENCE_CMD) fiwalk.dfxml uxtaf.dfxml >$@

py360_to_fiwalk.diffs.txt: $(IDIFFERENCE_PY) py360.dfxml fiwalk.dfxml
	$(IDIFFERENCE_CMD) py360.dfxml fiwalk.dfxml >$@

py360_to_uxtaf.diffs.txt: $(IDIFFERENCE_PY) py360.dfxml uxtaf.dfxml
	$(IDIFFERENCE_CMD) py360.dfxml uxtaf.dfxml >$@

uxtaf_to_fiwalk.diffs.txt: $(IDIFFERENCE_PY) uxtaf.dfxml fiwalk.dfxml
	$(IDIFFERENCE_CMD) uxtaf.dfxml fiwalk.dfxml >$@

uxtaf_to_py360.diffs.txt: $(IDIFFERENCE_PY) uxtaf.dfxml py360.dfxml
	$(IDIFFERENCE_CMD) uxtaf.dfxml py360.dfxml >$@

fiwalk.dfxml: $(FIWALK) $(IMAGE)
	echo "In progress..." >fiwalk.status.log
	$(FIWALK) $(FIWALK_MAYBE_ALLOC_ONLY) -Xfiwalk.dfxml $(IMAGE) >fiwalk.out.log 2>fiwalk.err.log; echo $$? >fiwalk.status.log

py360.dfxml: $(PY360_PYS) $(IMAGE)
	echo "In progress..." >py360.status.log
	rm -f py360out.dfxml
	$(PY360_CMD) $(IMAGE) >py360.out.log 2>py360.err.log; echo $$? >py360.status.log
	#TODO Check exit status here
	if [ -r py360out.dfxml ]; then \
	  mv py360out.dfxml py360.dfxml; \
	else \
	  echo "py360out.dfxml not found."; \
	  exit 5; \
	fi

uxtaf.dfxml: $(UXTAF) $(IMAGE)
	echo "In progress..." >uxtaf.status.log
	@rm -f uxtaf.info
	$(UXTAF) attach $(IMAGE) 5115674624 >uxtaf.out.log 2>uxtaf.err.log; \
	  rc=$$?; \
	  echo $$rc >uxtaf.status.log; \
	  if [ $$rc -ne 0 ]; then \
	    exit $$rc; \
	  fi
	$(UXTAF) dfxml >uxtaf.dfxml 2>>uxtaf.err.log; echo $$? >uxtaf.status.log
	@rm -f uxtaf.info
