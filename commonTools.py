def get_value(value):
    for i in value:
        return value[i]


def calculate_current_throughput(current_bits, prev_bits):
    return current_bits - prev_bits


def print_values(list):
    for i in list:
        print(list[i])
