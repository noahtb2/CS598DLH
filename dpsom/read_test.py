import h5py
import numpy as np
hf = h5py.File('../data/eICU_data.csv', 'r')
data_total = np.array(hf.get('x'))
endpoints_total = np.array(hf.get('y'))
hf.close()
print(f"Data contains NaN: {np.any(np.isnan(data_total))}")
print(data_total)
print(f"Data contains Inf: {np.any(np.isinf(data_total))}")
print(f"Endpoints contains NaN: {np.any(np.isnan(endpoints_total))}")
print(f"Endpoints contains Inf: {np.any(np.isinf(endpoints_total))}")
