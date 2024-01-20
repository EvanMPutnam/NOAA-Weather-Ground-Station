import simplesoapy


def sdr_listen():
    devices = simplesoapy.detect_devices()
    print(devices)


sdr_listen()
