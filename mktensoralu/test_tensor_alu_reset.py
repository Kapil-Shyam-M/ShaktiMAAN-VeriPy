import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
def test_tensor_alu_reset(dut):
    """ Test that checks tensor ALU on reset """

    clock = Clock(dut.CLK, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.fork(clock.start())  # Start the clock

    for i in range(3):
     val = random.randint(0, 1)
     dut.RST_N<= 0
     yield FallingEdge(dut.CLK)
     #assert dut.q == val, "output q was incorrect on the {}th cycle".format(i)

    for i in range (2):
     dut.RST_N <= 1
     yield FallingEdge(dut.CLK)
