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
from random_shaktimaan_instr_gen import *

load_data = []
store_data = []

Load_dep_parameters_Coverage    = coverage_section (CoverPoint("top.load_dep_flags", vname="inp_load_dep_flags", bins = [0b0000, 0b0001, 0b0100, 0b0101,]))
Store_dep_parameters_Coverage   = coverage_section (CoverPoint("top.store_dep_flags", vname="inp_store_dep_flags", bins = [0b0000, 0b0010, 0b1000, 0b1010]))
Gemm_dep_paramters_Coverage     = coverage_section (CoverPoint("top.gemm_dep_flags", vname="inp_gemm_dep_flags", bins = list(range(16))))
Talu_dep_parameters_Coverage    = coverage_section (CoverPoint("top.talu_dep_flags", vname="inp_talu_dep_flags", bins = list(range(16))))

@Load_dep_parameters_Coverage
def load_instruction_dep_coverage(inp_load_dep_flags):
    return inp_load_dep_flags

@Store_dep_parameters_Coverage
def store_instruction_dep_coverage(inp_store_dep_flags):
    return inp_store_dep_flags

@Gemm_dep_paramters_Coverage
def gemm_instruction_dep_coverage(inp_gemm_dep_flags):
    return inp_gemm_dep_flags

@Talu_dep_parameters_Coverage
def talu_instruction_dep_coverage(inp_talu_dep_flags):
    return inp_talu_dep_flags


@coroutine
def ins_feed(dut, number, instr):
 i = 0

 while (i<number):
  if dut.ifc_fetch_master_RREADY == 1:
   dut.ifc_fetch_master_RVALID <= 1
   dut.ifc_fetch_master_RDATA <= instr[i]

   print("Driven instruction from cocoTB : ",i,hex(instr[i]))
   if(int(hex(instr[i])[2],16) == 8):
     print("Load instruction with dep flag ",load_instruction_dep_coverage(int(hex(instr[i])[3],16)))
   elif(int(hex(instr[i])[2],16) == 9):
     print("Store instruction with dep flag ",store_instruction_dep_coverage(int(hex(instr[i])[3],16)))
   elif(int(hex(instr[i])[2],16) == 10):
     print("Compute instruction with dep flag ",gemm_instruction_dep_coverage(int(hex(instr[i])[3],16)))
   elif(int(hex(instr[i])[2],16) == 11):
     print("TALU instruction with dep flag ",talu_instruction_dep_coverage(int(hex(instr[i])[3],16)))

   if i == (number-1):
    dut.ifc_fetch_master_RLAST <= 1
   i += 1
   yield RisingEdge(dut.CLK)
   dut.ifc_fetch_master_RVALID <= 0
   dut.ifc_fetch_master_RLAST <= 0
  yield FallingEdge(dut.CLK)
addr_queue = []

@coroutine
def load_addr_feed(dut):

 while (True):
  if dut.ifc_load_master_ARVALID == 1:
   yield Timer(5)
   addr_queue.append(int(dut.ifc_load_master_ARLEN) + 1)
   yield Timer(5)
   print(" Load Address driving from cocoTB")
  else:
   yield Timer(10)

@coroutine
def load_feed(dut):
 i=0
 k=0
 
 while (True):
  if len(addr_queue) >= 1:
   no_load = addr_queue.pop(0)
   while (i<no_load):
    if dut.ifc_load_master_RREADY == 1:
     dut.ifc_load_master_RVALID <= 1
     load_data.append(k) #Feed random values
     dut.ifc_load_master_RDATA <= k
     if i == (no_load-1):
      dut.ifc_load_master_RLAST <= 1
     i += 1
     yield Timer(5)
     dut.ifc_load_master_RVALID <= 0
     dut.ifc_load_master_RLAST <= 0
     yield Timer(5)
   i=0
   k += 1
   print(" Load data driving from cocoTB ")
  else:
   yield Timer(10)

@coroutine
def store_feed(dut):
 i=0
 
 while (True):
  if dut.ifc_store_master_WVALID == 1:
    store_data.append({'data':int(dut.ifc_store_master_WDATA), 'last': int(dut.ifc_store_master_WLAST)})
    yield Timer(10)
    print(" Store got data from DUT : ",dut.ifc_store_master_WDATA)
  else:
   yield Timer(10)

@cocotb.test()
def test_shaktimaan_random_instr(dut):
    """ Test that checks compute on reset """

    no_of_ins_set = 35
    pc_val = 5

    
    ##Temporary Ins_queue feeding logic
    #ins_queue = []
    #ins_queue.append(170141183460469231731687303715884105728)

    ins_queue = random_shaktimaan_instr_gen(no_of_ins_set)
    no_of_ins = len(ins_queue)
    print("Driving inputs ", ins_queue, no_of_ins, no_of_ins_set)

    clock = Clock(dut.CLK, 4, units="ps")  # Create a 10us period clock on port clk
    cocotb.fork(clock.start())  # Start the clock

    for i in range(3):
     val = random.randint(0, 1)
     dut.RST_N<= 0
     yield FallingEdge(dut.CLK)
     #assert dut.q == val, "output q was incorrect on the {}th cycle".format(i)

    for i in range (2):
     dut.RST_N <= 1
     yield FallingEdge(dut.CLK)

    yield RisingEdge(dut.CLK)
    yield FallingEdge(dut.CLK)

    dut.ifc_fetch_slave_AWADDR <= 9437184 #Config_addr
    dut.ifc_fetch_slave_AWVALID <= 1
    dut.ifc_fetch_slave_WDATA <= pc_val + (no_of_ins<<32)
    dut.ifc_fetch_slave_WVALID <= 1

    yield RisingEdge(dut.CLK)

    dut.ifc_fetch_slave_AWVALID <= 0
    dut.ifc_fetch_slave_WVALID <= 0
    dut.ifc_fetch_slave_BREADY <= 1

    dut.ifc_fetch_master_ARREADY <= 1
    dut.ifc_fetch_master_RID <= 1
    dut.ifc_load_master_ARREADY <= 1
    dut.ifc_load_master_RID <= 2
    dut.ifc_store_master_AWREADY <= 1
    dut.ifc_store_master_WREADY <= 1
    dut.ifc_store_master_BID <= 3

    yield RisingEdge(dut.ifc_fetch_master_ARVALID)

    yield FallingEdge(dut.CLK)

    i = 0

    while dut.ifc_fetch_master_ARVALID == 1:
     if dut.ifc_fetch_master_ARADDR != (pc_val+(i*4080)):
      ##Throw Error
      print("Error")
     i += 1
     yield FallingEdge(dut.CLK)

    ins_feed_coroutine = cocotb.fork(ins_feed(dut,no_of_ins,ins_queue))
    cocotb.fork(load_feed(dut))
    cocotb.fork(load_addr_feed(dut))
    cocotb.fork(store_feed(dut))

    yield ins_feed_coroutine.join()

    for i in range (5000):
     yield RisingEdge(dut.CLK)

    coverage_db.export_to_yaml(filename="coverage_dep_flags_params.yml")
