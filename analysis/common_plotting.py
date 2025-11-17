import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from openmc_cylindrical_mesh_plotter import plot_mesh_tally_phir_slice
import sys
import os

def plot_cylindrical_flux(statepoint_path):
    statepoint = openmc.StatePoint(statepoint_path)

    tally = statepoint.get_tally(name="cyl_tally")

    energy_bins = tally.find_filter(openmc.EnergyFilter).bins

    for i, energy_bin in enumerate(energy_bins):
        flux_values = tally.get_slice(
            scores=['flux'],                  # Score to extract
            filters=[openmc.EnergyFilter],    # Specify the energy filter
            filter_bins=[(energy_bin,)],      # Specify the energy bin
        )

        # Generate the plot
        plot = plot_mesh_tally_phir_slice(tally=flux_values)

        #'''
        #Plot flux graphs
        # Save the plot with a filename indicating the energy bin
        plot.figure.savefig(f"energy_bin_{i}_flux_phi_r.png")
        print(f"Saved plot for energy bin {i}: energy_bin_{i}_flux_phi_r.png")
        #'''

    statepoint.close()

def plot_phir_slice(tally_data, volumes, phi_grid, r_grid, slice_index=1):
    """
    Plots a 2D (phi, r) slice of 3D cylindrical mesh data on a polar plot.
    Normalizes the data by the volume of the mesh elements.
    """
    
    # Accept either 3D (r,phi,z) or 2D (r,phi)
    if tally_data.ndim == 3:
        data = tally_data[:, :, slice_index]
    elif tally_data.ndim == 2:
        data = tally_data
    else:
        raise ValueError("tally_data must be 2D or 3D")

    slice_volumes = volumes[:, :, slice_index].squeeze()
    # Normalize by volume
    # Use np.divide with where to avoid divide-by-zero
    data = np.divide(data, slice_volumes, where=slice_volumes!=0)

    fig, axes = plt.subplots(subplot_kw=dict(projection="polar"))

    # Get the midpoints for the contourf plot
    # The grids are the bin *edges*, so we need one fewer point
    theta = np.linspace(phi_grid[0], phi_grid[-1], len(phi_grid) - 1)
    r = np.linspace(r_grid[0], r_grid[-1], len(r_grid) - 1)

    im = axes.contourf(theta, r, data)
    fig.colorbar(im)
    return axes

def plot_phir_slice_log(tally_data, volumes, phi_grid, r_grid,
                        slice_index=1, vmin=None, vmax=None, small=1e-15):
    """
    (Log) Plots a 2D (phi, r) slice of 3D cylindrical mesh data on a polar plot.
    Normalizes the data by the volume of the mesh elements.
    """

    if tally_data.ndim == 3:
        data = tally_data[:, :, slice_index]
    elif tally_data.ndim == 2:
        data = tally_data
    else:
        raise ValueError("tally_data must be 2D or 3D")

    slice_volumes = volumes[:, :, slice_index].squeeze()
    data = data / slice_volumes
    data = np.where((np.isfinite(data)) & (data <= 0), small, data)

    valid = data[np.isfinite(data) & (data > 0)]
    if valid.size == 0:
        vmin = small; vmax = 1.0
    else:
        vmin = vmin if vmin is not None else np.nanmin(valid)
        vmax = vmax if vmax is not None else np.nanmax(valid)
    if not (np.isfinite(vmin) and np.isfinite(vmax) and vmin > 0 and vmax > vmin):
        vmin = small
        vmax = max(vmin * 10.0, (np.nanmax(valid) if valid.size else 1.0))

    fig, axes = plt.subplots(subplot_kw=dict(projection="polar"))
    theta = np.linspace(phi_grid[0], phi_grid[-1], len(phi_grid) - 1)
    r = np.linspace(r_grid[0], r_grid[-1], len(r_grid) - 1)
    norm = LogNorm(vmin=vmin, vmax=vmax)
    im = axes.contourf(theta, r, data, levels=50, norm=norm)
    fig.colorbar(im, ax=axes)
    return axes

if __name__ == "__main__":
    # --- Add project root to path ---
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(project_root)
    # --------------------------------      


    # Example usage
    statepoint_path = os.path.join(project_root, 'data', 'run_full_source_flat', "statepoint.10.h5")
    # statepoint_path = os.path.join(project_root, 'data', 'run_full_source_nonlinear', "statepoint.10.h5")
    # statepoint_path = os.path.join(project_root, 'data', 'run_individual_sources_flat', "source_0001","statepoint.10.h5")

    plot_cylindrical_flux(statepoint_path)
