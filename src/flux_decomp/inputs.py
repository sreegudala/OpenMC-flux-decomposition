import openmc
import math
import numpy as np
import sys
import os

# --- This block must run first to make 'models' and 'src' available ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
# ---------------------------------------------------------------------
from models.msrr.lattice_data import get_pin_rows

# --- Base Settings ---
def get_base_settings():
    """
    Returns the base settings for all simulations.
    NO SOURCE is defined here.
    """
    settings = openmc.Settings()
    settings.run_mode = 'fixed source'
    settings.create_fission_neutrons = False
    settings.temperature = {'method': 'interpolation'}
    settings.batches = 100
    settings.particles = 100000
    
    return settings

# --- Tallies ---
def get_flux_tallies():
    """
    Returns a tallies object for flux.
    """
    ### Cylindrical Mesh Tally ###
    tallies = openmc.Tallies()

    # Create cylindrical mesh which will be used for tally
    r_grid = np.linspace(0, 129.8, 41)  # 0 to 129.8 (end of absorber wall)
    #r_grid = np.array([])              # custom r values in each material
    #z_grid = np.linspace(-10,10,4)
    phi_grid = np.linspace(0, 2*np.pi, 96) # 96 divisions
    z_grid = np.array([-10,-9.9,9.9,10])

    origin = np.array([0,0,0])
    cyl_mesh = openmc.CylindricalMesh(r_grid, z_grid, phi_grid, origin)

    # Create mesh filter for tally
    mesh_filter = openmc.MeshFilter(cyl_mesh)

    # Define energy bins corresponding to thermal and fast energy ranges
    energy_bins = [0.0, 0.625, 20.0e6]  # eV units
    energy_filter = openmc.EnergyFilter(energy_bins)

    # Create tally to score flux and absorption rate
    tally = openmc.Tally(name='cyl_tally')
    tally.filters = [mesh_filter, energy_filter]
    tally.scores = ['flux']

    tallies.append(tally)

    return tallies

# --- FLAT Source Generation ---

def _build_flat_source_list():
    """
    Private helper function to build the complete list of
    all individual source components with FLAT (strength=1.0) distributions.
    """
    # --- Build Annulus Sources ---
    r_annulus = openmc.stats.Uniform(64.0, 65.0)
    z_annulus = openmc.stats.Uniform(-10, 10)
    num_segments = 96
    phi_increment = 2 * math.pi / num_segments
    
    annulus_sources = []
    for i in range(num_segments):
        phi_min = i * phi_increment
        phi_max = (i + 1) * phi_increment
        source = openmc.IndependentSource()
        source.space = openmc.stats.CylindricalIndependent(
            r=r_annulus,
            phi=openmc.stats.Uniform(phi_min, phi_max),
            z=z_annulus,
            origin=(0.0, 0.0, 0.0)
        )
        source.angle = openmc.stats.Isotropic()
        source.energy = openmc.stats.Watt(a=0.988, b=2.249)
        source.strength = 1.0  # Flat strength
        annulus_sources.append(source)
    
    # --- Build Fuel Pin Sources ---
    rows = get_pin_rows() 
    
    r = openmc.stats.Uniform(0.0, 1.508)
    r_control_rod = openmc.stats.Uniform(1.9, 2.7)
    phi = openmc.stats.Uniform(0.0, 2 * math.pi)
    z = openmc.stats.Uniform(-10, 10)
    
    fuel_pin_sources = []
    for row_index, row in enumerate(rows):
        for col_index, origin in enumerate(row):
            source = openmc.IndependentSource()
            
            is_control_rod = (
                (row_index == 0 and col_index == 1) or
                (row_index == 5 and col_index == 0) or
                (row_index == 5 and col_index == 9)
            )

            if is_control_rod:
                source.space = openmc.stats.CylindricalIndependent(r_control_rod, phi, z, origin)
            else:
                source.space = openmc.stats.CylindricalIndependent(r, phi, z, origin)
            
            source.angle = openmc.stats.Isotropic()
            source.energy = openmc.stats.Watt(a=0.988, b=2.249)
            source.strength = 1.0  # Flat strength
            fuel_pin_sources.append(source)
            
    return fuel_pin_sources + annulus_sources

def get_flat_source_components():
    """
    Returns a list of all individual source components
    with flat (strength=1.0) distributions.
    """
    return _build_flat_source_list()


# --- NONLINEAR Source Generation ---

# Helper function for nonlinear strength
def _compute_nonlinear_strength(x, y, L_x, L_y, alpha):
    """Computes source strength with cosine squared and linear bias."""
    cosine_x_sq = np.cos((np.pi/2) * x / L_x) ** 2
    cosine_y_sq = np.cos((np.pi/2) * y / L_y) ** 2
    linear_term =  1 + alpha * (x + L_x)
    return cosine_x_sq * cosine_y_sq * linear_term

def _build_nonlinear_source_list():
    """
    Private helper function to build the complete list of
    all individual source components with NONLINEAR strength.
    """
    # Reactor dimensions (Half-widths in x and y directions)
    L_x = 65.0  
    L_y = 65.0  
    alpha = 0.1 # Linear bias factor

    # --- Build Annulus Sources ---
    r_inner, r_outer = 64.0, 65.0
    z_annulus = openmc.stats.Uniform(-10, 10)
    num_segments = 96
    phi_increment = 2 * math.pi / num_segments
    
    annulus_sources = []
    for i in range(num_segments):
        phi_min = i * phi_increment
        phi_max = (i + 1) * phi_increment

        r_avg = (r_inner + r_outer) / 2
        phi_avg = (phi_min + phi_max) / 2
        x_annulus = r_avg * np.cos(phi_avg)
        y_annulus = r_avg * np.sin(phi_avg)

        # Compute nonlinear strength
        strength = _compute_nonlinear_strength(x_annulus, y_annulus, L_x, L_y, alpha)

        source = openmc.IndependentSource()
        source.space = openmc.stats.CylindricalIndependent(
            r=openmc.stats.Uniform(r_inner, r_outer),
            phi=openmc.stats.Uniform(phi_min, phi_max),
            z=z_annulus,
            origin=(0.0, 0.0, 0.0)
        )
        source.angle = openmc.stats.Isotropic()
        source.energy = openmc.stats.Watt(a=0.988, b=2.249)
        source.strength = strength  # Apply computed strength
        annulus_sources.append(source)

    # --- Build Fuel Pin Sources ---
    rows = get_pin_rows() 
    
    r_fuel = openmc.stats.Uniform(0.0, 1.508)
    r_control_rod = openmc.stats.Uniform(1.9, 2.7)
    phi = openmc.stats.Uniform(0.0, 2 * math.pi)
    z = openmc.stats.Uniform(-10, 10)

    fuel_pin_sources = []
    for row_index, row in enumerate(rows):
        for col_index, origin in enumerate(row):
            x_fuel, y_fuel = origin[0], origin[1] # Get x, y coordinates

            # Compute nonlinear strength
            strength = _compute_nonlinear_strength(x_fuel, y_fuel, L_x, L_y, alpha)

            source = openmc.IndependentSource()
            
            is_control_rod = (
                (row_index == 0 and col_index == 1) or
                (row_index == 5 and col_index == 0) or
                (row_index == 5 and col_index == 9)
            )

            if is_control_rod:
                source.space = openmc.stats.CylindricalIndependent(r_control_rod, phi, z, origin)
            else:
                source.space = openmc.stats.CylindricalIndependent(r_fuel, phi, z, origin)
            
            source.angle = openmc.stats.Isotropic()
            source.energy = openmc.stats.Watt(a=0.988, b=2.249)
            source.strength = strength  # Apply computed strength
            fuel_pin_sources.append(source)
            
    return fuel_pin_sources + annulus_sources

def get_nonlinear_source_components():
    """
    Returns a list of all individual source components
    with nonlinear strength.
    """
    return _build_nonlinear_source_list()