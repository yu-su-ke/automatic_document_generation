def time_measurement(t):
    hour = int(t / 3600)
    minute = int((t - 3600 * hour) / 60)
    second = int((t - (3600 * hour + 60 * minute)))

    a = "\n" + "{}:{}:{}".format(str(hour), str(minute), str(second))
    return a
