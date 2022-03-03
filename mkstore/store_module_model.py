import math

max_bank_bits = 4
max_index_bits = 6
valid_bits = 4
num_buffers_bits = 2
datawidth = 128

ibank_bits = 4
wbank_bits = 4
obank_bits = 4

iindex_bits = 6
windex_bits = 6
oindex_bits = 6

in_bytes = 1
out_bytes = 4

obuf1_start = 0x03000000
obuf1_end   = 0x037fffff
obuf2_start = 0x03800000
obuf2_end   = 0x03ffffff

def store_module_model(dram_address, sram_address, x_size, y_size, z_size, z_stride, y_stride, data_bytes,data_bytes_1):
    gen_dram_address = []
    num_dram_requests = 0
    write_strobe = []

    sram_buffer = 0
    sram_index = []
    sram_bank = []
    sram_valid = []

    error = False

    if datawidth == 8:
        data_per_transaction = 1
    elif datawidth == 16:
        data_per_transaction = 2
    elif datawidth == 32:
        data_per_transaction = 4
    elif datawidth == 64:
        data_per_transaction = 8
    elif datawidth == 128:
        data_per_transaction = 16
    print("DRAM Address")
    print("",x_size,y_size,z_stride,y_stride,data_bytes)
    for i in range(x_size):
        for j in range(y_size):
            gen_dram_address.append(dram_address)
            num_dram_requests = num_dram_requests + 1
            if(j < y_size-1):
                dram_address = dram_address + z_stride*data_bytes
                #print(hex(dram_address))
        dram_address = dram_address + y_stride*data_bytes
        #print("\n")
        #print(hex(dram_address))

    total_len = z_size*data_bytes
    #if(total_len < data_per_transaction):
    #    burst_req_len = 0
    #else:
    burst_req_len = math.ceil(z_size*data_bytes/data_per_transaction)
    print("burst length : ",z_size,data_bytes,data_per_transaction,burst_req_len)

    burst_req_len_1 = math.ceil(z_size*data_bytes_1/data_per_transaction)
    print("burst length : ",z_size,data_bytes_1,data_per_transaction,burst_req_len_1)


    bank_bits = obank_bits
    index_bits = oindex_bits
    if(obuf1_start <= sram_address <= obuf1_end):
        sram_buffer = 2
    elif(obuf2_start <= sram_address <= obuf2_end):
        sram_buffer = 3
    else:
        error = True

    sram_address = sram_address << 26

    for i in range(num_dram_requests):
        for j in range(burst_req_len_1):
            sram_bank.append(int(bin(sram_address)[::-1][0:bank_bits][::-1],2))
            sram_index.append(int(bin(sram_address)[::-1][bank_bits:bank_bits+index_bits][::-1],2))
            if j == burst_req_len_1 -1 :
                if(int(z_size*data_bytes_1 % (datawidth/8)) == 0):
                    sram_valid.append(int(datawidth/8/data_bytes_1))
                else:
                    sram_valid.append(int(((z_size*data_bytes_1) % int(datawidth/8))/data_bytes_1))
            else:
                sram_valid.append(int(datawidth/8/data_bytes_1))
                sram_address = sram_address + int(datawidth/8/data_bytes_1)
            ##print(hex(sram_address))
        sram_address = ((sram_address >> bank_bits) << bank_bits) + (1 << bank_bits)

    #print("SRAM ADDRESS FROM MODEL")
    #print(sram_buffer)
    #print(sram_bank)
    #print(sram_index)
    #print(sram_valid)

    return gen_dram_address, num_dram_requests, write_strobe, burst_req_len-1, sram_buffer, sram_index, sram_bank, sram_valid, error

