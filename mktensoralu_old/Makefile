NG = verilog
VERILOG_SOURCES = $(shell pwd)/mktalu_Tb.v
TOPLEVEL = mktalu_Tb
MODULE = test_tensor_alu
EXTRA_ARGS += --trace --trace-structs --coverage --Wno-TIMESCALEMOD
COMPILE_ARGS += -O3 --x-assign fast --x-initial fast \
  --noassert --bbox-sys -Wno-STMTDLY -Wno-UNOPTFLAT -Wno-WIDTH \
  -Wno-lint -Wno-COMBDLY -Wno-INITIALDLY --autoflush  --threads 1 \
  -DBSV_RESET_FIFO_HEAD -DBSV_RESET_FIFO_ARRAY --output-split 20000 --output-split-ctrace 10000
#VERILATOR_TRACE = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
