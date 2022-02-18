import datetime
import sched
import time
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from pysnmp import hlapi
import commonTools
import getters
import logger
import trapHandler
# import tkinter as tk
from interface import Interface

# Sets our target device (our switch in this case).
target = "192.168.1.1"

# Sets the oids codes.
get_port_name = "1.3.6.1.2.1.2.2.1.2.3"
get_in_octs = "1.3.6.1.2.1.2.2.1.10.3"
get_out_octs = "1.3.6.1.2.1.2.2.1.16.3"

# Sets our credentials to the community we created on the switch.
credentials = hlapi.CommunityData('ciscolab')

# window = tk.Tk()
# motd = tk.Label(
#     text="Hello, user!"
# )
# motd.pack()

# trapHandler.trapHandler()

def interface_information(mib_code):
    get_info = getters.get(target, [mib_code], credentials)
    result = commonTools.get_value(get_info)
    return result


pi1 = Interface(interface_information(get_port_name))
print("Measuring on interface " + pi1.port_name)
bytes_in_r1 = []
bytes_out_r1 = []

s = sched.scheduler(time.time, time.sleep)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    bytes_in_r1.append(interface_information(get_in_octs))
    bytes_out_r1.append(interface_information(get_out_octs))

    if len(bytes_in_r1) == 2:
        throughput_bits_per_second = ((bytes_in_r1[1] - bytes_in_r1[0]) * 8) / 5
        print(str(throughput_bits_per_second) + " bps input")
        bytes_in_r1[0] = bytes_in_r1[1]
        bytes_in_r1.pop(1)
        pi1.in_oct.append(int(throughput_bits_per_second))

        if len(pi1.x_pos) == 0:
            pi1.x_pos.append(0)
        else:
            temp_value = pi1.x_pos[-1] + 5
            pi1.x_pos.append(temp_value)

    if len(bytes_out_r1) == 2:
        throughput_bits_per_second = ((bytes_out_r1[1] - bytes_out_r1[0]) * 8) / 5
        print(str(throughput_bits_per_second) + " bps output")
        bytes_out_r1[0] = bytes_out_r1[1]
        bytes_out_r1.pop(1)
        pi1.out_oct.append(int(throughput_bits_per_second))

    xar_in = []
    yar_in = []
    for index, cordinate in enumerate(pi1.x_pos):
        if len(pi1.x_pos) > 1:
            xar_in.append(int(pi1.x_pos[index]))
            yar_in.append(int(pi1.in_oct[index]))

    xar_out = []
    yar_out = []
    for index, cordinate in enumerate(pi1.x_pos):
        if len(pi1.x_pos) > 1:
            xar_out.append(int(pi1.x_pos[index]))
            yar_out.append(int(pi1.out_oct[index]))

    ax1.clear()
    ax1.plot(xar_in, yar_in, linestyle="-", color="blue")
    ax1.plot(xar_out, yar_out, linestyle="-", color="orange")

    input_label = patches.Patch(color="blue", label="Input")
    output_label = patches.Patch(color="orange", label="Output")
    plt.legend(handles=[input_label, output_label])

    plt.suptitle("Throughput Graphs")
    plt.xlabel("Seconds")
    plt.ylabel("Throughput")

    logger.log(bytes_in_r1[0], bytes_out_r1[0])


ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()
