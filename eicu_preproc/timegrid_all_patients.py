"""
Dispatch script for imputation/time-gridding
"""

import subprocess
import argparse
import pickle
import os.path
import os
import sys

import functions.util_filesystem as mlhc_fs

def timegrid_all_patients(configs):
    job_index = 0
    # Remove the "source activate" line since we're already in a virtual environment
    # subprocess.call(["source activate default_py36"], shell=True)
    mem_in_mbytes = configs["mem_in_mbytes"]
    n_cpu_cores = 1
    n_compute_hours = configs["nhours"]
    compute_script_path = configs["compute_script_path"]

    with open(configs["patient_batch_path"], 'rb') as fp:
        obj = pickle.load(fp)
        batch_to_lst = obj["batch_to_lst"]
        batches = list(sorted(batch_to_lst.keys()))

    for batch_idx in batches:
        print("Dispatching imputation for batch {}".format(batch_idx))
        job_name = "impute_batch_{}".format(batch_idx)
        log_result_file = os.path.join(configs["log_base_dir"], "impute_batch_{}_RESULT.txt".format(batch_idx))
        mlhc_fs.delete_if_exist(log_result_file)
        # Modified to run directly instead of using bsub
        cmd_line = ["python3", compute_script_path, "--run_mode", "LOCAL", "--batch_id", str(batch_idx)]
        # Removed bsub-specific arguments (-R, -n, -W, -J, -o)
        
        assert(" rm " not in " ".join(cmd_line))
        job_index += 1

        if not configs["dry_run"]:
            subprocess.run(cmd_line)
        else:
            print("Generated cmd line: [{}]".format(" ".join(cmd_line)))

if __name__=="__main__":
    
    parser=argparse.ArgumentParser()

    # Input paths
    parser.add_argument("--patient_batch_path", default="../data/patient_batches.pickle", help="The path of the PID-Batch map") 
    parser.add_argument("--compute_script_path", default="./timegrid_one_batch.py",help="Script to dispatch")

    # Output paths
    parser.add_argument("--log_base_dir", default="../data/logs", help="Log base directory") 

    # Parameters
    parser.add_argument("--dry_run", action="store_true", default=False, help="Dry run, do not generate any jobs")
    parser.add_argument("--mem_in_mbytes", type=int, default=5000, help="Number of MB to request per script")
    parser.add_argument("--nhours", type=int, default=4, help="Number of hours to request")

    args=parser.parse_args()
    configs=vars(args)
    
    timegrid_all_patients(configs)
    
