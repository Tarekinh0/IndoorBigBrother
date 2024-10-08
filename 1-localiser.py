import subprocess
import pandas as pd

# code must be launched with super user rights (use sudo, friends)

ADAPTER="wlan0"
NUMBER_OF_ZONES = 10
SCANS_PER_ZONE = 120

def start():
    for zone_index in range(NUMBER_OF_ZONES):
        subprocess.run([f"mkdir zone{zone_index+1}"], shell=True, capture_output = True, text = True,)
    print("Running Monitor Mode !")
    monitor_mode = subprocess.run([f"sudo ip link set {ADAPTER} up && sudo ip link show {ADAPTER} | grep -c UP"], shell=True, capture_output = True, text = True,)
    if monitor_mode.stdout != "1\n":
        print ("Error, the adapter is not in monitor mode. Exiting !")
        exit()
 
def stop():
    # subprocess.run([f"rm temp.tmp"], shell=True)
    print("Exiting Monitor Mode !")
    monitor_mode = subprocess.run([f"sudo ip link set {ADAPTER} down && sudo ip link show {ADAPTER} | grep -c DOWN"], shell=True, capture_output = True, text = True,)
    if monitor_mode.stdout != "1\n":
        print ("Error, the adapter could not exit monitor mode. Please do it manually. Exiting !")
        exit();


def run_scan(df, zone_index, scan_index):
    if scan_index <= SCANS_PER_ZONE:
        scan_results = subprocess.run(
            [f"sudo iw dev {ADAPTER} scan | sudo tee temp.tmp"],
            capture_output = True, 
            text = True,
            shell = True
        )

        if scan_results.stderr != "":
            print("Error !")
            print(scan_results.stderr)
            run_scan(df, zone_index, scan_index)

        scan_mac_adress_list = subprocess.run(
            [f"cat temp.tmp| grep '(on' | cut -d ' ' -f2 | cut -d '(' -f1 "],
            capture_output = True, 
            text = True,
            shell = True
        )

        scan_rssi_list = subprocess.run(
            [f"cat temp.tmp | grep 'signal: ' | cut -d ':' -f2 | cut -d ' ' -f2 "],
            capture_output = True, 
            text = True,
            shell = True
        )

        write_results(df, scan_mac_adress_list, scan_rssi_list, scan_index, zone_index)
        run_scan(df, zone_index, scan_index+1)



def create_dataframe(df, dictionary, zone_index, scan_index):
    # Loop through the dictionary items
    row = pd.Series(dtype = float)
    for key, value in dictionary.items():
        # If the key is already a column in the dataframe
        if key in df.columns:
            # Append the value to the column
            df.loc[df.shape[0], key] = value
        else:
            # Create a new column with the key and assign the value to the last row
            # Modified this line to use pd.Series instead of a list to avoid the ValueError
            df[key] = pd.Series([value], index=[df.shape[0]]) # Modified this line to use pd.Series instead of a list

        print(df)
    # Return the dataframe
    df["Zone", df.shape[0]] = zone_index
    df["Scan", df.shape[0]] = scan_index
    return df

def toCsv(zone_index, scan_index, dict):
    subprocess.run([f"cd zone{zone_index}"], shell=True, capture_output = False, text = True,)
    pd.DataFrame.from_dict(data=dict, orient='index').to_csv(f"zone{zone_index}//scan{scan_index}.csv", header=False)
    subprocess.run([f"cd .."], shell=True, capture_output = False, text = True,)



def write_results(df, scan_mac_adress_string, scan_rssi_string, scan_index, zone_index):

    scan_mac_adress_list =scan_mac_adress_string.stdout.split()
    scan_rssi_list =scan_rssi_string.stdout.split()

    dict = {scan_mac_adress_list[i]: scan_rssi_list[i] for i in range(len(scan_mac_adress_list))}
    # df = pd.concat([df, create_dataframe(df, dict, zone_index, scan_index)] )


    print(f"\n\n\nScan number {scan_index} got us these results !")
    toCsv(zone_index, scan_index, dict)
    print(dict)
    # print(df)


def new_zone(df, zone_index):
    if zone_index <= NUMBER_OF_ZONES:
        print(f"Move to the zone number {zone_index}! ")
        if input("Are you ready to capture ? (y/N)") != 'y':
            new_zone(df, zone_index)
        run_scan(df, zone_index, 1)
        # new_zone(df, zone_index+1)
    
start()
df = pd.DataFrame(columns=["Zone", "Scan"])
new_zone(df, 10)
stop()