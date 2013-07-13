
#Usage: ./nversion.mk IMAGE=full_path_to_image_file

#This really should be over-ridden.
PREFIX?=/usr/local
PYTHON?=$(shell which python)
PACKAGE?=fsnview
PKGDATADIR?=$(PREFIX)/share/$(PACKAGE)

IDIFFERENCE_PY=$(PKGDATADIR)/python3/idifference.py
IDIFFERENCE_CMD=python3 $(IDIFFERENCE_PY) --summary
FIWALK?=$(PREFIX)/bin/fiwalk
PY360_REPORT360_PY?=$(PKGDATADIR)/python2/report360.py
PY360_PARTITION360_PY=$(PKGDATADIR)/python2/py360/partition.py
PY360_PYS=$(PY360_PARTITION_PY) $(PY360_REPORT360_PY)
PY360_CMD=$(PYTHON) $(PY360_REPORT360_PY) -x
UXTAF_PROGS=$(PREFIX)/bin/uxtaf $(PKGDATADIR)/uxtaf_allparts.sh
UXTAF_CMD=$(PKGDATADIR)/uxtaf_allparts.sh
TIMELINE_PY=$(PKGDATADIR)/python3/demo_mac_timeline.py
TIMELINE_CMD=python3 $(TIMELINE_PY)

FIWALK_MAYBE_ALLOC_ONLY?=

TARGETS = \
  diffs.fiwalk_to_py360.txt \
  diffs.fiwalk_to_uxtaf.txt \
  diffs.py360_to_fiwalk.txt \
  diffs.py360_to_uxtaf.txt \
  diffs.uxtaf_to_fiwalk.txt \
  diffs.uxtaf_to_py360.txt \
  mactimeline.fiwalk.txt \
  mactimeline.py360.txt \
  mactimeline.uxtaf.txt 

all: $(TARGETS)

#TODO Add status and error logs to each timeline invocation.

mactimeline.fiwalk.txt: $(TIMELINE_PY) fiwalk.dfxml
	$(TIMELINE_CMD) fiwalk.dfxml >$@

mactimeline.py360.txt: $(TIMELINE_PY) py360.dfxml
	$(TIMELINE_CMD) py360.dfxml >$@

mactimeline.uxtaf.txt: $(TIMELINE_PY) uxtaf.dfxml
	$(TIMELINE_CMD) uxtaf.dfxml >$@

diffs.fiwalk_to_py360.txt: $(IDIFFERENCE_PY) fiwalk.dfxml py360.dfxml
	$(IDIFFERENCE_CMD) fiwalk.dfxml py360.dfxml >$@

diffs.fiwalk_to_uxtaf.txt: $(IDIFFERENCE_PY) fiwalk.dfxml uxtaf.dfxml
	$(IDIFFERENCE_CMD) fiwalk.dfxml uxtaf.dfxml >$@

diffs.py360_to_fiwalk.txt: $(IDIFFERENCE_PY) py360.dfxml fiwalk.dfxml
	$(IDIFFERENCE_CMD) py360.dfxml fiwalk.dfxml >$@

diffs.py360_to_uxtaf.txt: $(IDIFFERENCE_PY) py360.dfxml uxtaf.dfxml
	$(IDIFFERENCE_CMD) py360.dfxml uxtaf.dfxml >$@

diffs.uxtaf_to_fiwalk.txt: $(IDIFFERENCE_PY) uxtaf.dfxml fiwalk.dfxml
	$(IDIFFERENCE_CMD) uxtaf.dfxml fiwalk.dfxml >$@

diffs.uxtaf_to_py360.txt: $(IDIFFERENCE_PY) uxtaf.dfxml py360.dfxml
	$(IDIFFERENCE_CMD) uxtaf.dfxml py360.dfxml >$@

fiwalk.dfxml: $(FIWALK) $(IMAGE)
	echo "In progress..." >fiwalk.status.log
	rm -f fiwalk.dfxml
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

uxtaf.dfxml: $(UXTAF_PROGS) $(IMAGE)
	echo "In progress..." >uxtaf.status.log
	$(UXTAF_CMD) $(IMAGE) >uxtaf.out.log 2>uxtaf.err.log \
	  echo $$? >uxtaf.status.log
