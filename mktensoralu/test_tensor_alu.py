import random
import sys
import cocotb
import logging as log
import numpy as np
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb.monitors import BusMonitor
from cocotb.drivers import BusDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb_coverage.coverage import *

# Parameters : nRows = 4, nCols = 4, In_width = 16, Out_width = 32

num_cols = 4
alu_width = 16
of_index = 8
which_buffer = 1

TALU_parameters_Coverage = coverage_section (
  CoverPoint("top.alu_opcode", vname="alu_opcode", bins = [0,1,2,3]),
  CoverPoint("top.num_active", vname="num_active", bins = [1,2,3,4]),
  CoverPoint("top.immediate_val", vname="immediate_val", bins = [0,1]),
  #CoverPoint("top.inp_y_stride", vname="inp_y_stride", bins = [1,2,4,8,16,32,64,128]),
  #CoverPoint("top.inp_z_stride", vname="inp_z_stride", bins = [1,2,4,8,16,32,64,128]),
  #CoverPoint("top.inp_bitwidth", vname="inp_bitwidth", bins = [0,1])
)

##Parameter Declarations
class Parameter_Driver(BusDriver):
    _signals = [
        'subifc_put_alu_params_put',
        'EN_subifc_put_alu_params_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_params(self,dut,transaction):
        yield super()._wait_for_signal(dut.RDY_subifc_put_alu_params_put)
        yield super().send(transaction,False)
        yield RisingEdge(self.clock)
        self.bus.EN_subifc_put_alu_params_put <= 0; 


class Parameter_Transaction(object):

    def __init__(self, tb,
                subifc_put_alu_params_put=0,
                EN_subifc_put_alu_params_put=0
                 ):

        self.subifc_put_alu_params_put = BinaryValue(subifc_put_alu_params_put, tb.param_bits, False)
        self.EN_subifc_put_alu_params_put = BinaryValue(EN_subifc_put_alu_params_put, tb.EN_bits, False)


class Parameter_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        'subifc_put_alu_params_put',
        'EN_subifc_put_alu_params_put',
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
            if self.bus.EN_subifc_put_alu_params_put == 1:
                print('[IN_MON] {0:<25} : {1}'.format('subifc_put_alu_params_put', hex(self.bus.subifc_put_alu_params_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format('EN_subifc_put_alu_params_put', hex(self.bus.EN_subifc_put_alu_params_put.value.integer)))


test_if = ['EN_mv_send_req_op']

##Output SRAM Request Declarations
class get_op_sram_req_Driver(BusDriver):
    _signals = test_if

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def accept_sram_req(self,dut):

        while True:
           yield super()._wait_for_signal(dut.RDY_mv_send_req_op)
           print(self._signals[0])
           loc = self.bus._signals
           for a,b in loc.items():
            b <= 1

           #self.bus.EN_mv_send_req_op <= 1

           yield RisingEdge(self.clock)

           self.bus.EN_mv_send_req_op <= 0

           rand_count = random.randrange(0,2)
           count = 0
           while count < rand_count:
              yield RisingEdge(self.clock)
              count = count+1

input_req_queue = []

class get_op_sram_req_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        'EN_mv_send_req_op',
	'mv_send_req_op'
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
            if self.bus.EN_mv_send_req_op == 1:
                print('[IN_MON] {0:<25} : {1}'.format('mv_send_req_op', hex(self.bus.mv_send_req_op.value.integer)))
                input_req_queue.append(self.bus.mv_send_req_op.value.integer)


##Output Data fed in response to SRAM request
class put_op_sram_data_Driver(BusDriver):
    _signals = [
        'EN_ma_recv_op',
	'ma_recv_op_vec_data'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def send_op_sram_data(self,dut,transaction):
        while True:
           if dut.EN_mv_send_req_op == 1:
              yield super()._wait_for_signal(dut.RDY_ma_recv_op)
   
              self.bus.EN_ma_recv_op <= 1
   
              self.bus.ma_recv_op_vec_data <= random.randrange(0,2**64-1)
   
           yield RisingEdge(self.clock)
   	
           self.bus.EN_ma_recv_op <= 0

input_data_queue = []

class put_op_sram_data_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = [
        'EN_ma_recv_op',
	'ma_recv_op_vec_data'
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
            if self.bus.EN_ma_recv_op == 1:
                print('[IN_MON] {0:<25} : {1}'.format('ma_recv_op_vec_data', hex(self.bus.ma_recv_op_vec_data.value.integer)))
                input_data_queue.append(self.bus.ma_recv_op_vec_data.value.integer)


##Output SRAM Request for write
class put_op_sram_req_Driver(BusDriver):
    _signals = [
        'EN_mav_put_result'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)

    @coroutine
    def accept_result_sram_req(self,dut):

        while True:
           yield RisingEdge(dut.RDY_mav_put_result)

           self.bus.EN_mav_put_result <= 1

           yield RisingEdge(self.clock)

           self.bus.EN_mav_put_result <= 0

           #Commenting this assuming there is no contention on SRAM
           #rand_count = random.randrange(0,2) 
           #count = 0
           #while count < rand_count:
           #   yield RisingEdge(self.clock)
           #   count = count+1

output_data_queue = []

class put_op_sram_req_Monitor(BusMonitor):
    """Passive output monitor of DUT"""
    _signals = [
        'EN_mav_put_result',
	'mav_put_result'
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
            if self.bus.EN_mav_put_result == 1 and self.entity.RDY_mav_put_result == 1:
                print('[OUT_MON] {0:<25} : {1}'.format('mav_put_result', hex(self.bus.mav_put_result.value.integer)))
                output_data_queue.append(self.bus.mav_put_result.value.integer)


class TestBench(object):
    """Verification Test Bench"""

    def __init__(self, dut):
        self.dut = dut
        self.stopped = False

        self.EN_bits = 1
        self.RDY_bits = 1
        self.write_op_data_bits = 81
        self.vec_data_bits = 64
        self.param_bits = 106

        self.parameter_driver = Parameter_Driver(dut)
        self.parameter_monitor = Parameter_Monitor(dut)
        self.get_op_sram_req_driver = get_op_sram_req_Driver(dut)
        self.get_op_sram_req_monitor = get_op_sram_req_Monitor(dut)
        self.put_op_sram_data_driver = put_op_sram_data_Driver(dut)
        self.put_op_sram_data_monitor = put_op_sram_data_Monitor(dut)
        self.put_op_sram_req_driver = put_op_sram_req_Driver(dut)
        self.put_op_sram_req_monitor = put_op_sram_req_Monitor(dut)

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
        signal <= 0
        yield Timer(1)
        signal <= 1
        yield Timer(1)


@cocotb.test()
def run_test(dut):
    cocotb.fork(clock_gen(dut.CLK))
    tb = TestBench(dut)
    dut.RST_N <= 0
    yield Timer(2)
    dut.RST_N <= 1
    yield RisingEdge(dut.CLK)

    input_address = random.randrange(0,20)
    output_address = random.randrange(128,146)

    input_height = int(random.randrange(4,10))  ##Max value of 10 is chosen to fit the values into the 7 bit address space
    input_width = int(random.randrange(4,10))

    window_height = (random.randrange(1,(int(input_height/2))))
    window_width =  (random.randrange(1,(int(input_width/2))))

    mem_stride_S = input_width

    flag = 0
    while flag == 0:
       value = random.randrange(1,input_width-window_width)
       if (input_width-window_width)%value == 0:
        mem_stride_R = int(value)
        flag = 1

    flag = 0
    while flag == 0:
       value = random.randrange(1,input_height-window_height)
       if (input_height-window_height)%value == 0:
        mem_stride_OW_prel = int(value)
        flag = 1

    mem_stride_OW = mem_stride_OW_prel * input_width

    output_height = int(((input_height-window_height)/mem_stride_OW_prel) + 1)
    output_width = int(((input_width-window_width)/mem_stride_R) + 1)

    print(hex(input_address))
    print(hex(output_address))
    print(hex(input_height))
    print(hex(input_width))
    print(hex(window_height))
    print(hex(window_width))
    print(hex(mem_stride_S))
    print(hex(mem_stride_R))
    print(hex(mem_stride_OW_prel))
    print(hex(output_height))
    print(hex(output_width))

    alu_opcode = random.randrange(0,2)
    num_active = 4
    immediate_val = 0

    param_val = alu_opcode<<104    ## Alu opcode
    param_val += input_address<<96   ## Input address
    param_val += output_address<<88   ## Output address
    param_val += output_height<<80    ## Output height
    param_val += output_width<<72    ## Output width
    param_val += window_height<<68    ## Window height
    param_val += window_width<<64    ## Window width
    param_val += mem_stride_OW<<56    ## Stride ow
    param_val += mem_stride_R<<48    ## Stride R
    param_val += mem_stride_S<<40    ## Stride S
    param_val += num_active<<32    ## Num active
    param_val += 0x0<<31    ## Immediate flag
    param_val += immediate_val<<23    ## Immediate value
    param_val += 0x0        ## Padding

    @TALU_parameters_Coverage
    @cocotb.coroutine
    def send_alu_ins(alu_opcode,num_active,immediate_val):
     i = Parameter_Transaction(tb,param_val,1)
     yield tb.parameter_driver.send_params(dut,i)

    yield send_alu_ins(alu_opcode,num_active,immediate_val)

    cocotb.fork(tb.get_op_sram_req_driver.accept_sram_req(dut))

    cocotb.fork(tb.put_op_sram_data_driver.send_op_sram_data(dut,1))

    cocotb.fork(tb.put_op_sram_req_driver.accept_result_sram_req(dut))

    yield RisingEdge(dut.RDY_subifc_get_alu_complete_get)

    yield RisingEdge(dut.CLK)
    yield RisingEdge(dut.CLK)
    yield RisingEdge(dut.CLK)
    tb.stop()
    yield RisingEdge(dut.CLK)

    #Modelling the Tensor ALU for getting the expected queues
    local_input_address0 = local_input_address1 = local_input_address2 = local_input_address3 = input_address
    local_output_address = output_address
    exp_inp_address_queue = []
    exp_out_data_queue = []
    exp_out_addr_queue = []
    input_data_queue_replica = input_data_queue

    if((immediate_val>>7) == 1):                    # Taking 2's compliment
     immediate_val_compl = immediate_val & (127)
     immediate_val_compl = immediate_val_compl ^ (127)
     immediate_val_compl = immediate_val_compl + 1
     immediate_val_compl *= -1
    else:
     immediate_val_compl = immediate_val

    for i in range (output_height):
     for j in range (output_width):

      for k in range (window_height):
       for l in range (window_width):
         exp_inp_address_queue.append(local_input_address0)
         local_input_address0 += 1
         if(len(input_data_queue_replica)>0):
          compute_val = int(input_data_queue_replica.pop(0))
       local_input_address0 = local_input_address1 = local_input_address1 + mem_stride_S
     
      exp_out_addr_queue.append(local_output_address)
      local_output_address += 1

      local_queue_val = 0
      for i in range(num_active): 
       local_compute_val = (compute_val>>(i*alu_width)) & ((2**alu_width) - 1)

       if((local_compute_val>>(alu_width-1))==1):                          #Taking 2's compliment
        local_compute_val_compl = local_compute_val & ((2**(alu_width-1)) - 1)
        local_compute_val_compl = local_compute_val_compl ^ ((2**(alu_width-1)) - 1)
        local_compute_val_compl += 1
        local_compute_val_compl *= -1
       else:
        local_compute_val_compl = local_compute_val

       if(alu_opcode == 0):

        if(local_compute_val_compl>immediate_val_compl):
         local_queue_val += local_compute_val<<(i*alu_width)
        else:
         local_queue_val += immediate_val<<(i*alu_width)
       
       if(alu_opcode == 1):

        if(local_compute_val_compl<immediate_val_compl):
         local_queue_val += local_compute_val<<(i*alu_width)
        else:
         local_queue_val += immediate_val<<(i*alu_width)

       if(alu_opcode == 2): #TODO: Design Feedback
        sum_local = (local_compute_val + immediate_val) & ((2**alu_width) - 1)
        local_queue_val += (sum_local)<<(i*alu_width)

       if(alu_opcode == 3): #TODO: Update the functionality based on design feedback
        local_queue_val += (local_compute_val<<immediate_val)<<(i*alu_width)

      exp_out_data_queue.append(local_queue_val)

      local_input_address0 = local_input_address1 = local_input_address2 = local_input_address2 + mem_stride_R

     local_input_address0 = local_input_address1 = local_input_address2 = local_input_address3 = local_input_address3 + mem_stride_OW

    #print((exp_inp_address_queue))
    #print((input_req_queue))
    #print((input_data_queue))
    #print((output_data_queue))
    #print((exp_out_addr_queue))
    #print((exp_out_data_queue))

    if len(output_data_queue) != len(exp_out_addr_queue):
     raise out_count_mismatch("Number of output reuests is wrong")

    if len(input_req_queue) != len(exp_inp_address_queue):
     raise input_req_count_mismatch("Number of input requests is wrong")

    for i in range(len(exp_inp_address_queue)):
     input_data_val = 0

     input_data_val += num_active
     input_data_val += exp_inp_address_queue[i]<<8
     input_data_val += which_buffer<<(8+of_index)

     if input_data_val != input_req_queue[i]:
      print("Observed:" + hex(input_data_val) + " Expected:" + hex(input_req_queue[i]))
      raise Input_mismatch("Input Sram request mismatch")

    for i in range(len(output_data_queue)):
     output_data_val = 0

     output_data_val += num_active
     output_data_val += exp_out_data_queue[i]<<8
     output_data_val += exp_out_addr_queue[i]<<((alu_width*num_cols) + 8)
     output_data_val += which_buffer << (8 + of_index + (alu_width*num_cols))

     if output_data_val != output_data_queue[i]:
      print("Observed:" + hex(output_data_val)+" Expected:"+hex(output_data_queue[i]))
      raise Output_mismatch("Output Sram request mismatch")

     coverage_db.export_to_xml(filename="coverage_talu_params.xml")
     coverage_db.export_to_yaml(filename="coverage_talu_params.yml")
