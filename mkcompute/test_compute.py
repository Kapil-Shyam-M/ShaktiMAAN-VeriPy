import random
import sys
import cocotb
import logging as log
import numpy as np
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep, FallingEdge
from cocotb_bus.monitors import BusMonitor
from cocotb_bus.drivers import BusDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb_bus.scoreboard import Scoreboard
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb_coverage.coverage import *

# Parameters : nRows = 4, nCols = 4, In_width = 16, Out_width = 32

num_cols = 2
num_rows = 2

Preload_value_Coverage    = coverage_section (CoverPoint("top.preload_value", vname="inp_preload_value", bins = [0b0,0b1]))
Active_rows_value_Coverage    = coverage_section (CoverPoint("top.active_rows_value", vname="inp_act_row_value", bins = [1,2]))
Active_columns_value_Coverage    = coverage_section (CoverPoint("top.active_columns_value", vname="inp_act_col_value", bins = [1,2]))

@Preload_value_Coverage
def get_preload_value(inp_preload_value):
 return inp_preload_value

@Active_rows_value_Coverage
def get_act_row_value(inp_act_row_value):
 return inp_act_row_value

@Active_columns_value_Coverage
def get_act_col_value(inp_act_col_value):
 return inp_act_col_value

##Parameter Declarations
class Parameter_Driver(BusDriver):
    _signals = [
        'subifc_put_compute_params_put',
        'EN_subifc_put_compute_params_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def send_params(self,dut,transaction):
        yield super()._wait_for_signal(dut.RDY_subifc_put_compute_params_put)
        yield super().send(transaction,False)
        yield RisingEdge(self.clock)
        self.bus.EN_subifc_put_compute_params_put.value <= 0; 


class Parameter_Transaction(object):

    def __init__(self, tb,
                subifc_put_compute_params_put=0,
                EN_subifc_put_compute_params_put=0
                 ):

        self.subifc_put_compute_params_put = BinaryValue(subifc_put_compute_params_put, tb.param_bits, False)
        self.EN_subifc_put_compute_params_put = BinaryValue(EN_subifc_put_compute_params_put, tb.EN_bits, False)


class Parameter_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        'subifc_put_compute_params_put',
        'EN_subifc_put_compute_params_put',
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
             
            yield RisingEdge(self.clock)
            if self.bus.EN_subifc_put_compute_params_put.value == 1:
                print('[IN_MON] {0:<25} : {1}'.format('subifc_put_compute_params_put', hex(self.bus.subifc_put_compute_params_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format('EN_subifc_put_compute_params_put', hex(self.bus.EN_subifc_put_compute_params_put.value.integer)))


class get_wt_sram_req_Driver(BusDriver):
    _signals = ['EN_get_wt_addr']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def accept_sram_req(self,dut):

        while True:
           yield super()._wait_for_signal(dut.RDY_get_wt_addr)

           self.bus.EN_get_wt_addr.value <= 1

           yield RisingEdge(self.clock)

           self.bus.EN_get_wt_addr.value <= 0

wt_addr_queue_actual = []

class get_wt_sram_req_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        'EN_get_wt_addr',
	'get_wt_addr'
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
             
            yield RisingEdge(self.clock)
            if self.bus.EN_get_wt_addr.value == 1:
                print('[IN_MON] {0:<25} : {1}'.format('get_wt_addr', hex(self.bus.get_wt_addr.value.integer)))
                wt_addr_queue_actual.append(self.bus.get_wt_addr.value.integer)

##Output Data fed in response to SRAM request
class put_wt_sram_data_Driver(BusDriver):
    _signals = [
        'EN_put_wt_resp',
	'put_wt_resp_weights'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_wt_sram_data(self,dut):
        while True:
           if dut.EN_get_wt_addr.value == 1:
              yield super()._wait_for_signal(dut.RDY_put_wt_resp)
   
              self.bus.EN_put_wt_resp.value <= 1
   
              self.bus.put_wt_resp_weights.value <= 257
   
           yield RisingEdge(self.clock)
   	
           self.bus.EN_put_wt_resp.value <= 0


class put_wt_sram_data_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = [
        'EN_put_wt_resp',
	'put_wt_resp_weights'
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
             
            yield RisingEdge(self.clock)
            if self.bus.EN_put_wt_resp.value == 1:
                print('[IN_MON] {0:<25} : {1}'.format('put_wt_resp_weights', hex(self.bus.put_wt_resp_weights.value.integer)))

class get_ip_sram_req_Driver(BusDriver):
    _signals = ['EN_get_inp_addr_0_get','EN_get_inp_addr_1_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def accept_sram_req(self,dut):

        while True:
           
           yield super()._wait_for_signal(dut.RDY_get_inp_addr_0_get)
           
           self.bus.EN_get_inp_addr_0_get.value <= 1
           self.bus.EN_get_inp_addr_1_get.value <= 1

           yield RisingEdge(self.clock)

           self.bus.EN_get_inp_addr_0_get.value <= 0
           self.bus.EN_get_inp_addr_1_get.value <= 0

ip_addr_value_queue_actual = [[],[]]

class get_ip0_sram_req_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = ['EN_get_inp_addr_0_get','get_inp_addr_0_get']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:

           yield RisingEdge(self.clock)

           if self.bus.EN_get_inp_addr_0_get.value == 1:
              print('[IN_MON] {0:<25} : {1}'.format('get_ip_addr', hex(self.bus.get_inp_addr_0_get.value.integer)))
              ip_addr_value_queue_actual[0].append(self.bus.get_inp_addr_0_get.value.integer)


class put_ip0_sram_data_Driver(BusDriver):
    _signals = ['EN_put_inp_resp_0_put','put_inp_resp_0_put','get_inp_addr_0_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_ip_resp_sram_data(self,dut):

        while True:
           if (dut.EN_get_inp_addr_0_get.value == 1) and ((self.bus.get_inp_addr_0_get.value.integer >> 1) % 2 == 1):
              yield super()._wait_for_signal(dut.RDY_put_inp_resp_0_put)

              self.bus.EN_put_inp_resp_0_put.value <= 1
                  
              self.bus.put_inp_resp_0_put.value <= 1
              
           yield RisingEdge(self.clock)
           	   
           self.bus.EN_put_inp_resp_0_put.value <= 0

class put_ip0_sram_data_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = ['EN_put_inp_resp_0_put','put_inp_resp_0_put']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:
             
            yield RisingEdge(self.clock)

            if self.bus.EN_put_inp_resp_0_put.value == 1:
              print('[IN_MON] {0:<25} : {1}'.format('put_ip_resp', hex(self.bus.put_inp_resp_0_put.value.integer)))


class get_ip1_sram_req_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = ['EN_get_inp_addr_1_get','get_inp_addr_1_get']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:

           yield RisingEdge(self.clock)

           if self.bus.EN_get_inp_addr_1_get.value == 1:
              print('[IN_MON] {0:<25} : {1}'.format('get_ip_addr', hex(self.bus.get_inp_addr_1_get.value.integer)))
              ip_addr_value_queue_actual[1].append(self.bus.get_inp_addr_1_get.value.integer)


class put_ip1_sram_data_Driver(BusDriver):
    _signals = ['EN_put_inp_resp_1_put','put_inp_resp_1_put','get_inp_addr_1_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_ip_resp_sram_data(self,dut):

        while True:
           if (dut.EN_get_inp_addr_1_get.value == 1) and ((self.bus.get_inp_addr_1_get.value.integer >> 1) % 2 == 1):
              yield super()._wait_for_signal(dut.RDY_put_inp_resp_1_put)

              self.bus.EN_put_inp_resp_1_put.value <= 1
                  
              self.bus.put_inp_resp_1_put.value <= 1
              
           yield RisingEdge(self.clock)
           	   
           self.bus.EN_put_inp_resp_1_put.value <= 0

class put_ip1_sram_data_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = ['EN_put_inp_resp_1_put','put_inp_resp_1_put']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:
             
            yield RisingEdge(self.clock)

            if self.bus.EN_put_inp_resp_1_put.value == 1:
              print('[IN_MON] {0:<25} : {1}'.format('put_ip_resp', hex(self.bus.put_inp_resp_1_put.value.integer)))

old_op_addr_value_queue_actual = [[],[]]

class get_old_op_sram_req_Driver(BusDriver):
    _signals = ['EN_get_old_out_addr_0_get','EN_get_old_out_addr_1_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def accept_sram_req(self,dut):

        while True:

           #yield super()._wait_for_signal(dut.RDY_get_old_out_addr_0_get)
           yield FallingEdge(self.clock)

           if dut.RDY_get_old_out_addr_0_get.value == 1:
            self.bus.EN_get_old_out_addr_0_get.value <= 1
           if dut.RDY_get_old_out_addr_1_get.value == 1:
            self.bus.EN_get_old_out_addr_1_get.value <= 1

           yield RisingEdge(self.clock)

           if dut.RDY_get_old_out_addr_0_get.value == 1:
            self.bus.EN_get_old_out_addr_0_get.value <= 0
           if dut.RDY_get_old_out_addr_1_get.value == 1:
            self.bus.EN_get_old_out_addr_1_get.value <= 0


class get_old_op0_sram_req_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = ['EN_get_old_out_addr_0_get','get_old_out_addr_0_get']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:

            yield RisingEdge(self.clock)

            if self.bus.EN_get_old_out_addr_0_get == 1:
               print('[IN_MON] {0:<25} : {1}'.format('get_old_op_addr', hex(self.bus.get_old_out_addr_0_get.value.integer)))
               old_op_addr_value_queue_actual[0].append(self.bus.get_old_out_addr_0_get.value.integer)


class put_old_op0_sram_data_Driver(BusDriver):
    _signals = ['EN_put_old_out_resp_0_put','put_old_out_resp_0_put','get_old_out_addr_0_get','EN_get_old_out_addr_0_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_old_op_resp_sram_data(self,dut):

        while True:
           if (self.bus.EN_get_old_out_addr_0_get == 1) and ((self.bus.get_old_out_addr_0_get.value.integer >> 1) % 2 == 1):
              yield super()._wait_for_signal(dut.RDY_put_old_out_resp_0_put)
   
              self.bus.EN_put_old_out_resp_0_put.value <= 1
   
              self.bus.put_old_out_resp_0_put.value <= 1
   
           yield RisingEdge(self.clock)
   	
           self.bus.EN_put_old_out_resp_0_put.value <= 0

class put_old_op0_sram_data_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = ['EN_put_old_out_resp_0_put','put_old_out_resp_0_put']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:
             
            yield RisingEdge(self.clock)

            if self.bus.EN_put_old_out_resp_0_put.value == 1:
              print('[IN_MON] {0:<25} : {1}'.format('put_old_op_resp', hex(self.bus.put_old_out_resp_0_put.value.integer)))


class get_old_op1_sram_req_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = ['EN_get_old_out_addr_1_get','get_old_out_addr_1_get']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:

            yield RisingEdge(self.clock)

            if self.bus.EN_get_old_out_addr_1_get.value == 1:
               print('[IN_MON] {0:<25} : {1}'.format('get_old_op_addr', hex(self.bus.get_old_out_addr_1_get.value.integer)))
               old_op_addr_value_queue_actual[1].append(self.bus.get_old_out_addr_1_get.value.integer)


class put_old_op1_sram_data_Driver(BusDriver):
    _signals = ['EN_put_old_out_resp_1_put','put_old_out_resp_1_put','get_old_out_addr_1_get','EN_get_old_out_addr_1_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_old_op_resp_sram_data(self,dut):

        while True:
           if (self.bus.EN_get_old_out_addr_1_get.value == 1) and ((self.bus.get_old_out_addr_1_get.value.integer >> 1) % 2 == 1):
              yield super()._wait_for_signal(dut.RDY_put_old_out_resp_1_put)
   
              self.bus.EN_put_old_out_resp_1_put.value <= 1
   
              self.bus.put_old_out_resp_1_put.value <= 1
   
           yield RisingEdge(self.clock)
   	
           self.bus.EN_put_old_out_resp_1_put.value <= 0

class put_old_op1_sram_data_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = ['EN_put_old_out_resp_1_put','put_old_out_resp_1_put']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:
             
            yield RisingEdge(self.clock)

            if self.bus.EN_put_old_out_resp_1_put.value == 1:
              print('[IN_MON] {0:<25} : {1}'.format('put_old_op_resp', hex(self.bus.put_old_out_resp_1_put.value.integer)))

##Output SRAM Request for write
class get_new_op_sram_req_Driver(BusDriver):
    _signals = ['EN_get_new_output_data_0_get','EN_get_new_output_data_1_get']

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def accept_result_sram_req(self,dut):

        while True:

           #yield super()._wait_for_signal(dut.RDY_get_new_output_data_0_get or dut.RDY_get_new_output_data_1_get)
           yield FallingEdge(self.clock)

           if dut.RDY_get_new_output_data_0_get.value == 1:
            self.bus.EN_get_new_output_data_0_get.value <= 1
           if dut.RDY_get_new_output_data_1_get.value == 1:
            self.bus.EN_get_new_output_data_1_get.value <= 1	   

           yield RisingEdge(self.clock)

           if dut.RDY_get_new_output_data_0_get.value == 1:
            self.bus.EN_get_new_output_data_0_get.value <= 0
           if dut.RDY_get_new_output_data_1_get.value == 1:
            self.bus.EN_get_new_output_data_1_get.value <= 0

           #Commenting this assuming there is no contention on SRAM
           #rand_count = random.randrange(0,2) 
           #count = 0
           #while count < rand_count:
           #   yield RisingEdge(self.clock)
           #   count = count+1

new_op_addr_value_queue_actual = [[],[]]

class get_new_op0_sram_req_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = ['EN_get_new_output_data_0_get','get_new_output_data_0_get']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:
             
            yield RisingEdge(self.clock)

            if self.bus.EN_get_new_output_data_0_get == 1:
               print('[OUT_MON] {0:<25} : {1}'.format('get_new_op_data', hex(self.bus.get_new_output_data_0_get.value.integer)))
               new_op_addr_value_queue_actual[0].append(self.bus.get_new_output_data_0_get.value.integer)

class get_new_op1_sram_req_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = ['EN_get_new_output_data_1_get','get_new_output_data_1_get']

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):

        while True:
             
            yield RisingEdge(self.clock)

            if self.bus.EN_get_new_output_data_1_get.value == 1:
               print('[OUT_MON] {0:<25} : {1}'.format('get_new_op_data', hex(self.bus.get_new_output_data_1_get.value.integer)))
               new_op_addr_value_queue_actual[1].append(self.bus.get_new_output_data_1_get.value.integer)

class TestBench(object):
    """Verification Test Bench"""

    def __init__(self, dut):
        self.dut = dut
        self.stopped = False

        self.EN_bits = 1
        self.RDY_bits = 1
        self.write_op_data_bits = 81
        self.vec_data_bits = 64
        self.param_bits = 120

        self.parameter_driver = Parameter_Driver(dut)
        self.parameter_monitor = Parameter_Monitor(dut)
	##Weight Read SRAM IF
        self.get_wt_sram_req_driver = get_wt_sram_req_Driver(dut)
        self.get_wt_sram_req_monitor = get_wt_sram_req_Monitor(dut)
        self.put_wt_sram_data_driver = put_wt_sram_data_Driver(dut)
        self.put_wt_sram_data_monitor = put_wt_sram_data_Monitor(dut)
	##New output write SRAM interface
        self.get_new_op_sram_req_driver = get_new_op_sram_req_Driver(dut)
        self.get_new_op0_sram_req_monitor = get_new_op0_sram_req_Monitor(dut)
        self.get_new_op1_sram_req_monitor = get_new_op1_sram_req_Monitor(dut)
	#Input read SRAM interface
        self.get_ip_sram_req_driver = get_ip_sram_req_Driver(dut)
        self.get_ip0_sram_req_monitor = get_ip0_sram_req_Monitor(dut)
        self.put_ip0_sram_data_driver = put_ip0_sram_data_Driver(dut)
        self.put_ip0_sram_data_monitor = put_ip0_sram_data_Monitor(dut)
        self.get_ip1_sram_req_monitor = get_ip1_sram_req_Monitor(dut)
        self.put_ip1_sram_data_driver = put_ip1_sram_data_Driver(dut)
        self.put_ip1_sram_data_monitor = put_ip1_sram_data_Monitor(dut)
	#Old output read SRAM interface
        self.get_old_op_sram_req_driver = get_old_op_sram_req_Driver(dut)
        self.get_old_op0_sram_req_monitor = get_old_op0_sram_req_Monitor(dut)
        self.put_old_op0_sram_data_driver = put_old_op0_sram_data_Driver(dut)
        self.put_old_op0_sram_data_monitor = put_old_op0_sram_data_Monitor(dut)
        self.get_old_op1_sram_req_monitor = get_old_op1_sram_req_Monitor(dut)
        self.put_old_op1_sram_data_driver = put_old_op1_sram_data_Driver(dut)
        self.put_old_op1_sram_data_monitor = put_old_op1_sram_data_Monitor(dut)

        #init_val = Accum_out_Transaction(self)
        #self.accum_out_monitor = Accum_out_Monitor(dut, self)
        #self.accum_out_monitor = Accum_out_Monitor(dut, self, callback=self.accum_dut_output)

        #self.expected_output = []
        #self.dut_output = []
        #self.curr_row = 0
        #self.curr_col = 0
        #self.final_output = []

        #self.scoreboard = DUTScoreboard(dut)
        #self.scoreboard.add_interface(self.final_output, self.expected_output)

    #def model(self,input_matrix,filter_matrix):
      #mult_output = systolic_array_model(input_matrix,filter_matrix)
      #self.expected_output.append(mult_output)

    #def accum_dut_output(self,transaction):

    #  self.dut_output.append(transaction)

    #def update_output(self):
    #  self.final_output.append(self.dut_output)

        
    def stop(self):
        """
        Stop generation of expected output transactions.
        One more clock cycle must be executed afterwards, so that, output of
        D-FF can be checked.
        """
        self.stopped = True


@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1)
        signal.value <= 1
        yield Timer(1)


@cocotb.test()
def run_test(dut):
    cocotb.fork(clock_gen(dut.CLK))
    tb = TestBench(dut)
    dut.RST_N.value <= 0
    yield Timer(2)
    dut.RST_N.value <= 1
    yield RisingEdge(dut.CLK)

    input_address = random.randint(0,50) 
    output_address = int(random.randint(100,150)) + int(random.randint(0,1)<<14)
    weight_address = random.randint(200,250)

    output_height = random.randint(1,10)
    output_width =  random.randint(1,10)
    act_rows = random.randint(1,num_rows)
    act_cols = random.randint(1,num_cols)
    mem_stride_h = random.randint(1,10) #number of channels * input width
    mem_stride_w = random.randint(1,10) #number of channels
    
    p_left = random.randint(1,3) if output_width>8 else 0
    p_right = random.randint(1,3) if output_width>8 else 0
    p_bottom = random.randint(1,3) if output_height>8 else 0
    p_top = random.randint(1,3) if output_height>8 else 0

    preload_val = random.randint(0,1)

    param_val =0
    
    param_val += input_address<<105   ## Input address
    param_val += output_address<<90   ## Output address
    param_val += weight_address<<75    ## weight address
    param_val += output_height<<67    ## ofmap height
    param_val += output_width<<59    ## ofmap_width
    param_val += act_rows<<51    ## active_rows
    param_val += act_cols<<43    ## active_cols
    param_val += mem_stride_h<<39    ## stride_h
    param_val += mem_stride_w<<35    ## stride_w
    param_val += p_left<<31    ## pad left
    param_val += p_right<<27    ## pad right
    param_val += p_top<<23    ## pad top
    param_val += p_bottom<<19    ## pad bottom
    param_val += preload_val<<18    ## Preload value
    param_val += 0x0        ## Padding

    get_preload_value(preload_val)
    get_act_row_value(act_rows)
    get_act_col_value(act_cols)

    i = Parameter_Transaction(tb,param_val,1)
    yield tb.parameter_driver.send_params(dut,i)

    cocotb.fork(tb.get_wt_sram_req_driver.accept_sram_req(dut))

    cocotb.fork(tb.put_wt_sram_data_driver.send_wt_sram_data(dut))

    cocotb.fork(tb.get_new_op_sram_req_driver.accept_result_sram_req(dut))

    if preload_val == 1:
     cocotb.fork(tb.get_old_op_sram_req_driver.accept_sram_req(dut))
     cocotb.fork(tb.put_old_op0_sram_data_driver.send_old_op_resp_sram_data(dut))
     cocotb.fork(tb.put_old_op1_sram_data_driver.send_old_op_resp_sram_data(dut))

    cocotb.fork(tb.get_ip_sram_req_driver.accept_sram_req(dut))
    cocotb.fork(tb.put_ip0_sram_data_driver.send_ip_resp_sram_data(dut))
    cocotb.fork(tb.put_ip1_sram_data_driver.send_ip_resp_sram_data(dut))

    yield RisingEdge(dut.RDY_subifc_get_compute_finish_get)

    coverage_db.export_to_yaml(filename="coverage_compute_params.yml")

    #Modelling the Compute control fabric for getting the expected queues
    wt_addr_queue_expected = []
    for i in range(act_rows):
     wt_addr_queue_expected.append(((weight_address+act_rows-1-i)<<8)+act_cols)

    if len(wt_addr_queue_expected) != len(wt_addr_queue_actual):
     raise weight_mismatch("Weight Sram request mismatch")
    else:
     for i in range(act_rows):
      if wt_addr_queue_expected[i] != wt_addr_queue_actual[i]:
       print("Observed:" + hex(wt_addr_queue_actual[i])+" Expected:"+hex(wt_addr_queue_expected[i]))
       raise weight_mismatch("Weight Sram request mismatch")
    
    new_out_addr_queue_expected = [[],[]]
    for i in range(output_height*output_width):
     for j in range(act_cols):
      new_out_addr_queue_expected[j].append(((output_address+i)<<17) + (output_address>>14)) #Consider only the address and the selected buffer
    
    for i in range(act_cols):
     if len(new_out_addr_queue_expected[i]) != len(new_op_addr_value_queue_actual[i]):
      raise weight_mismatch("Old output Sram request mismatch")
     
     for j in range(output_height*output_width):
      if ((new_out_addr_queue_expected[i][j] & 0x1) != (new_op_addr_value_queue_actual[i][j] & 0x1)) or ((new_out_addr_queue_expected[i][j]>>17) != (new_op_addr_value_queue_actual[i][j]>>17)):
       print("Observed:" + hex(new_op_addr_value_queue_actual[i][j])+" Expected:"+hex(new_out_addr_queue_expected[i][j]))
       raise new_output_mismatch("New output Sram request mismatch")

     if preload_val == 1: 
      for i in range((output_height*output_width) + act_cols - 1):
       for j in range(act_cols):
        if i>=j and (i<((output_height*output_width)+j)):
         if ((old_op_addr_value_queue_actual[j][i]>>1) & 0x1) != 0x1:
          print("Expecting a valid output request for column ",j," and at time instant ",i)
          raise old_output_mismatch("Expecting a valid output request")
         if(old_op_addr_value_queue_actual[j][i]>>2) != (output_address + i - j):
          print("Observed:" + hex(old_op_addr_value_queue_actual[j][i]>>2)+" Expected:"+hex(output_address + i - j))
          raise old_output_mismatch("Expecting a correct output request")
        else:
         if ((old_op_addr_value_queue_actual[j][i]>>1) & 0x1) != 0x0:
          print("Not Expecting a valid output request for column ",j," and at time instant ",i)
          raise old_output_mismatch("Not expecting a valid output request")
     
     for i in range((output_height*output_width) + num_rows - 1):
      for j in range(num_rows):
       if i>=j and (i<((output_height*output_width)+j)):
        if ((ip_addr_value_queue_actual[j][i]>>1) & 0x1) != 0x1:
         print("Expecting a valid input request for column ",j," and at time instant ",i)
         raise input_mismatch("Expecting a valid input request")
        if j>=act_rows:
         if ((ip_addr_value_queue_actual[j][i]) & 0x1) != 0x1:
          print("Expecting a pad zero set request")
          raise input_mismatch("Expecting a valid input request")
        else:
         output_id = i-j
         h_idx = output_id // output_width
         w_idx = output_id - (h_idx*output_width)
         if w_idx < p_left or w_idx > (output_width-p_right-1) or h_idx < p_top or h_idx > (output_height-p_bottom-1):
          if ((ip_addr_value_queue_actual[j][i]) & 0x1) != 0x1:
           print("Expecting a pad zero set request for row ",j," and time instant ",i)
           raise input_mismatch("Expecting a valid input request")
         else:
          exp_address = input_address + (h_idx*mem_stride_h) + (w_idx*mem_stride_w)
          if (ip_addr_value_queue_actual[j][i]>>2) != exp_address:
           print("Wrong input address as observed is ",hex(ip_addr_value_queue_actual[j][i]>>2)," and expected is ",exp_address)
       else:
        if ((ip_addr_value_queue_actual[j][i]>>1) & 0x1) != 0x0:
          print("Not Expecting a valid input request for column ",j," and at time instant ",i)
          raise input_mismatch("Not expecting a valid input request")	 

