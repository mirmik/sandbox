#!/usr/bin/env python3

import alsaaudio, time, audioop
import pycrow

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)

pycrow.create_udpgate(12, 10010)
crowaddr = pycrow.compile_address(".12.127.0.0.1:10009")

while True:
    l,data = inp.read()
    if l:
        pycrow.publish(crowaddr, "mic", data, 0, 200)
        pycrow.onestep()

    time.sleep(.00001)