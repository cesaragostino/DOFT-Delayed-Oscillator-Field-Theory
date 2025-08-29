Execution Guide: From Zero to Simulation (Phase 1)
This document describes the complete process for setting up the simulation environment and running the Phase 1 experiments from a clean machine.

Step 1: Environment Setup

These steps only need to be performed once per machine.

1.1. Clone the Repository

First, download the source code from the GitHub repository.

git clone https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory.git
cd DOFT-Delayed-Oscillator-Field-Theory

1.2. Create the Conda Environment

The project uses a Conda environment to manage all Python dependencies. The environment.yml file in the project's root directory defines everything needed.

# This command will read the file and create an environment named 'doft_v12'
conda env create -f environment.yml

1.3. Activate the Environment

Once created, activate the environment to use the installed tools.

conda activate doft_v12

Note: You will need to run this command every time you open a new terminal to work on the project.

Step 2: Update Source Code for Phase 1

Before running, you must ensure your local files match the code provided for the Phase 1 experiments.

2.1. Update Simulator Code

Replace the content of the following files with the code I provided previously:

src/doft/model.py

src/doft/run_sim.py

2.2. Create Runner Script

Create the execution script scripts/run_phase1.sh.

Make sure its content is copied exactly from the code block I provided.

Step 3: Running the Phase 1 Experiments

With the environment set up and the files updated, you can now launch the simulations.

3.1. The Main Script

The `scripts/run_phase1.sh` script is the single entry point you need. It reads parameters from `configs/config_phase1.json`, handles setting variables, checks the environment, and launches the Python simulator.

3.2. CPU Execution

To run all Phase 1 simulations using your machine's CPU cores:

bash scripts/run_phase1.sh

3.3. GPU Execution

If your machine has a CUDA-compatible NVIDIA GPU and you have installed the PyTorch wheels, you can accelerate the simulation as follows:

USE_GPU=1 bash scripts/run_phase1.sh

The script will verify if a GPU is available. If not, it will notify you and proceed with the execution on the CPU.

*For a quick chaos LPC test use `bash scripts/run_quick.sh`. The script sets
the `DOFT_CONFIG` variable to a JSON file (`configs/config_chaos.json` by
default).  Any fields in that JSON are forwarded to `DOFTModel`, so you can
override parameters such as `gamma`, `grid_size`, or `dt_nondim` by editing the
file or exporting a different `DOFT_CONFIG` before invoking the script.*

3.4. Parallel Execution

To launch multiple simulations in parallel use the `*_multi.sh` wrappers:

- `scripts/run_phase1_multi.sh`
- `scripts/run_quick_multi.sh`

These are plain **Bash scripts** that shard the work across processes. There is
no accompanying `*_multi.py`; `run_phase1.sh` and `run_quick.sh` are invoked
repeatedly in the background.

Relevant environment variables:

- `PAR` – number of shards to run simultaneously (default: 4).
- `SEED_OFFSET_BASE` – base seed offset passed to the simulator (default: 0).
- `SEED_OFFSET` – per‑shard offset automatically set by the wrapper.

Example: run eight Phase 1 shards in parallel

```bash
PAR=8 bash scripts/run_phase1_multi.sh
```

3.5. Logging Step Diagnostics

To record per-integration-step diagnostics (energy terms and LPC metrics), pass
the `--log-steps` flag to `run_sim.py`.  Optionally, specify `--log-path` to
control the output file prefix:

```
python -m doft.simulation.run_sim --log-steps --log-path my_step_log
```

This creates `my_step_log.csv` and `my_step_log.json` with detailed step data.

Step 4: Results

Upon completion, the script will create a new directory inside the runs folder. The directory name will include the date and time of the run, for example: runs/phase1_run_20250825_183000.

Inside that folder, you will find the simulation artifacts (runs.csv, blocks.csv, etc.), ready for analysis.

