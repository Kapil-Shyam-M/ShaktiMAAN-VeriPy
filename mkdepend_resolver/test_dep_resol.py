import random
import sys
import cocotb
import logging as log
import numpy as np
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.monitors import BusMonitor
from cocotb_bus.drivers import BusDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb_bus.scoreboard import Scoreboard
from cocotb.result import TestFailure
from cocotb.clock import Clock
from collections import namedtuple

flags = namedtuple("flags","push_prev pop_prev push_next pop_next")

class put_load_ins_Driver(BusDriver):
    _signals = [
        'ifc_put_load_params_put',
        'EN_ifc_put_load_params_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def send_params(self,dut,transaction):
        yield super()._wait_for_signal(dut.RDY_ifc_put_load_params_put)
        yield super().send(transaction,False)
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_load_params_put.value <= 0; 


class put_load_ins_Transaction(object):

    def __init__(self, tb,
                ifc_put_load_params_put=0,
                EN_ifc_put_load_params_put=0
                 ):

        self.ifc_put_load_params_put = BinaryValue(ifc_put_load_params_put, tb.param_bits, False)
        self.EN_ifc_put_load_params_put = BinaryValue(EN_ifc_put_load_params_put, tb.EN_bits, False)


class put_load_ins_Monitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        'ifc_put_load_params_put',
        'EN_ifc_put_load_params_put',
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
            if self.bus.EN_ifc_put_load_params_put.value == 1:
                print('[IN_MON] {0:<25} : {1}'.format('ifc_put_load_params_put', hex(self.bus.ifc_put_load_params_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format('EN_ifc_put_load_params_put', hex(self.bus.EN_ifc_put_load_params_put.value.integer)))


class get_load_ins_Driver(BusDriver):
    _signals = [
        'ifc_get_load_instruction_get',
        'EN_ifc_get_load_instruction_get'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def get_params(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_get_load_instruction_get)
        self.bus.EN_ifc_get_load_instruction_get.value <= 1; 
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_get_load_instruction_get.value <= 0; 

class put_load_complete_Driver(BusDriver):
    _signals = [
        'EN_ifc_put_load_complete_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def put_complete(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_put_load_complete_put)
        self.bus.EN_ifc_put_load_complete_put.value <= 1; 
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_load_complete_put.value <= 0; 

class put_compute_ins_Driver(BusDriver):
    _signals = [
        'ifc_put_compute_params_put',
        'EN_ifc_put_compute_params_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def send_params(self,dut,transaction):
        yield super()._wait_for_signal(dut.RDY_ifc_put_compute_params_put)
        yield super().send(transaction,False)
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_compute_params_put.value <= 0; 


class put_compute_ins_Transaction(object):

    def __init__(self, tb,
                ifc_put_compute_params_put=0,
                EN_ifc_put_compute_params_put=0
                 ):

        self.ifc_put_compute_params_put = BinaryValue(ifc_put_compute_params_put, tb.param_bits, False)
        self.EN_ifc_put_compute_params_put = BinaryValue(EN_ifc_put_compute_params_put, tb.EN_bits, False)

class get_compute_ins_Driver(BusDriver):
    _signals = [
        'ifc_get_gemm_instruction_get',
        'EN_ifc_get_gemm_instruction_get'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def get_params(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_get_gemm_instruction_get)
        self.bus.EN_ifc_get_gemm_instruction_get.value <= 1;
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_get_gemm_instruction_get.value <= 0; 

class put_compute_complete_Driver(BusDriver):
    _signals = [
        'EN_ifc_put_gemm_complete_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def put_complete(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_put_gemm_complete_put)
        self.bus.EN_ifc_put_gemm_complete_put.value <= 1; 
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_gemm_complete_put.value <= 0; 

class put_alu_ins_Driver(BusDriver):
    _signals = [
        'ifc_put_alu_params_put',
        'EN_ifc_put_alu_params_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def send_params(self,dut,transaction):
        yield super()._wait_for_signal(dut.RDY_ifc_put_alu_params_put)
        yield super().send(transaction,False)
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_alu_params_put.value <= 0; 


class put_alu_ins_Transaction(object):

    def __init__(self, tb,
                ifc_put_alu_params_put=0,
                EN_ifc_put_alu_params_put=0
                 ):

        self.ifc_put_alu_params_put = BinaryValue(ifc_put_alu_params_put, tb.param_bits, False)
        self.EN_ifc_put_alu_params_put = BinaryValue(EN_ifc_put_alu_params_put, tb.EN_bits, False)

class get_alu_ins_Driver(BusDriver):
    _signals = [
        'ifc_get_alu_instruction_get',
        'EN_ifc_get_alu_instruction_get'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def get_params(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_get_alu_instruction_get)
        self.bus.EN_ifc_get_alu_instruction_get.value <= 1;
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_get_alu_instruction_get.value <= 0; 

class put_alu_complete_Driver(BusDriver):
    _signals = [
        'EN_ifc_put_alu_complete_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def put_complete(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_put_alu_complete_put)
        self.bus.EN_ifc_put_alu_complete_put.value <= 1; 
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_alu_complete_put.value <= 0; 

class put_store_ins_Driver(BusDriver):
    _signals = [
        'ifc_put_store_params_put',
        'EN_ifc_put_store_params_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def send_params(self,dut,transaction):
        yield super()._wait_for_signal(dut.RDY_ifc_put_store_params_put)
        yield super().send(transaction,False)
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_store_params_put.value <= 0; 


class put_store_ins_Transaction(object):

    def __init__(self, tb,
                ifc_put_store_params_put=0,
                EN_ifc_put_store_params_put=0
                 ):

        self.ifc_put_store_params_put = BinaryValue(ifc_put_store_params_put, tb.param_bits, False)
        self.EN_ifc_put_store_params_put = BinaryValue(EN_ifc_put_store_params_put, tb.EN_bits, False)

class get_store_ins_Driver(BusDriver):
    _signals = [
        'ifc_get_store_instruction_get',
        'EN_ifc_get_store_instruction_get'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def get_params(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_get_store_instruction_get)
        self.bus.EN_ifc_get_store_instruction_get.value <= 1;
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_get_store_instruction_get.value <= 0; 

class put_store_complete_Driver(BusDriver):
    _signals = [
        'EN_ifc_put_store_complete_put'
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


    @coroutine
    def put_complete(self,dut):
        yield super()._wait_for_signal(dut.RDY_ifc_put_store_complete_put)
        self.bus.EN_ifc_put_store_complete_put.value <= 1; 
        yield RisingEdge(self.clock)
        self.bus.EN_ifc_put_store_complete_put.value <= 0; 

class TestBench(object):
    """Verification Test Bench"""

    def __init__(self, dut):
        self.dut = dut
        self.stopped = False

        self.EN_bits = 1
        self.RDY_bits = 1
        self.param_bits = 124

        self.put_load_ins_driver = put_load_ins_Driver(dut)
        self.put_load_ins_monitor = put_load_ins_Monitor(dut)
        self.get_load_ins_driver = get_load_ins_Driver(dut)
        self.put_load_complete_driver = put_load_complete_Driver(dut)

        self.put_compute_ins_driver = put_compute_ins_Driver(dut)
        self.get_compute_ins_driver = get_compute_ins_Driver(dut)
        self.put_compute_complete_driver = put_compute_complete_Driver(dut)

        self.put_alu_ins_driver = put_alu_ins_Driver(dut)
        self.get_alu_ins_driver = get_alu_ins_Driver(dut)
        self.put_alu_complete_driver = put_alu_complete_Driver(dut)

        self.put_store_ins_driver = put_store_ins_Driver(dut)
        self.get_store_ins_driver = get_store_ins_Driver(dut)
        self.put_store_complete_driver = put_store_complete_Driver(dut)

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

    i = random.randrange(0,3)
    if i==0:
     load_flags = flags(0,0,0,0)
     compute_flags = flags(0,0,0,0)
    elif i==1:
     load_flags = flags(0,0,1,0)
     compute_flags = flags(0,1,0,0)
    else:
     load_flags = flags(0,0,0,1)
     compute_flags = flags(1,0,0,0)

    i = random.randrange(0,3)
    if i==0:
     compute_flags = flags(compute_flags.push_prev,compute_flags.pop_prev,0,0)
     alu_flags = flags(0,0,0,0)
    elif i==1:
     compute_flags = flags(compute_flags.push_prev,compute_flags.pop_prev,1,0)
     alu_flags = flags(0,1,0,0)
    else:
     compute_flags = flags(compute_flags.push_prev,compute_flags.pop_prev,0,1)
     alu_flags = flags(1,0,0,0)

    i = random.randrange(0,3)
    if i==0:
     alu_flags = flags(alu_flags.push_prev,alu_flags.pop_prev,0,0)
     store_flags = flags(0,0,0,0)
    elif i==1:
     alu_flags = flags(alu_flags.push_prev,alu_flags.pop_prev,1,0)
     store_flags = flags(0,1,0,0)
    else:
     alu_flags = flags(alu_flags.push_prev,alu_flags.pop_prev,0,1)
     store_flags = flags(1,0,0,0)

    print("Load Flags: ",load_flags)
    print("Compute Flags: ",compute_flags)
    print("Alu Flags: ",alu_flags)
    print("Store Flags: ",store_flags)

    local_flags = 0
    if load_flags.push_next == 1:
     local_flags += 1<<120
    elif load_flags.pop_next == 1:
     local_flags += 1<<121
    elif load_flags.push_prev == 1:
     local_flags += 1<<122
    elif load_flags.pop_prev == 1:
     local_flags += 1<<123

    i = put_load_ins_Transaction(tb,local_flags,1)
    yield tb.put_load_ins_driver.send_params(dut,i)

    local_flags = 0
    if compute_flags.push_next == 1:
     local_flags += 1<<120
    elif compute_flags.pop_next == 1:
     local_flags += 1<<121
    elif compute_flags.push_prev == 1:
     local_flags += 1<<122
    elif compute_flags.pop_prev == 1:
     local_flags += 1<<123

    i = put_compute_ins_Transaction(tb,local_flags,1)
    yield tb.put_compute_ins_driver.send_params(dut,i)

    local_flags = 0
    if alu_flags.push_next == 1:
     local_flags += 1<<120
    elif alu_flags.pop_next == 1:
     local_flags += 1<<121
    elif alu_flags.push_prev == 1:
     local_flags += 1<<122
    elif alu_flags.pop_prev == 1:
     local_flags += 1<<123

    i = put_alu_ins_Transaction(tb,local_flags,1)
    yield tb.put_alu_ins_driver.send_params(dut,i)

    local_flags = 0
    if store_flags.push_next == 1:
     local_flags += 1<<120
    elif store_flags.pop_next == 1:
     local_flags += 1<<121
    elif store_flags.push_prev == 1:
     local_flags += 1<<122
    elif store_flags.pop_prev == 1:
     local_flags += 1<<123

    i = put_store_ins_Transaction(tb,local_flags,1)
    yield tb.put_store_ins_driver.send_params(dut,i)

    for i in range(50):
     yield RisingEdge(dut.CLK)

    #All ins with no dependencies, enable if needed for basic testing 
    # i = put_load_ins_Transaction(tb,0,1)
    # yield tb.put_load_ins_driver.send_params(dut,i)
    # i = put_compute_ins_Transaction(tb,0,1)
    # yield tb.put_compute_ins_driver.send_params(dut,i)
    # i = put_alu_ins_Transaction(tb,0,1)
    # yield tb.put_alu_ins_driver.send_params(dut,i)
    # i = put_store_ins_Transaction(tb,0,1)
    # yield tb.put_store_ins_driver.send_params(dut,i)
    # yield RisingEdge(dut.CLK)
    # yield RisingEdge(dut.CLK)
    # yield tb.get_load_ins_driver.get_params(dut)
    # yield tb.get_compute_ins_driver.get_params(dut)
    # yield tb.get_alu_ins_driver.get_params(dut)
    # yield tb.get_store_ins_driver.get_params(dut)
    # yield tb.put_load_complete_driver.put_complete(dut)
    # yield tb.put_compute_complete_driver.put_complete(dut)
    # yield tb.put_alu_complete_driver.put_complete(dut)
    # yield tb.put_store_complete_driver.put_complete(dut)
    # yield RisingEdge(dut.CLK)
