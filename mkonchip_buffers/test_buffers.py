import random
import sys
import cocotb
import logging as log
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb_bus.monitors import BusMonitor
from cocotb_bus.drivers import BusDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb_bus.scoreboard import Scoreboard
from cocotb.result import TestFailure
from cocotb.clock import Clock

# Parameters for interfaces bsv 
sram_addr_width = 26
if_entries = 256
if_bank = 16
wt_entries = 256
wt_bank = 16
of_entries = 256
of_bank = 16
in_width = 8
out_width = 32

