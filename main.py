from pysnmp import hlapi
import commonTools
import getters
import sched, time

# Sets our target device (our switch in this case).
target = "192.168.1.1"

# Sets the oids codes.
get_port_name = "1.3.6.1.2.1.2.2.1.2.3"
get_in_octs = "1.3.6.1.2.1.2.2.1.10.3"
get_out_octs = "1.3.6.1.2.1.2.2.1.16.3"

# Sets our credentials to the community we created on the switch.
credentials = hlapi.CommunityData('ciscolab')


def interface_information():
    # Gets
    get_info = (getters.get(target, [get_in_octs, get_port_name], credentials))
    result = commonTools.get_value(get_info)
    return result


bits = []
graph_bits = []

s = sched.scheduler(time.time, time.sleep)


def calculate_throughput(sc):
    print("Calculating")
    bits.append(interface_information())
    if len(bits) == 2:
        throughput_bits_per_second = ((bits[1] - bits[0]) * 8) / 5
        print(str(throughput_bits_per_second) + " bps")
        bits[0] = bits[1]
        bits.pop(1)
        graph_bits.append(throughput_bits_per_second)

    s.enter(5, 1, calculate_throughput, (sc,))


s.enter(5, 1, calculate_throughput, (s,))
s.run()
