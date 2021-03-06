def calc(flag):

    chars = [0x61,0x92,0x59,0x3b,0x07,0xec,0xc8,0xcc,0xb1,0x7e,0xa3,0x85,0x6b,0x51,0x47,0x31,0x19,0xf6,0x09,0x27,0x1d,0xf2,0xca,0xa5,0x87,0x6c,0x48,0x28,0xf9,0xcc,0xac,0x91,0x73,0x4f,0x63,0xf3,0x02,0x0f,0x27,0x3f,0x4b,0x28,0x57,0x39,0x4b,0x2b,0x43,0x4f,0x31,0x00,0xdd,0xc0,0x9d,0xa9,0x85,0x9d,0x24,0x36,0x44,0x4f,0x5e,0x6c,0x7c,0x7c,0xa0,0xb8,0xc8,0xa9,0xba,0xde,0x5e,0x69,0x4b,0x27,0x06,0x2a,0x0a,0x68,0x75,0x82,0x5f,0x83,0x5f,0x41,0xc7,0xd8,0xf0,0xd0,0xe1,0xc0,0x9b,0x82,0x99,0xa6,0x82,0x90,0xb4,0xc4,0x18,0x24,0x3c,0x4e,0x65,0x78,0x90,0xf1,0x04,0x15,0x22,0x3c,0x5b,0x37,0xec,0xc3,0x94,0x7c,0x4d,0x29,0xfc,0x86,0x9a,0x8c,0x6c,0x37,0x5c,0x7b,0x15,0x26,0x31,0x55,0x60,0x2c,0x0f,0xd5,0xf9,0x0b,0x1c,0x3b,0x4c,0x5d,0x71,0x8c,0x9d,0xb0,0xc9,0xda,0xe5,0xb2,0xd1,0xcf,0xd3,0xc0,0xda,0xf9,0x8d,0x6a,0x50,0x34,0x14,0xfb,0xe2,0x28,0x3c,0x61,0x46,0x18,0xe9,0xc7,0x4e,0x2c,0x05,0xde,0x04,0xe5,0xcb,0xec,0xd0,0xea,0x0a,0xda,0xba,0x85,0x3a,0x21,0x35,0x5b,0x79,0x93,0xb4,0xc1,0x8f,0x77,0x5e,0x39,0x1f,0xee,0x16,0x3b,0x18,0xfd,0xdf,0xab,0x8f,0xc8,0xa4,0x89,0x56,0x7b,0x60,0x46,0x01,0xe4,0xc4,0x8f,0x77,0x5d,0x44,0x53,0x67,0x44,0x2a,0x0c,0xd7,0xbb,0xd3,0xaf,0x96,0x61,0x88,0x74,0x65,0xb3,0xe7,0x3b]

    pos = 232
    while pos >= 2:
        chars[pos] = (-chars[pos]) & 0xff
        chars[pos] = (((chars[pos] >> 1) | ((chars[pos] << 7) & 0xff)) - 198) & 0xff
        pos -= 1

    pos = 231
    while pos >= 3:
        chars[pos] = (chars[pos] - chars[pos - 1]) & 0xff
        pos -= 1

    pos = 1
    while True:
        if pos > 231:
            break
        chars[pos] = ((((((chars[pos] + 128) & 0xff) + 101) & 0xff) << 1) & 0xff) | (((((chars[pos] + 128) & 0xff) + 101) & 0xff) >> 7)
        pos += 1
        
    res = ""
    for pos in range(1, len(chars)-1):
        if pos % 7:
            res += chr(chars[pos] ^ flag)
    
    return res

calc(138)