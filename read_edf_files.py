import os
import mne, re 

import pandas as pd
import numpy.fft as fft
import numpy as np



path = '/home/ticsocial/Escritorio/data/Datos/Paciente1/'

# valida la extension del fichero
""" def is_edf_file(file_name):
    return file_name[len(file_name)-3:len(file_name)] == "edf" """


# revisa si es un canal valido
match_regex = lambda channel_name : re.compile(r'(P|F|O|T)').search(channel_name)

# valida la extension del fichero
is_edf_file = lambda file_name : file_name[len(file_name)-3:len(file_name)] == "edf"


files = os.listdir(path)

edf_files = [name for name in files if is_edf_file(name)]
print(edf_files)

def extraer_canal(datos, nombre_canal):

    canal = pd.DataFrame(datos[
        datos.ch_names.index(nombre_canal)
    ][0])
    valores_canal = canal.T
    valores_canal.describe()
    datos = valores_canal.values

    return datos

        # Definir las bandas de frecuencia de EEG
bandas_eeg = {
    'Delta': (0, 4),
    'Theta': (4, 8),
    'Alpha': (8, 12),
    'Beta': (12, 30),
    'Gamma': (30, 50)
    }



for file_name in edf_files:

    #edf_file = pyedflib.EdfReader(path+file_name)
    datos_edf = mne.io.read_raw_edf(path+file_name, preload=True, stim_channel=None)
   
    """ num_signals = edf_file.signals_in_file
    signal_labels = edf_file.getSignalLabels()
        
    channels = signal_labels[0:21] + signal_labels[24:26] """

    list_channels = list(
        filter(
            lambda channel_name : len(channel_name) > 4 and channel_name[0:3] == "EEG", 
            datos_edf.info["ch_names"]
        )
    )
    list_channels = [channel for channel in list_channels if match_regex(channel[4])]
    print(len(list_channels))
    arr_canal = []
    list_test = []
    fs = 250

    dataChannel = pd.DataFrame()
    for channel in list_channels:

        arr_canal = extraer_canal(datos_edf, channel)
        fft_vals = np.absolute(np.fft.rfft(arr_canal))
        fft_freq = np.fft.rfftfreq(len(arr_canal), 1.0/fs)

        bandas_eeg = {'Delta': (0, 4),
                 'Theta': (4, 8),
                 'Alpha': (8, 12),
                 'Beta': (12, 30),
                 'Gamma': (30, 50)}

        # Tomamos la media de las amplitudes de la fft para cada banda de frecuencia .. estan definidas en un diccionario..
        bandas_eeg_fft = dict()
        for band in bandas_eeg:  
            freq_ix = np.where((fft_freq >= bandas_eeg[band][0]) & 
                            (fft_freq <= bandas_eeg[band][1]))[0]
            bandas_eeg_fft[band] = np.mean(fft_vals[freq_ix])
        
        df = pd.DataFrame(columns=['band', 'val'])
        df['band'] = bandas_eeg.keys()
        df['val'] = [bandas_eeg_fft[band] for band in bandas_eeg]

        list_test.append(df)

        
        dataChannel= pd.concat(list_test,ignore_index=True)

    
    dataChannel.to_csv(file_name+".csv", sep='\t')
    print(dataChannel)
