TOPLEVEL_LANG = verilog
SIM = verilator
VERILOG_SOURCES = $(shell pwd)/mkcompute.v $(shell pwd)/FIFO2.v $(shell pwd)/mkdepend_resolver.v $(shell pwd)/mkfetchdecode.v $(shell pwd)/mkload.v $(shell pwd)/mkmac_ws.v $(shell pwd)/mkonchip_buffers.v $(shell pwd)/mkshaktimaan.v $(shell pwd)/mkstore.v $(shell pwd)/mksystolic_ws.v $(shell pwd)/mktensoralu.v $(shell pwd)/SizedFIFO.v $(shell pwd)/BRAM2.v
TOPLEVEL = mkshaktimaan
MODULE = test_shaktimaan_random_instr
EXTRA_ARGS += --trace --trace-structs --coverage -Wno-WIDTH -Wno-STMTDLY -Wno-CASEINCOMPLETE -Wno-MULTIDRIVEN
VERILATOR_TRACE = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
