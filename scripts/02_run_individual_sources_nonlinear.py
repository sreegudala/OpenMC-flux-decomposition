# scripts/02_run_individual_sources.py

import openmc
import sys
import os

# Set OPENMC_CROSS_SECTIONS #
#os.environ["OPENMC_CROSS_SECTIONS"] = "/path/to/cross_sections.xml"
#

# --- Add project root to path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
# --------------------------------

# 1. Import all the builder functions
from models.msrr.build_materials import get_materials_dict
from models.msrr.build_geometry import get_geometry
from src.flux_decomp.inputs import (
    get_base_settings, 
    get_flux_tallies,
    get_nonlinear_source_components # <-- Get the list of individual nonlinear sources
)

print("--- Starting 'Individual Sources' Simulation Loop ---")

# --- 2. Build the constant parts of the model ONCE ---
print("Building constant model parts (materials, geometry, etc.)...")
materials_dict = get_materials_dict()
geometry = get_geometry(materials_dict)
tallies = get_flux_tallies()

materials_collection = openmc.Materials(materials_dict.values())

# --- 3. Get the list of all sources to run ---
# This list contains ALL fuel pins and ALL annulus segments
individual_sources = get_nonlinear_source_components()
print(f"Found {len(individual_sources)} individual sources to simulate.")

base_run_dir = os.path.join(project_root, 'data', 'run_individual_sources_nonlinear')

# --- 4. Loop over each source (this is your logic) ---
for i, single_source in enumerate(individual_sources):
    # e.g., "source_0001", "source_0002", etc.
    run_name = f"source_{i+1:04d}" 
    run_dir = os.path.join(base_run_dir, run_name)
    
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
        
    print(f"\n--- Running Simulation {i+1}/{len(individual_sources)} ({run_name}) ---")
    
    # Get a fresh copy of base settings
    settings = get_base_settings() 
    
    # --- Assign only ONE source from the list ---
    settings.source = single_source
    
    # --- 5. Create model and export ALL XML files ---
    # This replaces your shutil.copy()
    # It builds the model from scratch, ensuring it's always up to date.
    model = openmc.model.Model(
        geometry=geometry, 
        materials=materials_collection, 
        settings=settings, 
        tallies=tallies
    )
    model.export_to_xml(directory=run_dir)
    print(f"Running OpenMC in {run_dir}...")
    
    # --- 6. Run without changing directory ---
    # This is much safer than os.chdir()
    # It runs the simulation *inside* the target directory.
    openmc.run(cwd=run_dir)
    
    print(f"Simulation complete for {run_name}.")

print("\nAll individual source simulations finished.")