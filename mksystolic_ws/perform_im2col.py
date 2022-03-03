import numpy as np

def perform_im2col(image, block_size, skip=1):
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