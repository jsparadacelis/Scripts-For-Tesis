import re
import mne
import matplotlib.pyplot as plt
import numpy as np
datos_edf = mne.io.read_raw_edf(
        "00000558_s003_t000.edf", 
        preload=True, 
        stim_channel=None
)

match_regex = lambda channel_name : re.compile(r'(P|F|O|T|C)').search(channel_name)
list_channels = list(
        filter(
            lambda channel_name : len(channel_name) > 4 and channel_name[0:3] == "EEG", 
            datos_edf.info["ch_names"]
        )
    )
list_channels = [channel for channel in list_channels if match_regex(channel[4])]
get_data_channel = lambda channel_name : datos_edf[datos_edf.ch_names.index(channel)][0][0]

freq_bands_list = []
for channel in list_channels:
    
    current_data = get_data_channel(channel)
    channel_f = np.fft.fft(current_data)
    sampling_freq = datos_edf.info['sfreq']
    len_channel = len(channel_f)
    k_array = [i for i in range(0, len_channel)]
    f_values = [((sampling_freq*i)/len_channel) for i in k_array]

    channel_f = abs(channel_f)
    plt.plot(f_values, channel_f)
    plt.show()
    
    get_index = lambda x : f_values.index(x)
    
    band_width = {
        "delta" : np.mean(channel_f[0:get_index(4)]),
        "tetha" : np.mean(channel_f[get_index(4):get_index(8)]),
        "alpha" : np.mean(channel_f[get_index(8):get_index(13)]),
        "beta" : np.mean(channel_f[get_index(13):get_index(30)]),
    }
    freq_bands_list.append(band_width)
    
print(freq_bands_list)
