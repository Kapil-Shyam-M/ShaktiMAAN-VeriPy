TOPLEVEL_LANG ?= verilog
#COMPILE_ARGS = -LDFLAGS -Wl,--no-as-needed +define+BSV_RESET_FIFO_HEAD +define+BSV_RESET_FIFO_ARRAY
EXTRA_ARGS += --trace --trace-structs --coverage --Wno-TIMESCALEMOD
COMPILE_ARGS += -O3 --x-assign fast --x-initial fast \
  --noassert --bbox-sys -Wno-STMTDLY -Wno-UNOPTFLAT -Wno-WIDTH \
  -Wno-lint -Wno-COMBDLY -Wno-INITIALDLY --autoflush  --threads 1 \
  -DBSV_RESET_FIFO_HEAD -DBSV_RESET_FIFO_ARRAY --output-split 20000 --output-split-ctrace 10000

WPWD=$(shell pwd)
SIM=verilator
ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(WPWD)/*.v
endif

TOPLEVEL := mkdep_Tb
MODULE   := test_dep_resol

include $(shell cocotb-config --makefiles)/Makefile.sim
