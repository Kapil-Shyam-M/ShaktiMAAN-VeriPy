//
// Generated by Bluespec Compiler (build 8d454e4)
//
// On Tue Mar 16 15:56:54 IST 2021
//
//
// Ports:
// Name                         I/O  size props
// RDY_ifc_put_load_params_put    O     1
// RDY_ifc_put_store_params_put   O     1
// RDY_ifc_put_compute_params_put  O     1
// RDY_ifc_put_alu_params_put     O     1
// ifc_get_load_instruction_get   O   120 reg
// RDY_ifc_get_load_instruction_get  O     1
// ifc_get_store_instruction_get  O   120 reg
// RDY_ifc_get_store_instruction_get  O     1
// ifc_get_gemm_instruction_get   O   120 reg
// RDY_ifc_get_gemm_instruction_get  O     1
// ifc_get_alu_instruction_get    O   120 reg
// RDY_ifc_get_alu_instruction_get  O     1
// RDY_ifc_put_load_complete_put  O     1
// RDY_ifc_put_store_complete_put  O     1
// RDY_ifc_put_gemm_complete_put  O     1
// RDY_ifc_put_alu_complete_put   O     1
// CLK                            I     1 clock
// RST_N                          I     1 reset
// ifc_put_load_params_put        I   124 reg
// ifc_put_store_params_put       I   124 reg
// ifc_put_compute_params_put     I   124 reg
// ifc_put_alu_params_put         I   124 reg
// ifc_put_load_complete_put      I     1 unused
// ifc_put_store_complete_put     I     1 unused
// ifc_put_gemm_complete_put      I     1 unused
// ifc_put_alu_complete_put       I     1 unused
// EN_ifc_put_load_params_put     I     1
// EN_ifc_put_store_params_put    I     1
// EN_ifc_put_compute_params_put  I     1
// EN_ifc_put_alu_params_put      I     1
// EN_ifc_put_load_complete_put   I     1
// EN_ifc_put_store_complete_put  I     1
// EN_ifc_put_gemm_complete_put   I     1
// EN_ifc_put_alu_complete_put    I     1
// EN_ifc_get_load_instruction_get  I     1
// EN_ifc_get_store_instruction_get  I     1
// EN_ifc_get_gemm_instruction_get  I     1
// EN_ifc_get_alu_instruction_get  I     1
//
// No combinational paths from inputs to outputs
//
//

`ifdef BSV_ASSIGNMENT_DELAY
`else
  `define BSV_ASSIGNMENT_DELAY
`endif

`ifdef BSV_POSITIVE_RESET
  `define BSV_RESET_VALUE 1'b1
  `define BSV_RESET_EDGE posedge
`else
  `define BSV_RESET_VALUE 1'b0
  `define BSV_RESET_EDGE negedge
`endif

module mkdep_Tb(CLK,
		RST_N,

		ifc_put_load_params_put,
		EN_ifc_put_load_params_put,
		RDY_ifc_put_load_params_put,

		ifc_put_store_params_put,
		EN_ifc_put_store_params_put,
		RDY_ifc_put_store_params_put,

		ifc_put_compute_params_put,
		EN_ifc_put_compute_params_put,
		RDY_ifc_put_compute_params_put,

		ifc_put_alu_params_put,
		EN_ifc_put_alu_params_put,
		RDY_ifc_put_alu_params_put,

		EN_ifc_get_load_instruction_get,
		ifc_get_load_instruction_get,
		RDY_ifc_get_load_instruction_get,

		EN_ifc_get_store_instruction_get,
		ifc_get_store_instruction_get,
		RDY_ifc_get_store_instruction_get,

		EN_ifc_get_gemm_instruction_get,
		ifc_get_gemm_instruction_get,
		RDY_ifc_get_gemm_instruction_get,

		EN_ifc_get_alu_instruction_get,
		ifc_get_alu_instruction_get,
		RDY_ifc_get_alu_instruction_get,

		ifc_put_load_complete_put,
		EN_ifc_put_load_complete_put,
		RDY_ifc_put_load_complete_put,

		ifc_put_store_complete_put,
		EN_ifc_put_store_complete_put,
		RDY_ifc_put_store_complete_put,

		ifc_put_gemm_complete_put,
		EN_ifc_put_gemm_complete_put,
		RDY_ifc_put_gemm_complete_put,

		ifc_put_alu_complete_put,
		EN_ifc_put_alu_complete_put,
		RDY_ifc_put_alu_complete_put);
  input  CLK;
  input  RST_N;

  // action method ifc_put_load_params_put
  input  [123 : 0] ifc_put_load_params_put;
  input  EN_ifc_put_load_params_put;
  output RDY_ifc_put_load_params_put;

  // action method ifc_put_store_params_put
  input  [123 : 0] ifc_put_store_params_put;
  input  EN_ifc_put_store_params_put;
  output RDY_ifc_put_store_params_put;

  // action method ifc_put_compute_params_put
  input  [123 : 0] ifc_put_compute_params_put;
  input  EN_ifc_put_compute_params_put;
  output RDY_ifc_put_compute_params_put;

  // action method ifc_put_alu_params_put
  input  [123 : 0] ifc_put_alu_params_put;
  input  EN_ifc_put_alu_params_put;
  output RDY_ifc_put_alu_params_put;

  // actionvalue method ifc_get_load_instruction_get
  input  EN_ifc_get_load_instruction_get;
  output [119 : 0] ifc_get_load_instruction_get;
  output RDY_ifc_get_load_instruction_get;

  // actionvalue method ifc_get_store_instruction_get
  input  EN_ifc_get_store_instruction_get;
  output [119 : 0] ifc_get_store_instruction_get;
  output RDY_ifc_get_store_instruction_get;

  // actionvalue method ifc_get_gemm_instruction_get
  input  EN_ifc_get_gemm_instruction_get;
  output [119 : 0] ifc_get_gemm_instruction_get;
  output RDY_ifc_get_gemm_instruction_get;

  // actionvalue method ifc_get_alu_instruction_get
  input  EN_ifc_get_alu_instruction_get;
  output [119 : 0] ifc_get_alu_instruction_get;
  output RDY_ifc_get_alu_instruction_get;

  // action method ifc_put_load_complete_put
  input  ifc_put_load_complete_put;
  input  EN_ifc_put_load_complete_put;
  output RDY_ifc_put_load_complete_put;

  // action method ifc_put_store_complete_put
  input  ifc_put_store_complete_put;
  input  EN_ifc_put_store_complete_put;
  output RDY_ifc_put_store_complete_put;

  // action method ifc_put_gemm_complete_put
  input  ifc_put_gemm_complete_put;
  input  EN_ifc_put_gemm_complete_put;
  output RDY_ifc_put_gemm_complete_put;

  // action method ifc_put_alu_complete_put
  input  ifc_put_alu_complete_put;
  input  EN_ifc_put_alu_complete_put;
  output RDY_ifc_put_alu_complete_put;

  // signals for module outputs
  wire [119 : 0] ifc_get_alu_instruction_get,
		 ifc_get_gemm_instruction_get,
		 ifc_get_load_instruction_get,
		 ifc_get_store_instruction_get;
  wire RDY_ifc_get_alu_instruction_get,
       RDY_ifc_get_gemm_instruction_get,
       RDY_ifc_get_load_instruction_get,
       RDY_ifc_get_store_instruction_get,
       RDY_ifc_put_alu_complete_put,
       RDY_ifc_put_alu_params_put,
       RDY_ifc_put_compute_params_put,
       RDY_ifc_put_gemm_complete_put,
       RDY_ifc_put_load_complete_put,
       RDY_ifc_put_load_params_put,
       RDY_ifc_put_store_complete_put,
       RDY_ifc_put_store_params_put;

  // ports of submodule inst1_ff_alu_params
  wire [119 : 0] inst1_ff_alu_params$D_IN, inst1_ff_alu_params$D_OUT;
  wire inst1_ff_alu_params$CLR,
       inst1_ff_alu_params$DEQ,
       inst1_ff_alu_params$EMPTY_N,
       inst1_ff_alu_params$ENQ,
       inst1_ff_alu_params$FULL_N;

  // ports of submodule inst1_ff_alu_queue
  wire [3 : 0] inst1_ff_alu_queue$D_IN, inst1_ff_alu_queue$D_OUT;
  wire inst1_ff_alu_queue$CLR,
       inst1_ff_alu_queue$DEQ,
       inst1_ff_alu_queue$EMPTY_N,
       inst1_ff_alu_queue$ENQ,
       inst1_ff_alu_queue$FULL_N;

  // ports of submodule inst1_ff_alu_to_gemm
  wire inst1_ff_alu_to_gemm$CLR,
       inst1_ff_alu_to_gemm$DEQ,
       inst1_ff_alu_to_gemm$D_IN,
       inst1_ff_alu_to_gemm$EMPTY_N,
       inst1_ff_alu_to_gemm$ENQ,
       inst1_ff_alu_to_gemm$FULL_N;

  // ports of submodule inst1_ff_alu_to_store
  wire inst1_ff_alu_to_store$CLR,
       inst1_ff_alu_to_store$DEQ,
       inst1_ff_alu_to_store$D_IN,
       inst1_ff_alu_to_store$EMPTY_N,
       inst1_ff_alu_to_store$ENQ,
       inst1_ff_alu_to_store$FULL_N;

  // ports of submodule inst1_ff_gemm_params
  wire [119 : 0] inst1_ff_gemm_params$D_IN, inst1_ff_gemm_params$D_OUT;
  wire inst1_ff_gemm_params$CLR,
       inst1_ff_gemm_params$DEQ,
       inst1_ff_gemm_params$EMPTY_N,
       inst1_ff_gemm_params$ENQ,
       inst1_ff_gemm_params$FULL_N;

  // ports of submodule inst1_ff_gemm_queue
  wire [3 : 0] inst1_ff_gemm_queue$D_IN, inst1_ff_gemm_queue$D_OUT;
  wire inst1_ff_gemm_queue$CLR,
       inst1_ff_gemm_queue$DEQ,
       inst1_ff_gemm_queue$EMPTY_N,
       inst1_ff_gemm_queue$ENQ,
       inst1_ff_gemm_queue$FULL_N;

  // ports of submodule inst1_ff_gemm_to_alu
  wire inst1_ff_gemm_to_alu$CLR,
       inst1_ff_gemm_to_alu$DEQ,
       inst1_ff_gemm_to_alu$D_IN,
       inst1_ff_gemm_to_alu$EMPTY_N,
       inst1_ff_gemm_to_alu$ENQ,
       inst1_ff_gemm_to_alu$FULL_N;

  // ports of submodule inst1_ff_gemm_to_load
  wire inst1_ff_gemm_to_load$CLR,
       inst1_ff_gemm_to_load$DEQ,
       inst1_ff_gemm_to_load$D_IN,
       inst1_ff_gemm_to_load$EMPTY_N,
       inst1_ff_gemm_to_load$ENQ,
       inst1_ff_gemm_to_load$FULL_N;

  // ports of submodule inst1_ff_load_params
  wire [119 : 0] inst1_ff_load_params$D_IN, inst1_ff_load_params$D_OUT;
  wire inst1_ff_load_params$CLR,
       inst1_ff_load_params$DEQ,
       inst1_ff_load_params$EMPTY_N,
       inst1_ff_load_params$ENQ,
       inst1_ff_load_params$FULL_N;

  // ports of submodule inst1_ff_load_queue
  wire [3 : 0] inst1_ff_load_queue$D_IN, inst1_ff_load_queue$D_OUT;
  wire inst1_ff_load_queue$CLR,
       inst1_ff_load_queue$DEQ,
       inst1_ff_load_queue$EMPTY_N,
       inst1_ff_load_queue$ENQ,
       inst1_ff_load_queue$FULL_N;

  // ports of submodule inst1_ff_load_to_gemm
  wire inst1_ff_load_to_gemm$CLR,
       inst1_ff_load_to_gemm$DEQ,
       inst1_ff_load_to_gemm$D_IN,
       inst1_ff_load_to_gemm$EMPTY_N,
       inst1_ff_load_to_gemm$ENQ,
       inst1_ff_load_to_gemm$FULL_N;

  // ports of submodule inst1_ff_store_params
  wire [119 : 0] inst1_ff_store_params$D_IN, inst1_ff_store_params$D_OUT;
  wire inst1_ff_store_params$CLR,
       inst1_ff_store_params$DEQ,
       inst1_ff_store_params$EMPTY_N,
       inst1_ff_store_params$ENQ,
       inst1_ff_store_params$FULL_N;

  // ports of submodule inst1_ff_store_queue
  wire [3 : 0] inst1_ff_store_queue$D_IN, inst1_ff_store_queue$D_OUT;
  wire inst1_ff_store_queue$CLR,
       inst1_ff_store_queue$DEQ,
       inst1_ff_store_queue$EMPTY_N,
       inst1_ff_store_queue$ENQ,
       inst1_ff_store_queue$FULL_N;

  // ports of submodule inst1_ff_store_to_alu
  wire inst1_ff_store_to_alu$CLR,
       inst1_ff_store_to_alu$DEQ,
       inst1_ff_store_to_alu$D_IN,
       inst1_ff_store_to_alu$EMPTY_N,
       inst1_ff_store_to_alu$ENQ,
       inst1_ff_store_to_alu$FULL_N;

  // action method ifc_put_load_params_put
  assign RDY_ifc_put_load_params_put =
	     inst1_ff_load_queue$FULL_N && inst1_ff_load_params$FULL_N ;

  // action method ifc_put_store_params_put
  assign RDY_ifc_put_store_params_put =
	     inst1_ff_store_queue$FULL_N && inst1_ff_store_params$FULL_N ;

  // action method ifc_put_compute_params_put
  assign RDY_ifc_put_compute_params_put =
	     inst1_ff_gemm_queue$FULL_N && inst1_ff_gemm_params$FULL_N ;

  // action method ifc_put_alu_params_put
  assign RDY_ifc_put_alu_params_put =
	     inst1_ff_alu_queue$FULL_N && inst1_ff_alu_params$FULL_N ;

  // actionvalue method ifc_get_load_instruction_get
  assign ifc_get_load_instruction_get = inst1_ff_load_params$D_OUT ;
  assign RDY_ifc_get_load_instruction_get =
	     inst1_ff_load_queue$EMPTY_N &&
	     (!inst1_ff_load_queue$D_OUT[1] ||
	      inst1_ff_gemm_to_load$EMPTY_N) &&
	     inst1_ff_load_params$EMPTY_N ;

  // actionvalue method ifc_get_store_instruction_get
  assign ifc_get_store_instruction_get = inst1_ff_store_params$D_OUT ;
  assign RDY_ifc_get_store_instruction_get =
	     inst1_ff_store_queue$EMPTY_N &&
	     (!inst1_ff_store_queue$D_OUT[3] ||
	      inst1_ff_alu_to_store$EMPTY_N) &&
	     inst1_ff_store_params$EMPTY_N ;

  // actionvalue method ifc_get_gemm_instruction_get
  assign ifc_get_gemm_instruction_get = inst1_ff_gemm_params$D_OUT ;
  assign RDY_ifc_get_gemm_instruction_get =
	     inst1_ff_gemm_queue$EMPTY_N &&
	     (!inst1_ff_gemm_queue$D_OUT[3] ||
	      inst1_ff_load_to_gemm$EMPTY_N) &&
	     (!inst1_ff_gemm_queue$D_OUT[1] ||
	      inst1_ff_alu_to_gemm$EMPTY_N) &&
	     inst1_ff_gemm_params$EMPTY_N ;

  // actionvalue method ifc_get_alu_instruction_get
  assign ifc_get_alu_instruction_get = inst1_ff_alu_params$D_OUT ;
  assign RDY_ifc_get_alu_instruction_get =
	     inst1_ff_alu_queue$EMPTY_N &&
	     (!inst1_ff_alu_queue$D_OUT[3] || inst1_ff_gemm_to_alu$EMPTY_N) &&
	     (!inst1_ff_alu_queue$D_OUT[1] ||
	      inst1_ff_store_to_alu$EMPTY_N) &&
	     inst1_ff_alu_params$EMPTY_N ;

  // action method ifc_put_load_complete_put
  assign RDY_ifc_put_load_complete_put =
	     inst1_ff_load_queue$EMPTY_N && inst1_ff_load_to_gemm$FULL_N ;

  // action method ifc_put_store_complete_put
  assign RDY_ifc_put_store_complete_put =
	     inst1_ff_store_queue$EMPTY_N && inst1_ff_store_to_alu$FULL_N ;

  // action method ifc_put_gemm_complete_put
  assign RDY_ifc_put_gemm_complete_put =
	     inst1_ff_gemm_queue$EMPTY_N && inst1_ff_gemm_to_load$FULL_N &&
	     inst1_ff_gemm_to_alu$FULL_N ;

  // action method ifc_put_alu_complete_put
  assign RDY_ifc_put_alu_complete_put =
	     inst1_ff_alu_queue$EMPTY_N && inst1_ff_alu_to_gemm$FULL_N &&
	     inst1_ff_alu_to_store$FULL_N ;

  // submodule inst1_ff_alu_params
  SizedFIFO #(.p1width(32'd120),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_alu_params(.RST(RST_N),
						   .CLK(CLK),
						   .D_IN(inst1_ff_alu_params$D_IN),
						   .ENQ(inst1_ff_alu_params$ENQ),
						   .DEQ(inst1_ff_alu_params$DEQ),
						   .CLR(inst1_ff_alu_params$CLR),
						   .D_OUT(inst1_ff_alu_params$D_OUT),
						   .FULL_N(inst1_ff_alu_params$FULL_N),
						   .EMPTY_N(inst1_ff_alu_params$EMPTY_N));

  // submodule inst1_ff_alu_queue
  SizedFIFO #(.p1width(32'd4),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_alu_queue(.RST(RST_N),
						  .CLK(CLK),
						  .D_IN(inst1_ff_alu_queue$D_IN),
						  .ENQ(inst1_ff_alu_queue$ENQ),
						  .DEQ(inst1_ff_alu_queue$DEQ),
						  .CLR(inst1_ff_alu_queue$CLR),
						  .D_OUT(inst1_ff_alu_queue$D_OUT),
						  .FULL_N(inst1_ff_alu_queue$FULL_N),
						  .EMPTY_N(inst1_ff_alu_queue$EMPTY_N));

  // submodule inst1_ff_alu_to_gemm
  SizedFIFO #(.p1width(32'd1),
	      .p2depth(32'd4),
	      .p3cntr_width(32'd2),
	      .guarded(32'd1)) inst1_ff_alu_to_gemm(.RST(RST_N),
						    .CLK(CLK),
						    .D_IN(inst1_ff_alu_to_gemm$D_IN),
						    .ENQ(inst1_ff_alu_to_gemm$ENQ),
						    .DEQ(inst1_ff_alu_to_gemm$DEQ),
						    .CLR(inst1_ff_alu_to_gemm$CLR),
						    .D_OUT(),
						    .FULL_N(inst1_ff_alu_to_gemm$FULL_N),
						    .EMPTY_N(inst1_ff_alu_to_gemm$EMPTY_N));

  // submodule inst1_ff_alu_to_store
  SizedFIFO #(.p1width(32'd1),
	      .p2depth(32'd4),
	      .p3cntr_width(32'd2),
	      .guarded(32'd1)) inst1_ff_alu_to_store(.RST(RST_N),
						     .CLK(CLK),
						     .D_IN(inst1_ff_alu_to_store$D_IN),
						     .ENQ(inst1_ff_alu_to_store$ENQ),
						     .DEQ(inst1_ff_alu_to_store$DEQ),
						     .CLR(inst1_ff_alu_to_store$CLR),
						     .D_OUT(),
						     .FULL_N(inst1_ff_alu_to_store$FULL_N),
						     .EMPTY_N(inst1_ff_alu_to_store$EMPTY_N));

  // submodule inst1_ff_gemm_params
  SizedFIFO #(.p1width(32'd120),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_gemm_params(.RST(RST_N),
						    .CLK(CLK),
						    .D_IN(inst1_ff_gemm_params$D_IN),
						    .ENQ(inst1_ff_gemm_params$ENQ),
						    .DEQ(inst1_ff_gemm_params$DEQ),
						    .CLR(inst1_ff_gemm_params$CLR),
						    .D_OUT(inst1_ff_gemm_params$D_OUT),
						    .FULL_N(inst1_ff_gemm_params$FULL_N),
						    .EMPTY_N(inst1_ff_gemm_params$EMPTY_N));

  // submodule inst1_ff_gemm_queue
  SizedFIFO #(.p1width(32'd4),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_gemm_queue(.RST(RST_N),
						   .CLK(CLK),
						   .D_IN(inst1_ff_gemm_queue$D_IN),
						   .ENQ(inst1_ff_gemm_queue$ENQ),
						   .DEQ(inst1_ff_gemm_queue$DEQ),
						   .CLR(inst1_ff_gemm_queue$CLR),
						   .D_OUT(inst1_ff_gemm_queue$D_OUT),
						   .FULL_N(inst1_ff_gemm_queue$FULL_N),
						   .EMPTY_N(inst1_ff_gemm_queue$EMPTY_N));

  // submodule inst1_ff_gemm_to_alu
  SizedFIFO #(.p1width(32'd1),
	      .p2depth(32'd4),
	      .p3cntr_width(32'd2),
	      .guarded(32'd1)) inst1_ff_gemm_to_alu(.RST(RST_N),
						    .CLK(CLK),
						    .D_IN(inst1_ff_gemm_to_alu$D_IN),
						    .ENQ(inst1_ff_gemm_to_alu$ENQ),
						    .DEQ(inst1_ff_gemm_to_alu$DEQ),
						    .CLR(inst1_ff_gemm_to_alu$CLR),
						    .D_OUT(),
						    .FULL_N(inst1_ff_gemm_to_alu$FULL_N),
						    .EMPTY_N(inst1_ff_gemm_to_alu$EMPTY_N));

  // submodule inst1_ff_gemm_to_load
  SizedFIFO #(.p1width(32'd1),
	      .p2depth(32'd4),
	      .p3cntr_width(32'd2),
	      .guarded(32'd1)) inst1_ff_gemm_to_load(.RST(RST_N),
						     .CLK(CLK),
						     .D_IN(inst1_ff_gemm_to_load$D_IN),
						     .ENQ(inst1_ff_gemm_to_load$ENQ),
						     .DEQ(inst1_ff_gemm_to_load$DEQ),
						     .CLR(inst1_ff_gemm_to_load$CLR),
						     .D_OUT(),
						     .FULL_N(inst1_ff_gemm_to_load$FULL_N),
						     .EMPTY_N(inst1_ff_gemm_to_load$EMPTY_N));

  // submodule inst1_ff_load_params
  SizedFIFO #(.p1width(32'd120),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_load_params(.RST(RST_N),
						    .CLK(CLK),
						    .D_IN(inst1_ff_load_params$D_IN),
						    .ENQ(inst1_ff_load_params$ENQ),
						    .DEQ(inst1_ff_load_params$DEQ),
						    .CLR(inst1_ff_load_params$CLR),
						    .D_OUT(inst1_ff_load_params$D_OUT),
						    .FULL_N(inst1_ff_load_params$FULL_N),
						    .EMPTY_N(inst1_ff_load_params$EMPTY_N));

  // submodule inst1_ff_load_queue
  SizedFIFO #(.p1width(32'd4),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_load_queue(.RST(RST_N),
						   .CLK(CLK),
						   .D_IN(inst1_ff_load_queue$D_IN),
						   .ENQ(inst1_ff_load_queue$ENQ),
						   .DEQ(inst1_ff_load_queue$DEQ),
						   .CLR(inst1_ff_load_queue$CLR),
						   .D_OUT(inst1_ff_load_queue$D_OUT),
						   .FULL_N(inst1_ff_load_queue$FULL_N),
						   .EMPTY_N(inst1_ff_load_queue$EMPTY_N));

  // submodule inst1_ff_load_to_gemm
  SizedFIFO #(.p1width(32'd1),
	      .p2depth(32'd4),
	      .p3cntr_width(32'd2),
	      .guarded(32'd1)) inst1_ff_load_to_gemm(.RST(RST_N),
						     .CLK(CLK),
						     .D_IN(inst1_ff_load_to_gemm$D_IN),
						     .ENQ(inst1_ff_load_to_gemm$ENQ),
						     .DEQ(inst1_ff_load_to_gemm$DEQ),
						     .CLR(inst1_ff_load_to_gemm$CLR),
						     .D_OUT(),
						     .FULL_N(inst1_ff_load_to_gemm$FULL_N),
						     .EMPTY_N(inst1_ff_load_to_gemm$EMPTY_N));

  // submodule inst1_ff_store_params
  SizedFIFO #(.p1width(32'd120),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_store_params(.RST(RST_N),
						     .CLK(CLK),
						     .D_IN(inst1_ff_store_params$D_IN),
						     .ENQ(inst1_ff_store_params$ENQ),
						     .DEQ(inst1_ff_store_params$DEQ),
						     .CLR(inst1_ff_store_params$CLR),
						     .D_OUT(inst1_ff_store_params$D_OUT),
						     .FULL_N(inst1_ff_store_params$FULL_N),
						     .EMPTY_N(inst1_ff_store_params$EMPTY_N));

  // submodule inst1_ff_store_queue
  SizedFIFO #(.p1width(32'd4),
	      .p2depth(32'd8),
	      .p3cntr_width(32'd3),
	      .guarded(32'd1)) inst1_ff_store_queue(.RST(RST_N),
						    .CLK(CLK),
						    .D_IN(inst1_ff_store_queue$D_IN),
						    .ENQ(inst1_ff_store_queue$ENQ),
						    .DEQ(inst1_ff_store_queue$DEQ),
						    .CLR(inst1_ff_store_queue$CLR),
						    .D_OUT(inst1_ff_store_queue$D_OUT),
						    .FULL_N(inst1_ff_store_queue$FULL_N),
						    .EMPTY_N(inst1_ff_store_queue$EMPTY_N));

  // submodule inst1_ff_store_to_alu
  SizedFIFO #(.p1width(32'd1),
	      .p2depth(32'd4),
	      .p3cntr_width(32'd2),
	      .guarded(32'd1)) inst1_ff_store_to_alu(.RST(RST_N),
						     .CLK(CLK),
						     .D_IN(inst1_ff_store_to_alu$D_IN),
						     .ENQ(inst1_ff_store_to_alu$ENQ),
						     .DEQ(inst1_ff_store_to_alu$DEQ),
						     .CLR(inst1_ff_store_to_alu$CLR),
						     .D_OUT(),
						     .FULL_N(inst1_ff_store_to_alu$FULL_N),
						     .EMPTY_N(inst1_ff_store_to_alu$EMPTY_N));

  // submodule inst1_ff_alu_params
  assign inst1_ff_alu_params$D_IN = ifc_put_alu_params_put[119:0] ;
  assign inst1_ff_alu_params$ENQ = EN_ifc_put_alu_params_put ;
  assign inst1_ff_alu_params$DEQ = EN_ifc_get_alu_instruction_get ;
  assign inst1_ff_alu_params$CLR = 1'b0 ;

  // submodule inst1_ff_alu_queue
  assign inst1_ff_alu_queue$D_IN = ifc_put_alu_params_put[123:120] ;
  assign inst1_ff_alu_queue$ENQ = EN_ifc_put_alu_params_put ;
  assign inst1_ff_alu_queue$DEQ = EN_ifc_put_alu_complete_put ;
  assign inst1_ff_alu_queue$CLR = 1'b0 ;

  // submodule inst1_ff_alu_to_gemm
  assign inst1_ff_alu_to_gemm$D_IN = 1'd1 ;
  assign inst1_ff_alu_to_gemm$ENQ =
	     EN_ifc_put_alu_complete_put && inst1_ff_alu_queue$D_OUT[2] ;
  assign inst1_ff_alu_to_gemm$DEQ =
	     EN_ifc_get_gemm_instruction_get &&
	     inst1_ff_alu_to_gemm$EMPTY_N &&
	     inst1_ff_gemm_queue$D_OUT[1] ;
  assign inst1_ff_alu_to_gemm$CLR = 1'b0 ;

  // submodule inst1_ff_alu_to_store
  assign inst1_ff_alu_to_store$D_IN = 1'd1 ;
  assign inst1_ff_alu_to_store$ENQ =
	     EN_ifc_put_alu_complete_put && inst1_ff_alu_queue$D_OUT[0] ;
  assign inst1_ff_alu_to_store$DEQ =
	     EN_ifc_get_store_instruction_get &&
	     inst1_ff_alu_to_store$EMPTY_N &&
	     inst1_ff_store_queue$D_OUT[3] ;
  assign inst1_ff_alu_to_store$CLR = 1'b0 ;

  // submodule inst1_ff_gemm_params
  assign inst1_ff_gemm_params$D_IN = ifc_put_compute_params_put[119:0] ;
  assign inst1_ff_gemm_params$ENQ = EN_ifc_put_compute_params_put ;
  assign inst1_ff_gemm_params$DEQ = EN_ifc_get_gemm_instruction_get ;
  assign inst1_ff_gemm_params$CLR = 1'b0 ;

  // submodule inst1_ff_gemm_queue
  assign inst1_ff_gemm_queue$D_IN = ifc_put_compute_params_put[123:120] ;
  assign inst1_ff_gemm_queue$ENQ = EN_ifc_put_compute_params_put ;
  assign inst1_ff_gemm_queue$DEQ = EN_ifc_put_gemm_complete_put ;
  assign inst1_ff_gemm_queue$CLR = 1'b0 ;

  // submodule inst1_ff_gemm_to_alu
  assign inst1_ff_gemm_to_alu$D_IN = 1'd1 ;
  assign inst1_ff_gemm_to_alu$ENQ =
	     EN_ifc_put_gemm_complete_put && inst1_ff_gemm_queue$D_OUT[0] ;
  assign inst1_ff_gemm_to_alu$DEQ =
	     EN_ifc_get_alu_instruction_get && inst1_ff_gemm_to_alu$EMPTY_N &&
	     inst1_ff_alu_queue$D_OUT[3] ;
  assign inst1_ff_gemm_to_alu$CLR = 1'b0 ;

  // submodule inst1_ff_gemm_to_load
  assign inst1_ff_gemm_to_load$D_IN = 1'd1 ;
  assign inst1_ff_gemm_to_load$ENQ =
	     EN_ifc_put_gemm_complete_put && inst1_ff_gemm_queue$D_OUT[2] ;
  assign inst1_ff_gemm_to_load$DEQ =
	     EN_ifc_get_load_instruction_get &&
	     inst1_ff_gemm_to_load$EMPTY_N &&
	     inst1_ff_load_queue$D_OUT[1] ;
  assign inst1_ff_gemm_to_load$CLR = 1'b0 ;

  // submodule inst1_ff_load_params
  assign inst1_ff_load_params$D_IN = ifc_put_load_params_put[119:0] ;
  assign inst1_ff_load_params$ENQ = EN_ifc_put_load_params_put ;
  assign inst1_ff_load_params$DEQ = EN_ifc_get_load_instruction_get ;
  assign inst1_ff_load_params$CLR = 1'b0 ;

  // submodule inst1_ff_load_queue
  assign inst1_ff_load_queue$D_IN = ifc_put_load_params_put[123:120] ;
  assign inst1_ff_load_queue$ENQ = EN_ifc_put_load_params_put ;
  assign inst1_ff_load_queue$DEQ = EN_ifc_put_load_complete_put ;
  assign inst1_ff_load_queue$CLR = 1'b0 ;

  // submodule inst1_ff_load_to_gemm
  assign inst1_ff_load_to_gemm$D_IN = 1'd1 ;
  assign inst1_ff_load_to_gemm$ENQ =
	     EN_ifc_put_load_complete_put && inst1_ff_load_queue$D_OUT[0] ;
  assign inst1_ff_load_to_gemm$DEQ =
	     EN_ifc_get_gemm_instruction_get &&
	     inst1_ff_load_to_gemm$EMPTY_N &&
	     inst1_ff_gemm_queue$D_OUT[3] ;
  assign inst1_ff_load_to_gemm$CLR = 1'b0 ;

  // submodule inst1_ff_store_params
  assign inst1_ff_store_params$D_IN = ifc_put_store_params_put[119:0] ;
  assign inst1_ff_store_params$ENQ = EN_ifc_put_store_params_put ;
  assign inst1_ff_store_params$DEQ = EN_ifc_get_store_instruction_get ;
  assign inst1_ff_store_params$CLR = 1'b0 ;

  // submodule inst1_ff_store_queue
  assign inst1_ff_store_queue$D_IN = ifc_put_store_params_put[123:120] ;
  assign inst1_ff_store_queue$ENQ = EN_ifc_put_store_params_put ;
  assign inst1_ff_store_queue$DEQ = EN_ifc_put_store_complete_put ;
  assign inst1_ff_store_queue$CLR = 1'b0 ;

  // submodule inst1_ff_store_to_alu
  assign inst1_ff_store_to_alu$D_IN = 1'd1 ;
  assign inst1_ff_store_to_alu$ENQ =
	     EN_ifc_put_store_complete_put && inst1_ff_store_queue$D_OUT[2] ;
  assign inst1_ff_store_to_alu$DEQ =
	     EN_ifc_get_alu_instruction_get &&
	     inst1_ff_store_to_alu$EMPTY_N &&
	     inst1_ff_alu_queue$D_OUT[1] ;
  assign inst1_ff_store_to_alu$CLR = 1'b0 ;
endmodule  // mkdep_Tb

