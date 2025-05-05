import pandas as pd
import numpy as np

# Load eICU data
patients = pd.read_csv('data/eicu/patient.csv')
vitals = pd.read_csv('data/eicu/vitalPeriodic.csv')

# Subset to 10,000 patients
patients = patients.head(10000)
vitals = vitals[vitals['patientunitstayid'].isin(patients['patientunitstayid'])]

# Extract 48 hours (576 time steps, 5-min intervals)
features = ['heartrate', 'systemicsystolic', 'systemicdiastolic', 'respiration', 'sao2']
data = np.zeros((10000, 576, 5))

for i, pid in enumerate(patients['patientunitstayid']):
    patient_vitals = vitals[vitals['patientunitstayid'] == pid].sort_values('observationoffset')
    patient_vitals = patient_vitals[features].iloc[:576].fillna(method='ffill').fillna(method='bfill')
    if len(patient_vitals) < 576:
        # Pad with last value if less than 576 time steps
        last_row = patient_vitals.iloc[-1:].reindex(range(576), method='ffill')
        patient_vitals = last_row
    data[i] = patient_vitals.values

np.save('data/eicu/eicu_subset.npy', data)