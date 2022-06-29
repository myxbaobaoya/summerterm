import csv
import numpy as np
import pandas as pd

# filename = '../Buccal_mucosa.csv'
# filename = '../Stool.csv'
filename = '../anterior_nares.csv'
with open(filename) as f:
    r = csv.reader(f)
    l = list(r)
    k = np.array(l)
    data = pd.read_csv(filename)
    afterMapping = data['after Mapping']
    with open('../pairwise.csv', 'a+',newline='') as f:
        csv_write = csv.writer(f)
        for i in range(1,k.shape[0]-1):
            for j in range(i+1,k.shape[1]-1):
                if(float(k[i][j]) > 0 and k[i][0] in afterMapping.tolist() and k[0][j] in afterMapping.tolist()):
                    data_row = [k[i][0],k[0][j],k[i][j]]
                    csv_write.writerow(data_row)