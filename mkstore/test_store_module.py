import random
import sys
import cocotb
import logging as log
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.monitors import BusMonitor
from cocotb.drivers import BusDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure
from cocotb.clock import Clock
from store_module_model import store_module_model
from cocotb_coverage.coverage import *


# Store module parameters
#
# Store instruction -> (SRAM request -> SRAM response -> AXI_write_request -> AXI_write_response) -> Store complete

bank_bits = 4
index_bits = 6
valid_bits = 4
num_buffers_bits = 2
data_width = 128

obuf1_start = 0x03000000
obuf1_end   = 0x037fffff
obuf2_start = 0x03800000
obuf2_end   = 0x03ffffff

store_master_index = 3

##Current load module parameters
#Ifc_load_Module#(`DRAM_ADDR_WIDTH, Datawidth, `SRAM_ADDR_WIDTH, 
#                                    `WBUF_INDEX, `WBUF_Bankbits, `INWIDTH,
#                                    `IBUF_INDEX, `IBUF_Bankbits, `INWIDTH,
#                                    `OBUF_INDEX, `OBUF_Bankbits, `OUTWIDTH, 
#                                    Max_index, Max_bank, Max_data, Max_words, 20)
##

Store_parameters_Coverage = coverage_section (
  CoverPoint("top.inp_x_size", vname="inp_x_size", bins = [1,2,4,8,16,32,64,128]),
  CoverPoint("top.inp_y_size", vname="inp_y_size", bins = [1,2,4,8,16,32,64,128]),
  CoverPoint("top.inp_z_size", vname="inp_z_size", bins = [1,2,4,8,16]),
  CoverPoint("top.inp_y_stride", vname="inp_y_stride", bins = [1,2,4,8,16,32,64,128]),
  CoverPoint("top.inp_z_stride", vname="inp_z_stride", bins = [1,2,4,8,16,32,64,128]),
  CoverPoint("top.inp_bitwidth", vname="inp_bitwidth", bins = [0]),
  CoverCross("top.cross_cover", items = ["top.inp_x_size", "top.inp_y_size", "top.inp_z_size", 
                                    "top.inp_y_stride", "top.inp_z_stride", "top.inp_bitwidth"])
)


class Store_instruction(BusDriver):

    _signals = [
        'EN_subifc_put_storeparams_put',
        'subifc_put_storeparams_put',
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


class Store_instruction_transaction(object):

    def __init__(self, tb,
                 EN_subifc_put_storeparams_put=0,
                 subifc_put_storeparams_put=0
                 ):
        self.EN_subifc_put_storeparams_put = BinaryValue(
            EN_subifc_put_storeparams_put, tb.EN_width, False)
        self.subifc_put_storeparams_put = BinaryValue(
            subifc_put_storeparams_put, tb.store_instruction_width, False)


class Store_instruction_monitor(BusMonitor):

    _signals = [
        'EN_subifc_put_storeparams_put',
        'subifc_put_storeparams_put',
    ]

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):
        EN_inp_edge = RisingEdge(self.bus.EN_subifc_put_storeparams_put)
        while True:
            yield EN_inp_edge
            if self.bus.EN_subifc_put_storeparams_put.value.integer == 1:
                print('[IN_MON] {0:25} : {1}'.format(
                    'subifc_put_storeparams_put', self.bus.subifc_put_storeparams_put.value.integer))
                vec = (
                    self.bus.EN_subifc_put_storeparams_put.value.integer,
                    self.bus.subifc_put_storeparams_put.value.integer
                )
                self._recv(vec)
            yield RisingEdge(self.clock)


class AXI_master_write_response(BusDriver):

    _signals = [
        # 1 # Write address ready. This signal indicates that the slave is ready to accept an address and associated control signals.
        'master_AWREADY',
        'master_WREADY',
        'master_BVALID',
        'master_BRESP',
        'master_BID',
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


class AXI_master_write_response_transaction(object):

    def __init__(self, tb,
                 master_AWREADY=1,
                 master_WREADY=1,
                 master_BVALID=0,
                 master_BRESP=0,
                 master_BID=0
                 ):
        self.master_AWREADY = BinaryValue(master_AWREADY, tb.awready_width, False)
        self.master_WREADY = BinaryValue(master_WREADY, tb.wready_width, False)
        self.master_BVALID = BinaryValue(master_BVALID, tb.bvalid_width, False)
        self.master_BRESP = BinaryValue(master_BRESP, tb.bresp_width, False)
        self.master_BID = BinaryValue(master_BID, tb.bid_width, False)


class AXI_master_write_response_monitor(BusMonitor):

    _signals = [
        'master_AWREADY',
        'master_WREADY',
        'master_BVALID',
        'master_BRESP',
        'master_BID',
    ]

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):
        while True:
            write_valid_edge = RisingEdge(self.bus.master_BVALID)
            yield write_valid_edge
            if self.bus.master_BVALID.value.integer == 1:
                print('[IN_MON] {0:25} : {1}'.format('master_AWREADY', self.bus.master_AWREADY.value.integer))
                print('[IN_MON] {0:25} : {1}'.format('master_WREADY', self.bus.master_WREADY.value.integer))
                print('[IN_MON] {0:25} : {1}'.format('master_BVALID', self.bus.master_BVALID.value.integer))
                print('[IN_MON] {0:25} : {1}'.format('master_BRESP', self.bus.master_BRESP.value.integer))
                print('[IN_MON] {0:25} : {1}'.format('master_BID', self.bus.master_BID.value.integer))

                vec = (
                    self.bus.master_AWREADY.value.integer,
                    self.bus.master_WREADY.value.integer,
                    self.bus.master_BVALID.value.integer,
                    self.bus.master_BRESP.value.integer,
                    self.bus.master_BID.value.integer
                )
                self._recv(vec)
            yield RisingEdge(self.clock)

class AXI_master_write_request_transaction(object):
    """ Transaction to be expected / received by OutputMonitor"""

    def __init__(self, tb=None,
                 #
                 master_AWVALID=1, 
                 master_AWADDR=0,
                 master_AWPROT=0,
                 master_AWLEN=0,
                 master_AWSIZE=0,
                 master_AWBURST=0,  
                 master_AWID=0,
                 master_WVALID=1,
                 master_WDATA=0,
                 master_WSTRB=0,
                 master_WLAST=0,
                 master_WID=0,
                 master_BREADY=0,
                 ):
        """For expected transactions, value 'None' means don't care.
        tb must be an instance of the Testbench class."""
#
        if master_AWVALID is not None and isinstance(master_AWVALID, int):
            master_AWVALID = BinaryValue(master_AWVALID, tb.awvalid_width, False)
        if master_AWADDR is not None and isinstance(master_AWADDR, int):
            master_AWADDR = BinaryValue(master_AWADDR, tb.awaddr_width, False)
        if master_AWPROT is not None and isinstance(master_AWPROT, int):
            master_AWPROT = BinaryValue(master_AWPROT, tb.awprot_width, False)
        if master_AWLEN is not None and isinstance(master_AWLEN, int):
            master_AWLEN = BinaryValue(master_AWLEN, tb.awlen_width, False)
        if master_AWSIZE is not None and isinstance(master_AWSIZE, int):
            master_AWSIZE = BinaryValue(master_AWSIZE, tb.awsize_width, False)
        if master_AWBURST is not None and isinstance(master_AWBURST, int):
            master_AWBURST = BinaryValue(master_AWBURST, tb.awburst_width, False)
        if master_AWID is not None and isinstance(master_AWID, int):
            master_AWID = BinaryValue(master_AWID, tb.awid_width, False)
        if master_WVALID is not None and isinstance(master_WVALID, int):
            master_WVALID = BinaryValue(master_WVALID, tb.wvalid_width, False)
        if master_WDATA is not None and isinstance(master_WDATA, int):
            master_WDATA = BinaryValue(master_WDATA, tb.wdata_width, False)
        if master_WSTRB is not None and isinstance(master_WSTRB, int):
            master_WSTRB = BinaryValue(master_WSTRB, tb.wstrb_width, False)
        if master_WLAST is not None and isinstance(master_WLAST, int):
            master_WLAST = BinaryValue(master_WLAST, tb.wlast_width, False)
        if master_WID is not None and isinstance(master_WID, int):
            master_WID = BinaryValue(master_WID, tb.wid_width, False)
        if master_BREADY is not None and isinstance(master_BREADY, int):
            master_BREADY = BinaryValue(master_BREADY, tb.bready_width, False)
#
        self.value = (
            master_AWVALID,
            master_AWADDR,
            master_AWPROT,
            master_AWLEN,
            master_AWSIZE,
            master_AWBURST,
            master_AWID,
            master_WVALID,
            master_WDATA,
            master_WSTRB,
            master_WLAST,
            master_WID,
            master_BREADY
        )


class AXI_master_write_request_monitor(BusMonitor):
    """Observes signals of DUT"""
    _signals = [
        #
        'master_AWVALID',
        'master_AWADDR',
        'master_AWPROT',
        'master_AWLEN',
        'master_AWSIZE',
        'master_AWBURST',
        'master_AWID',
        'master_WVALID',
        'master_WDATA',
        'master_WSTRB',
        'master_WLAST',
        'master_WID',
        'master_BREADY',
        'master_AWREADY',
    ]

    def __init__(self, dut, tb, callback=None, event=None):
        BusMonitor.__init__(self, dut, None, dut.CLK, dut.RST_N,
                            callback=callback, event=event)
        self.name = "out"
        self.tb = tb

    @coroutine
    def _monitor_recv(self):
        outp_ready_edge = RisingEdge(self.clock)
        while True:
            yield outp_ready_edge
            if self.bus.master_AWVALID.value.integer == 1 and self.bus.master_AWREADY.value.integer == 1:
                print('[DUT_MON] {0:<25} : {1}'.format('master_BREADY ', hex(self.bus.master_BREADY.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWVALID ', hex(self.bus.master_AWVALID.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWADDR ', hex(self.bus.master_AWADDR.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWPROT ', hex(self.bus.master_AWPROT.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWLEN ', hex(self.bus.master_AWLEN.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWSIZE ', hex(self.bus.master_AWSIZE.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWBURST ', hex(self.bus.master_AWBURST.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWID ', hex(self.bus.master_AWID.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_WVALID ', hex(self.bus.master_WVALID.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_WDATA ', hex(self.bus.master_WDATA.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_WSTRB ', hex(self.bus.master_WSTRB.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_WLAST ', hex(self.bus.master_WLAST.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_WID ', hex(self.bus.master_WID.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('master_AWREADY ',
                    hex(self.bus.master_AWREADY.value)))

                
                vec = (
                    self.bus.master_BREADY.value.integer,
                    self.bus.master_AWVALID.value.integer,
                    self.bus.master_AWADDR.value.integer,
                    self.bus.master_AWPROT.value.integer,
                    self.bus.master_AWLEN.value.integer,
                    self.bus.master_AWSIZE.value.integer,
                    self.bus.master_AWBURST.value.integer,
                    self.bus.master_AWID.value.integer,
                    self.bus.master_WVALID.value.integer,
                    self.bus.master_WDATA.value.integer,
                    self.bus.master_WSTRB.value.integer,
                    self.bus.master_WLAST.value.integer,
                    self.bus.master_WID.value.integer,
                    self.bus.master_AWREADY.value.integer,
                )
                self._recv(vec)
            #yield RisingEdge(self.clock)

class SRAM_read_transaction(object):
    """ Transaction to be expected / received by OutputMonitor"""

    def __init__(self, tb=None,
                 #
                 RDY_send_sram_req=0,
                 send_sram_req=0,
                 ):
#
        if RDY_send_sram_req is not None and isinstance(RDY_send_sram_req, int):
            RDY_send_sram_req = BinaryValue(RDY_send_sram_req, tb.RDY_width, False)
        if send_sram_req is not None and isinstance(send_sram_req, int):
            send_sram_req = BinaryValue(send_sram_req, tb.send_sram_req_width, False)
#
        self.value = (
            RDY_send_sram_req,
            send_sram_req
        )


class SRAM_read_monitor(BusMonitor):
    """Observes signals of DUT"""
    _signals = [
        #
        'RDY_send_sram_req',
        'send_sram_req',
        'EN_send_sram_req',
    ]

    def __init__(self, dut, tb, callback=None, event=None):
        BusMonitor.__init__(self, dut, None, dut.CLK, dut.RST_N,
                            callback=callback, event=event)
        self.name = "out"
        self.tb = tb

    @coroutine
    def _monitor_recv(self):
        outp_ready_edge = RisingEdge(self.bus.RDY_send_sram_req)
        while True:
            #yield outp_ready_edge
            if self.bus.RDY_send_sram_req.value.integer == 1 and self.bus.EN_send_sram_req.value.integer == 1:
                print('[DUT_MON] {0:<25} : {1}'.format('RDY_send_sram_req ', hex(self.bus.RDY_send_sram_req.value)))
                print('[DUT_MON] {0:<25} : {1}'.format('send_sram_req ', hex(self.bus.send_sram_req.value)))
                
                vec = (
                    self.bus.RDY_send_sram_req.value.integer,
                    self.bus.send_sram_req.value.integer
                )
                self._recv(vec)
            yield RisingEdge(self.clock)


class DUTScoreboard(Scoreboard):
    def compare(self, exp_count, exp_addr,exp_wrstrb, exp_awlen, 
                got_count, got_addr,got_wrstrb, got_awlen, 
                exp_buffer, exp_index, exp_bank, exp_valid, 
                got_buffer, got_index, got_bank, got_valid,log, **_):
        print("Entered Scoreboard")
        print(exp_count)
        print(got_count)
        print(exp_addr)
        print(got_addr)
        print(exp_awlen)
        print(got_awlen)
        print(exp_buffer)
        print(got_buffer)
        print(exp_index)
        print(got_index)
        print(exp_bank)
        print(got_bank)
        print(exp_valid)
        print(got_valid)
        if(exp_count == got_count):
            if(exp_awlen == got_awlen):
                for n in range(exp_count):
                    if(exp_addr[n] == got_addr[n]):
                        print("DRAM Address matched : ",hex(exp_addr[n]),n)
                    else:
                        print("DRAM Address mismatch : ",hex(exp_addr[n]),hex(got_addr[n]),n)
            else:
                print("AWLEN mismatch ",exp_awlen,got_awlen)
        else:
            print("mismatch in number of AXI requests ", exp_count, got_count)


        if(exp_buffer == got_buffer):
            print("SRAM Buffer matched : ",hex(exp_buffer))
        else:
            print("SRAM Buffer mismatch ", hex(exp_buffer), hex(got_buffer))
        for n in range(exp_count*(exp_awlen+1)):
            if(exp_bank[n] == got_bank[n]):
                print("SRAM Bank matched : ",hex(exp_bank[n]))
            else:
                print("SRAM Bank mismatch : ",hex(exp_bank[n]), hex(got_bank[n]))
            if(exp_index[n] == got_index[n]):
                print("SRAM Index matched : ",hex(exp_index[n]))
            else:
                print("SRAM Index mismatch : ",hex(exp_index[n]), hex(got_index[n]))
            if(exp_valid[n] == got_valid[n]):
                print("SRAM Valid matched : ",hex(exp_valid[n]))
            else:
                print("SRAM Valid mismatch : ",hex(exp_valid[n]), hex(got_valid[n]))


class TestBench(object):
    """Verification Test Bench"""

    def __init__(self, dut):
        self.dut = dut
        self.stopped = False

        """Signal length"""
        self.EN_width = 1
        self.RDY_width = 1
        self.store_instruction_width = 120
        self.awready_width = 1
        self.wready_width = 1
        self.bvalid_width = 1
        self.bresp_width = 2
        self.bid_width = 4

        self.awvalid_width = 1
        self.awaddr_width = 32
        self.awprot_width = 3
        self.awlen_width = 8
        self.awsize_width = 3
        self.awburst_width = 2
        self.awid_width = 4
        self.wvalid_width = 1
        self.wdata_width = 128
        self.wstrb_width = 16
        self.wlast_width = 1
        self.wid_width = 4
        self.bready_width = 1

        self.out_width = 32
        self.in_width = 8

        self.send_sram_req_width = 27

        self.store_instruction_drv = Store_instruction(dut)
        self.store_instruction_mon = Store_instruction_monitor(
            dut, callback=self.store_module_model)
        self.axi_master_write_response_drv = AXI_master_write_response(dut)
        self.axi_master_write_response_mon = AXI_master_write_response_monitor(dut)

        init_val = AXI_master_write_request_transaction(self)
        self.mon = AXI_master_write_request_monitor(dut, self, callback = self.count_axi_write_req)

        self.expected_dram_req_count = 0
        self.axi_dram_write_req_count = 0

        self.expected_dram_address = []
        self.axi_dram_write_req_addr = []

        self.expected_wstrb = []
        self.axi_dram_write_strobe = []

        self.expected_awlen = 0
        self.axi_dram_write_req_awlen = 0

        sram_init_val = SRAM_read_transaction(self)
        self.sram_mon = SRAM_read_monitor(dut,self, callback = self.count_sram_read_req)

        self.expected_sram_buffer = 0
        self.sram_req_buffer = 0

        self.expected_sram_index = []
        self.sram_req_index = []

        self.expected_sram_bank = []
        self.sram_req_bank = []

        self.expected_sram_valid = []
        self.sram_req_valid = []

        self.scoreboard = DUTScoreboard(dut)


    def store_module_model(self, transaction):
        (
            EN_subifc_put_storeparams_put,
            subifc_put_storeparams_put,
        ) = transaction

        print(hex(subifc_put_storeparams_put))
        subifc_put_storeparams_put = int(
            (bin(subifc_put_storeparams_put)[2:])[::-1], 2)
        print(hex(subifc_put_storeparams_put))
        model_bitwidth = int((bin(subifc_put_storeparams_put)[22:23])[::-1], 2)
        model_is_reset = int((bin(subifc_put_storeparams_put)[23:24])[::-1], 2)
        model_y_stride = int((bin(subifc_put_storeparams_put)[24:32])[::-1], 2)
        model_z_stride = int((bin(subifc_put_storeparams_put)[32:40])[::-1], 2)
        model_z_size = int((bin(subifc_put_storeparams_put)[40:48])[::-1], 2)
        model_y_size = int((bin(subifc_put_storeparams_put)[48:56])[::-1], 2)
        model_x_size = int((bin(subifc_put_storeparams_put)[56:64])[::-1], 2)
        model_sram_addr = int((bin(subifc_put_storeparams_put)[64:90])[::-1], 2)
        model_dram_addr = int((bin(subifc_put_storeparams_put)[90:])[::-1], 2)

        print("MODEL")
        print(model_dram_addr, model_sram_addr, model_x_size, model_y_size,
              model_z_size, model_y_stride, model_z_stride, model_is_reset, model_bitwidth)
        if(model_bitwidth == 1):
            model_bitwidth = int(self.in_width/8)
        else:
            model_bitwidth = int(self.out_width/8)

        data_bytes_1 = int(self.out_width/8)

        print("bitwidth : ",model_bitwidth,self.out_width)

        expected_address,expected_count,expected_write_strobe,expected_burst_len,expected_sram_buffer,expected_sram_indices,expected_sram_bank, expected_sram_valid,error = store_module_model(model_dram_addr, model_sram_addr, model_x_size, model_y_size, model_z_size, model_z_stride, model_y_stride, model_bitwidth,data_bytes_1)
        print("FROM MODEL expected requests : ",expected_count)
        print("From MODEL expected addresses : ",expected_address)
        print("FROM MODEL expected awlen : ",expected_burst_len)
        self.expected_dram_address = expected_address
        self.expected_dram_req_count = expected_count
        self.expected_awlen = expected_burst_len
        self.expected_wstrb = expected_write_strobe
        self.expected_sram_buffer = expected_sram_buffer
        self.expected_sram_index = expected_sram_indices
        self.expected_sram_bank = expected_sram_bank
        self.expected_sram_valid = expected_sram_valid

    def count_axi_write_req(self, transaction):
        (
            master_BREADY,
            master_AWVALID,
            master_AWADDR,
            master_AWPROT,
            master_AWLEN,
            master_AWSIZE,
            master_AWBURST,
            master_AWID,
            master_WVALID,
            master_WDATA,
            master_WSTRB,
            master_WLAST,
            master_WID,
            master_AWREADY,
        )=transaction

        self.axi_dram_write_req_count = self.axi_dram_write_req_count + 1
        self.axi_dram_write_req_addr.append(master_AWADDR)
        self.axi_dram_write_strobe.append(master_WSTRB)
        self.axi_dram_write_req_awlen = master_AWLEN
        print("From count_axi_write_req count and addr")
        print(self.axi_dram_write_req_count)
        print(hex(master_AWADDR))
        print(master_AWLEN)

    def count_sram_read_req(self,transaction):
        (
            RDY_send_sram_req,
            send_sram_req,
        )=transaction

        print("From count sram read req : ",hex(send_sram_req))
        send_sram_req = send_sram_req | 1 << 17
        print("",hex(send_sram_req))
        sram_buffer = int((bin(send_sram_req)[3:5]),2)
        sram_index = int((bin(send_sram_req)[5:11]),2)
        sram_bank = int((bin(send_sram_req)[11:15]),2)
        sram_valid = int((bin(send_sram_req)[15:]),2)
        self.sram_req_valid.append(sram_valid)
        self.sram_req_bank.append(sram_bank)
        self.sram_req_index.append(sram_index)
        self.sram_req_buffer = sram_buffer
        print("SRAM request from DUT : ",hex(send_sram_req),hex(sram_buffer),hex(sram_index),hex(sram_bank),hex(sram_valid))

    def send_output_to_scoreboard(self):
        print("output comparison")
        self.scoreboard.compare(self.expected_dram_req_count,self.expected_dram_address,self.expected_wstrb,self.expected_awlen,
                                self.axi_dram_write_req_count,self.axi_dram_write_req_addr,self.axi_dram_write_strobe,self.axi_dram_write_req_awlen,
                                self.expected_sram_buffer,self.expected_sram_index,self.expected_sram_bank,self.expected_sram_valid,
                                self.sram_req_buffer,self.sram_req_index,self.sram_req_bank,self.sram_req_valid,
                                self.scoreboard.log)
        self.expected_dram_address.clear
        self.axi_dram_write_req_addr = [] ## Not able to clear the contents by .clear ??
        self.expected_dram_req_count = 0
        self.axi_dram_write_req_count = 0
        self.expected_wstrb.clear
        self.axi_dram_write_strobe = []
        self.expected_awlen = 0
        self.axi_dram_write_req_awlen = 0
        self.expected_sram_buffer = 0
        self.sram_req_buffer = 0
        self.expected_sram_index.clear
        self.sram_req_index = []
        self.expected_sram_bank.clear
        self.sram_req_bank = []
        self.expected_sram_valid.clear
        self.sram_req_valid = []

    def stop(self):
        self.stopped = True


def axi_write_response_from_tb(tb, awready, wready, bvalid, bresp, bid):
    master_AWREADY = awready
    master_WREADY = wready
    master_BVALID = bvalid
    master_BRESP = bresp
    master_BID = bid
    yield AXI_master_write_response_transaction(tb,
                                               master_AWREADY,
                                               master_WREADY,
                                               master_BVALID,
                                               master_BRESP,
                                               master_BID)


@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal <= 0
        yield Timer(1)
        signal <= 1
        yield Timer(1)

@cocotb.coroutine
def drive_sram_req(dut):
    while True:
        if(dut.RDY_send_sram_req != 1):
            yield RisingEdge(dut.RDY_send_sram_req)
        dut.EN_send_sram_req = 1
        yield RisingEdge(dut.CLK)
        dut.EN_send_sram_req = 0
        yield RisingEdge(dut.CLK)
        yield RisingEdge(dut.CLK)
        yield RisingEdge(dut.CLK)
        if(dut.RDY_recv_sram_resp != 1):
            yield RisingEdge(dut.RDY_recv_sram_resp)
        dut.EN_recv_sram_resp = 1
        yield RisingEdge(dut.CLK)
        dut.EN_recv_sram_resp = 0
        yield RisingEdge(dut.CLK)


@cocotb.test()
def run_test(dut):
    log = cocotb.logging.getLogger("cocotb.test") #logger instance
    cocotb.fork(clock_gen(dut.CLK))
    cocotb.fork(drive_sram_req(dut))
    tb = TestBench(dut)
    dut.RST_N <= 0
    yield Timer(2)
    dut.RST_N <= 1

    data_width = 128
    out_width = 32
    in_width = 8

    tb.out_width = out_width

    @Store_parameters_Coverage
    @cocotb.coroutine
    def send_store_instruction(inp_dram_address,inp_sram_address,inp_x_size,inp_y_size,inp_z_size,inp_z_stride,inp_y_stride,
                                    inp_is_reset,inp_bitwidth,inp_padding):
        subifc_put_storeparams_put = (inp_padding | inp_bitwidth << 20 | inp_is_reset << 21 |
                                        inp_y_stride << 22 | inp_z_stride << 30 | inp_z_size << 38 |
                                        inp_y_size << 46 | inp_x_size << 54 | inp_sram_address << 62 |
                                        inp_dram_address << 88)
        EN_subifc_put_storeparams_put = 1
        yield tb.store_instruction_drv.send(Store_instruction_transaction(tb,EN_subifc_put_storeparams_put,
            subifc_put_storeparams_put))
        EN_subifc_put_storeparams_put = 0
        yield tb.store_instruction_drv.send(Store_instruction_transaction(tb,EN_subifc_put_storeparams_put,
            subifc_put_storeparams_put))

    for n in range(2):
        size_array_1 = [1,2,4,8,16,32,64,128]
        size_array_2 = [1,2,4,8,16]
        inp_dram_address = 0x80000000   # 32
        inp_sram_address = 0x3000000    # 26
        inp_x_size = random.choice(size_array_1)               # 8
        inp_y_size = random.choice(size_array_1)               # 8
        inp_z_size = random.choice(size_array_2)               # 8
        inp_z_stride = random.choice(size_array_1)             # 8
        inp_y_stride = random.choice(size_array_1)             # 8
        inp_is_reset = 0x1                                   # 1
        #inp_x_size = 32            # 8
        #inp_y_size = 8           # 8
        #inp_z_size = 16            # 8
        #inp_z_stride = 64            # 8
        #inp_y_stride =  8           # 8
        inp_bitwidth = random.choice([0,1])
        inp_padding = 0x80001           # 20

        print("Input to DUT")
        print("dram address: ",inp_dram_address)
        print("sram address: ",inp_sram_address)
        print("x size: ",inp_x_size)
        print("y size: ",inp_y_size)
        print("z size: ",inp_z_size)
        print("y stride: ",inp_y_stride)
        print("z stride: ",inp_z_stride)
        print("is reset: ",inp_is_reset)
        print("bitwidth: ",inp_bitwidth)
        print("padding: ",inp_padding)

        yield send_store_instruction(inp_dram_address,inp_sram_address,inp_x_size,inp_y_size,inp_z_size,inp_z_stride,inp_y_stride,
                                    inp_is_reset,inp_bitwidth,inp_padding)

        if(inp_bitwidth == 1):
            inp_bitwidth = in_width/8
        else:
            inp_bitwidth = out_width/8

        num_axi_data_req = int(inp_z_size * inp_bitwidth / (data_width/8))
        print("Write burst length : ", num_axi_data_req)
        num_req = 0
        for delay in range(10):
            yield RisingEdge(dut.CLK)
        while(dut.master_AWVALID == 1 or dut.master_WVALID == 1):
            if((num_req == 0 and dut.master_AWVALID == 1 and dut.master_WVALID == 1) or num_req != 0):
                if(dut.master_AWVALID == 1):
                    awready = 1
                else:
                    awready = 0
                if(dut.master_WVALID == 1):
                    wready = 1
                else:
                    wready = 0
                axi_response = axi_write_response_from_tb(tb, awready, wready, 0, 0, 3)
                print("Sending AXI AWREADY and WREADY 1 ")
                for a in axi_response:
                    yield tb.axi_master_write_response_drv.send(a)
                print("Sent AXI AWREADY and WREADY")
                axi_response = axi_write_response_from_tb(tb, 0, 0, 0, 0, 3)
                print("Sending AXI AWREADY and WREADY 0 ")
                for a in axi_response:
                    yield tb.axi_master_write_response_drv.send(a)
                print("Sent AXI AWREADY and WREADY")

                if(dut.master_BREADY != 1):
                    yield RisingEdge(dut.master_BREADY)
                axi_response = axi_write_response_from_tb(tb, 0, 0, 1, 0, 3)
                print("Sending AXI response ")
                for a in axi_response:
                    yield tb.axi_master_write_response_drv.send(a)
                print("Sent AXI response ")
                axi_response = axi_write_response_from_tb(tb, 0, 0, 0, 0, 3)
                print("End of AXI Request - Sending AXI BVALID low ")
                for a in axi_response:
                    yield tb.axi_master_write_response_drv.send(a)
                print("Sent AXI BVALID 0 ")
                for delay in range(2):
                    yield RisingEdge(dut.CLK)
                if(num_req < num_axi_data_req - 1):
                    num_req = num_req + 1
                else:
                    num_req = 0
            else:
                yield RisingEdge(dut.CLK)

        print("Store operation done waiting for store finish signal")

        if(dut.RDY_subifc_send_store_finish_get != 1):
            yield RisingEdge(dut.RDY_subifc_send_store_finish_get)

        dut.EN_subifc_send_store_finish_get <= 1
        yield RisingEdge(dut.CLK)
        dut.EN_subifc_send_store_finish_get <= 0
        for s in range(10):
            yield RisingEdge(dut.CLK)

        tb.send_output_to_scoreboard()

    tb.stop()
    for s in range(10):
        yield RisingEdge(dut.CLK)

    coverage_db.export_to_xml(filename="coverage_store_params.xml")
    coverage_db.export_to_yaml(filename="coverage_store_params.yml")
