import concurrent.futures
import logging
import os
import re
import time
from datetime import datetime

import pandas as pd
import requests


def replace_umlaute(astring):
    unicodes = {
        'Ä': '&#196;',
        'ä': '&#228;',
        'Ö': '&#214;',
        'ö': '&#246;',
        'Ü': '&#220;',
        'ü': '&#252;',
        'ß': '&#223;'
    }

    for key, value in unicodes.items():
        astring = astring.replace(value, key)
    return astring


def re_findall(key, txt):
    result = re.findall(f'"{key}":"([^"]*)', txt)
    if len(result) == 0:
        result = re.findall(f'"{key}":([^,]*)', txt)
    return result[0]


def createLogger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="delays.log",
        level=logging.INFO,
        format="[%(asctime)s]:%(levelname)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s]:%(filename)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def getDelays(station, url):
    result_string = requests.get(url).text
    result_string = result_string.replace(' ', '')
    result_string = replace_umlaute(result_string)
    start_id = result_string.find('[')
    end_id = result_string.rfind(']')
    result_string = result_string[start_id+1:end_id]

    entries = result_string.splitlines()

    keys = ['date', 'time',  'status', 'progTime',
            'progDelay', 'name', 'direction', 'platform']
    dic = {key: [] for key in keys}
    for entry in entries:
        if 'DELAYED' in entry:
            if int(re_findall('progDelay', entry)) > 10:
                dic['station'] = station
                for key in keys:
                    dic[key].append(re_findall(key, entry))

    return pd.DataFrame.from_dict(dic)

# urls of rmv api anzeigetafel
current_time = re.findall(r'\d\d:\d\d:\d\d', str(datetime.now()))[0]
urls = [
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzHaupt_3006904_396855748&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=FrankfurtM_3001830_1780579642&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=Rsselsheim_3004912_59409684&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzMnste_3025439_1601009508&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzHecht_3029139_1212749291&dataOnly=true&start=1maxJourneys=198&{current_time}",
    f"https://www.rmv.de/auskunft/bin/jp/stboard.exe/dn?L=vs_anzeigetafel&cfgfile=MainzMnchf_3029013_1498928858&dataOnly=true&start=1maxJourneys=198&{current_time}"
]
stations = [
    'Mainzer Hauptbahnhof',
    'Frankfurter Hauptbahnhof',
    'Rüsselsheimer Bahnhof',
    'Mainz Münsterplatz', 
    'Mainz Am Schinnergraben', 
    'Mainz Im Münchfeld'
    ]

logger = createLogger()

t1 = time.perf_counter()
logger.info("Start execution!")
with concurrent.futures.ThreadPoolExecutor() as executor:
    res = [executor.submit(getDelays, station, url)
           for url, station in zip(urls, stations)]
logger.info("It took {:.2f} seconds to check {} urls.".format(
    time.perf_counter()-t1, len(urls)))

# create single dataframe out of all the dataframes
df = pd.concat([r.result() for r in res], ignore_index=True, sort=False)
logger.info("Number of delayed rides: {}.".format(df.shape[0]))

# save dataframe
if df.shape[0] > 0:
    file_name = 'delays.csv'
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
        
    df.to_csv(file_name, header=None, index=False, mode='a')
    logger.info(f"Saved results in {file_name}.")
