import re
import mne
import matplotlib.pyplot as plt
import numpy as np
datos_edf = mne.io.read_raw_edf(
        "EXAM/PATH", 
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

channel = 'EEG F8-REF'
channel_f = get_data_channel(channel)
channel_f = abs(channel_f)
plt.plot(channel_f)
plt.show()
