# OpenMC-flux-decomposition
Repo to analyze (SVD/POD) modes of flux from OpenMC reactor models

### 1. Prerequisites

You must have the following installed on your system:

    Python 3.8+

    OpenMC (A pre-compiled version or a reliable installation is required.)

    Nuclear Data Libraries: The OPENMC_CROSS_SECTIONS environment variable must be set to the path of your cross_sections.xml file.

### 2. Environment Setup

Clone the repository and install the required Python libraries. Since this project uses a Conda environment, we recommend installing via the `environment.yml` file for full compatibility.

```bash
# Clone the repository
git clone [https://github.com/sreegudala/openmc-flux-decomposition.git](https://github.com/sreegudala/openmc-flux-decomposition.git)
cd openmc-flux-decomposition

# Create the Conda environment using the YAML file
conda env create -f environment.yml

# Activate the new environment
conda activate openmc-flux-decomposition # (or the name specified in the .yml file)
```

## Workflow Execution

The project workflow is strictly divided into two logical stages: **Simulation (Data Generation)** and **Analysis (Interactive Decomposition)**.

### Stage 1: Generate Simulation Data

This stage executes the OpenMC calculations and generates the necessary flux data files. All output files (`.h5`, `.xml`) will be saved automatically into the `data/` directory.

Users have two ways to run the simulations:

#### Option A: Run All (Recommended)

Execute the shell script to run both the full-core and individual-source decomposition runs for the **flat source** case in the correct order:

```bash
# This script executes 01_run_full_source_flat.py and 02_run_individual_sources_flat.py
bash scripts/run_all_simulations_flat.sh
```


#### Option B: Run Individually

```bash
# 1. Run the Full Core Simulation (Reference)
# Output saves to: data/run_full_source_flat/
python scripts/01_run_full_source_flat.py

# 2. Run the Individual Source Components (Decomposition Inputs)
# Output saves to: data/run_individual_sources_flat/source_0001/ ...
python scripts/02_run_individual_sources_flat.py
```

### Stage 2: Analysis and Visualization

Once the simulations are complete, the analysis is performed interactively in the Jupyter Notebook to load the data, perform the summation, and execute the Singular Value Decomposition (SVD).

```
# Run analysis/01_compare_decomposition.ipynb
```

Run the Notebook: Execute the cells sequentially. The notebook handles the following:

    Loading the single Full Run statepoint.

    Loading, flattening, and summing the data from all individual source statepoints.

    Creating the required flux matrices for both Thermal and Fast energy groups.

    Performing the Singular Value Decomposition (SVD) on the source matrices.

    Plotting the visual comparison of the Full Run flux versus the Summed Run flux.

