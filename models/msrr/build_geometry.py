import openmc
import math
import numpy as np
import matplotlib.pyplot as plt

def get_geometry(materials_dict):
    """
    Returns an openmc.Geometry object for the MSRR model.
    
    Parameters:
    -----------
    materials_dict : dict
        A dictionary of openmc.Material objects
    """

    # --- Extract materials from the dictionary ---
    # This is now correct, as materials_dict is a dict
    fuel = materials_dict['fuel']
    mod = materials_dict['mod']
    steel = materials_dict['steel']
    absorber = materials_dict['absorber']
    helium = materials_dict['helium']
    steel_cold = materials_dict['steel_cold']
    air_hot = materials_dict['air_hot']
    kaowool = materials_dict['kaowool']
    air_cold = materials_dict['air_cold']
    Al6061 = materials_dict['Al6061']
    HDPE = materials_dict['HDPE']
    M1Concrete = materials_dict['M1Concrete']


    ### Define Geometry ###

    # Define all the z planes
    bottom_plane = openmc.ZPlane(z0=0, boundary_type = 'vacuum')
    containment_vessel_plenum_plane = openmc.ZPlane(z0=2)
    plenum_grid_plate_plane = openmc.ZPlane(z0=11.920061973333334)
    grid_plate_fuel_channel_plane = openmc.ZPlane(z0=20.920061973333334)
    fuel_channel_upper_head_plane = openmc.ZPlane(z0=157.84884763)
    upper_plenum_top = openmc.ZPlane(z0=159.84884763)
    top_plane = openmc.ZPlane(z0=161.84884763, boundary_type = 'vacuum')



    # Define the hex plane
    pitch = 10.16
    hex_lat = openmc.model.HexagonalPrism(edge_length=10*pitch/(math.sqrt(3)), orientation='x', origin=(0.0, 0.0))

    # Define the radius of the fuel pincell in the grid plate
    grid_plate_r_pin = openmc.ZCylinder(r=4.26735617756927)

    # Define the radius of the fuel pincell in the fuel channel
    fuel_channel_r_pin = openmc.ZCylinder(r=1.508)

    # Define the 2D fuel cell
    graphite_region_2D = -hex_lat & +fuel_channel_r_pin
    fuel_region_2D = -fuel_channel_r_pin
    fuel_channel_graphite_cell_2D = openmc.Cell(fill=mod, region=graphite_region_2D)
    fuel_channel_fuel_cell_2D = openmc.Cell(fill=fuel, region=fuel_region_2D)

    fuel_pin_universe = openmc.Universe(cells=(fuel_channel_graphite_cell_2D,fuel_channel_fuel_cell_2D))

    # Geometry for the control rod
    pitch = 10.16
    hex_lat = openmc.model.HexagonalPrism(edge_length=10*pitch/(math.sqrt(3)), orientation='x', origin=(0.0, 0.0))
    fuel_or = openmc.ZCylinder(r=2.7)
    steel_or = openmc.ZCylinder(r=1.9)
    helium_or = openmc.ZCylinder(r=1.7)
    absorber_or = openmc.ZCylinder(r=1.5)

    graphite_region_2D_cr = -hex_lat & +fuel_or
    fuel_region_2D_cr = -fuel_or & +steel_or
    steel_region_2D_cr = -steel_or & +helium_or
    helium_region_2D_cr = -helium_or & +absorber_or
    absorber_region_2D_cr = -absorber_or

    cr_graphite_cell_2D = openmc.Cell(fill=mod, region = graphite_region_2D_cr)
    cr_fuel_cell_2D = openmc.Cell(fill=fuel, region=fuel_region_2D_cr)
    cr_steel_cell_2D = openmc.Cell(fill=steel, region=steel_region_2D_cr)
    cr_helium_cell_2D = openmc.Cell(fill=helium, region=helium_region_2D_cr)
    cr_absorber_cell_2D = openmc.Cell(fill=helium, region=absorber_region_2D_cr)

    control_rod_pin_universe = openmc.Universe(cells=(cr_graphite_cell_2D,cr_fuel_cell_2D,cr_steel_cell_2D,cr_helium_cell_2D,cr_absorber_cell_2D))

    # Graphite pin
    pitch = 10.16
    hex_lat = openmc.model.HexagonalPrism(edge_length=10*pitch/(math.sqrt(3)), orientation='x', origin=(0.0, 0.0), boundary_type='transmission')
    graphite_pin_region = -hex_lat
    graphite_pin_cell = openmc.Cell(fill=mod, region=graphite_pin_region)

    graphite_pin_universe = openmc.Universe(cells=(graphite_pin_cell,))

    all_graphite_cell = openmc.Cell(fill=mod)
    outer_universe = openmc.Universe(cells=(all_graphite_cell,))


    # Define assembly
    lattice = openmc.HexLattice()
    lattice.center = (0., 0.)
    lattice.pitch = (10.16,)
    lattice.outer = outer_universe

    # Set pins in assembly
    outer_ring = [graphite_pin_universe]*36 # Adds up to 36
    outer_ring[21] = fuel_pin_universe
    outer_ring[22] = fuel_pin_universe
    outer_ring[26] = fuel_pin_universe
    outer_ring[27] = control_rod_pin_universe
    outer_ring[28] = fuel_pin_universe
    outer_ring[32] = fuel_pin_universe
    outer_ring[33] = fuel_pin_universe

    ring_1 = [graphite_pin_universe] + [fuel_pin_universe]*29 # Adds up to 30
    ring_1[4] = graphite_pin_universe
    ring_1[5] = graphite_pin_universe
    ring_1[6] = graphite_pin_universe
    ring_1[9] = graphite_pin_universe
    ring_1[10] = graphite_pin_universe
    ring_1[11] = graphite_pin_universe
    ring_1[15] = graphite_pin_universe
    ring_1[16] = control_rod_pin_universe
    ring_1[29] = control_rod_pin_universe

    ring_2 = [fuel_pin_universe]*24 # Adds up to 24
    ring_3 = [fuel_pin_universe]*18 # Adds up to 18
    ring_4 = [fuel_pin_universe]*12 # Adds up to 12
    ring_5 = [fuel_pin_universe]*6 # Adds up to 6

    inner_ring = [fuel_pin_universe]

    lattice.universes = [outer_ring, ring_1, ring_2, ring_3, ring_4, ring_5, inner_ring]
    lattice.orientation = 'x'
    lattice.center = (0.0, -5.865878734966597)

    # Create Geometry and set root Universe
    graphite_block_surface = openmc.ZCylinder(r=64.0)
    inner_vessel_wall = openmc.ZCylinder(r=65.0)
    outer_vessel_wall = openmc.ZCylinder(r=67)

    # Create vessel cells
    main_cell = openmc.Cell(fill=lattice, region=-graphite_block_surface)
    fuel_cell = openmc.Cell(fill=fuel, region=(-inner_vessel_wall & +graphite_block_surface))
    steel_cell = openmc.Cell(fill=steel, region=(-outer_vessel_wall & +inner_vessel_wall))

    # Containment walls
    hot_air_wall = openmc.ZCylinder(r=88.9)
    steel1_wall = openmc.ZCylinder(r=89.5)
    kaowool_wall = openmc.ZCylinder(r=102.2)
    cold_air1_wall = openmc.ZCylinder(r=114.9)
    Al1_wall = openmc.ZCylinder(r=115.5)
    HDPE_wall = openmc.ZCylinder(r=128.2)
    Al2_wall = openmc.ZCylinder(r=128.5)
    absorber_wall = openmc.ZCylinder(r=129.8)
    Al3_wall = openmc.ZCylinder(r=130.4)
    cold_air2_wall = openmc.ZCylinder(r=152.4)
    steel2_wall = openmc.ZCylinder(r=154.94)
    cold_air3_wall = openmc.ZCylinder(r=170.18)
    M1Concrete_wall = openmc.model.RectangularPrism(width=457.2,height=457.2,boundary_type='vacuum')

    # Containment cells
    hot_air_cell = openmc.Cell(fill=air_hot, region=(-hot_air_wall & +outer_vessel_wall))
    steel1_cell = openmc.Cell(fill=steel, region=(-steel1_wall & +hot_air_wall))
    kaowool_cell = openmc.Cell(fill=kaowool, region=(-kaowool_wall & +steel1_wall))
    cold_air1_cell = openmc.Cell(fill=air_cold, region=(-cold_air1_wall & +kaowool_wall))
    Al1_cell = openmc.Cell(fill=Al6061, region=(-Al1_wall & +cold_air1_wall))
    HDPE_cell = openmc.Cell(fill=HDPE, region=(-HDPE_wall & +Al1_wall))
    Al2_cell = openmc.Cell(fill=Al6061, region=(-Al2_wall & +HDPE_wall))
    absorber_cell = openmc.Cell(fill=absorber, region=(-absorber_wall & +Al2_wall))
    Al3_cell = openmc.Cell(fill=Al6061, region=(-Al3_wall & +absorber_wall))
    cold_air2_cell = openmc.Cell(fill=air_cold, region=(-cold_air2_wall & +Al3_wall))
    steel2_cell = openmc.Cell(fill=steel, region=(-steel2_wall & +cold_air2_wall))
    cold_air3_cell = openmc.Cell(fill=air_cold, region=(-cold_air3_wall & +steel2_wall))
    M1Concrete_cell = openmc.Cell(fill=M1Concrete, region=(-M1Concrete_wall & +cold_air3_wall))

    # Create universe
    main_universe = openmc.Universe(cells=(main_cell,fuel_cell, steel_cell, hot_air_cell, steel1_cell, kaowool_cell, cold_air1_cell, Al1_cell, HDPE_cell, Al2_cell, absorber_cell, Al3_cell, cold_air2_cell, steel2_cell, cold_air3_cell, M1Concrete_cell))
    #main_universe.plot(origin = [0,0,0], width=(500, 500), pixels=(1000,1000), color_by ='material')

    # Export universe to geometry file
    geometry = openmc.Geometry(main_universe)
    return geometry
