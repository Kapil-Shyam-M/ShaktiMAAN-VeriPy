import cocotb
import logging
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, Edge
from cocotb.result import TestFailure
from cocotb.binary import BinaryValue
from systolic_array_model import systolic_array_model
import random
import numpy as np

CLK_PERIOD = 0.01


@cocotb.coroutine
def reset(dut):
    dut.RST_N <= 0
    yield Timer(CLK_PERIOD * 10, units='ns')
    dut.RST_N <= 1
    yield Timer(CLK_PERIOD * 10, units='ns')
    yield RisingEdge(dut.CLK)


@cocotb.coroutine
def output_from_systolic(cfifo0_out_rdy, cfifo1_out_rdy, cfifo2_out_rdy, cfifo3_out_rdy, cfifo4_out_rdy, cfifo5_out_rdy, cfifo0_out, cfifo1_out, cfifo2_out, cfifo3_out, cfifo4_out, cfifo5_out, num_input_rows, num_cols, bitwidth):
    systolic_output = np.zeros((num_input_rows, num_cols), dtype='int')
    cfifo_counter = np.zeros((1, num_cols), dtype='int')
    while(1):
        yield Timer(1*CLK_PERIOD, units='ns')
        if (BinaryValue(int(cfifo0_out_rdy), 1, False) == 1):
            temp = cfifo_counter[0][0]
            systolic_output[temp][0] = BinaryValue(
                int(cfifo0_out), 2*bitwidth, False).signed_integer
            cfifo_counter[0][0] = cfifo_counter[0][0] + 1
        if (BinaryValue(int(cfifo1_out_rdy), 1, False) == 1):
            temp = cfifo_counter[0][1]
            systolic_output[temp][1] = BinaryValue(
                int(cfifo1_out), 2*bitwidth, False).signed_integer
            cfifo_counter[0][1] = cfifo_counter[0][1] + 1
        if (BinaryValue(int(cfifo2_out_rdy), 1, False) == 1):
            temp = cfifo_counter[0][2]
            systolic_output[temp][2] = BinaryValue(
                int(cfifo2_out), 2*bitwidth, False).signed_integer
            cfifo_counter[0][2] = cfifo_counter[0][2] + 1
        if (BinaryValue(int(cfifo3_out_rdy), 1, False) == 1):
            temp = cfifo_counter[0][3]
            systolic_output[temp][3] = BinaryValue(
                int(cfifo3_out), 2*bitwidth, False).signed_integer
            cfifo_counter[0][3] = cfifo_counter[0][3] + 1
        if (BinaryValue(int(cfifo4_out_rdy), 1, False) == 1):
            temp = cfifo_counter[0][4]
            systolic_output[temp][4] = BinaryValue(
                int(cfifo4_out), 2*bitwidth, False).signed_integer
            cfifo_counter[0][4] = cfifo_counter[0][4] + 1
        if (BinaryValue(int(cfifo5_out_rdy), 1, False) == 1):
            temp = cfifo_counter[0][5]
            systolic_output[temp][5] = BinaryValue(
                int(cfifo5_out), 2*bitwidth, False).signed_integer
            cfifo_counter[0][5] = cfifo_counter[0][5] + 1
        if(cfifo_counter[0][5] == num_input_rows):
            break
    return systolic_output


def im2col_sliding(image, block_size, skip=1):
    rows, cols = image.shape
    horz_blocks = cols - block_size[1] + 1
    vert_blocks = rows - block_size[0] + 1

    output_vectors = np.zeros(
        (block_size[0] * block_size[1], horz_blocks * vert_blocks), dtype=int)
    itr = 0
    for v_b in range(vert_blocks):
        for h_b in range(horz_blocks):
            output_vectors[:, itr] = image[v_b: v_b +
                                           block_size[0], h_b: h_b + block_size[1]].ravel()
            itr += 1
    return output_vectors[:, ::skip]


def weight_generate(prev_weight_generated, filter_in, filter_index):
    f_row, f_col = filter_in.shape
    for i in range(f_row):
        for j in range(f_col):
            prev_weight_generated[i*f_col+j, filter_index] = filter_in[i, j]
    return prev_weight_generated


def counter_generate(systolic_rows, systolic_cols):
    output_vector = np.zeros((systolic_rows, systolic_cols), dtype=int)
    for i in range(systolic_rows):
        for j in range(systolic_cols):
            output_vector[i, j] = systolic_rows - i
    return output_vector


@cocotb.test()
def systolic_basic_test(dut):
    cocotb.fork(Clock(dut.CLK, period=CLK_PERIOD, units='ns').start())
    yield reset(dut)
    yield Timer(2*CLK_PERIOD, units='ns')

    num_systolic_rows = 9
    num_systolic_cols = 6
    bitwidth = 16

    for test_iter in range(10):
        ifmap_rows = random.randint(1,256)
        ifmap_cols = random.randint(1,256)
        num_filter_rows = random.randint(1,3)
        num_filter_cols = random.randint(1,3)
        num_filters = random.randint(1,num_systolic_cols)

        cfifo_input_acc = np.zeros((1, num_systolic_cols), dtype='int')
        cfifo_input_acc[0][0] = random.randint(-2**(bitwidth-2),2**(bitwidth-2)-1)
        cfifo_input_acc[0][1] = random.randint(-2**(bitwidth-2),2**(bitwidth-2)-1)
        cfifo_input_acc[0][2] = random.randint(-2**(bitwidth-2),2**(bitwidth-2)-1)
        cfifo_input_acc[0][3] = random.randint(-2**(bitwidth-2),2**(bitwidth-2)-1)
        cfifo_input_acc[0][4] = random.randint(-2**(bitwidth-2),2**(bitwidth-2)-1)
        cfifo_input_acc[0][5] = random.randint(-2**(bitwidth-2),2**(bitwidth-2)-1)

#       cfifo_input_acc[0][0] = 0
#       cfifo_input_acc[0][1] = 0
#       cfifo_input_acc[0][2] = 0
#       cfifo_input_acc[0][3] = 0
#       cfifo_input_acc[0][4] = 0
#       cfifo_input_acc[0][5] = 0

        input_array = np.random.randint(-2**(bitwidth-2),high=2**(bitwidth-2),size=(ifmap_rows,ifmap_cols))

#       input_array = np.zeros((ifmap_rows, ifmap_cols), dtype=int)
#       for i in range(ifmap_rows):
#           for j in range(ifmap_cols):
#               input_array[i][j] = j

        filters = np.zeros((num_filters,num_filter_rows,num_filter_cols))
        for f_iter in range(num_filters):
            filters[f_iter] = np.random.randint(-2**(bitwidth-2), high=2**(bitwidth-2), size=(num_filter_rows, num_filter_cols))

#       for f_iter in range(num_filters):
#           filters[f_iter] = np.random.randint(-1, high=2, size=(num_filter_rows, num_filter_cols))

        num_input_rows = (ifmap_rows - num_filter_rows + 1) * \
            (ifmap_cols - num_filter_cols + 1)
        num_input_cols = num_filter_rows*num_filter_cols

        """ row buffer input """
        temp_im2col_output = im2col_sliding(
            input_array, (num_filter_rows, num_filter_cols))
        input_to_model = np.transpose(temp_im2col_output)

        temp_input_to_systolic = np.zeros(
            (num_input_rows, num_systolic_rows), dtype=int)
        for i in range(num_input_rows):
            for j in range(num_input_cols):
                temp_input_to_systolic[i][j] = input_to_model[i][j]

        input_to_systolic = ((1 << bitwidth) | (
            temp_input_to_systolic & (2**bitwidth-1)))

        """ col buffer input """
        temp_weight_to_model = np.zeros(
            (num_systolic_rows, num_systolic_cols), dtype=int)
        for i in range(num_filters):
            temp_weight_to_model = weight_generate(
                temp_weight_to_model, filters[i], i)
        weight_to_model = np.zeros((num_input_cols, num_filters), dtype=int)
        for i in range(num_input_cols):
            for j in range(num_filters):
                weight_to_model[i][j] = temp_weight_to_model[i][j]
        weight_to_systolic = temp_weight_to_model

        counter_to_model = counter_generate(
            num_systolic_rows, num_systolic_cols)

        input_weight_shift = 10+2*bitwidth
        input_weight_valid_shift = input_weight_shift + bitwidth
        filter_to_systolic = (((((1 << input_weight_valid_shift) | ((weight_to_systolic & (2**bitwidth-1)) << (10+2*bitwidth))) | (0 << 10)) | (
            (counter_to_model & 255) << 2)) | (0 << 0))

        """ Put weights onto PE array """
        dut.EN_cfifo_0_send_colbuf_value = 0x1
        dut.EN_cfifo_1_send_colbuf_value = 0x1
        dut.EN_cfifo_2_send_colbuf_value = 0x1
        dut.EN_cfifo_3_send_colbuf_value = 0x1
        dut.EN_cfifo_4_send_colbuf_value = 0x1
        dut.EN_cfifo_5_send_colbuf_value = 0x1
        for w_iter in range(num_systolic_rows):
            temp_clk = random.randint(1,20)
            yield Timer(temp_clk*CLK_PERIOD, units='ns')
            dut.cfifo_0_send_colbuf_value_value = filter_to_systolic.item(
                (num_systolic_rows-1-w_iter, 0))
            dut.cfifo_1_send_colbuf_value_value = filter_to_systolic.item(
                (num_systolic_rows-1-w_iter, 1))
            dut.cfifo_2_send_colbuf_value_value = filter_to_systolic.item(
                (num_systolic_rows-1-w_iter, 2))
            dut.cfifo_3_send_colbuf_value_value = filter_to_systolic.item(
                (num_systolic_rows-1-w_iter, 3))
            dut.cfifo_4_send_colbuf_value_value = filter_to_systolic.item(
                (num_systolic_rows-1-w_iter, 4))
            dut.cfifo_5_send_colbuf_value_value = filter_to_systolic.item(
                (num_systolic_rows-1-w_iter, 5))

        """ Passing initial input accumulation """
        yield Timer(1*CLK_PERIOD, units='ns')
        dut.EN_cfifo_0_send_acc_value = 0x1
        dut.EN_cfifo_1_send_acc_value = 0x1
        dut.EN_cfifo_2_send_acc_value = 0x1
        dut.EN_cfifo_3_send_acc_value = 0x1
        dut.EN_cfifo_4_send_acc_value = 0x1
        dut.EN_cfifo_5_send_acc_value = 0x1
        dut.cfifo_0_send_acc_value_accinput = cfifo_input_acc.item((0,0))
        dut.cfifo_1_send_acc_value_accinput = cfifo_input_acc.item((0,1))
        dut.cfifo_2_send_acc_value_accinput = cfifo_input_acc.item((0,2))
        dut.cfifo_3_send_acc_value_accinput = cfifo_input_acc.item((0,3))
        dut.cfifo_4_send_acc_value_accinput = cfifo_input_acc.item((0,4))
        dut.cfifo_5_send_acc_value_accinput = cfifo_input_acc.item((0,5))

        systolic_output = np.zeros(
            (num_input_rows, num_systolic_cols), dtype='int')

        systolic_complete = cocotb.fork(output_from_systolic(dut.RDY_cfifo_0_send_accumbuf_value, dut.RDY_cfifo_1_send_accumbuf_value, dut.RDY_cfifo_2_send_accumbuf_value, dut.RDY_cfifo_3_send_accumbuf_value, dut.RDY_cfifo_4_send_accumbuf_value, dut.RDY_cfifo_5_send_accumbuf_value,
                                                             dut.cfifo_0_send_accumbuf_value, dut.cfifo_1_send_accumbuf_value, dut.cfifo_2_send_accumbuf_value, dut.cfifo_3_send_accumbuf_value, dut.cfifo_4_send_accumbuf_value, dut.cfifo_5_send_accumbuf_value, num_input_rows, num_systolic_cols, bitwidth))
        """ Feeding input to systolic array """
        for i_iter in range(num_systolic_rows+num_input_rows):
            yield Timer(1*CLK_PERIOD, units='ns')
            dut.EN_rfifo_0_send_rowbuf_value = 0x0
            dut.EN_rfifo_1_send_rowbuf_value = 0x0
            dut.EN_rfifo_2_send_rowbuf_value = 0x0
            dut.EN_rfifo_3_send_rowbuf_value = 0x0
            dut.EN_rfifo_4_send_rowbuf_value = 0x0
            dut.EN_rfifo_5_send_rowbuf_value = 0x0
            dut.EN_rfifo_6_send_rowbuf_value = 0x0
            dut.EN_rfifo_7_send_rowbuf_value = 0x0
            dut.EN_rfifo_8_send_rowbuf_value = 0x0
            temp_clk = random.randint(1,20)
            yield Timer(temp_clk*CLK_PERIOD, units='ns')
            if (i_iter >= 0)and(i_iter <= num_input_rows-1):
                dut.EN_rfifo_0_send_rowbuf_value = 0x1
                dut.rfifo_0_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter, 0))
            if (i_iter >= 1)and(i_iter <= num_input_rows):
                dut.EN_rfifo_1_send_rowbuf_value = 0x1
                dut.rfifo_1_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-1, 1))
            if (i_iter >= 2)and(i_iter <= num_input_rows + 1):
                dut.EN_rfifo_2_send_rowbuf_value = 0x1
                dut.rfifo_2_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-2, 2))
            if (i_iter >= 3)and(i_iter <= num_input_rows + 2):
                dut.EN_rfifo_3_send_rowbuf_value = 0x1
                dut.rfifo_3_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-3, 3))
            if (i_iter >= 4)and(i_iter <= num_input_rows + 3):
                dut.EN_rfifo_4_send_rowbuf_value = 0x1
                dut.rfifo_4_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-4, 4))
            if (i_iter >= 5)and(i_iter <= num_input_rows + 4):
                dut.EN_rfifo_5_send_rowbuf_value = 0x1
                dut.rfifo_5_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-5, 5))
            if (i_iter >= 6)and(i_iter <= num_input_rows + 5):
                dut.EN_rfifo_6_send_rowbuf_value = 0x1
                dut.rfifo_6_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-6, 6))
            if (i_iter >= 7)and(i_iter <= num_input_rows + 6):
                dut.EN_rfifo_7_send_rowbuf_value = 0x1
                dut.rfifo_7_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-7, 7))
            if (i_iter >= 8)and(i_iter <= num_input_rows + 7):
                dut.EN_rfifo_8_send_rowbuf_value = 0x1
                dut.rfifo_8_send_rowbuf_value_value = input_to_systolic.item(
                    (i_iter-8, 8))

        systolic_output = yield systolic_complete.join()
#       print("systolic_done")
#       print(systolic_output)
        truncated_systolic_output = np.zeros(
            (num_input_rows, num_filters), dtype='int')
        for i_iter in range(num_input_rows):
            for j_iter in range(num_filters):
                truncated_systolic_output[i_iter][j_iter] = systolic_output[i_iter][j_iter]

        ip_to_model_rows, ip_to_model_col = input_to_model.shape
        wg_to_model_rows, wg_to_model_col = weight_to_model.shape
        dut._log.info("Ifmap dimensions %s %s Filter dimensions %s %s num_filters %s total elements in convolved matrix %s number of MAC per output %s ; %s %s ; %s %s " % (ifmap_rows,ifmap_cols,num_filter_rows,num_filter_cols,num_filters,num_input_rows,num_input_cols,ip_to_model_rows,ip_to_model_col,wg_to_model_rows,wg_to_model_col))
        print("Filters")
        print(filters)
        print("Input")
        print(input_array)
        print("input to model")
        print(input_to_model)
        print("weight_to_model")
        print(weight_to_model)
        print("counter to systolic")
        print(counter_to_model)
        print("weight to systolic")
        print(weight_to_systolic)
        print("filter_to_systolic")
        print(filter_to_systolic)
        print("Input accumulation to columns")
        print(cfifo_input_acc)

        output_from_model = systolic_array_model(
            input_to_model, weight_to_model)

        for i_iter in range(num_filters):
            for j_iter in range(num_input_rows):
                output_from_model[j_iter][i_iter] = output_from_model[j_iter][i_iter] + \
                    cfifo_input_acc[0][i_iter]

        print("Output from systolic")
        print(systolic_output)
        print("Output from model")
        print(output_from_model)
        print("truncated output")
        print(truncated_systolic_output)

        error = False
        error_row = 0
        error_col = 0
        for check_i in range(num_input_rows):
            for check_j in range(num_filters):
                if(truncated_systolic_output[check_i][check_j] != output_from_model[check_i][check_j]):
                    error = True
                    error_row = check_i
                    error_col = check_j
                    dut._log.info("Values didn't match at %s %s" % (error_row,error_col)) 


        dut._log.info("Ifmap dimensions %s %s Filter dimensions %s %s num_filters %s total elements in convolved matrix %s number of MAC per output %s ; %s %s ; %s %s " % (ifmap_rows,ifmap_cols,num_filter_rows,num_filter_cols,num_filters,num_input_rows,num_input_cols,ip_to_model_rows,ip_to_model_col,wg_to_model_rows,wg_to_model_col))
        if error:
            raise TestFailure(" Check iteration %s : Matric outputs doesn't match: %s != %s at the element [%s , %s]" %
                              (test_iter,truncated_systolic_output, output_from_model,error_row,error_col))
        else:
            dut._log.info("Convolution values are correct %s ",truncated_systolic_output)
