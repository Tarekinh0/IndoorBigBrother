import subprocess
import pandas as pd
import os

NUMBER_OF_ZONES = 10
SCANS_PER_ZONE = 120

def compile_adresses():
    for zone_index in range(NUMBER_OF_ZONES):
        subprocess.run([f"cd zone{zone_index+1} && cat ./* | cut -d ',' -f1 | sort | uniq >> ../adresses.txt && cd .."], shell=True, text = True,)
    subprocess.run([f"cat adresses.txt | sort | uniq > ./adresses_final.txt"], shell=True, text = True,)
    return open("adresses_final.txt", "r").read().split('\n')

def fill_in_dataframe(df):
    for zone_index in range(NUMBER_OF_ZONES):
        os.chdir(f"./zone{zone_index+1}")
        for scan_index in range(SCANS_PER_ZONE):
            list_of_key_value = open(f"scan{scan_index+1}.csv", "r").read().split('\n')
            list_of_key_value = list(filter(None, list_of_key_value)) #filter to remove empty elements because it causes errors (usually the last line is empty)
            dict = {item.split(',')[0]: float(item.split(',')[1]) for item in list_of_key_value}
            dict['Zone'] = int(zone_index+1)
            dict['Scan'] = int(scan_index+1)
            df.loc[len(df)] = dict
        os.chdir(f"../")
        dict.clear()
    return df


adresses = compile_adresses()
cols = ["Zone", "Scan"] + adresses

df = pd.DataFrame(columns=cols)
df = fill_in_dataframe(df)
df.to_csv('trier.csv', index=False)  

