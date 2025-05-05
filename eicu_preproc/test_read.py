import pandas as pd

# Test reading a few tables
tables = ["lab", "patient", "vitalPeriodic"]
for table in tables:
    hdf_path = f"../data/hdf/{table}.h5"
    try:
        df = pd.read_hdf(hdf_path, key="data")  # Match the key used in hdf_convert.py
        print(f"Table {table} loaded with shape: {df.shape}")
        print(df.head())  # Inspect the first few rows
    except Exception as e:
        print(f"Error reading {hdf_path}: {e}")
