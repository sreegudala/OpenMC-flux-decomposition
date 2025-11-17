def get_pin_rows():
    """
    Returns the nested list of (x, y, z) coordinates for pin centers.
    """

    # Info to determine coordinates of a fuel pin:
    # The origin of the array of fuel channels/graphite block is just below the center row
    # (with the two control rods), in the geometric center of the 3 pin grid triangle
    # (that is to say 2.9329393674832986 cm from the north pins and 5.865878734966597 cm from the south pin)
    # Building from a bunch of 10.16 cm wide and 8.798818102449896 cm tall blocks,
    # the core is 14 blocks wide and 16 blocks high (rounding up each and filling with void).
    # So the entire created grid is 142.24 cm wide and 140.78108963919834 cm tall
    # e.g. the top control rod is at (x0=0, y0=46.9270298797) bc y = 2.9329393674832986 + 8.798818102449896 * 5
    # e.g. the right control rod is at (x0=45.72, y0=2.9329393674832986) bc x = 10.16 * 4.5

    height = 8.798818102449896
    width = 10.16
    row_0_y = 2.9329393674832986 + height * 5
    row_1_y = 2.9329393674832986 + height * 4
    row_2_y = 2.9329393674832986 + height * 3
    row_3_y = 2.9329393674832986 + height * 2
    row_4_y = 2.9329393674832986 + height * 1
    row_5_y = 2.9329393674832986 + height * 0
    row_6_y = 2.9329393674832986 + height * -1
    row_7_y = 2.9329393674832986 + height * -2
    row_8_y = 2.9329393674832986 + height * -3
    row_9_y = 2.9329393674832986 + height * -4
    row_10_y = 2.9329393674832986 + height * -5
    row_11_y = 2.9329393674832986 + height * -6

    row_0 = [[-width, row_0_y, 0], [0, row_0_y, 0], [width, row_0_y, 0]]
    row_1 = [[-2.5*width, row_1_y, 0], [-1.5*width, row_1_y, 0], [-0.5*width, row_1_y, 0], [0.5*width, row_1_y, 0], [1.5*width, row_1_y, 0], [2.5*width, row_1_y, 0]]
    row_2 = [[-4*width, row_2_y, 0], [-3*width, row_2_y, 0], [-2*width, row_2_y, 0], [-1*width, row_2_y, 0], [0, row_2_y, 0], [1*width, row_2_y, 0], [2*width, row_2_y, 0], [3*width, row_2_y, 0], [4*width, row_2_y, 0]]
    row_3 = [[-4.5*width, row_3_y, 0], [-3.5*width, row_3_y, 0], [-2.5*width, row_3_y, 0], [-1.5*width, row_3_y, 0], [-0.5*width, row_3_y, 0], [0.5*width, row_3_y, 0], [1.5*width, row_3_y, 0], [2.5*width, row_3_y, 0], [3.5*width, row_3_y, 0], [4.5*width, row_3_y, 0]]
    row_4 = [[-4*width, row_4_y, 0], [-3*width, row_4_y, 0], [-2*width, row_4_y, 0], [-1*width, row_4_y, 0], [0, row_4_y, 0], [1*width, row_4_y, 0], [2*width, row_4_y, 0], [3*width, row_4_y, 0], [4*width, row_4_y, 0]]
    row_5 = [[-4.5*width, row_5_y, 0], [-3.5*width, row_5_y, 0], [-2.5*width, row_5_y, 0], [-1.5*width, row_5_y, 0], [-0.5*width, row_5_y, 0], [0.5*width, row_5_y, 0], [1.5*width, row_5_y, 0], [2.5*width, row_5_y, 0], [3.5*width, row_5_y, 0], [4.5*width, row_5_y, 0]]
    row_6 = [[-4*width, row_6_y, 0], [-3*width, row_6_y, 0], [-2*width, row_6_y, 0], [-1*width, row_6_y, 0], [0, row_6_y, 0], [1*width, row_6_y, 0], [2*width, row_6_y, 0], [3*width, row_6_y, 0], [4*width, row_6_y, 0]]
    row_7 = [[-4.5*width, row_7_y, 0], [-3.5*width, row_7_y, 0], [-2.5*width, row_7_y, 0], [-1.5*width, row_7_y, 0], [-0.5*width, row_7_y, 0], [0.5*width, row_7_y, 0], [1.5*width, row_7_y, 0], [2.5*width, row_7_y, 0], [3.5*width, row_7_y, 0], [4.5*width, row_7_y, 0]]
    row_8 = [[-4*width, row_8_y, 0], [-3*width, row_8_y, 0], [-2*width, row_8_y, 0], [-1*width, row_8_y, 0], [0, row_8_y, 0], [1*width, row_8_y, 0], [2*width, row_8_y, 0], [3*width, row_8_y, 0], [4*width, row_8_y, 0]]
    row_9 = [[-3.5*width, row_9_y, 0], [-2.5*width, row_9_y, 0], [-1.5*width, row_9_y, 0], [-0.5*width, row_9_y, 0], [0.5*width, row_9_y, 0], [1.5*width, row_9_y, 0], [2.5*width, row_9_y, 0], [3.5*width, row_9_y, 0]]
    row_10 = [[-2*width, row_10_y, 0], [-1*width, row_10_y, 0], [0, row_10_y, 0], [1*width, row_10_y, 0], [2*width, row_10_y, 0]]
    row_11 = [[-0.5*width, row_9_y, 0], [0.5*width, row_9_y, 0]]

    rows = [row_0,row_1,row_2,row_3,row_4,row_5,row_6,row_7,row_8,row_9,row_10,row_11]

    return rows
