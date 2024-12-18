#!/bin/bash
#PJM -L rscgrp=a-pj24001724
#PJM -L vnode-core=60
#PJM --mpi proc=60
#PJM -L elapse=12:00:00
#PJM -j

source .env

# 指定するpyファイルの名前は変更すること
python_env="$REMOTE_DIR/.venv"
python_dir="$REMOTE_DIR$WORK_DIR/scripts/generate-poscars/generator_perovskite_poscar.py"
log_file="$REMOTE_DIR$WORK_DIR/scripts/generate-poscars/generator_perovskite_poscar.log"

# Ensure log directory exists
mkdir -p "$(dirname "$log_file")"

{
  echo "Starting job at $(date)"

  # Check if Python environment exists
  if [[ ! -d "$python_env" ]]; then
    echo "Python environment $python_env does not exist. Exiting."
    exit 1
  fi
  echo "Python environment $python_env found."

  # Check if Python script exists
  if [[ ! -f "$python_dir" ]]; then
    echo "Python script $python_dir does not exist. Exiting."
    exit 1
  fi
  echo "Python script $python_dir found."
} &>"$log_file" &


# .venb activate
source $python_env/bin/activate

python3 $python_dir

deactivate


count=$(ls -1 $REMOTE_DIR$WORK_DIR/structures/one_million_models/POSCARs | wc -l)
echo "POSCAR file count: $count" >> "$log_file"

first_file=$(find "$REMOTE_DIR$WORK_DIR/structures/one_million_models/POSCARs" -type f | sort -V | awk 'NR==1')
last_file=$(find $REMOTE_DIR$WORK_DIR/structures/one_million_models/POSCARs -type f | sort -V | awk 'END { print }')

echo "First file: $first_file" >> "$log_file"
echo "Last file: $last_file" >> "$log_file"

echo "Job finished at $(date)" >> "$log_file"
