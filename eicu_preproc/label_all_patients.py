"""
Cluster dispatch script for endpoint computation, modified to run locally
"""

import subprocess
import argparse
import pickle
import os.path
import os

import functions.util_filesystem as mlhc_fs

def label_all_patients(configs):
    # Load the batch-to-patient mapping
    with open(configs["patient_batch_path"], 'rb') as fp:
        obj = pickle.load(fp)
        batch_to_lst = obj["batch_to_lst"]
        batches = list(sorted(batch_to_lst.keys()))

    # Process each batch sequentially
    for batch_idx in batches:
        print(f"Dispatching labels for batch {batch_idx}")
        log_result_file = os.path.join(configs["log_base_dir"], f"label_batch_{batch_idx}_RESULT.txt")
        mlhc_fs.delete_if_exist(log_result_file)

        # Construct the command to run label_data_one_batch.py
        cmd_line = [
            "python3",
            configs["compute_script_path"],
            "--run_mode", "CLUSTER",  # Keep this for compatibility with label_data_one_batch.py
            "--batch_id", str(batch_idx)
        ]

        if not configs["dry_run"]:
            try:
                # Run the command and redirect output to the log file
                with open(log_result_file, "w") as log_file:
                    result = subprocess.run(
                        cmd_line,
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                print(f"Batch {batch_idx} completed with return code {result.returncode}")
            except Exception as e:
                print(f"Error running batch {batch_idx}: {e}")
        else:
            print(f"Generated cmd line: {' '.join(cmd_line)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Input paths
    parser.add_argument("--patient_batch_path", default="../data/patient_batches.pickle", help="The path of the PID-Batch map")
    parser.add_argument("--compute_script_path", default="./label_data_one_batch.py", help="Script to dispatch")

    # Output paths
    parser.add_argument("--log_base_dir", default="../data/logs", help="Log base directory")

    # Parameters
    parser.add_argument("--dry_run", action="store_true", default=False, help="Dry run, do not generate any jobs")
    parser.add_argument("--mem_in_mbytes", type=int, default=5000, help="Number of MB to request per script (ignored in local mode)")
    parser.add_argument("--nhours", type=int, default=4, help="Number of hours to request (ignored in local mode)")

    args = parser.parse_args()
    configs = vars(args)
    
    label_all_patients(configs)
