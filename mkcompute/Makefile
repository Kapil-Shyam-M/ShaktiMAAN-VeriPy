TOPLEVEL_LANG = verilog
#VERILOG_SOURCES = $(shell pwd)/mkgemm_Tb.v $(shell pwd)/FIFO2.v

#EXTRA_ARGS = --coverage -Wno-warning
EXTRA_ARGS += --trace --trace-structs --coverage --Wno-TIMESCALEMOD
COMPILE_ARGS += -O3 --x-assign fast --x-initial fast \
  --noassert --bbox-sys -Wno-STMTDLY -Wno-UNOPTFLAT -Wno-WIDTH \
  -Wno-lint -Wno-COMBDLY -Wno-INITIALDLY --autoflush  --threads 1 \
  -DBSV_RESET_FIFO_HEAD -DBSV_RESET_FIFO_ARRAY --output-split 20000 --output-split-ctrace 10000 
#VERILATOR_TRACE = 1

WPWD=$(shell pwd)
SIM=verilator
ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(WPWD)/*.v
endif

TOPLEVEL = mkgemm_Tb
MODULE = test_compute

include $(shell cocotb-config --makefiles)/Makefile.sim
