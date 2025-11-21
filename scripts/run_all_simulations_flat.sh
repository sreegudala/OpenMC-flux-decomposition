#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting Simulation Workflow..."

# 1. Full Source Run (e.g., Thermal Flux Reference)
python scripts/01_run_full_source_flat.py

# 2. Individual Source Decomposition Runs
python scripts/02_run_individual_sources_flat.py

echo "--- All OpenMC Simulations Queued/Finished. ---"