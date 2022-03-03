import random

def gen_load_instruction():
    load_dram_address       = 0x80000000
    load_sram_address       = 0x01000000
    load_x_size             = 0x2
    load_y_size             = 0x2
    load_z_size             = 0x2
    load_z_stride           = 0x2
    load_y_stride           = 0x2
    load_is_reset           = 0
    load_bitwidth           = 0
    load_padding            = 20

    load_instruction = (load_bitwidth << 99) | (load_is_reset << 98) | (load_y_stride << 90) | (load_z_stride << 82) | (load_z_size << 74) | (load_y_size << 66)  |(load_x_size << 58) | (load_sram_address << 32) | (load_dram_address)
    return load_instruction


def gen_gemm_instruction():
    gemm_input_address      = 0x01000000
    gemm_output_address     = 0x03000000
    gemm_weigth_address     = 0x02000000
    gemm_ofmap_height       = 0x16
    gemm_ofmap_width        = 0x16
    gemm_active_rows        = 0x16
    gemm_active_cols        = 0x16
    gemm_stride_h           = 0x0
    gemm_stride_w           = 0x0
    gemm_pad_left           = 0x0
    gemm_pad_right          = 0x0
    gemm_pad_top            = 0x0
    gemm_pad_bottom         = 0x0
    gemm_preload_output     = 0x0
    gemm_padding            = 18

    gemm_instruction = (gemm_preload_output << 101) | (gemm_pad_bottom << 97) | (gemm_pad_top << 93) | (gemm_pad_right << 89) | (gemm_pad_left << 85) | (gemm_stride_w << 81) | (gemm_stride_h << 77) | (gemm_active_cols << 69) | (gemm_active_rows << 61) | (gemm_ofmap_width << 53) | (gemm_ofmap_height << 45) | (gemm_weigth_address << 30) | (gemm_output_address << 15) | (gemm_input_address)
    return gemm_instruction

def gen_talu_instruction():
    talu_opcode             = 0x0
    talu_input_address      = 0x03800000
    talu_output_address     = 0x03A00000
    talu_output_height      = 0x3
    talu_output_width       = 0x3
    talu_window_height      = 0x3
    talu_window_width       = 0x3
    talu_mem_stride_OW      = 0x4
    talu_mem_stride_R       = 0x1
    talu_mem_stride_S       = 0x5
    talu_num_active         = 0x10
    talu_use_immediate      = 0x0
    talu_immediate_value    = 0x0
    talu_padding            = 23

    talu_instruction = (talu_immediate_value << 89) | (talu_use_immediate << 88) | (talu_num_active << 80) | (talu_mem_stride_S << 72) | (talu_mem_stride_R << 64) | (talu_mem_stride_OW << 56) | (talu_window_width << 52) | (talu_window_height << 48) | (talu_output_width << 40) | (talu_output_height << 32) | (talu_output_address << 17) | (talu_input_address << 2) | (talu_opcode)
    return talu_instruction

def gen_store_instruction():
    store_dram_address      = 0x80000000
    store_sram_address      = 0x03000000
    store_x_size            = 0x2
    store_y_size            = 0x2
    store_z_size            = 0x2
    store_z_stride          = 0x2
    store_y_stride          = 0x2
    store_is_reset          = 0
    store_bitwidth          = 0x1
    store_padding           = 14

    store_instruction = (store_bitwidth << 99) | (store_is_reset << 98) | (store_y_stride << 90) | (store_z_stride << 82) | (store_z_size << 74) | (store_y_size << 66)  |(store_x_size << 58) | (store_sram_address << 32) | (store_dram_address)
    return store_instruction

#120+
pop_next_bit    = 0
pop_prev_bit    = 1
push_next_bit   = 2
push_prev_bit   = 3

load_opcode     = 0x8
store_opcode    = 0x9
gemm_opcode     = 0xA
talu_opcode     = 0xB

def random_shaktimaan_instr_gen(num_instruction_set):
    instruction_queue = []
    gemm_load_dep_flags     = 0b0000
    load_gemm_dep_flags     = 0b0000
    talu_gemm_dep_flags     = 0b0000
    gemm_talu_dep_flags     = 0b0000
    store_talu_dep_flags    = 0b0000
    talu_store_dep_flags    = 0b0000
    for i in range(num_instruction_set):
        load_dep_flags = gemm_load_dep_flags | random.choice([0b0000, (1<<push_next_bit)])
        load_param = gen_load_instruction()
        load_instr = (load_opcode << 124) | (load_dep_flags << 120) | load_param
        instruction_queue.append(load_instr)
        while load_dep_flags == 0b0000:
            load_dep_flags = gemm_load_dep_flags | random.choice([0b0000, (1<<push_next_bit)])
            load_param = gen_load_instruction()
            load_instr = (load_opcode << 124) | (load_dep_flags << 120) | load_param
            instruction_queue.append(load_instr)
        load_gemm_dep_flags = load_dep_flags >> 1

        gemm_dep_flags = load_gemm_dep_flags | talu_gemm_dep_flags | random.choice([0b0000, (1<<push_next_bit), (1<<push_prev_bit), ((1 << push_next_bit) | (1 << push_prev_bit))])
        gemm_param = gen_gemm_instruction()
        gemm_instr = (gemm_opcode << 124) | (gemm_dep_flags << 120) | gemm_param
        instruction_queue.append(gemm_instr)
        while gemm_dep_flags == 0b0000:
            gemm_dep_flags = load_gemm_dep_flags | talu_gemm_dep_flags | random.choice([0b0000, (1<<push_next_bit), (1<<push_prev_bit), ((1 << push_next_bit) | (1 << push_prev_bit))])
            gemm_param = gen_gemm_instruction()
            gemm_instr = (gemm_opcode << 124) | (gemm_dep_flags << 120) | gemm_param
            instruction_queue.append(gemm_instr)
        gemm_load_dep_flags = int(bin(gemm_dep_flags)[2:].zfill(4)[::-1][push_prev_bit],2)         
        gemm_talu_dep_flags = int(bin(gemm_dep_flags)[2:].zfill(4)[::-1][push_next_bit],2) << 1 

        talu_dep_flags = gemm_talu_dep_flags | store_talu_dep_flags | random.choice([0b0000, (1<<push_next_bit), (1<<push_prev_bit), ((1 << push_next_bit) | (1 << push_prev_bit))])
        talu_param = gen_talu_instruction()
        talu_instr = (talu_opcode << 124) | (talu_dep_flags << 120) | talu_param
        instruction_queue.append(talu_instr)
        while talu_dep_flags == 0b0000:
            talu_dep_flags = gemm_talu_dep_flags | store_talu_dep_flags | random.choice([0b0000, (1<<push_next_bit), (1<<push_prev_bit), ((1 << push_next_bit) | (1 << push_prev_bit))])
            talu_param = gen_talu_instruction()
            talu_instr = (talu_opcode << 124) | (talu_dep_flags << 120) | talu_param
            instruction_queue.append(talu_instr)
        talu_gemm_dep_flags  = int(bin(talu_dep_flags)[2:].zfill(4)[::-1][push_prev_bit],2)  
        talu_store_dep_flags = int(bin(talu_dep_flags)[2:].zfill(4)[::-1][push_next_bit],2) << 1 

        store_dep_flags = talu_store_dep_flags | random.choice([0b0000, (1<<push_prev_bit)])
        store_param = gen_store_instruction()
        store_instr = (store_opcode << 124) | (store_dep_flags << 120) | store_param
        instruction_queue.append(store_instr)
        while store_dep_flags == 0b0000:
            store_dep_flags = talu_store_dep_flags | random.choice([0b0000, (1<<push_prev_bit)])
            store_param = gen_store_instruction()
            store_instr = (store_opcode << 124) | (store_dep_flags << 120) | store_param
            instruction_queue.append(store_instr)
        store_talu_dep_flags = store_dep_flags >> 3
   
    return instruction_queue