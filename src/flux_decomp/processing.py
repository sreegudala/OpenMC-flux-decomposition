import openmc
import numpy as np
import os
import sys

def load_tally_data(statepoint_path, tally_name='cyl_tally', value_type='mean', mesh=False):
    """
    Load tally data from an OpenMC statepoint file.
    Parameters: 
        statepoint_path (str): Path to the OpenMC statepoint file.
        tally_name (str): Name of the tally to extract.
        value_type (str): Type of tally value to extract ('mean', 'std_dev', etc.).
        mesh (bool): Whether to return the mesh object along with the data.
    Returns:
        np.ndarray: Reshaped tally data array with dimensions (R, Phi, Z, Energy).
        openmc.Mesh (optional): The mesh object if mesh=True.
    """

    statepoint = openmc.StatePoint(statepoint_path)
    tally = statepoint.get_tally(name=tally_name)
    statepoint.close()

    # Get the raw data (flattened)
    # Shape is (Total_Bins, Nuclides, Scores)
    if value_type == 'mean':
        raw_data = tally.mean
    elif value_type == 'std_dev':
        raw_data = tally.std_dev
    else:
        print(f"Value type '{value_type}' not recognized. Defaulting to 'mean'.")
        raw_data = tally.mean

    # Squeeze to remove single-dimensional entries (Nuclides, Scores)
    raw_data = np.squeeze(raw_data)

    # Get dimensions for reshaping
    n_energy = len(tally.find_filter(openmc.EnergyFilter).bins)
    mesh_filter = tally.find_filter(openmc.MeshFilter)
    nr, nphi, nz = mesh_filter.mesh.dimension # Retrieves the (R, Phi, Z) sizes

    # print(f"Reshaping tally data to dimensions: R={nr}, Phi={nphi}, Z={nz}, Energy={n_energy}")

    # Reshape the array
    # The new shape order should logically match: (Energy, Z, Phi, R). Removes: (Nuclides, Scores)
    shaped_data = raw_data.reshape(nr, nphi, nz, n_energy).T

    if mesh:
        return shaped_data, mesh_filter.mesh
    else:
        return shaped_data

def create_individual_source_matrices(base_dir='data/run_individual_sources_flat', tally_name='cyl_tally'):
    """
    Loads mean and standard deviation flux data from individual source simulations
    and assembles them into matrices for decomposition.
    """
    
    thermal_mean_cols = []
    thermal_stdev_cols = []
    fast_mean_cols = []
    fast_stdev_cols = []
    
    try:
        project_root = sys.path[0]
    except IndexError:
        print("ERROR: Project root not found in sys.path[0]. Did you run the setup?")
        return
    
    target_dir = os.path.join(project_root, base_dir)

    # Sort the run directories numerically to ensure the columns are in order
    run_dirs = sorted([d for d in os.listdir(target_dir) if d.startswith('source_')], 
                      key=lambda x: int(x.split('_')[-1]))

    for index, run_dir in enumerate(run_dirs):
        # NOTE: Using statepoint.100.h5 as a common placeholder
        sp_file = os.path.join(target_dir, run_dir, "statepoint.100.h5") 
        
        if os.path.isfile(sp_file):
            try:
                # Load mean and standard deviation data separately
                # Each is a list: [Thermal_3D_array, Fast_3D_array, ...]
                mean_data_list = load_tally_data(sp_file, tally_name, 'mean', False)
                stdev_data_list = load_tally_data(sp_file, tally_name, 'std_dev', False)
                
                # Check for the required energy bins (assuming 0=Thermal, 1=Fast)
                if len(mean_data_list) < 2:
                    raise ValueError(f"Statepoint in {run_dir} only has {len(mean_data_list)} energy bins. Need at least 2.")
                
                # --- Extract and Flatten ---
                # thermal_mean_col = mean_data[0]
                thermal_mean_cols.append(mean_data_list[0].flatten(order='F'))
                thermal_stdev_cols.append(stdev_data_list[0].flatten(order='F'))
                fast_mean_cols.append(mean_data_list[1].flatten(order='F'))
                fast_stdev_cols.append(stdev_data_list[1].flatten(order='F'))
            
            except Exception as e:
                print(f"Error processing {run_dir} (File: {sp_file}): {e}")
                continue
        else:
            print(f"Warning: Statepoint not found at {sp_file}")


    # Assemble thermal and fast flux matrices (N_spatial_voxels x N_sources)
    thermal_mean_matrix = np.column_stack(thermal_mean_cols) if thermal_mean_cols else np.empty((0,0))
    thermal_stdev_matrix = np.column_stack(thermal_stdev_cols) if thermal_stdev_cols else np.empty((0,0))
    fast_mean_matrix = np.column_stack(fast_mean_cols) if fast_mean_cols else np.empty((0,0))
    fast_stdev_matrix = np.column_stack(fast_stdev_cols) if fast_stdev_cols else np.empty((0,0))

    return {
        'thermal_mean': thermal_mean_matrix,
        'thermal_stdev': thermal_stdev_matrix,
        'fast_mean': fast_mean_matrix,
        'fast_stdev': fast_stdev_matrix
    }

def save_mesh_data_as_npz(mesh, file_path='data/analysis_npz_files', file_name='mesh_data.npz'):
    """
    Saves structured mesh data as a compressed NumPy .npz file in a directory
    relative to the project root (sys.path[0]).

    Args:
        mesh (openmc.Mesh): The mesh object containing the data to save.
        file_path (str): The sub-directory relative to the project root (defaults to 'data').
        file_name (str): The name of the file to save (defaults to 'mesh_data.npz').
    """
    
    try:
        project_root = sys.path[0]
    except IndexError:
        print("ERROR: Project root not found in sys.path[0]. Did you run the setup?")
        return
    
    target_dir = os.path.join(project_root, file_path)
    full_path = os.path.join(target_dir, file_name)

    os.makedirs(target_dir, exist_ok=True)

    np.savez(
        f"{full_path}",
        
        # Your mesh/plotting data
        volumes=mesh.volumes,
        phi_grid=mesh.phi_grid,
        r_grid=mesh.r_grid,
        mesh_dimension=mesh.dimension
    )
    
    print(f"Mesh data saved to {full_path}")

def save_full_source_data_as_npz(mean_tally, stdev_tally, file_path='data/analysis_npz_files', mean_file_name='full_source_mean.npz', stdev_file_name='full_source_stdev.npz'):
    """
    Saves full source tally data as a compressed NumPy .npz file in a directory
    relative to the project root (sys.path[0]).

    Args:
        mean_tally (np.ndarray): The mean tally data array to save.
        stdev_tally (np.ndarray): The standard deviation tally data array to save.
        file_path (str): The sub-directory relative to the project root (defaults to 'data').
        mean_file_name (str): The name of the mean tally file to save (defaults to 'full_source_mean.npz').
        stdev_file_name (str): The name of the standard deviation tally file to save (defaults to 'full_source_stdev.npz').
    """
    
    try:
        project_root = sys.path[0]
    except IndexError:
        print("ERROR: Project root not found in sys.path[0]. Did you run the setup?")
        return
    
    target_dir = os.path.join(project_root, file_path)
    mean_full_path = os.path.join(target_dir, mean_file_name)
    stdev_full_path = os.path.join(target_dir, stdev_file_name)

    os.makedirs(target_dir, exist_ok=True)

    np.savez(
        f"{mean_full_path}",
        
        # Your tally data
        full_source_mean=mean_tally
    )

    np.savez(
        f"{stdev_full_path}",
        
        # Your tally data
        full_source_stdev=stdev_tally
    )
    
    print(f"Full source tally data saved to {mean_full_path} and {stdev_full_path}")

def save_individual_source_matrices_as_npz(thermal_mean_matrix, fast_mean_matrix, thermal_stdev_matrix, fast_stdev_matrix, file_path='data/analysis_npz_files', thermal_mean_file_name_template='thermal_mean_matrix.npz', fast_mean_file_name_template='fast_mean_matrix.npz', thermal_stdev_file_name_template='thermal_stdev_matrix.npz', fast_stdev_file_name_template='fast_stdev_matrix.npz'):
    """
    Saves individual source tally data as a compressed NumPy .npz file in a directory
    relative to the project root (sys.path[0]).

    Args:
        thermal_mean_matrix (np.ndarray): The thermal mean tally data array to save.
        fast_mean_matrix (np.ndarray): The fast mean tally data array to save.
        thermal_stdev_matrix (np.ndarray): The thermal standard deviation tally data array to save.
        fast_stdev_matrix (np.ndarray): The fast standard deviation tally data array to save.
        file_path (str): The sub-directory relative to the project root (defaults to 'data').
        thermal_mean_file_name_template (str): The name of the thermal mean tally file to save (defaults to 'thermal_mean_matrix.npz').
        fast_mean_file_name_template (str): The name of the fast mean tally file to save (defaults to 'fast_mean_matrix.npz').
        thermal_stdev_file_name_template (str): The name of the thermal standard deviation tally file to save (defaults to 'thermal_stdev_matrix.npz').
        fast_stdev_file_name_template (str): The name of the fast standard deviation tally file to save (defaults to 'fast_stdev_matrix.npz').
    """
    
    try:
        project_root = sys.path[0]
    except IndexError:
        print("ERROR: Project root not found in sys.path[0]. Did you run the setup?")
        return
    
    target_dir = os.path.join(project_root, file_path)
    thermal_mean_full_path = os.path.join(target_dir, thermal_mean_file_name_template)
    fast_mean_full_path = os.path.join(target_dir, fast_mean_file_name_template)
    thermal_stdev_full_path = os.path.join(target_dir, thermal_stdev_file_name_template)
    fast_stdev_full_path = os.path.join(target_dir, fast_stdev_file_name_template)  
    os.makedirs(target_dir, exist_ok=True)
    np.savez(
        f"{thermal_mean_full_path}",
        
        # Your tally data
        thermal_mean_matrix=thermal_mean_matrix
    )
    np.savez(
        f"{fast_mean_full_path}",
        
        # Your tally data
        fast_mean_matrix=fast_mean_matrix
    )
    np.savez(
        f"{thermal_stdev_full_path}",
        
        # Your tally data
        thermal_stdev_matrix=thermal_stdev_matrix
    )
    np.savez(
        f"{fast_stdev_full_path}",
        
        # Your tally data
        fast_stdev_matrix=fast_stdev_matrix
    )
    print(f"Individual source tally data saved to {thermal_mean_full_path}, {fast_mean_full_path}, {thermal_stdev_full_path}, and {fast_stdev_full_path}")
