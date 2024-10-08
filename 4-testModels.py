import pandas as pd
import numpy as np
import time
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from models.svm import launchSVM
from models.mlp import launchMLP
from models.knn import launchKNNeuclidian, launchKNNmanhattan
import os, subprocess
from sklearn.metrics import confusion_matrix


ADAPTER="wlan0"
X = pd.read_csv('X.csv')
Y = pd.read_csv('Y.csv')
ALL_ADRESSES=X.columns.values.tolist()

def runScan():
    scan_results = subprocess.run(
        [f"sudo iw dev {ADAPTER} scan | sudo tee temp.tmp"],
        capture_output = True, 
        text = True,
        shell = True
    )

    scan_mac_adress_list = subprocess.run(
            [f"cat temp.tmp| grep '(on' | cut -d ' ' -f2 | cut -d '(' -f1 "],
            capture_output = True, 
            text = True,
            shell = True
    ).stdout.split()

    scan_rssi_list = subprocess.run(
            [f"cat temp.tmp | grep 'signal: ' | cut -d ':' -f2 | cut -d ' ' -f2 "],
            capture_output = True, 
            text = True,
            shell = True
    ).stdout.split()

    df = pd.DataFrame(columns=ALL_ADRESSES)
    dicc = dict()
    for address in ALL_ADRESSES:
        if address in scan_mac_adress_list:
            i = scan_mac_adress_list.index(address)
            dicc[address] = float(scan_rssi_list[i])
        else:
            dicc[address] = -95.0

    df.loc[len(df)] = dicc
    df.to_csv('X_now.csv', index=False)

    return df

def main():

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    scaler = StandardScaler().fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    svm = launchSVM(X_train_scaled, Y_train)
    knne = launchKNNeuclidian(X_train_scaled, Y_train)
    knnm = launchKNNmanhattan(X_train_scaled, Y_train)
    mlp = launchMLP(X_train_scaled, Y_train)


    svm_predictions = []
    knne_predictions = []
    knnm_predictions = []
    mlp_predictions = []



    for i in range(len(Y_test.values)):
        print(f"For i = {i} in Y_test : ",  Y_test.values[i][0])
        svm_predictions.append(svm.predict([X_test_scaled[i]])[0])
        knne_predictions.append(knne.predict([X_test_scaled[i]])[0])
        knnm_predictions.append(knnm.predict([X_test_scaled[i]])[0])
        mlp_predictions.append(mlp.predict([X_test_scaled[i]])[0])

        print("\tSVM: " , svm_predictions[i])
        print("\tKNNE: " , knne_predictions[i])
        print("\tKNNM: " , knnm_predictions[i])
        print("\tMLP: " , mlp_predictions[i])
        

    print(f"SVM Score: {svm.score(X_test_scaled, Y_test)}")
    print(f"Euclidian KNN Score: {knne.score(X_test_scaled, Y_test)}")
    print(f"Manhattan KNN Score: {knnm.score(X_test_scaled, Y_test)}")
    print(f"MLP Score: {mlp.score(X_test_scaled, Y_test)}")
    
    cnm_svm = confusion_matrix(Y_test, svm_predictions)
    cnm_knne = confusion_matrix(Y_test, knne_predictions)
    cnm_knnm = confusion_matrix(Y_test, knnm_predictions)
    cnm_mlp = confusion_matrix(Y_test, mlp_predictions)


    print(cnm_svm)
    input()
    print(cnm_knne)
    input()
    print(cnm_knnm)
    input()
    print(cnm_mlp)
    input("Press [ENTER] to start scanning live !")

    with open("zones.json" ,'rb') as f:
        zones = f.read()

    zones = json.loads(zones)

    while True:
        X_now = runScan()
        X_now_scaled = scaler.transform(X_now)
        time.sleep(1)   
        # input("Enter to see prediction\n")
        svm_pred = str(int(svm.predict(X_now_scaled)[0]))
        knne_pred = str(int(knne.predict(X_now_scaled)[0]))
        knnm_pred = str(int(knnm.predict(X_now_scaled)[0]))
        mlp_pred = str(int(mlp.predict(X_now_scaled)[0]))  
        print(f"SVM predicts: {zones[svm_pred]}")
        print(f"Euclidian KNN predicts: {zones[knne_pred]}")
        print(f"Manhattan KNN predicts: {zones[knnm_pred]}")
        print(f"MLP predicts: {zones[mlp_pred]}")

if "__main__":
    main()



# overfitting, underfitting, 2 courbes
# epoch: le nombre de fois ou on balance les donnees au model.
# confusion_metrics 
# confusion_matrix_display