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
from intMul_model import intMul_model

# Parameters : In width - 8, out width - 32, coordinate - 1

in_width = 16
out_width = 32

def twos_comp(val,bits):
    if(val & (1 << (bits - 1))) != 0 :
        val = val - (1 << bits)
    return val

class Driver(BusDriver):
    """Drives inputs to DUT"""
    _signals = [
        #
        'EN_ifc_get_wgt_put',
        'ifc_get_wgt_put',
        'EN_ifc_get_inp_put',
        'ifc_get_inp_put',
        'EN_ifc_get_out_get',
        'EN_ifc_put_wgt_get',
        'EN_ifc_put_inp_get',
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


class InputTransaction(object):
    """Transactions sent to Driver"""

    def __init__(self, tb,
                 #
                 EN_ifc_get_wgt_put=1,
                 ifc_get_wgt_put=0,
                 EN_ifc_get_inp_put=1,
                 ifc_get_inp_put=0,
                 EN_ifc_get_out_get=1,
                 EN_ifc_put_wgt_get=1,
                 EN_ifc_put_inp_get=1,
                 ):
        #
        self.EN_ifc_get_wgt_put = BinaryValue(
            EN_ifc_get_wgt_put, tb.EN_ifc_get_wgt_put_bits, False)
        self.ifc_get_wgt_put = BinaryValue(
            ifc_get_wgt_put, tb.ifc_get_wgt_put_bits, False)
        self.EN_ifc_get_inp_put = BinaryValue(
            EN_ifc_get_inp_put, tb.EN_ifc_get_inp_put_bits, False)
        self.ifc_get_inp_put = BinaryValue(
            ifc_get_inp_put, tb.ifc_get_inp_put_bits, False)
        self.EN_ifc_get_out_get = BinaryValue(
            EN_ifc_get_out_get, tb.EN_ifc_get_out_get_bits, False)
        self.EN_ifc_put_wgt_get = BinaryValue(
            EN_ifc_put_wgt_get, tb.EN_ifc_put_wgt_get_bits, False)
        self.EN_ifc_put_inp_get = BinaryValue(
            EN_ifc_put_inp_get, tb.EN_ifc_put_inp_get_bits, False)


class InputMonitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        #
        'EN_ifc_get_wgt_put',
        'ifc_get_wgt_put',
        'EN_ifc_get_inp_put',
        'ifc_get_inp_put',
        'EN_ifc_get_out_get',
        'EN_ifc_put_wgt_get',
        'EN_ifc_put_inp_get',
    ]

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):
        EN_inp_edge = RisingEdge(self.bus.EN_ifc_get_inp_put)

        while True:
            yield RisingEdge(self.clock)
            if self.bus.EN_ifc_get_wgt_put == 1 and self.bus.EN_ifc_get_inp_put == 1 :
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_ifc_get_wgt_put', self.bus.EN_ifc_get_wgt_put.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'ifc_get_wgt_put', hex(self.bus.ifc_get_wgt_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_ifc_get_inp_put', self.bus.EN_ifc_get_inp_put.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'ifc_get_inp_put', hex(self.bus.ifc_get_inp_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_ifc_get_out_get', self.bus.EN_ifc_get_out_get.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_ifc_put_wgt_get', self.bus.EN_ifc_put_wgt_get.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_ifc_put_inp_get', self.bus.EN_ifc_put_inp_get.value.integer))

                vec = (
                    #
                    self.bus.EN_ifc_get_wgt_put.value.integer,
                    self.bus.ifc_get_wgt_put.value.integer,
                    self.bus.EN_ifc_get_inp_put.value.integer,
                    self.bus.ifc_get_inp_put.value.integer,
                    self.bus.EN_ifc_get_out_get.value.integer,
                    self.bus.EN_ifc_put_wgt_get.value.integer,
                    self.bus.EN_ifc_put_inp_get.value.integer
                )
                self._recv(vec)
            yield RisingEdge(self.clock)

class OutputTransaction(object):
    """ Transaction to be expected / received by OutputMonitor"""

    def __init__(self, tb=None,
                 #
                 RDY_ifc_get_wgt_put=0,
                 RDY_ifc_get_inp_put=0,
                 ifc_get_out_get=0,
                 RDY_ifc_get_out_get=0,
                 ifc_put_wgt_get=0,
                 RDY_ifc_put_wgt_get=0,
                 ifc_put_inp_get=0,
                 RDY_ifc_put_inp_get=0,
                 ):
        """For expected transactions, value 'None' means don't care.
        tb must be an instance of the Testbench class."""
#
        if RDY_ifc_get_wgt_put is not None and isinstance(RDY_ifc_get_wgt_put, int):
            RDY_ifc_get_wgt_put = BinaryValue(
                RDY_ifc_get_wgt_put, tb.RDY_ifc_get_wgt_put_bits, False)
        if RDY_ifc_get_inp_put is not None and isinstance(RDY_ifc_get_inp_put, int):
            RDY_ifc_get_inp_put = BinaryValue(
                RDY_ifc_get_inp_put, tb.RDY_ifc_get_inp_put_bits, False)
        if ifc_get_out_get is not None and isinstance(ifc_get_out_get, int):
            ifc_get_out_get = BinaryValue(
                ifc_get_out_get, tb.ifc_get_out_get_bits, False)
        if RDY_ifc_get_out_get is not None and isinstance(RDY_ifc_get_out_get, int):
            RDY_ifc_get_out_get = BinaryValue(
                RDY_ifc_get_out_get, tb.RDY_ifc_get_out_get_bits, False)
        if ifc_put_wgt_get is not None and isinstance(ifc_put_wgt_get, int):
            ifc_put_wgt_get = BinaryValue(
                ifc_put_wgt_get, tb.ifc_put_wgt_get_bits, False)
        if RDY_ifc_put_wgt_get is not None and isinstance(RDY_ifc_put_wgt_get, int):
            RDY_ifc_put_wgt_get = BinaryValue(
                RDY_ifc_put_wgt_get, tb.RDY_ifc_put_wgt_get_bits, False)
        if ifc_put_inp_get is not None and isinstance(ifc_put_inp_get, int):
            ifc_put_inp_get = BinaryValue(
                ifc_put_inp_get, tb.ifc_put_inp_get_bits, False)
        if RDY_ifc_put_inp_get is not None and isinstance(RDY_ifc_put_inp_get, int):
            RDY_ifc_put_inp_get = BinaryValue(
                RDY_ifc_put_inp_get, tb.RDY_ifc_put_inp_get_bits, False)
#
        self.value = (
            RDY_ifc_get_wgt_put,
            RDY_ifc_get_inp_put,
            ifc_get_out_get,
            RDY_ifc_get_out_get,
            ifc_put_wgt_get,
            RDY_ifc_put_wgt_get,
            ifc_put_inp_get,
            RDY_ifc_put_inp_get
        )


class Monitor(BusMonitor):
    """Observes signals of DUT"""
    _signals = [
        #
        'RDY_ifc_get_wgt_put',
        'RDY_ifc_get_inp_put',
        'ifc_get_out_get',
        'RDY_ifc_get_out_get',
        'ifc_put_wgt_get',
        'RDY_ifc_put_wgt_get',
        'ifc_put_inp_get',
        'RDY_ifc_put_inp_get',
        'EN_ifc_get_out_get',
    ]

    def __init__(self, dut, tb, callback=None, event=None):
        BusMonitor.__init__(self, dut, None, dut.CLK, dut.RST_N,
                            callback=callback, event=event)
        self.name = "out"
        self.tb = tb

    @coroutine
    def _monitor_recv(self):
        outp_ready_edge = RisingEdge(self.bus.EN_ifc_get_out_get)
        while True:
            yield RisingEdge(self.clock)
            # Should there be any check on weight RDY signal
            if self.bus.RDY_ifc_get_out_get == 1:
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_ifc_get_wgt_put ', self.bus.RDY_ifc_get_wgt_put.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_ifc_get_inp_put ', self.bus.RDY_ifc_get_inp_put.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'ifc_get_out_get ', hex(self.bus.ifc_get_out_get.value)))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_ifc_get_out_get ', self.bus.RDY_ifc_get_out_get.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'ifc_put_wgt_get ', hex(self.bus.ifc_put_wgt_get.value)))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_ifc_put_wgt_get ', self.bus.RDY_ifc_put_wgt_get.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'ifc_put_inp_get ', hex(self.bus.ifc_put_inp_get.value)))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_ifc_put_inp_get ', self.bus.RDY_ifc_put_inp_get.value))

                pe_out = twos_comp(self.bus.ifc_get_out_get.value,out_width)

                self._recv(OutputTransaction(self.tb,
                                             #
                                             self.bus.RDY_ifc_get_wgt_put.value,
                                             self.bus.RDY_ifc_get_inp_put.value,
                                             hex(pe_out),
                                             self.bus.RDY_ifc_get_out_get.value,
                                             hex(self.bus.ifc_put_wgt_get.value),
                                             self.bus.RDY_ifc_put_wgt_get.value,
                                             hex(self.bus.ifc_put_inp_get.value),
                                             self.bus.RDY_ifc_put_inp_get.value
                                             ))

                yield RisingEdge(self.clock)
class DUTScoreboard(Scoreboard):
    def compare(self, got, exp, log, **_):

        if got.value[2] == exp.value[2] and got.value[3] == 1 and got.value[4] == exp.value[4] and got.value[6] == exp.value[6] and got.value[7] == 1 :
            print('PASSED Outputs match Exp={0} Got={1}   {2}'.format(
                exp.value[2], got.value[2], got.value[3]))
            print('PASSED Outputs match Exp={0} Got={1}   {2}'.format(
                exp.value[4], got.value[4], got.value[5]))
            print('PASSED Outputs match Exp={0} Got={1}   {2}'.format(
                exp.value[6], got.value[6], got.value[7]))
        else:
            print('ERROR Outputs differ Exp={0} Got={1}   {2}'.format(
                exp.value[2], got.value[2], got.value[3]))
            print('ERROR Outputs differ Exp={0} Got={1}   {2}'.format(
                exp.value[4], got.value[4], got.value[5]))
            print('ERROR Outputs differ Exp={0} Got={1}  {2}'.format(
                exp.value[6], got.value[6], got.value[7]))
            exit(1)


class TestBench(object):
    """Verification Test Bench"""

    def __init__(self, dut):
        self.dut = dut
        self.stopped = False

        """Signal length"""
#
        self.EN_ifc_get_wgt_put_bits = 1
        self.ifc_get_wgt_put_bits = in_width + 8
        self.EN_ifc_get_inp_put_bits = 1
        self.ifc_get_inp_put_bits = in_width
        self.EN_ifc_get_out_get_bits = 1
        self.EN_ifc_put_wgt_get_bits = 1
        self.EN_ifc_put_inp_get_bits = 1
#
        self.RDY_ifc_get_wgt_put_bits = 1
        self.RDY_ifc_get_inp_put_bits = 1
        self.ifc_get_out_get_bits = out_width
        self.RDY_ifc_get_out_get_bits = 1
        self.ifc_put_wgt_get_bits = in_width + 8
        self.RDY_ifc_put_wgt_get_bits = 1
        self.ifc_put_inp_get_bits = in_width
        self.RDY_ifc_put_inp_get_bits = 1

        self.input_drv = Driver(dut)

        self.input_mon = InputMonitor(dut, callback=self.model)

        init_val = OutputTransaction(self)

        self.mon = Monitor(dut, self)

        self.expected_output = []
        self.scoreboard = DUTScoreboard(dut)
        self.scoreboard.add_interface(self.mon, self.expected_output)

    def model(self, transaction):
        """Model"""
#
        (
            EN_ifc_get_wgt_put,
            ifc_get_wgt_put,
            EN_ifc_get_inp_put,
            ifc_get_inp_put,
            EN_ifc_get_out_get,
            EN_ifc_put_wgt_get,
            EN_ifc_put_inp_get,
        ) = transaction

        input_to_model = twos_comp(int(bin(ifc_get_inp_put)[2:],2),in_width)
        weight_to_model = twos_comp(int((bin(ifc_get_wgt_put)[2:].zfill(in_width+8)[:in_width]),2),in_width)
        counter_val = int((bin(ifc_get_wgt_put)[2:].zfill(in_width+8)[in_width:]),2)

        print('[MODEL] {0:<25} : {1}'.format('input', hex(input_to_model)))
        print('[MODEL] {0:<25} : {1}'.format('weight', hex(weight_to_model)))
        print('[MODEL] {0:<25} : {1}'.format('counter', hex(counter_val)))
        """ Model being called here """
        ifc_get_out_get = intMul_model(input_to_model, weight_to_model)
        print('[MODEL] {0:<25} : {1}'.format('output_accumulator', hex(ifc_get_out_get)))

        RDY_ifc_get_wgt_put = 1
        RDY_ifc_get_inp_put = 1
        RDY_ifc_put_acc_put = 1
        RDY_ifc_put_wgt_get = 1
        RDY_ifc_put_inp_get = 1
        RDY_ifc_get_out_get = 1
        ifc_put_wgt_get = ifc_get_wgt_put
        ifc_put_inp_get = ifc_get_inp_put

        self.expected_output.append(OutputTransaction(self,
                                                      #
                                                      RDY_ifc_get_wgt_put,
                                                      RDY_ifc_get_inp_put,
                                                      hex(ifc_get_out_get),
                                                      RDY_ifc_get_out_get,
                                                      hex(ifc_put_wgt_get),
                                                      RDY_ifc_put_wgt_get,
                                                      hex(ifc_put_inp_get),
                                                      RDY_ifc_put_inp_get,
                                                      ))

    def stop(self):
        """
        Stop generation of expected output transactions.
        One more clock cycle must be executed afterwards, so that, output of
        D-FF can be checked.
        """
        self.stopped = True


def random_input_gen(tb):
    valid = 1
    input_to_pe = random.randint(0, (2**in_width) - 1)
    weight_to_pe = random.randint(0, (2**in_width) - 1)
    counter = 0

    EN_ifc_get_wgt_put = 1
    ifc_get_wgt_put = weight_to_pe << 8 | counter
    EN_ifc_get_inp_put = 1
    ifc_get_inp_put = input_to_pe
    EN_ifc_get_out_get = 0
    EN_ifc_put_wgt_get = 0
    EN_ifc_put_inp_get = 0

    yield InputTransaction(tb,
                           EN_ifc_get_wgt_put,
                           ifc_get_wgt_put,
                           EN_ifc_get_inp_put,
                           ifc_get_inp_put,
                           EN_ifc_get_out_get,
                           EN_ifc_put_wgt_get,
                           EN_ifc_put_inp_get,
                           )

    EN_ifc_get_wgt_put = 0
    EN_ifc_get_inp_put = 0
    EN_ifc_put_wgt_get = 1
    EN_ifc_put_inp_get = 1
    EN_ifc_get_out_get = 1
    yield InputTransaction(tb,
                           EN_ifc_get_wgt_put,
                           ifc_get_wgt_put,
                           EN_ifc_get_inp_put,
                           ifc_get_inp_put,
                           EN_ifc_get_out_get,
                           EN_ifc_put_wgt_get,
                           EN_ifc_put_inp_get,
                           )

    EN_ifc_put_wgt_get = 0
    EN_ifc_put_inp_get = 0
    EN_ifc_get_out_get = 0
    yield InputTransaction(tb,
                           EN_ifc_get_wgt_put,
                           ifc_get_wgt_put,
                           EN_ifc_get_inp_put,
                           ifc_get_inp_put,
                           EN_ifc_get_out_get,
                           EN_ifc_put_wgt_get,
                           EN_ifc_put_inp_get,
                           )



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

    for n in range(1000):
        input_gen = random_input_gen(tb)
        for t in input_gen:
            yield tb.input_drv.send(t)
        time_delay = random.randint(0,5)
        for delay in range(time_delay):
            yield RisingEdge(dut.CLK)

    tb.stop()
    yield RisingEdge(dut.CLK)
