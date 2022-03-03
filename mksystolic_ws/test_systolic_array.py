import random
import sys
import cocotb
import logging as log
import numpy as np
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.monitors import BusMonitor
from cocotb.drivers import BusDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure
from cocotb.clock import Clock
from systolic_array_model import systolic_array_model
from perform_im2col import perform_im2col

# Parameters : nRows = 4, nCols = 4, In_width = 8, Out_width = 32

dut_num_rows = 4
dut_num_cols = 4
dut_inwidth = 8
dut_outwidth = 32

#TODO:
#5. Randomise all the inputs
#6. Parameterise with respect to DUT systolic_rows, systolic_cols, inwidth, outwidth

## Driving all the cols with input accumulation value even if num_filters < systolic_cols
## Driving all the rows even if filter_rows*filter_cols < systolic_rows


class Weight_Driver(BusDriver):
		_signals = [
				'EN_subifc_cols_0_subifc_put_wgt_put',
				'subifc_cols_0_subifc_put_wgt_put',
				'EN_subifc_cols_1_subifc_put_wgt_put',
				'subifc_cols_1_subifc_put_wgt_put',
				'EN_subifc_cols_2_subifc_put_wgt_put',
				'subifc_cols_2_subifc_put_wgt_put',
				'EN_subifc_cols_3_subifc_put_wgt_put',
				'subifc_cols_3_subifc_put_wgt_put',
		]

		def __init__(self, dut):
				BusDriver.__init__(self, dut, None, dut.CLK)


class Weight_Transaction(object):
		def __init__(self, tb,
								EN_subifc_cols_0_subifc_put_wgt_put=0,
								subifc_cols_0_subifc_put_wgt_put=0,
								EN_subifc_cols_1_subifc_put_wgt_put=0,
								subifc_cols_1_subifc_put_wgt_put=0,
								EN_subifc_cols_2_subifc_put_wgt_put=0,
								subifc_cols_2_subifc_put_wgt_put=0,
								EN_subifc_cols_3_subifc_put_wgt_put=0,
								subifc_cols_3_subifc_put_wgt_put=0,
								 ):

				self.EN_subifc_cols_0_subifc_put_wgt_put = BinaryValue(
						EN_subifc_cols_0_subifc_put_wgt_put, tb.EN_bits, False)
				self.subifc_cols_0_subifc_put_wgt_put = BinaryValue(
						subifc_cols_0_subifc_put_wgt_put, tb.wgt_bits, False)
				self.EN_subifc_cols_1_subifc_put_wgt_put = BinaryValue(
						EN_subifc_cols_1_subifc_put_wgt_put, tb.EN_bits, False)
				self.subifc_cols_1_subifc_put_wgt_put = BinaryValue(
						subifc_cols_1_subifc_put_wgt_put, tb.wgt_bits, False)
				self.EN_subifc_cols_2_subifc_put_wgt_put = BinaryValue(
						EN_subifc_cols_2_subifc_put_wgt_put, tb.EN_bits, False)
				self.subifc_cols_2_subifc_put_wgt_put = BinaryValue(
						subifc_cols_2_subifc_put_wgt_put, tb.wgt_bits, False)
				self.EN_subifc_cols_3_subifc_put_wgt_put = BinaryValue(
						EN_subifc_cols_3_subifc_put_wgt_put, tb.EN_bits, False)
				self.subifc_cols_3_subifc_put_wgt_put = BinaryValue(
						subifc_cols_3_subifc_put_wgt_put, tb.wgt_bits, False)


class Weight_Monitor(BusMonitor):
		_signals = [
				'EN_subifc_cols_0_subifc_put_wgt_put',
				'subifc_cols_0_subifc_put_wgt_put',
				'EN_subifc_cols_1_subifc_put_wgt_put',
				'subifc_cols_1_subifc_put_wgt_put',
				'EN_subifc_cols_2_subifc_put_wgt_put',
				'subifc_cols_2_subifc_put_wgt_put',
				'EN_subifc_cols_3_subifc_put_wgt_put',
				'subifc_cols_3_subifc_put_wgt_put',
		]

		def __init__(self, dut, callback=None, event=None):
				BusMonitor.__init__(self, dut, None,
														dut.CLK, dut.RST_N,
														callback=callback,
														event=event)
				self.name = "in"

		@coroutine
		def _monitor_recv(self):
				# EN_inp_edge = RisingEdge(self.bus.EN_subifc_cols_0_subifc_put_wgt_put) or
				#              RisingEdge(self.bus.EN_subifc_cols_1_subifc_put_wgt_put) or
				#              RisingEdge(self.bus.EN_subifc_cols_2_subifc_put_wgt_put) or
				#              RisingEdge(self.bus.EN_subifc_cols_3_subifc_put_wgt_put) or

				while True:
						#
						yield RisingEdge(self.clock)
						if self.bus.EN_subifc_cols_0_subifc_put_wgt_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_cols_0_subifc_put_wgt_put', self.bus.EN_subifc_cols_0_subifc_put_wgt_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_0_subifc_put_wgt_put', hex(
										self.bus.subifc_cols_0_subifc_put_wgt_put.value.integer)))
						if self.bus.EN_subifc_cols_1_subifc_put_wgt_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_cols_1_subifc_put_wgt_put', self.bus.EN_subifc_cols_1_subifc_put_wgt_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_1_subifc_put_wgt_put', hex(
										self.bus.subifc_cols_1_subifc_put_wgt_put.value.integer)))
						if self.bus.EN_subifc_cols_2_subifc_put_wgt_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_cols_2_subifc_put_wgt_put', self.bus.EN_subifc_cols_2_subifc_put_wgt_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_2_subifc_put_wgt_put', hex(
										self.bus.subifc_cols_2_subifc_put_wgt_put.value.integer)))
						if self.bus.EN_subifc_cols_3_subifc_put_wgt_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_cols_3_subifc_put_wgt_put', self.bus.EN_subifc_cols_3_subifc_put_wgt_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_3_subifc_put_wgt_put', hex(
										self.bus.subifc_cols_3_subifc_put_wgt_put.value.integer)))

						yield RisingEdge(self.clock)


class Accum_in_Driver(BusDriver):
		_signals = [
				'EN_subifc_cols_0_subifc_put_acc_put',
				'subifc_cols_0_subifc_put_acc_put',
				'EN_subifc_cols_1_subifc_put_acc_put',
				'subifc_cols_1_subifc_put_acc_put',
				'EN_subifc_cols_2_subifc_put_acc_put',
				'subifc_cols_2_subifc_put_acc_put',
				'EN_subifc_cols_3_subifc_put_acc_put',
				'subifc_cols_3_subifc_put_acc_put',
		]

		def __init__(self, dut):
				BusDriver.__init__(self, dut, None, dut.CLK)


class Accum_in_Transaction(object):
		def __init__(self, tb,
				EN_subifc_cols_0_subifc_put_acc_put=0,
				subifc_cols_0_subifc_put_acc_put=0,
				EN_subifc_cols_1_subifc_put_acc_put=0,
				subifc_cols_1_subifc_put_acc_put=0,
				EN_subifc_cols_2_subifc_put_acc_put=0,
				subifc_cols_2_subifc_put_acc_put=0,
				EN_subifc_cols_3_subifc_put_acc_put=0,
				subifc_cols_3_subifc_put_acc_put=0,
								 ):

				self.EN_subifc_cols_0_subifc_put_acc_put = BinaryValue(
						EN_subifc_cols_0_subifc_put_acc_put, tb.EN_bits, False)
				self.subifc_cols_0_subifc_put_acc_put = BinaryValue(
						subifc_cols_0_subifc_put_acc_put, tb.output_bits, False)
				self.EN_subifc_cols_1_subifc_put_acc_put = BinaryValue(
						EN_subifc_cols_1_subifc_put_acc_put, tb.EN_bits, False)
				self.subifc_cols_1_subifc_put_acc_put = BinaryValue(
						subifc_cols_1_subifc_put_acc_put, tb.output_bits, False)
				self.EN_subifc_cols_2_subifc_put_acc_put = BinaryValue(
						EN_subifc_cols_2_subifc_put_acc_put, tb.EN_bits, False)
				self.subifc_cols_2_subifc_put_acc_put = BinaryValue(
						subifc_cols_2_subifc_put_acc_put, tb.output_bits, False)
				self.EN_subifc_cols_3_subifc_put_acc_put = BinaryValue(
						EN_subifc_cols_3_subifc_put_acc_put, tb.EN_bits, False)
				self.subifc_cols_3_subifc_put_acc_put = BinaryValue(
						subifc_cols_3_subifc_put_acc_put, tb.output_bits, False)


class Accum_in_Monitor(BusMonitor):
		_signals = [
				'EN_subifc_cols_0_subifc_put_acc_put',
				'subifc_cols_0_subifc_put_acc_put',
				'EN_subifc_cols_1_subifc_put_acc_put',
				'subifc_cols_1_subifc_put_acc_put',
				'EN_subifc_cols_2_subifc_put_acc_put',
				'subifc_cols_2_subifc_put_acc_put',
				'EN_subifc_cols_3_subifc_put_acc_put',
				'subifc_cols_3_subifc_put_acc_put',
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
						#
						yield RisingEdge(self.clock)
						#if self.bus.EN_subifc_cols_0_subifc_put_acc_put == 1:
								#print('[IN_MON] {0:<25} : {1}'.format(
								#		'EN_subifc_cols_0_subifc_put_acc_put', self.bus.EN_subifc_cols_0_subifc_put_acc_put.value.integer))
								#print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_0_subifc_put_acc_put', hex(
								#		self.bus.subifc_cols_0_subifc_put_acc_put.value.integer)))
						#if self.bus.EN_subifc_cols_1_subifc_put_acc_put == 1:
								#print('[IN_MON] {0:<25} : {1}'.format(
								#		'EN_subifc_cols_1_subifc_put_acc_put', self.bus.EN_subifc_cols_1_subifc_put_acc_put.value.integer))
								#print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_1_subifc_put_acc_put', hex(
								#		self.bus.subifc_cols_1_subifc_put_acc_put.value.integer)))
						#if self.bus.EN_subifc_cols_2_subifc_put_acc_put == 1:
								#print('[IN_MON] {0:<25} : {1}'.format(
								#		'EN_subifc_cols_2_subifc_put_acc_put', self.bus.EN_subifc_cols_2_subifc_put_acc_put.value.integer))
								#print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_2_subifc_put_acc_put', hex(
								#		self.bus.subifc_cols_2_subifc_put_acc_put.value.integer)))
						#if self.bus.EN_subifc_cols_3_subifc_put_acc_put == 1:
								#print('[IN_MON] {0:<25} : {1}'.format(
								#		'EN_subifc_cols_3_subifc_put_acc_put', self.bus.EN_subifc_cols_3_subifc_put_acc_put.value.integer))
								#print('[IN_MON] {0:<25} : {1}'.format('subifc_cols_3_subifc_put_acc_put', hex(
								#		self.bus.subifc_cols_3_subifc_put_acc_put.value.integer)))

						yield RisingEdge(self.clock)


class Ifmap_Driver(BusDriver):
		_signals = [
				'EN_subifc_rows_0_subifc_put_inp_put',
				'subifc_rows_0_subifc_put_inp_put',
				'EN_subifc_rows_1_subifc_put_inp_put',
				'subifc_rows_1_subifc_put_inp_put',
				'EN_subifc_rows_2_subifc_put_inp_put',
				'subifc_rows_2_subifc_put_inp_put',
				'EN_subifc_rows_3_subifc_put_inp_put',
				'subifc_rows_3_subifc_put_inp_put',
		]

		def __init__(self, dut):
				BusDriver.__init__(self, dut, None, dut.CLK)


class Ifmap_Transaction(object):
		def __init__(self, tb,
				EN_subifc_rows_0_subifc_put_inp_put=0,
				subifc_rows_0_subifc_put_inp_put=0,
				EN_subifc_rows_1_subifc_put_inp_put=0,
				subifc_rows_1_subifc_put_inp_put=0,
				EN_subifc_rows_2_subifc_put_inp_put=0,
				subifc_rows_2_subifc_put_inp_put=0,
				EN_subifc_rows_3_subifc_put_inp_put=0,
				subifc_rows_3_subifc_put_inp_put=0,
								 ):

				self.EN_subifc_rows_0_subifc_put_inp_put = BinaryValue(
						EN_subifc_rows_0_subifc_put_inp_put, tb.EN_bits, False)
				self.subifc_rows_0_subifc_put_inp_put = BinaryValue(
						subifc_rows_0_subifc_put_inp_put, tb.inp_bits, False)
				self.EN_subifc_rows_1_subifc_put_inp_put = BinaryValue(
						EN_subifc_rows_1_subifc_put_inp_put, tb.EN_bits, False)
				self.subifc_rows_1_subifc_put_inp_put = BinaryValue(
						subifc_rows_1_subifc_put_inp_put, tb.inp_bits, False)
				self.EN_subifc_rows_2_subifc_put_inp_put = BinaryValue(
						EN_subifc_rows_2_subifc_put_inp_put, tb.EN_bits, False)
				self.subifc_rows_2_subifc_put_inp_put = BinaryValue(
						subifc_rows_2_subifc_put_inp_put, tb.inp_bits, False)
				self.EN_subifc_rows_3_subifc_put_inp_put = BinaryValue(
						EN_subifc_rows_3_subifc_put_inp_put, tb.EN_bits, False)
				self.subifc_rows_3_subifc_put_inp_put = BinaryValue(
						subifc_rows_3_subifc_put_inp_put, tb.inp_bits, False)


class Ifmap_Monitor(BusMonitor):
		_signals = [
				'EN_subifc_rows_0_subifc_put_inp_put',
				'subifc_rows_0_subifc_put_inp_put',
				'EN_subifc_rows_1_subifc_put_inp_put',
				'subifc_rows_1_subifc_put_inp_put',
				'EN_subifc_rows_2_subifc_put_inp_put',
				'subifc_rows_2_subifc_put_inp_put',
				'EN_subifc_rows_3_subifc_put_inp_put',
				'subifc_rows_3_subifc_put_inp_put',
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
						if self.bus.EN_subifc_rows_0_subifc_put_inp_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_rows_0_subifc_put_inp_put', self.bus.EN_subifc_rows_0_subifc_put_inp_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_rows_0_subifc_put_inp_put', hex(
										self.bus.subifc_rows_0_subifc_put_inp_put.value.integer)))
						if self.bus.EN_subifc_rows_1_subifc_put_inp_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_rows_1_subifc_put_inp_put', self.bus.EN_subifc_rows_1_subifc_put_inp_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_rows_1_subifc_put_inp_put', hex(
										self.bus.subifc_rows_1_subifc_put_inp_put.value.integer)))
						if self.bus.EN_subifc_rows_2_subifc_put_inp_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_rows_2_subifc_put_inp_put', self.bus.EN_subifc_rows_2_subifc_put_inp_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_rows_2_subifc_put_inp_put', hex(
										self.bus.subifc_rows_2_subifc_put_inp_put.value.integer)))
						if self.bus.EN_subifc_rows_3_subifc_put_inp_put == 1:
								print('[IN_MON] {0:<25} : {1}'.format(
										'EN_subifc_rows_3_subifc_put_inp_put', self.bus.EN_subifc_rows_3_subifc_put_inp_put.value.integer))
								print('[IN_MON] {0:<25} : {1}'.format('subifc_rows_3_subifc_put_inp_put', hex(
										self.bus.subifc_rows_3_subifc_put_inp_put.value.integer)))

						yield RisingEdge(self.clock)



class Accum_out_EN_Driver(BusDriver):
		_signals = [
				'EN_subifc_cols_0_subifc_get_acc_get',
				'EN_subifc_cols_1_subifc_get_acc_get',
				'EN_subifc_cols_2_subifc_get_acc_get',
				'EN_subifc_cols_3_subifc_get_acc_get',
		]

		def __init__(self, dut):
				BusDriver.__init__(self, dut, None, dut.CLK)


class Accum_out_EN_Transaction(object):
		def __init__(self, tb,
								EN_subifc_cols_0_subifc_get_acc_get=0,
								EN_subifc_cols_1_subifc_get_acc_get=0,
								EN_subifc_cols_2_subifc_get_acc_get=0,
								EN_subifc_cols_3_subifc_get_acc_get=0,
								 ):

				self.EN_subifc_cols_0_subifc_get_acc_get = BinaryValue(
						EN_subifc_cols_0_subifc_get_acc_get, tb.EN_bits, False)
				self.EN_subifc_cols_1_subifc_get_acc_get = BinaryValue(
						EN_subifc_cols_1_subifc_get_acc_get, tb.EN_bits, False)
				self.EN_subifc_cols_2_subifc_get_acc_get = BinaryValue(
						EN_subifc_cols_2_subifc_get_acc_get, tb.EN_bits, False)
				self.EN_subifc_cols_3_subifc_get_acc_get = BinaryValue(
						EN_subifc_cols_3_subifc_get_acc_get, tb.EN_bits, False)


class Accum_out_Transaction(object):

		def __init__(self, tb=None,
								 RDY_subifc_cols_0_subifc_get_acc_get=0,
								 subifc_cols_0_subifc_get_acc_get=0,
								 RDY_subifc_cols_1_subifc_get_acc_get=0,
								 subifc_cols_1_subifc_get_acc_get=0,
								 RDY_subifc_cols_2_subifc_get_acc_get=0,
								 subifc_cols_2_subifc_get_acc_get=0,
								 RDY_subifc_cols_3_subifc_get_acc_get=0,
								 subifc_cols_3_subifc_get_acc_get=0,
								 ):
				"""For expected transactions, value 'None' means don't care.
				tb must be an instance of the Testbench class."""
#
				if RDY_subifc_cols_0_subifc_get_acc_get is not None and isinstance(RDY_subifc_cols_0_subifc_get_acc_get, int):
						RDY_subifc_cols_0_subifc_get_acc_get = BinaryValue(
								RDY_subifc_cols_0_subifc_get_acc_get, tb.RDY_bits, False)
				if subifc_cols_0_subifc_get_acc_get is not None and isinstance(subifc_cols_0_subifc_get_acc_get, int):
						subifc_cols_0_subifc_get_acc_get = BinaryValue(
								subifc_cols_0_subifc_get_acc_get, tb.output_bits, False)
				if RDY_subifc_cols_1_subifc_get_acc_get is not None and isinstance(RDY_subifc_cols_1_subifc_get_acc_get, int):
						RDY_subifc_cols_1_subifc_get_acc_get = BinaryValue(
								RDY_subifc_cols_1_subifc_get_acc_get, tb.RDY_bits, False)
				if subifc_cols_1_subifc_get_acc_get is not None and isinstance(subifc_cols_1_subifc_get_acc_get, int):
						subifc_cols_1_subifc_get_acc_get = BinaryValue(
								subifc_cols_1_subifc_get_acc_get, tb.output_bits, False)
				if RDY_subifc_cols_2_subifc_get_acc_get is not None and isinstance(RDY_subifc_cols_2_subifc_get_acc_get, int):
						RDY_subifc_cols_2_subifc_get_acc_get = BinaryValue(
								RDY_subifc_cols_2_subifc_get_acc_get, tb.RDY_bits, False)
				if subifc_cols_2_subifc_get_acc_get is not None and isinstance(subifc_cols_2_subifc_get_acc_get, int):
						subifc_cols_2_subifc_get_acc_get = BinaryValue(
								subifc_cols_2_subifc_get_acc_get, tb.output_bits, False)
				if RDY_subifc_cols_3_subifc_get_acc_get is not None and isinstance(RDY_subifc_cols_3_subifc_get_acc_get, int):
						RDY_subifc_cols_3_subifc_get_acc_get = BinaryValue(
								RDY_subifc_cols_3_subifc_get_acc_get, tb.RDY_bits, False)
				if subifc_cols_3_subifc_get_acc_get is not None and isinstance(subifc_cols_3_subifc_get_acc_get, int):
						subifc_cols_3_subifc_get_acc_get = BinaryValue(
								subifc_cols_3_subifc_get_acc_get, tb.output_bits, False)
#
				self.value = (
						RDY_subifc_cols_0_subifc_get_acc_get,
						subifc_cols_0_subifc_get_acc_get,
						RDY_subifc_cols_1_subifc_get_acc_get,
						subifc_cols_1_subifc_get_acc_get,
						RDY_subifc_cols_2_subifc_get_acc_get,
						subifc_cols_2_subifc_get_acc_get,
						RDY_subifc_cols_3_subifc_get_acc_get,
						subifc_cols_3_subifc_get_acc_get,
				)

class Accum_out_Monitor(BusMonitor):
		"""Observes signals of DUT"""
		_signals = [
				#
								'RDY_subifc_cols_0_subifc_get_acc_get',
								'subifc_cols_0_subifc_get_acc_get',
								'RDY_subifc_cols_1_subifc_get_acc_get',
								'subifc_cols_1_subifc_get_acc_get',
								'RDY_subifc_cols_2_subifc_get_acc_get',
								'subifc_cols_2_subifc_get_acc_get',
								'RDY_subifc_cols_3_subifc_get_acc_get',
								'subifc_cols_3_subifc_get_acc_get',
								'EN_subifc_cols_0_subifc_get_acc_get',
								'EN_subifc_cols_1_subifc_get_acc_get',
								'EN_subifc_cols_2_subifc_get_acc_get',
								'EN_subifc_cols_3_subifc_get_acc_get',

							]

		def __init__(self, dut, tb, callback=None, event=None):
				BusMonitor.__init__(self, dut, None, dut.CLK, dut.RST_N,
														callback=callback, event=event)
				self.name = "out"
				self.tb = tb

		@coroutine
		def _monitor_recv(self):
				while True:
						yield RisingEdge(self.clock)
						if self.bus.RDY_subifc_cols_0_subifc_get_acc_get.value == 1 and self.bus.EN_subifc_cols_0_subifc_get_acc_get.value == 1:
								print('[DUT_MON] {0:<25} : {1}'.format(
										'RDY_subifc_cols_0_subifc_get_acc_get ', self.bus.RDY_subifc_cols_0_subifc_get_acc_get.value.integer))
								print('[DUT_MON] {0:<25} : {1}'.format('subifc_cols_0_subifc_get_acc_get ', hex(
										self.bus.subifc_cols_0_subifc_get_acc_get.value.integer)))
						if self.bus.RDY_subifc_cols_1_subifc_get_acc_get.value == 1 and self.bus.EN_subifc_cols_1_subifc_get_acc_get.value == 1:
								print('[DUT_MON] {0:<25} : {1}'.format(
										'RDY_subifc_cols_1_subifc_get_acc_get ', self.bus.RDY_subifc_cols_1_subifc_get_acc_get.value.integer))
								print('[DUT_MON] {0:<25} : {1}'.format('subifc_cols_1_subifc_get_acc_get ', hex(
										self.bus.subifc_cols_1_subifc_get_acc_get.value.integer)))
						if self.bus.RDY_subifc_cols_2_subifc_get_acc_get.value == 1 and self.bus.EN_subifc_cols_2_subifc_get_acc_get.value == 1:
								print('[DUT_MON] {0:<25} : {1}'.format(
										'RDY_subifc_cols_2_subifc_get_acc_get ', self.bus.RDY_subifc_cols_2_subifc_get_acc_get.value.integer))
								print('[DUT_MON] {0:<25} : {1}'.format('subifc_cols_2_subifc_get_acc_get ', hex(
										self.bus.subifc_cols_2_subifc_get_acc_get.value.integer)))
						if self.bus.RDY_subifc_cols_3_subifc_get_acc_get.value == 1 and self.bus.EN_subifc_cols_3_subifc_get_acc_get.value == 1:
								print('[DUT_MON] {0:<25} : {1}'.format(
										'RDY_subifc_cols_3_subifc_get_acc_get ', self.bus.RDY_subifc_cols_3_subifc_get_acc_get.value.integer))
								print('[DUT_MON] {0:<25} : {1}'.format('subifc_cols_3_subifc_get_acc_get ', hex(
										self.bus.subifc_cols_3_subifc_get_acc_get.value.integer)))

						vec = (
						self.bus.RDY_subifc_cols_0_subifc_get_acc_get.value,
						hex(self.bus.subifc_cols_0_subifc_get_acc_get.value),
						self.bus.RDY_subifc_cols_1_subifc_get_acc_get.value,
						hex(self.bus.subifc_cols_1_subifc_get_acc_get.value),
						self.bus.RDY_subifc_cols_2_subifc_get_acc_get.value,
						hex(self.bus.subifc_cols_2_subifc_get_acc_get.value),
						self.bus.RDY_subifc_cols_3_subifc_get_acc_get.value,
						hex(self.bus.subifc_cols_3_subifc_get_acc_get.value)
						)
						self._recv(vec)

						# yield RisingEdge(self.clock)


class DUTScoreboard(Scoreboard):
		def compare(self, num_filters, matrix_rows, got, exp, log, **_):
				print("Got Values to Scoreboard ")
				print(got)
				print(exp)
				for i in range(num_filters):
						for j in range(matrix_rows):
								if(got[i][j] != hex(exp[0][j][i])):
										print("Value  mismatched ")
										print(i)
										print(j)
										exit(1)
								else:
										print("Value matched ")
										print(i)
										print(j)


class TestBench(object):
		"""Verification Test Bench"""

		def __init__(self, dut):
				self.dut = dut
				self.stopped = False

				self.EN_bits = 1
				self.RDY_bits = 1
				self.wgt_bits = 16
				self.inp_bits = 8
				self.output_bits = 32

				self.num_filters = 1
				self.matrix_rows = 1

				self.weight_driver = Weight_Driver(dut)
				self.weight_monitor = Weight_Monitor(dut)
				self.ifmap_driver = Ifmap_Driver(dut)
				self.ifmap_monitor = Ifmap_Monitor(dut)
				self.accum_in_driver = Accum_in_Driver(dut)
				self.accum_in_monitor = Accum_in_Monitor(dut)

				self.accum_out_driver = Accum_out_EN_Driver(dut)

				init_val = Accum_out_Transaction(self)
				self.accum_out_monitor = Accum_out_Monitor(
						dut, self, callback=self.accum_dut_output)


				self.expected_output = []
				self.dut_output = []

				self.scoreboard = DUTScoreboard(dut)
				#self.scoreboard.add_interface(self.final_output, tuple(self.expected_output))

		def model(self, input_matrix, filter_matrix):
			mult_output = systolic_array_model(input_matrix, filter_matrix)
			print("model output")
			print(mult_output)
			self.expected_output.append(mult_output)

		def accum_dut_output(self, transaction):
				(
				RDY_col_0,
				col_0_val,
				RDY_col_1,
				col_1_val,
				RDY_col_2,
				col_2_val,
				RDY_col_3,
				col_3_val,
				) = transaction

				if(RDY_col_0 == 1):
						print('[DUT_OUT] {0:<25} : {1}'.format('col_0_val ', col_0_val))
						self.dut_output[0].append(col_0_val)
				if(RDY_col_1 == 1 and self.num_filters > 1):
						print('[DUT_OUT] {0:<25} : {1}'.format('col_1_val ', col_1_val))
						self.dut_output[1].append(col_1_val)
				if(RDY_col_2 == 1 and self.num_filters > 2):
						print('[DUT_OUT] {0:<25} : {1}'.format('col_2_val ', col_2_val))
						self.dut_output[2].append(col_2_val)
				if(RDY_col_3 == 1 and self.num_filters > 3):
						print('[DUT_OUT] {0:<25} : {1}'.format('col_3_val ', col_3_val))
						self.dut_output[3].append(col_3_val)



		def send_output_to_scoreboard(self):
				print("output comparison")
				self.scoreboard.compare(self.num_filters,self.matrix_rows,self.dut_output,self.expected_output,self.scoreboard.log)
				self.expected_output = []
				self.dut_output.clear

		def stop(self):
				"""
				Stop generation of expected output transactions.
				One more clock cycle must be executed afterwards, so that, output of
				D-FF can be checked.
				"""
				self.stopped = True


# Functions to generate and convert inputs

def counter_generate(systolic_rows, systolic_cols):
		output_vector = np.zeros((systolic_rows, systolic_cols), dtype=int)
		for i in range(systolic_rows):
				for j in range(systolic_cols):
						output_vector[i, j] = systolic_rows - i
		return output_vector


def weight_generate(prev_weight_generated, filter_in, filter_index):
		f_row, f_col = filter_in.shape
		for i in range(f_row):
				for j in range(f_col):
						prev_weight_generated[i*f_col+j, filter_index] = filter_in[i, j]
		return prev_weight_generated

@cocotb.coroutine
def send_weights_to_systolic(tb, dut, weight_matrix, systolic_rows):

		EN_subifc_cols_0_subifc_put_wgt_put = 0
		subifc_cols_0_subifc_put_wgt_put = 0
		EN_subifc_cols_1_subifc_put_wgt_put = 0
		subifc_cols_1_subifc_put_wgt_put = 0
		EN_subifc_cols_2_subifc_put_wgt_put = 0
		subifc_cols_2_subifc_put_wgt_put = 0
		EN_subifc_cols_3_subifc_put_wgt_put = 0
		subifc_cols_3_subifc_put_wgt_put = 0

		count_0 = 0
		count_1 = 0
		count_2 = 0
		count_3 = 0

		while(count_0 <= 4 or count_1 <= 4 or count_2 <= 4 or count_3 <= 4):
			if(dut.RDY_subifc_cols_0_subifc_put_wgt_put == 1 and count_0 < 4):
				subifc_cols_0_subifc_put_wgt_put = weight_matrix.item(
					(systolic_rows-1-count_0, 0))
				count_0 = count_0 + 1
				EN_subifc_cols_0_subifc_put_wgt_put = 1
			else:
				EN_subifc_cols_0_subifc_put_wgt_put = 0
				if(count_0 == 4):
					count_0 = count_0 + 1
			if(dut.RDY_subifc_cols_1_subifc_put_wgt_put == 1 and count_1 < 4):
				subifc_cols_1_subifc_put_wgt_put = weight_matrix.item(
					(systolic_rows-1-count_1, 1))
				count_1 = count_1 + 1
				EN_subifc_cols_1_subifc_put_wgt_put = 1
			else:
				EN_subifc_cols_1_subifc_put_wgt_put = 0
				if(count_1 == 4):
					count_1 = count_1 + 1

			if(dut.RDY_subifc_cols_2_subifc_put_wgt_put == 1 and count_2 < 4):
				subifc_cols_2_subifc_put_wgt_put = weight_matrix.item(
					(systolic_rows-1-count_2, 2))
				count_2 = count_2 + 1
				EN_subifc_cols_2_subifc_put_wgt_put = 1
			else:
				EN_subifc_cols_2_subifc_put_wgt_put = 0
				if(count_2 == 4):
					count_2 = count_2 + 1

			if(dut.RDY_subifc_cols_3_subifc_put_wgt_put == 1 and count_3 < 4):
				subifc_cols_3_subifc_put_wgt_put = weight_matrix.item(
					(systolic_rows-1-count_3, 3))
				count_3 = count_3 + 1
				EN_subifc_cols_3_subifc_put_wgt_put = 1
			else:
				EN_subifc_cols_3_subifc_put_wgt_put = 0
				if(count_3 == 4):
					count_3 = count_3 + 1

			yield tb.weight_driver.send(Weight_Transaction(tb,
															 EN_subifc_cols_0_subifc_put_wgt_put,
															 subifc_cols_0_subifc_put_wgt_put,
															 EN_subifc_cols_1_subifc_put_wgt_put,
															 subifc_cols_1_subifc_put_wgt_put,
															 EN_subifc_cols_2_subifc_put_wgt_put,
															 subifc_cols_2_subifc_put_wgt_put,
															 EN_subifc_cols_3_subifc_put_wgt_put,
															 subifc_cols_3_subifc_put_wgt_put))

## Should modify after the bug fix
@cocotb.coroutine
def send_accum_in_to_systolic(tb, dut, acc_in_matrix, num_filters):

		EN_subifc_cols_0_subifc_put_acc_put = 0
		subifc_cols_0_subifc_put_acc_put = 0
		EN_subifc_cols_1_subifc_put_acc_put = 0
		subifc_cols_1_subifc_put_acc_put = 0
		EN_subifc_cols_2_subifc_put_acc_put = 0
		subifc_cols_2_subifc_put_acc_put = 0
		EN_subifc_cols_3_subifc_put_acc_put = 0
		subifc_cols_3_subifc_put_acc_put = 0

		##TODO: This condition will be added if the inputs are dequeued from the last columns at the compute module
		#if(num_filters > 0):
		EN_subifc_cols_0_subifc_put_acc_put = 1
		subifc_cols_0_subifc_put_acc_put = 0
		#if(num_filters > 1):
		EN_subifc_cols_1_subifc_put_acc_put = 1
		subifc_cols_1_subifc_put_acc_put = 0
		#if(num_filters > 2):
		EN_subifc_cols_2_subifc_put_acc_put = 1
		subifc_cols_2_subifc_put_acc_put = 0
		#if(num_filters > 3):
		EN_subifc_cols_3_subifc_put_acc_put = 1
		subifc_cols_3_subifc_put_acc_put = 0

		yield tb.accum_in_driver.send(Accum_in_Transaction(tb,
															EN_subifc_cols_0_subifc_put_acc_put,
															subifc_cols_0_subifc_put_acc_put,
															EN_subifc_cols_1_subifc_put_acc_put,
															subifc_cols_1_subifc_put_acc_put,
															EN_subifc_cols_2_subifc_put_acc_put,
															subifc_cols_2_subifc_put_acc_put,
															EN_subifc_cols_3_subifc_put_acc_put,
															subifc_cols_3_subifc_put_acc_put))


@cocotb.coroutine
def send_ifmap_to_systolic(tb, dut, systolic_matrix, matrix_rows, matrix_cols):

		EN_subifc_rows_0_subifc_put_inp_put = 0
		subifc_rows_0_subifc_put_inp_put = 0
		EN_subifc_rows_1_subifc_put_inp_put = 0
		subifc_rows_1_subifc_put_inp_put = 0
		EN_subifc_rows_2_subifc_put_inp_put = 0
		subifc_rows_2_subifc_put_inp_put = 0
		EN_subifc_rows_3_subifc_put_inp_put = 0
		subifc_rows_3_subifc_put_inp_put = 0

		count_0 = 0
		count_1 = 0
		count_2 = 0
		count_3 = 0
		count_delay_0 = False
		count_delay_1 = False
		count_delay_2 = False
		count_delay_3 = False
		##TODO : Will be removed if unused input rows are driven at compute module
		#if(matrix_cols == 1):
		#	count_1 = matrix_rows + 1
		#	count_2 = matrix_rows + 1
		#	count_3 = matrix_rows + 1
		#elif(matrix_cols == 2):
		#	count_2 = matrix_rows + 1
		#	count_3 = matrix_rows + 1
		#elif(matrix_cols == 3):
		#	count_3 = matrix_rows + 1

		yield Timer(2)
		while(count_0 <= matrix_rows or count_1 <= matrix_rows or count_2 <= matrix_rows or count_3 <= matrix_rows):
				if (count_0 < matrix_rows and count_delay_0 == False and dut.RDY_subifc_rows_0_subifc_put_inp_put == 1):
						EN_subifc_rows_0_subifc_put_inp_put = 0x1
						subifc_rows_0_subifc_put_inp_put = systolic_matrix.item(
								(count_0, 0))
						count_delay_0 = random.choice([False,True])
				else:
						EN_subifc_rows_0_subifc_put_inp_put = 0x0
						if(count_0 == matrix_rows):
							count_0 = count_0 + 1
						count_delay_0 = random.choice([False,True])
				if (count_1 < matrix_rows and count_delay_1 == False and dut.RDY_subifc_rows_1_subifc_put_inp_put == 1):
						EN_subifc_rows_1_subifc_put_inp_put = 0x1
						subifc_rows_1_subifc_put_inp_put = systolic_matrix.item(
								(count_1, 1))
						count_delay_1 = random.choice([True,False])
				else:
						EN_subifc_rows_1_subifc_put_inp_put = 0x0
						if(count_1 == matrix_rows):
							count_1 = count_1 + 1
						count_delay_1 = random.choice([True,False])
				if (count_2 < matrix_rows and count_delay_2 == False and dut.RDY_subifc_rows_2_subifc_put_inp_put == 1):
						EN_subifc_rows_2_subifc_put_inp_put = 0x1
						subifc_rows_2_subifc_put_inp_put = systolic_matrix.item(
								(count_2, 2))
						count_delay_2 = random.choice([True,False])
				else:
						EN_subifc_rows_2_subifc_put_inp_put = 0x0
						if(count_2 == matrix_rows):
							count_2 = count_2 + 1
						count_delay_2 = random.choice([True,False])
				if (count_3 < matrix_rows and count_delay_3 == False and dut.RDY_subifc_rows_3_subifc_put_inp_put == 1):
						EN_subifc_rows_3_subifc_put_inp_put = 0x1
						subifc_rows_3_subifc_put_inp_put = systolic_matrix.item(
								(count_3, 3))
						count_delay_3 = random.choice([True,False])
				else:
						EN_subifc_rows_3_subifc_put_inp_put = 0x0
						if(count_3 == matrix_rows):
							count_3 = count_3 + 1
						count_delay_3 = random.choice([True,False])

				if(EN_subifc_rows_0_subifc_put_inp_put == 1):
					count_0 = count_0 + 1
				if(EN_subifc_rows_1_subifc_put_inp_put == 1):
					count_1 = count_1 + 1
				if(EN_subifc_rows_2_subifc_put_inp_put == 1):
					count_2 = count_2 + 1
				if(EN_subifc_rows_3_subifc_put_inp_put == 1):
					count_3 = count_3 + 1
				
				#print('[INP_DRV] {0:<25} : {1}'.format('RDY_subifc_rows_0_subifc_put_inp_put', dut.RDY_subifc_rows_0_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('EN_subifc_rows_0_subifc_put_inp_put ', EN_subifc_rows_0_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('subifc_rows_0_subifc_put_inp_put ', subifc_rows_0_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('RDY_subifc_rows_1_subifc_put_inp_put', dut.RDY_subifc_rows_1_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('EN_subifc_rows_1_subifc_put_inp_put ', EN_subifc_rows_1_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('subifc_rows_1_subifc_put_inp_put ', subifc_rows_1_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('RDY_subifc_rows_2_subifc_put_inp_put', dut.RDY_subifc_rows_2_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('EN_subifc_rows_2_subifc_put_inp_put ', EN_subifc_rows_2_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('subifc_rows_2_subifc_put_inp_put ', subifc_rows_2_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('RDY_subifc_rows_3_subifc_put_inp_put', dut.RDY_subifc_rows_3_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('EN_subifc_rows_3_subifc_put_inp_put ', EN_subifc_rows_3_subifc_put_inp_put))
				#print('[INP_DRV] {0:<25} : {1}'.format('subifc_rows_3_subifc_put_inp_put ', subifc_rows_3_subifc_put_inp_put))
#
				#print('[INP_DRV] {0:<25} : {1}'.format('count_0 ', count_0))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_1 ', count_1))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_2 ', count_2))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_3 ', count_3))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_delay_0 ', count_delay_0))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_delay_1 ', count_delay_1))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_delay_2 ', count_delay_2))
				#print('[INP_DRV] {0:<25} : {1}'.format('count_delay_3 ', count_delay_3))


				yield tb.ifmap_driver.send(Ifmap_Transaction(tb,
																EN_subifc_rows_0_subifc_put_inp_put,
																subifc_rows_0_subifc_put_inp_put,
																EN_subifc_rows_1_subifc_put_inp_put,
																subifc_rows_1_subifc_put_inp_put,
																EN_subifc_rows_2_subifc_put_inp_put,
																subifc_rows_2_subifc_put_inp_put,
																EN_subifc_rows_3_subifc_put_inp_put,
																subifc_rows_3_subifc_put_inp_put),sync=False)

				yield Timer(2)




		EN_subifc_rows_0_subifc_put_inp_put = 0
		EN_subifc_rows_1_subifc_put_inp_put = 0
		EN_subifc_rows_2_subifc_put_inp_put = 0
		EN_subifc_rows_3_subifc_put_inp_put = 0
		yield tb.ifmap_driver.send(Ifmap_Transaction(tb,
																EN_subifc_rows_0_subifc_put_inp_put,
																subifc_rows_0_subifc_put_inp_put,
																EN_subifc_rows_1_subifc_put_inp_put,
																subifc_rows_1_subifc_put_inp_put,
																EN_subifc_rows_2_subifc_put_inp_put,
																subifc_rows_2_subifc_put_inp_put,
																EN_subifc_rows_3_subifc_put_inp_put,
																subifc_rows_3_subifc_put_inp_put))


@cocotb.coroutine
def clock_gen(signal):
		while True:
				signal <= 0
				yield Timer(1)
				signal <= 1
				yield Timer(1)


@cocotb.coroutine
def send_accum_out_en(tb,dut):
	while True:
		EN_0 = 0
		EN_1 = 0
		EN_2 = 0
		EN_3 = 0
		if(dut.RDY_subifc_cols_0_subifc_get_acc_get == 1):
			EN_0 = 1
		if(dut.RDY_subifc_cols_1_subifc_get_acc_get == 1):
			EN_1 = 1
		if(dut.RDY_subifc_cols_2_subifc_get_acc_get == 1):
			EN_2 = 1
		if(dut.RDY_subifc_cols_3_subifc_get_acc_get == 1):
			EN_3 = 1
		dut.EN_subifc_cols_0_subifc_get_acc_get <= EN_0
		dut.EN_subifc_cols_1_subifc_get_acc_get <= EN_1
		dut.EN_subifc_cols_2_subifc_get_acc_get <= EN_2
		dut.EN_subifc_cols_3_subifc_get_acc_get <= EN_3
		yield Timer(1)


@cocotb.test()
def run_test(dut):
		cocotb.fork(clock_gen(dut.CLK))
		tb = TestBench(dut)
		dut.RST_N <= 0
		yield Timer(2)
		dut.RST_N <= 1
		cocotb.fork(send_accum_out_en(tb,dut))

		systolic_rows = 4
		systolic_cols = 4
		inwidth = 8
		outwidth = 32

		for n in range(2):
				ifmap_rows = random.choice([3,4,5,6,7,8,9,10])
				ifmap_cols = random.choice([3,4,5,6,7,8,9,10])
				#ifmap_rows = 4
				#ifmap_cols = 4
				num_filters = random.choice([1,2,3,4])
				#num_filters = 4
				filter_rows = random.choice([1,2])
				filter_cols = random.choice([1,2])
				#filter_rows = 1
				#filter_cols = 2

				matrix_rows = (ifmap_rows - filter_rows + 1) * \
											 (ifmap_cols - filter_cols + 1)
				matrix_cols = filter_rows*filter_cols

				tb.dut_output = [[0 for i in range(0)] for j in range(num_filters)]
				tb.num_filters = num_filters
				tb.matrix_rows = matrix_rows
				#filters = np.ones((num_filters,filter_rows,filter_cols))
				filters = np.zeros((num_filters,filter_rows,filter_cols))
				for f_iter in range(num_filters):
				    filters[f_iter] = np.random.randint(0, high=2**(inwidth-2), size=(filter_rows, filter_cols))
				weight_to_systolic = np.zeros((systolic_rows, systolic_cols), dtype=int)
				for i in range(num_filters):
						weight_to_systolic = weight_generate(weight_to_systolic, filters[i], i)
				weight_to_model = np.zeros((matrix_cols, num_filters), dtype=int)
				for i in range(matrix_cols):
						for j in range(num_filters):
								weight_to_model[i][j] = weight_to_systolic[i][j]

				counter_to_systolic = counter_generate(systolic_rows, systolic_cols)
				weight_to_systolic = (weight_to_systolic << (8)) | counter_to_systolic

				print("filter rows cols ",num_filters,filter_rows,filter_cols)
				print("weight to model")
				print(weight_to_model)
				print("Counter values")
				print(counter_to_systolic)
				print("Weight to systolic")
				print(weight_to_systolic)

				yield send_weights_to_systolic(tb,dut,weight_to_systolic,systolic_rows)

				acc_in_value = np.zeros((1, systolic_cols), dtype='int')
				for i in range(num_filters):
						acc_in_value[0][i] = random.randint(0,2**(inwidth-2)-1)
				# acc_in_value = np.random.randint(0,high=2**(inwidth-2),size=(1,num_filters)) 
				yield send_accum_in_to_systolic(tb, dut, acc_in_value, num_filters) ## TODO : Change to outwidth

				# input_array = np.random.randint(0,high=2**(inwidth-2),size=(ifmap_rows,ifmap_cols))
				input_array = np.zeros((ifmap_rows, ifmap_cols), dtype=int)
				for i in range(ifmap_rows):
						for j in range(ifmap_cols):
								input_array[i][j] = i*5 + j
				im2col_output = perform_im2col(input_array, (filter_rows, filter_cols))
				input_to_model = np.transpose(im2col_output)
				input_to_systolic = np.zeros((matrix_rows, systolic_rows), dtype=int)
				#input_to_systolic = np.zeros((matrix_rows, matric_cols), dtype=int)
				for i in range(matrix_rows):
						for j in range(matrix_cols):
								input_to_systolic[i][j] = input_to_model[i][j]
				print("Input Array")
				print(input_array)
				print("Input to model")
				print(input_to_model)
				print("Input to systolic")
				print(input_to_systolic)

				tb.model(input_to_model, weight_to_model)

				yield send_ifmap_to_systolic(tb, dut, input_to_systolic, matrix_rows, matrix_cols)

				for inp_delay in range(systolic_rows):
					yield RisingEdge(dut.CLK)
				print(tb.dut_output)
				tb.send_output_to_scoreboard()
				yield RisingEdge(dut.CLK)	
		tb.stop()
		yield RisingEdge(dut.CLK)
