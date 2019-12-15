mport re
import requests
from requests.auth import HTTPBasicAuth
import time
user = 'nedc_tuh_eeg'

url_lists = [
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/084/00008476/s003_2012_10_22/00008476_s003_t003.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/068/00006894/s003_2010_09_02/00006894_s003_t000.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/099/00009992/s002_2013_03_13/00009992_s002_t001.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/100/00010052/s004_2013_03_22/00010052_s004_t002.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/101/00010138/s001_2013_02_20/00010138_s001_t000.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/102/00010270/s003_2012_11_19/00010270_s003_t000.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/103/00010347/s001_2013_05_20/00010347_s001_t000.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/104/00010412/s001_2013_03_12/00010412_s001_t000.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/epilepsy/01_tcp_ar/105/00010590/s001_2013_08_01/00010590_s001_t000.edf",
    "https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_epilepsy/v1.0.0/edf/no_epilepsy/01_tcp_ar/108/00010838/s001_2013_11_15/00010838_s001_t000.edf",
]

def get_name_by_url(url):
    return re.findall('([0-9]*_[a-z][0-9]*_[a-z][0-9]*)', url)[0]

def make_request(path):
    response = requests.get(
        path,
        auth=HTTPBasicAuth(
            user,
            user
        )
    )
    return response

def save_file(content, name):
    with open(name, 'w') as f:
        f.write(content)

for url in url_lists:
    name = get_name_by_url(url)
    name += ".edf"
    response = make_request(url)
    save_file(response.content, name)
