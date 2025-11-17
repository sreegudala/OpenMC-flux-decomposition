import openmc

def get_materials_dict():
    """
    Returns a DICTIONARY of all materials, keyed by name for the MSRR model.
    """
    
    ### Define Materials ###

    fuel_N = 3.60023497372237E-06+3.43781777753314E-04+1.63974929875485E-06+1.37407724198127E-03+2.38322492560063E-06+2.31469771314323E-02+4.92106581865012E-02+9.58536509526980E-03
    U234_atom_percent = 3.60023497372237E-06/fuel_N
    U235_atom_percent = 3.43781777753314E-04/fuel_N
    U236_atom_percent = 1.63974929875485E-06/fuel_N
    U238_atom_percent = 1.37407724198127E-03/fuel_N
    Li6_atom_percent = 2.38322492560063E-06/fuel_N
    Li7_atom_percent = 2.31469771314323E-02/fuel_N
    F19_atom_percent = 4.92106581865012E-02/fuel_N
    Be9_atom_percent = 9.58536509526980E-03/fuel_N

    mod_N = 9.02514751641051E-02+3.61006622669666E-08+1.44402649067866E-07
    graphite_atom_percent = 9.02514751641051E-02/mod_N
    B10_atom_percent = 3.61006622669666E-08/mod_N
    B11_atom_percent = 1.44402649067866E-07/mod_N

    steel_N = 1.644496609239440E-04+8.696790489283100E-04+3.574616313767830E-05+2.250363781064500E-05+1.575133473310780E-02+8.892399033329480E-04+5.771412781597680E-02+9.849928822172420E-03+1.255356780021520E-03
    C_atom_percent = 1.644496609239440E-04/steel_N
    Si_atom_percent = 8.696790489283100E-04/steel_N
    P31_atom_percent = 3.574616313767830E-05/steel_N
    S_atom_percent = 2.250363781064500E-05/steel_N
    Cr_atom_percent = 1.575133473310780E-02/steel_N
    Mn55_atom_percent = 8.892399033329480E-04/steel_N
    Fe_atom_percent = 5.771412781597680E-02/steel_N
    Ni_atom_percent = 9.849928822172420E-03/steel_N
    Mo_atom_percent = 1.255356780021520E-03/steel_N


    control_rod_absorber_N = 2.064131901926640E-02+2.174197622320780E-04+8.936540784419590E-06+5.625909452661240E-06+3.937833683276960E-03+2.223099758332370E-04+1.442853195399420E-02+2.462482205543100E-03+3.138391950053790E-04+1.648016528322840E-02+6.592066113291350E-02
    C_absorber_atom_percent = 2.064131901926640E-02/control_rod_absorber_N
    Si_absorber_atom_percent = 2.174197622320780E-04/control_rod_absorber_N
    P31_absorber_atom_percent = 8.936540784419590E-06/control_rod_absorber_N
    S_absorber_atom_percent = 5.625909452661240E-06/control_rod_absorber_N
    Cr_absorber_atom_percent = 3.937833683276960E-03/control_rod_absorber_N
    Mn55_absorber_atom_percent = 2.223099758332370E-04/control_rod_absorber_N
    Fe_absorber_atom_percent = 1.442853195399420E-02/control_rod_absorber_N
    Ni_absorber_atom_percent = 2.462482205543100E-03/control_rod_absorber_N
    Mo_absorber_atom_percent = 3.138391950053790E-04/control_rod_absorber_N
    B10_absorber_atom_percent = 1.648016528322840E-02/control_rod_absorber_N
    B11_absorber_atom_percent = 6.592066113291350E-02/control_rod_absorber_N

    helium_N = 8.275064807874880E-06

    air_N = 7.48287061985493E-09+3.89895472505582E-05+1.42423970797905E-07+1.05133334492879E-05+7.98172866117859E-10+1.49657412397099E-10+2.32068760823767E-07
    C12_air_atom_percent = 7.48287061985493E-09/air_N
    N14_air_atom_percent = 3.89895472505582E-05/air_N
    N15_air_atom_percent = 1.42423970797905E-07/air_N
    O16_air_atom_percent = 1.05133334492879E-05/air_N
    Ar36_air_atom_percent = 7.98172866117859E-10/air_N
    Ar38_air_atom_percent = 1.49657412397099E-10/air_N
    Ar40_air_atom_percent = 2.32068760823767E-07/air_N

    kaowool_N = 4.45098760453152E-07+1.77092485541999E-06+3.01200225235927E-03+8.50631082157937E-04+8.35942823062983E-04+1.71883883026058E-06+2.05124237264155E-05+1.20697525573945E-05
    B10_kaowool_atom_percent = 4.45098760453152E-07/kaowool_N
    B11_kaowool_atom_percent = 1.77092485541999E-06/kaowool_N
    O16_kaowool_atom_percent = 3.01200225235927E-03/kaowool_N
    Al27_kaowool_atom_percent = 8.50631082157937E-04/kaowool_N
    Si_kaowool_atom_percent = 8.35942823062983E-04/kaowool_N
    Ca_kaowool_atom_percent = 1.71883883026058E-06/kaowool_N
    Ti_kaowool_atom_percent = 2.05124237264155E-05/kaowool_N
    Fe_kaowool_atom_percent = 1.20697525573945E-05/kaowool_N

    Al6061_N = 6.68978726858390E-04+5.85745954333342E-02+3.47375085188249E-04+2.99068611989193E-05+6.09524605998014E-05+2.60711114659917E-05+1.19088042489484E-04+7.03620341633892E-05+3.63197552836575E-05
    Mg_Al_atom_percent = 6.68978726858390E-04/Al6061_N
    Al27_Al_atom_percent = 5.85745954333342E-02/Al6061_N
    Si_Al_atom_percent = 3.47375085188249E-04/Al6061_N
    Ti_Al_atom_percent = 2.99068611989193E-05/Al6061_N
    Cr_Al_atom_percent = 6.09524605998014E-05/Al6061_N
    Mn55_Al_atom_percent = 2.60711114659917E-05/Al6061_N
    Fe_Al_atom_percent = 1.19088042489484E-04/Al6061_N
    Cu_Al_atom_percent = 7.03620341633892E-05/Al6061_N
    Zn_Al_atom_percent = 3.63197552836575E-05/Al6061_N

    HDPE_N = 8.07151005586064E-02+4.03575502793032E-02
    H1_HDPE_atom_percent = 8.07151005586064E-02/HDPE_N
    C_HDPE_atom_percent = 4.03575502793032E-02/HDPE_N

    M1Concrete_N = 2.15113796480411E-02+4.87163168531722E-04+1.77229497193753E-03+1.81286419103555E-02+4.79442190824933E-03+1.60520211434857E-03+1.47982884539238E-04+7.43789534407904E-04+3.87241608251410E-02
    H1_concrete_atom_percent = 2.15113796480411E-02/M1Concrete_N
    B10_concrete_atom_percent = 4.87163168531722E-04/M1Concrete_N
    B11_concrete_atom_percent = 1.77229497193753E-03/M1Concrete_N
    O16_concrete_atom_percent = 1.81286419103555E-02/M1Concrete_N
    Mg_concrete_atom_percent = 4.79442190824933E-03/M1Concrete_N
    Cl_concrete_atom_percent = 1.60520211434857E-03/M1Concrete_N
    Mn55_concrete_atom_percent = 1.47982884539238E-04/M1Concrete_N
    Ca_concrete_atom_percent = 7.43789534407904E-04/M1Concrete_N
    Fe_concrete_atom_percent = 3.87241608251410E-02/M1Concrete_N


    fuel = openmc.Material(name='fuel',temperature=873.15)
    fuel.add_nuclide('U234', U234_atom_percent)
    fuel.add_nuclide('U235', U235_atom_percent)
    fuel.add_nuclide('U236', U236_atom_percent)
    fuel.add_nuclide('U238', U238_atom_percent)
    fuel.add_nuclide('Li6', Li6_atom_percent)
    fuel.add_nuclide('Li7', Li7_atom_percent)
    fuel.add_nuclide('F19', F19_atom_percent)
    fuel.add_nuclide('Be9', Be9_atom_percent)
    fuel.set_density('atom/b-cm', fuel_N)

    mod = openmc.Material(name='mod',temperature=873.15)
    mod.add_nuclide('C0', graphite_atom_percent)
    mod.add_s_alpha_beta('c_Graphite')
    mod.add_nuclide('B10',B10_atom_percent)
    mod.add_nuclide('B11',B11_atom_percent)
    mod.set_density('atom/b-cm', mod_N)

    steel = openmc.Material(name='steel',temperature=873.15)
    steel.add_element('C', C_atom_percent)
    steel.add_element('Si', Si_atom_percent)
    steel.add_nuclide('P31', P31_atom_percent)
    steel.add_element('S', S_atom_percent)
    steel.add_element('Cr', C_atom_percent)
    steel.add_nuclide('Mn55', Mn55_atom_percent)
    steel.add_element('Fe', Fe_atom_percent)
    steel.add_element('Ni', Ni_atom_percent)
    steel.add_element('Mo', Mo_atom_percent)
    steel.set_density('atom/b-cm', steel_N)

    absorber = openmc.Material(name='absorber',temperature=873.15)
    absorber.add_element('C', C_absorber_atom_percent)
    absorber.add_element('Si', Si_absorber_atom_percent)
    absorber.add_nuclide('P31', P31_absorber_atom_percent)
    absorber.add_element('S', S_absorber_atom_percent)
    absorber.add_element('Cr', C_absorber_atom_percent)
    absorber.add_nuclide('Mn55', Mn55_absorber_atom_percent)
    absorber.add_element('Fe', Fe_absorber_atom_percent)
    absorber.add_element('Ni', Ni_absorber_atom_percent)
    absorber.add_element('Mo', Mo_absorber_atom_percent)
    absorber.add_nuclide('B10',B10_absorber_atom_percent)
    absorber.add_nuclide('B11',B11_absorber_atom_percent)
    absorber.set_density('atom/b-cm', control_rod_absorber_N)

    helium = openmc.Material(name='helium',temperature=873.15)
    helium.add_element('He', 1.00)

    steel_cold = openmc.Material(name='steel_cold',temperature=300)
    steel_cold.add_element('C', C_atom_percent)
    steel_cold.add_element('Si', Si_atom_percent)
    steel_cold.add_nuclide('P31', P31_atom_percent)
    steel_cold.add_element('S', S_atom_percent)
    steel_cold.add_element('Cr', C_atom_percent)
    steel_cold.add_nuclide('Mn55', Mn55_atom_percent)
    steel_cold.add_element('Fe', Fe_atom_percent)
    steel_cold.add_element('Ni', Ni_atom_percent)
    steel_cold.add_element('Mo', Mo_atom_percent)
    steel_cold.set_density('atom/b-cm', steel_N)

    air_hot = openmc.Material(name='air_hot',temperature=873.15)
    air_hot.add_element('C', C12_air_atom_percent)                         # air_cold.add_nuclide('C12', C12_air_atom_percent) isn't working
    air_hot.add_nuclide('N14', N14_air_atom_percent)
    air_hot.add_nuclide('N15', N15_air_atom_percent)
    air_hot.add_nuclide('O16', O16_air_atom_percent)
    air_hot.add_nuclide('Ar36', Ar36_air_atom_percent)
    air_hot.add_nuclide('Ar38', Ar38_air_atom_percent)
    air_hot.add_nuclide('Ar40', Ar40_air_atom_percent)
    air_hot.set_density('atom/b-cm', air_N)

    kaowool = openmc.Material(name='kaowool',temperature=300)
    kaowool.add_nuclide('B10', B10_kaowool_atom_percent)
    kaowool.add_nuclide('B11', B11_kaowool_atom_percent)
    kaowool.add_nuclide('O16', O16_kaowool_atom_percent)
    kaowool.add_nuclide('Al27', Al27_kaowool_atom_percent)
    kaowool.add_element('Si', Si_kaowool_atom_percent)
    kaowool.add_element('Ca', Ca_kaowool_atom_percent)
    kaowool.add_element('Ti', Ti_kaowool_atom_percent)
    kaowool.add_element('Fe', Fe_kaowool_atom_percent)
    kaowool.set_density('atom/b-cm',kaowool_N)

    air_cold = openmc.Material(name='air_cold',temperature=300)
    air_cold.add_element('C', C12_air_atom_percent)                         # air_cold.add_nuclide('C12', C12_air_atom_percent) isn't working
    air_cold.add_nuclide('N14', N14_air_atom_percent)
    air_cold.add_nuclide('N15', N15_air_atom_percent)
    air_cold.add_nuclide('O16', O16_air_atom_percent)
    air_cold.add_nuclide('Ar36', Ar36_air_atom_percent)
    air_cold.add_nuclide('Ar38', Ar38_air_atom_percent)
    air_cold.add_nuclide('Ar40', Ar40_air_atom_percent)
    air_cold.set_density('atom/b-cm', air_N)

    Al6061 = openmc.Material(name="Al6061",temperature=300)
    Al6061.add_element('Mg', Mg_Al_atom_percent)
    Al6061.add_nuclide('Al27', Al27_Al_atom_percent)
    Al6061.add_element('Si', Si_Al_atom_percent)
    Al6061.add_element('Ti', Ti_Al_atom_percent)
    Al6061.add_element('Cr', Cr_Al_atom_percent)
    Al6061.add_nuclide('Mn55', Mn55_Al_atom_percent)
    Al6061.add_element('Fe', Fe_Al_atom_percent)
    Al6061.add_element('Cu', Cu_Al_atom_percent)
    Al6061.add_element('Zn', Zn_Al_atom_percent)
    Al6061.set_density('atom/b-cm', Al6061_N)

    HDPE = openmc.Material(name='HDPE',temperature=300)
    HDPE.add_nuclide('H1', H1_HDPE_atom_percent)
    HDPE.add_element('C', C_HDPE_atom_percent)
    HDPE.set_density('atom/b-cm', HDPE_N)

    M1Concrete = openmc.Material(name='M1Concrete',temperature=300)
    M1Concrete.add_nuclide('H1', H1_concrete_atom_percent)
    M1Concrete.add_nuclide('B10', B10_concrete_atom_percent)
    M1Concrete.add_nuclide('B11', B11_concrete_atom_percent)
    M1Concrete.add_nuclide('O16', O16_concrete_atom_percent)
    M1Concrete.add_element('Mg', Mg_concrete_atom_percent)
    M1Concrete.add_element('Cl', Cl_concrete_atom_percent)
    M1Concrete.add_nuclide('Mn55', Mn55_concrete_atom_percent)
    M1Concrete.add_element('Ca', Ca_concrete_atom_percent)
    M1Concrete.add_element('Fe', Fe_concrete_atom_percent)
    M1Concrete.set_density('atom/b-cm', M1Concrete_N)

    # --- Create and return a dictionary ---
    materials_dict = {
        'fuel': fuel,
        'mod': mod,
        'steel': steel,
        'absorber': absorber,
        'helium': helium,
        'steel_cold': steel_cold,
        'air_hot': air_hot,
        'kaowool': kaowool,
        'air_cold': air_cold,
        'Al6061': Al6061,
        'HDPE': HDPE,
        'M1Concrete': M1Concrete
    }
    
    return materials_dict