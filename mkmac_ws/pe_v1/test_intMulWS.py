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

in_width = 8
out_width = 32

def twos_comp(val,bits):
    if(val & (1 << (bits - 1))) != 0 :
        val = val - (1 << bits)
    return val

class Driver(BusDriver):
    """Drives inputs to DUT"""
    _signals = [
        #
        'EN_subifc_put_wgt_put',
        'subifc_put_wgt_put',
        'EN_subifc_put_inp_put',
        'subifc_put_inp_put',
        'EN_subifc_put_acc_put',
        'subifc_put_acc_put',
        'EN_subifc_get_acc_get',
        'EN_subifc_get_wgt_get',
        'EN_subifc_get_inp_get',
    ]

    def __init__(self, dut):
        BusDriver.__init__(self, dut, None, dut.CLK)


class InputTransaction(object):
    """Transactions sent to Driver"""

    def __init__(self, tb,
                 #
                 EN_subifc_put_wgt_put=1,
                 subifc_put_wgt_put=0,
                 EN_subifc_put_inp_put=1,
                 subifc_put_inp_put=0,
                 EN_subifc_put_acc_put=1,
                 subifc_put_acc_put=0,
                 EN_subifc_get_acc_get=1,
                 EN_subifc_get_wgt_get=1,
                 EN_subifc_get_inp_get=1,
                 ):
        #
        self.EN_subifc_put_wgt_put = BinaryValue(
            EN_subifc_put_wgt_put, tb.EN_subifc_put_wgt_put_bits, False)
        self.subifc_put_wgt_put = BinaryValue(
            subifc_put_wgt_put, tb.subifc_put_wgt_put_bits, False)
        self.EN_subifc_put_inp_put = BinaryValue(
            EN_subifc_put_inp_put, tb.EN_subifc_put_inp_put_bits, False)
        self.subifc_put_inp_put = BinaryValue(
            subifc_put_inp_put, tb.subifc_put_inp_put_bits, False)
        self.EN_subifc_put_acc_put = BinaryValue(
            EN_subifc_put_acc_put, tb.EN_subifc_put_acc_put_bits, False)
        self.subifc_put_acc_put = BinaryValue(
            subifc_put_acc_put, tb.subifc_put_acc_put_bits, False)
        self.EN_subifc_get_acc_get = BinaryValue(
            EN_subifc_get_acc_get, tb.EN_subifc_get_acc_get_bits, False)
        self.EN_subifc_get_wgt_get = BinaryValue(
            EN_subifc_get_wgt_get, tb.EN_subifc_get_wgt_get_bits, False)
        self.EN_subifc_get_inp_get = BinaryValue(
            EN_subifc_get_inp_get, tb.EN_subifc_get_inp_get_bits, False)


class InputMonitor(BusMonitor):
    """Passive input monitor of DUT"""
    _signals = [
        #
        'EN_subifc_put_wgt_put',
        'subifc_put_wgt_put',
        'EN_subifc_put_inp_put',
        'subifc_put_inp_put',
        'EN_subifc_put_acc_put',
        'subifc_put_acc_put',
        'EN_subifc_get_acc_get',
        'EN_subifc_get_wgt_get',
        'EN_subifc_get_inp_get',
    ]

    def __init__(self, dut, callback=None, event=None):
        BusMonitor.__init__(self, dut, None,
                            dut.CLK, dut.RST_N,
                            callback=callback,
                            event=event)
        self.name = "in"

    @coroutine
    def _monitor_recv(self):
        EN_inp_edge = RisingEdge(self.bus.EN_subifc_put_inp_put)

        while True:
            yield EN_inp_edge
            if self.bus.EN_subifc_put_wgt_put.value.integer == 1 and self.bus.EN_subifc_put_inp_put == 1 and self.bus.EN_subifc_put_acc_put == 1:
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_subifc_put_wgt_put', self.bus.EN_subifc_put_wgt_put.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'subifc_put_wgt_put', hex(self.bus.subifc_put_wgt_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_subifc_put_inp_put', self.bus.EN_subifc_put_inp_put.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'subifc_put_inp_put', hex(self.bus.subifc_put_inp_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_subifc_put_acc_put', self.bus.EN_subifc_put_acc_put.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'subifc_put_acc_put', hex(self.bus.subifc_put_acc_put.value.integer)))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_subifc_get_acc_get', self.bus.EN_subifc_get_acc_get.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_subifc_get_wgt_get', self.bus.EN_subifc_get_wgt_get.value.integer))
                print('[IN_MON] {0:<25} : {1}'.format(
                    'EN_subifc_get_inp_get', self.bus.EN_subifc_get_inp_get.value.integer))

                vec = (
                    #
                    self.bus.EN_subifc_put_wgt_put.value.integer,
                    self.bus.subifc_put_wgt_put.value.integer,
                    self.bus.EN_subifc_put_inp_put.value.integer,
                    self.bus.subifc_put_inp_put.value.integer,
                    self.bus.EN_subifc_put_acc_put.value.integer,
                    self.bus.subifc_put_acc_put.value.integer,
                    self.bus.EN_subifc_get_acc_get.value.integer,
                    self.bus.EN_subifc_get_wgt_get.value.integer,
                    self.bus.EN_subifc_get_inp_get.value.integer
                )
                self._recv(vec)
            yield RisingEdge(self.clock)

class OutputTransaction(object):
    """ Transaction to be expected / received by OutputMonitor"""

    def __init__(self, tb=None,
                 #
                 RDY_subifc_put_wgt_put=0,
                 RDY_subifc_put_inp_put=0,
                 RDY_subifc_put_acc_put=0,
                 subifc_get_acc_get=0,
                 RDY_subifc_get_acc_get=0,
                 subifc_get_wgt_get=0,
                 RDY_subifc_get_wgt_get=0,
                 subifc_get_inp_get=0,
                 RDY_subifc_get_inp_get=0,
                 ):
        """For expected transactions, value 'None' means don't care.
        tb must be an instance of the Testbench class."""
#
        if RDY_subifc_put_wgt_put is not None and isinstance(RDY_subifc_put_wgt_put, int):
            RDY_subifc_put_wgt_put = BinaryValue(
                RDY_subifc_put_wgt_put, tb.RDY_subifc_put_wgt_put_bits, False)
        if RDY_subifc_put_inp_put is not None and isinstance(RDY_subifc_put_inp_put, int):
            RDY_subifc_put_inp_put = BinaryValue(
                RDY_subifc_put_inp_put, tb.RDY_subifc_put_inp_put_bits, False)
        if RDY_subifc_put_acc_put is not None and isinstance(RDY_subifc_put_acc_put, int):
            RDY_subifc_put_acc_put = BinaryValue(
                RDY_subifc_put_acc_put, tb.RDY_subifc_put_acc_put_bits, False)
        if subifc_get_acc_get is not None and isinstance(subifc_get_acc_get, int):
            subifc_get_acc_get = BinaryValue(
                subifc_get_acc_get, tb.subifc_get_acc_get_bits, False)
        if RDY_subifc_get_acc_get is not None and isinstance(RDY_subifc_get_acc_get, int):
            RDY_subifc_get_acc_get = BinaryValue(
                RDY_subifc_get_acc_get, tb.RDY_subifc_get_acc_get_bits, False)
        if subifc_get_wgt_get is not None and isinstance(subifc_get_wgt_get, int):
            subifc_get_wgt_get = BinaryValue(
                subifc_get_wgt_get, tb.subifc_get_wgt_get_bits, False)
        if RDY_subifc_get_wgt_get is not None and isinstance(RDY_subifc_get_wgt_get, int):
            RDY_subifc_get_wgt_get = BinaryValue(
                RDY_subifc_get_wgt_get, tb.RDY_subifc_get_wgt_get_bits, False)
        if subifc_get_inp_get is not None and isinstance(subifc_get_inp_get, int):
            subifc_get_inp_get = BinaryValue(
                subifc_get_inp_get, tb.subifc_get_inp_get_bits, False)
        if RDY_subifc_get_inp_get is not None and isinstance(RDY_subifc_get_inp_get, int):
            RDY_subifc_get_inp_get = BinaryValue(
                RDY_subifc_get_inp_get, tb.RDY_subifc_get_inp_get_bits, False)
#
        self.value = (
            RDY_subifc_put_wgt_put,
            RDY_subifc_put_inp_put,
            RDY_subifc_put_acc_put,
            subifc_get_acc_get,
            RDY_subifc_get_acc_get,
            subifc_get_wgt_get,
            RDY_subifc_get_wgt_get,
            subifc_get_inp_get,
            RDY_subifc_get_inp_get
        )


class Monitor(BusMonitor):
    """Observes signals of DUT"""
    _signals = [
        #
        'RDY_subifc_put_wgt_put',
        'RDY_subifc_put_inp_put',
        'RDY_subifc_put_acc_put',
        'subifc_get_acc_get',
        'RDY_subifc_get_acc_get',
        'subifc_get_wgt_get',
        'RDY_subifc_get_wgt_get',
        'subifc_get_inp_get',
        'RDY_subifc_get_inp_get',
    ]

    def __init__(self, dut, tb, callback=None, event=None):
        BusMonitor.__init__(self, dut, None, dut.CLK, dut.RST_N,
                            callback=callback, event=event)
        self.name = "out"
        self.tb = tb

    @coroutine
    def _monitor_recv(self):
        outp_ready_edge = RisingEdge(self.bus.RDY_subifc_get_acc_get)
        while True:
            yield outp_ready_edge
            # Should there be any check on weight RDY signal
            if self.bus.RDY_subifc_get_acc_get.value == 1 and self.bus.RDY_subifc_get_inp_get:
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_subifc_put_wgt_put ', self.bus.RDY_subifc_put_wgt_put.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_subifc_put_inp_put ', self.bus.RDY_subifc_put_inp_put.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_subifc_put_acc_put ', self.bus.RDY_subifc_put_acc_put.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'subifc_get_acc_get ', hex(self.bus.subifc_get_acc_get.value)))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_subifc_get_acc_get ', self.bus.RDY_subifc_get_acc_get.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'subifc_get_wgt_get ', hex(self.bus.subifc_get_wgt_get.value)))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_subifc_get_wgt_get ', self.bus.RDY_subifc_get_wgt_get.value))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'subifc_get_inp_get ', hex(self.bus.subifc_get_inp_get.value)))
                print('[DUT_MON] {0:<25} : {1}'.format(
                    'RDY_subifc_get_inp_get ', self.bus.RDY_subifc_get_inp_get.value))

                pe_out = twos_comp(self.bus.subifc_get_acc_get.value,out_width)

                self._recv(OutputTransaction(self.tb,
                                             #
                                             self.bus.RDY_subifc_put_wgt_put.value,
                                             self.bus.RDY_subifc_put_inp_put.value,
                                             self.bus.RDY_subifc_put_acc_put.value,
                                             hex(pe_out),
                                             self.bus.RDY_subifc_get_acc_get.value,
                                             hex(self.bus.subifc_get_wgt_get.value),
                                             self.bus.RDY_subifc_get_wgt_get.value,
                                             hex(self.bus.subifc_get_inp_get.value),
                                             self.bus.RDY_subifc_get_inp_get.value
                                             ))
            yield RisingEdge(self.clock)

class DUTScoreboard(Scoreboard):
    def compare(self, got, exp, log, **_):

        if(exp.value[4] == 0):
            print("Overflow!")
        if got.value[3] == exp.value[3] and got.value[5] == exp.value[5] and got.value[7] == exp.value[7]:
            print('PASSED Outputs match Exp={0} Got={1}   {2}'.format(
                exp.value[3], got.value[3], got.value[4]))
            print('PASSED Outputs match Exp={0} Got={1}   {2}'.format(
                exp.value[5], got.value[5], got.value[6]))
            print('PASSED Outputs match Exp={0} Got={1}   {2}'.format(
                exp.value[7], got.value[7], got.value[8]))
        else:
            print('ERROR Outputs differ Exp={0} Got={1}   {2}'.format(
                exp.value[3], got.value[3], got.value[4]))
            print('ERROR Outputs differ Exp={0} Got={1}   {2}'.format(
                exp.value[5], got.value[5], got.value[6]))
            print('ERROR Outputs differ Exp={0} Got={1}  {2}'.format(
                exp.value[7], got.value[7], got.value[8]))
            exit(1)


class TestBench(object):
    """Verification Test Bench"""

    def __init__(self, dut):
        self.dut = dut
        self.stopped = False

        """Signal length"""
#
        self.EN_subifc_put_wgt_put_bits = 1
        self.subifc_put_wgt_put_bits = in_width + 8
        self.EN_subifc_put_inp_put_bits = 1
        self.subifc_put_inp_put_bits = in_width
        self.EN_subifc_put_acc_put_bits = 1
        self.subifc_put_acc_put_bits = out_width
        self.EN_subifc_get_acc_get_bits = 1
        self.EN_subifc_get_wgt_get_bits = 1
        self.EN_subifc_get_inp_get_bits = 1
#
        self.RDY_subifc_put_wgt_put_bits = 1
        self.RDY_subifc_put_inp_put_bits = 1
        self.RDY_subifc_put_acc_put_bits = 1
        self.subifc_get_acc_get_bits = out_width
        self.RDY_subifc_get_acc_get_bits = 1
        self.subifc_get_wgt_get_bits = in_width + 8
        self.RDY_subifc_get_wgt_get_bits = 1
        self.subifc_get_inp_get_bits = in_width
        self.RDY_subifc_get_inp_get_bits = 1

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
            EN_subifc_put_wgt_put,
            subifc_put_wgt_put,
            EN_subifc_put_inp_put,
            subifc_put_inp_put,
            EN_subifc_put_acc_put,
            subifc_put_acc_put,
            EN_subifc_get_acc_get,
            EN_subifc_get_wgt_get,
            EN_subifc_get_inp_get,
        ) = transaction

        input_to_model = twos_comp(int(bin(subifc_put_inp_put)[2:].zfill(in_width),2),in_width)
        weight_to_model = twos_comp(int((bin(subifc_put_wgt_put)[2:].zfill(in_width+8)[:in_width]),2),in_width)
        counter_val = int((bin(subifc_put_wgt_put)[2:].zfill(in_width+8)[in_width:]),2)
        acc_in_to_model = twos_comp(subifc_put_acc_put,out_width)

        print('[MODEL] {0:<25} : {1}'.format('input', hex(input_to_model)))
        print('[MODEL] {0:<25} : {1}'.format('accumulator', hex(acc_in_to_model)))
        print('[MODEL] {0:<25} : {1}'.format('weight', hex(weight_to_model)))
        print('[MODEL] {0:<25} : {1}'.format('counter', hex(counter_val)))
        """ Model being called here """
        subifc_get_acc_get = intMul_model(
            acc_in_to_model, input_to_model, weight_to_model)
        print('[MODEL] {0:<25} : {1}'.format('output_accumulator', hex(subifc_get_acc_get)))

        RDY_subifc_put_wgt_put = 1
        RDY_subifc_put_inp_put = 1
        RDY_subifc_put_acc_put = 1
        RDY_subifc_get_acc_get = 1
        RDY_subifc_get_wgt_get = 1
        RDY_subifc_get_inp_get = 1
        subifc_get_wgt_get = subifc_put_wgt_put
        subifc_get_inp_get = subifc_put_inp_put

        self.expected_output.append(OutputTransaction(self,
                                                      #
                                                      RDY_subifc_put_wgt_put,
                                                      RDY_subifc_put_inp_put,
                                                      RDY_subifc_put_acc_put,
                                                      hex(subifc_get_acc_get),
                                                      RDY_subifc_get_acc_get,
                                                      hex(subifc_get_wgt_get),
                                                      RDY_subifc_get_wgt_get,
                                                      hex(subifc_get_inp_get),
                                                      RDY_subifc_get_inp_get,
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
    accum_to_pe = random.randint(0, (2**out_width) - 1)
    weight_to_pe = random.randint(0, (2**in_width) - 1)
    counter = 0

    EN_subifc_put_wgt_put = 1
    subifc_put_wgt_put = weight_to_pe << 8 | counter
    EN_subifc_put_inp_put = 1
    subifc_put_inp_put = input_to_pe
    EN_subifc_put_acc_put = 1
    subifc_put_acc_put = accum_to_pe
    EN_subifc_get_acc_get = 0
    EN_subifc_get_wgt_get = 0
    EN_subifc_get_inp_get = 0

    yield InputTransaction(tb,
                           EN_subifc_put_wgt_put,
                           subifc_put_wgt_put,
                           EN_subifc_put_inp_put,
                           subifc_put_inp_put,
                           EN_subifc_put_acc_put,
                           subifc_put_acc_put,
                           EN_subifc_get_acc_get,
                           EN_subifc_get_wgt_get,
                           EN_subifc_get_inp_get,
                           )

    EN_subifc_put_wgt_put = 0
    EN_subifc_put_inp_put = 0
    EN_subifc_put_acc_put = 0
    EN_subifc_get_wgt_get = 1
    EN_subifc_get_inp_get = 1
    EN_subifc_get_acc_get = 1
    yield InputTransaction(tb,
                           EN_subifc_put_wgt_put,
                           subifc_put_wgt_put,
                           EN_subifc_put_inp_put,
                           subifc_put_inp_put,
                           EN_subifc_put_acc_put,
                           subifc_put_acc_put,
                           EN_subifc_get_acc_get,
                           EN_subifc_get_wgt_get,
                           EN_subifc_get_inp_get,
                           )

    EN_subifc_get_wgt_get = 0
    EN_subifc_get_inp_get = 0
    EN_subifc_get_acc_get = 0
    yield InputTransaction(tb,
                           EN_subifc_put_wgt_put,
                           subifc_put_wgt_put,
                           EN_subifc_put_inp_put,
                           subifc_put_inp_put,
                           EN_subifc_put_acc_put,
                           subifc_put_acc_put,
                           EN_subifc_get_acc_get,
                           EN_subifc_get_wgt_get,
                           EN_subifc_get_inp_get,
                           )



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

    for n in range(1000):
        input_gen = random_input_gen(tb)
        for t in input_gen:
            yield tb.input_drv.send(t)
        time_delay = random.randint(0,5)
        for delay in range(time_delay):
            yield RisingEdge(dut.CLK)

    tb.stop()
    yield RisingEdge(dut.CLK)