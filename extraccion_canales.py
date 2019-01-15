import mne, re 
import pandas as pd
import numpy.fft as fft
import numpy as np


""" def is_edf_file(file_name):
    return file_name[len(file_name)-3:len(file_name)] == "edf" """

def extraer_canal(datos, nombre_canal):

    canal = pd.DataFrame(datos[
        datos.ch_names.index("EEG "+nombre_canal+"-REF")
    ][0])
    valores_canal = canal.T
    valores_canal.describe()
    datos = valores_canal.values

    return datos

def analizar_canales_archivo(archivo, nombre_canal):


    datos_edf = mne.io.read_raw_edf(archivo, preload=True, stim_channel=None)
    nombre_canales = datos_edf.info["chs"][0]["loc"]
    fs = datos_edf.info["sfreq"]

    arr_canal = extraer_canal(datos_edf, nombre_canal)
    
       

    # Obtener las amplitudes de la FFT .. Solo frecuencias positivas
    fft_vals = np.absolute(np.fft.rfft(arr_canal))

    # Obtener las frecuencias para esas amplitudes que obtuvimos en Hertz
    fft_freq = np.fft.rfftfreq(len(arr_canal), 1.0/fs)

    # Definir las bandas de frecuencia de EEG
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

    return df
    

    



    


ruta = '/home/neftali/Descargas/00003281_s002_t000.edf'


etiquetas_canales = ['FP1',
 'FP2',
 'F3',
 'F4',
 'C3',
 'C4',
 'P3',
 'P4',
 'O1',
 'O2',
 'F7',
 'F8',
 'T3',
 'T4',
 'T5',
 'T6',
 'A1',
 'A2',
 'FZ',
 'CZ',
 'PZ',
 'T1',
 'T2',
]
dataChannel = pd.DataFrame()
datos_canales = list()
""" for i in etiquetas_canales:
    datos_canales = pd.concat([analizar_canales_archivo(ruta,i)]) """  

for i in range(0, len(etiquetas_canales) -1 ):
    datos_canales.append(analizar_canales_archivo(ruta,etiquetas_canales[i]))

dataChannel= pd.concat(datos_canales,ignore_index=True)
print(dataChannel)


