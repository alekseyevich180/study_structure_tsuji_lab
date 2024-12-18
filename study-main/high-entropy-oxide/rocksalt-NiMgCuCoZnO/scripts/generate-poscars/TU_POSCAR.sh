#!/bin/bash
#PBS -T necmpi
#PBS -q sxs
#PBS --venode 2
#PBS -l elapstim_req=6:00:00

LANG=C

python_env="$HOME/anaconda3/envs/ueno/bin/python"
python_dir="$HOME/ueno/study/high-entropy-oxide/rocksalt-NiMgCuCoZnO/scripts/generate-poscars/generate_nacl_poscar.py"
log_file="$HOME/ueno/study/high-entropy-oxide/rocksalt-NiMgCuCoZnO/scripts/generate-poscars/generate_nacl_poscar.log"

# Ensure log directory exists
mkdir -p "$(dirname "$log_file")"

{
  echo "Starting job at $(date)"

  # Check if Python environment exists
  if [[ ! -f "$python_env" ]]; then
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

  # Initialize conda for the current shell
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
  echo "Conda initialized."

  # Activate conda environment
  conda activate ueno || {
    echo "Failed to activate conda environment"
    exit 1
  }
  echo "Conda environment activated."

  # Run Python script
  $python_env $python_dir || {
    echo "Failed to execute Python script"
    exit 1
  }
  echo "Python script executed successfully."

  # Deactivate conda environment
  conda deactivate || {
    echo "Failed to deactivate conda environment"
    exit 1
  }
  echo "Conda environment deactivated."

  echo "Job finished at $(date)"
} &>"$log_file" &
