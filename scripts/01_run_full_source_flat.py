# scripts/01_run_full_source.py

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

from models.msrr.build_materials import get_materials_dict
from models.msrr.build_geometry import get_geometry
from src.flux_decomp.inputs import (
    get_base_settings, 
    get_flux_tallies,
    get_flat_source_components  # <-- We get the "full" source function
)

print("--- Starting 'Full Source (Flat)' Simulation ---")
run_dir = os.path.join(project_root, 'data', 'run_full_source_flat')
if not os.path.exists(run_dir): os.makedirs(run_dir)

# --- 1. Build Model ---
materials_dict = get_materials_dict()
geometry = get_geometry(materials_dict)
tallies = get_flux_tallies()

# --- Create the final openmc.Materials list ---
# This is the list OpenMC needs for the model
materials_collection = openmc.Materials(materials_dict.values())

# --- 2. Build Settings ---
settings = get_base_settings() # Get common settings

# --- 3. Set the specific source for this run ---
# Get the list of all source components
all_sources = get_flat_source_components()
# Assign the ENTIRE LIST as the source
settings.source = all_sources 
print(f"Assigning {len(all_sources)} source components to the full run.")

# --- 4. Export to XML and Run ---
model = openmc.model.Model(
    geometry=geometry, 
    materials=materials_collection,
    settings=settings, 
    tallies=tallies
)
model.export_to_xml(directory=run_dir)

print(f"Running OpenMC with {len(all_sources)} combined sources...")
openmc.run(cwd=run_dir)
print(f"Simulation complete. Outputs are in {run_dir}/")