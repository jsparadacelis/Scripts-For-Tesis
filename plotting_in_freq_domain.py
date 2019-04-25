import pyedflib
import matplotlib.pyplot as plt
import numpy as np
f = pyedflib.EdfReader("00000558_s003_t000.edf")
f.signals_in_file

channel_01 = f.readSignal(0)
channel_01_f = np.fft.fft(f.readSignal(0))
sampling_freq = 250

len_channel = len(channel_01_f)
k_array = [i for i in range(0, len_channel)]
f_values = [((sampling_freq*i)/len_channel) for i in k_array]

channel_01_f = abs(channel_01_f)
plt.plot(f_values, channel_01_f)
plt.show()

get_index = lambda x : f_values.index(x)

band_width = {
    "delta" : np.mean(channel_01_f[0:get_index(4)]),
    "tetha" : np.mean(channel_01_f[get_index(4):get_index(8)]),
    "alpha" : np.mean(channel_01_f[get_index(8):get_index(13)]),
    "beta" : np.mean(channel_01_f[get_index(13):get_index(30)]),
}

print(band_width)
