import os
path = '/home/ticsocial/Descargas/'

# valida la extensión del fichero
"""def is_edf_file(file_name):
    return file_name[len(file_name)-3:len(file_name)] == "edf"
"""
# revisa si es un canal valido
match_regex = lambda channel_name : re.compile(r'(P|F|O|T)').search(channel_name)

# valida la extension del fichero
is_edf_file = lambda file_name : file_name[len(file_name)-3:len(file_name)] == "edf"


def calc_auto(path):
    # Encontrar los archivos edf dentro del directorio
    files = os.listdir(path)
    edf_files = [name for name in files if is_edf_file(name)]
    
    #iterando sobre los ficheros D:
    for file_name in edf_files:
        
        edf_file = pyedflib.EdfReader(path+file_name)
        
        num_signals = edf_file.signals_in_file
        signal_labels = edf_file.getSignalLabels()
        
        channels = signal_labels[0:21] + signal_labels[24:26]
        print(len(channels))

        
        
        

calc_auto(path)
