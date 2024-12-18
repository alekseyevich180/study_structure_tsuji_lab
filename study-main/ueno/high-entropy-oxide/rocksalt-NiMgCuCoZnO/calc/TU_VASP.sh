#!/bin/bash
#PBS -T necmpi
#PBS -q sxs
#PBS --venode 8
#PBS -l elapstim_req=720:00:00
#PBS -jo N vasp6.4.3

set -eo pipefail

# Environment setup
LANG=C
# shellcheck disable=SC1091
source /opt/nec/ve3/nlc/3.0.0/bin/nlcvars.sh

export PATH="/uhome/a01576/syc/vasp_6.4.3_nec_240625/bin:$PATH"
export LD_LIBRARY_PATH="/uhome/a01576/syc/vasp_6.4.3_nec_240625/lib:$LD_LIBRARY_PATH"
export VE_FORT_SETBUF87=0
export NUMEXPR_MAX_THREADS=64
export NUMEXPR_NUM_THREADS=64

python_env="$HOME/anaconda3/envs/ueno/bin/python"
python_env_test="$HOME/projects/code/study/.venv/bin/python"
num_jobs=100
num_jobs_test=2
num_candidates=4
sleep_time=10
sleep_time_test=1

base_dir="$HOME/ueno/study/high-entropy-oxide/rocksalt-NiMgCuCoZnO"

results_dir="$base_dir/results/bo"
log_file="$results_dir/bo.log"
job_file="$results_dir/jobfile.txt"
template_dir="$base_dir/calc/NiMgCuCoZnO"
scripts_dir="$base_dir/scripts"
poscar_dir="$scripts_dir/generate-poscars/POSCARs"
candidates_dir="$scripts_dir/bo/index.py"
candidates_dir_random="$scripts_dir/random/index.py"

is_test=false

# Utility functions
check_directory() {
  if [[ ! -d "$1" ]]; then
    echo "$(date) Directory $1 does not exist. Exiting."
    exit 1
  fi
}

check_file() {
  if [[ ! -f "$1" ]]; then
    echo "$(date) File $1 does not exist. Exiting."
    exit 1
  fi
}

handle_error() {
  echo "$(date) $1"
  exit 1
}

vasp_job() {
  local job_id=$1
  local results_dir=$2
  local data_file="${results_dir}/data.csv"
  local result
  local energy
  local energy_check

  mpirun -np 32 /uhome/a01576/syc/vasp_6.4.3_nec_240625/bin/vasp_std >log || handle_error "Error running vasp_std for job $job_id."
  vef.pl >/dev/null 2>&1 || handle_error "Error running vef.pl for job $job_id."

  result=$(tail -1 log)
  if [[ ! $result =~ "reached required accuracy - stopping structural energy minimisation" ]]; then
    echo "$job_id $result" >>error.txt
    handle_error "Job $job_id did not reach required accuracy."
  fi
  echo "$job_id $result" >>check.txt

  energy=$(awk 'END {print $3}' fe.dat)
  echo "$job_id $energy" >>energy.txt

  energy_check=$(tail -1 fe.dat)
  echo "$job_id $energy_check" >>energy_check.txt

  awk -v id="$job_id" -v energy="$energy" -F, 'BEGIN {OFS = FS} $1 == id {$(NF) = energy} 1' "$data_file" >tmp && mv tmp "$data_file"

  echo "$job_id" >>"$job_file"
}

# Get options from environment variable
if [ -n "${ARGS:-}" ]; then
  set -- "$ARGS"
  while getopts "tr" opt; do
    case $opt in
    t)
      is_test=true
      python_env=$python_env_test
      num_jobs=$num_jobs_test
      sleep_time=$sleep_time_test
      ;;
    r)
      candidates_dir=$candidates_dir_random
      results_dir="$base_dir/results/random"
      log_file="$results_dir/random.log"
      job_file="$results_dir/jobfile.txt"
      ;;
    \?)
      echo "$(date) Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    esac
  done
fi

# Ensure log directory exists
mkdir -p "$(dirname "$log_file")"

{
  echo "$(date) Starting job"

  # Initialize conda for the current shell
  # shellcheck disable=SC1091
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
  echo "$(date) Conda initialized"

  if ! $is_test; then
    conda activate ueno
  fi

  # Check if required directories and files exist
  check_directory "$base_dir"
  if [[ ! -d "$results_dir" ]]; then
    echo "$(date) Results directory $results_dir does not exist. Creating it."
    mkdir -p "$results_dir"
  fi
  check_directory "$template_dir"
  check_directory "$poscar_dir"
  check_file "$candidates_dir"

  if [[ ! -f "$results_dir/data.csv" ]]; then
    cp "$scripts_dir/generate-poscars/data.csv" "$results_dir/data.csv" || handle_error "Failed to copy data.csv to $results_dir. Exiting."
  fi

  : >"$job_file"

  for i in $(seq 1 "$num_jobs"); do
    # Get the list of jobs to submit
    jobs=$($python_env "$candidates_dir" "$results_dir" "$num_candidates") || handle_error "Failed to run Python script $candidates_dir. Exiting."
    mapfile -t jobs_array <<<"$jobs"

    echo -e "\n$(date) $i Submitting jobs: ${jobs_array[*]}"

    # Submit the jobs
    for id in "${jobs_array[@]}"; do
      job_dir="$results_dir/$id"
      mkdir -p "$job_dir"

      # Copy the VASP calculation template
      cp -r "$template_dir/"* "$job_dir/" || handle_error "Failed to copy template files to $job_dir. Exiting."

      # Copy and rename the POSCAR file
      if [[ ! -f "$poscar_dir/POSCAR_$id" ]]; then
        echo "$(date) POSCAR file $poscar_dir/POSCAR_$id does not exist. Skipping job $id."
        continue
      fi
      cp "$poscar_dir/POSCAR_$id" "$job_dir/POSCAR" || handle_error "Failed to copy POSCAR file to $job_dir. Exiting."

      # Submit the job
      cd "$job_dir" || handle_error "Failed to change directory to $job_dir. Exiting."

      if $is_test; then
        bash vasp-test.sh "$id" "$results_dir" &
      else
        vasp_job "$id" "$results_dir" &
      fi

      cd - >/dev/null || handle_error "Failed to change directory back. Exiting."
    done

    while true; do
      sleep "$sleep_time"

      mapfile -t completed_ids <"$job_file"

      if [[ ${#completed_ids[@]} -ge ${#jobs_array[@]} ]]; then
        echo "$(date) $i ${completed_ids[*]} All jobs for this iteration are completed."
        break
      fi
    done

    # Remove the completed jobs from the jobfile
    : >"$job_file"
  done

  if ! $is_test; then
    conda deactivate
  fi

  echo "$(date) Job finished"
} &>"$log_file" &
