import random
def generate_random_name(max_length = 16):
    cap = 'ABCDEFGHIJKLMNOPQRSTUBWXYZabcdefghijklmnopqrstuvqxyz1234567890'
    rstring = ''
    for _ in range(max_length):
        rindex = random.randint(0, len(cap) - 1)
        rstring += cap[rindex]
    return rstring
