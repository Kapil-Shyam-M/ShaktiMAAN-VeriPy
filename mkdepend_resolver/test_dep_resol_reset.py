import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
def test_dep_resol_reset(dut):
    """ Test that checks dep resolver on reset """

    clock = Clock(dut.CLK, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.fork(clock.start())  # Start the clock

    for i in range(3):
     val = random.randint(0, 1)
     dut.RST_N.value <= 0
     yield FallingEdge(dut.CLK)
     #assert dut.q == val, "output q was incorrect on the {}th cycle".format(i)

    for i in range (2):
     dut.RST_N.value <= 1
     yield FallingEdge(dut.CLK)
