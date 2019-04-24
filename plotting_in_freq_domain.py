import pyedflib
import matplotlib.pyplot as plt
import numpy as np
f = pyedflib.EdfReader("00000558_s003_t000.edf")
f.signals_in_file
channel_01 = f.readSignal(0)
plt.plot(channel_01)
plt.show()
channel_01_f = np.fft.fft(f.readSignal(0))
plt.plot(abs(channel_01_f))
plt.show()
