from datetime import datetime


def log(input, output):
    current_time = datetime.now()
    time = current_time.strftime("%d") + "-" + current_time.strftime("%m") + "-" + current_time.strftime("%y")
    # replace the %s with our time variable to use as filename.
    filename = "%s.txt" % time
    # appends to the file due to the "a".
    f = open(filename, "a")
    f.write(current_time.strftime("%m/%d/%Y %H:%M:%S#") + " input: " + str(input) + " output: " + str(output) + "\r")
    f.close()
