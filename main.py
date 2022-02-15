from pysnmp import hlapi
import commonTools
import getters
import sched, time


# Parameters
inOctsArray = []
outOctsArray = []
# Sets our target device (our switch in this case).
target = "192.168.1.1"
# Sets the oids codes.
get_in_octs = "1.3.6.1.2.1.2.2.1.10.3"
get_out_octs = "1.3.6.1.2.1.2.2.1.16.3"

# Sets our credentials to the community we created on the switch.
credentials = hlapi.CommunityData('ciscolab')

def meassureBits():
    # Gets
    get_bites = (getters.get(target, [get_in_octs], credentials))
    result = commonTools.get_value(get_bites)
    return result

bits = []
graphbits = []


s = sched.scheduler(time.time, time.sleep)
def calculate_throughput(sc):
    print("Calculating")
    bits.append(meassureBits())
    if len(bits) == 2:
        throughputBitsPerSecond = (((bits[1] - bits[0])*8)) / 5
        print(str(throughputBitsPerSecond) + " bps")
        bits[0] = bits[1]
        bits.pop(1)
        graphbits.append(throughputBitsPerSecond)


    s.enter(5, 1, calculate_throughput, (sc,))

s.enter(5, 1, calculate_throughput, (s,))
s.run()

