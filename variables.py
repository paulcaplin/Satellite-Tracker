import standardizer as st

with open("Data/satellite_data.txt", "r") as tle:
    line1 = tle.readline()
    line2 = tle.readline()

    # line 1 variables --------------------------------------------------------------------
    catalog_num = line1[2:7] # string
    #print(repr(catalog_num))

    classification = line1[7:8] # U = unclassified, C = classified, S = secret
    # string
    #print(repr(classification))

    launch_year = line1[9:11]
    # string
    #print(repr(launch_year))

    launch_num = line1[11:14]
    #print(repr(launch_num))

    int_desig = line1[14:17]
    # international designator
    #print(repr(int_desig))

    s0 = line1[18:20]
    epoch_year = int(s0)
    #print(repr(epoch_year))

    s1 = line1[20:32]
    epoch_day = float(s1)
    #print(repr(epoch_day))

    s = line1[33:43]
    firstDeriv_mm = float(s)
    # float
    #print(repr(firstDeriv_mm))

    s2 = line1[44:52]
    secondDeriv_mm = st.standardizer(s2)       
    secondDeriv_mm = float(secondDeriv_mm)
    #print(repr(secondDeriv_mm))

    s3 = line1[53:61]
    b_dragTerm = st.standardizer(s3)
    b_dragTerm = float(b_dragTerm)
    #print(repr(b_dragTerm)) 
    #print(repr(b_dragTerm))

    ephemeris_type = line1[62:63] # nearly always zero
    #print(repr(ephemeris_type))

    s4 = line1[64:68]
    element_setNum = int(s4)
    #print(repr(element_setNum))

    checksum = line1[68:69]
    #print(repr(checksum))

    # line 2 variables --------------------------------------------------------------------

    #print("\n")
    catalog_num2 = line2[2:7] # this should match line 1
    #print(repr(catalog_num2))

    s5 = line2[8:16] # degrees
    inclination = float(s5)
    #print(repr(inclination))

    s6 = line2[17:25] # degrees
    raan = float(s6)
    #print(repr(raan))

    s10 = line2[26:33] # implied leading decimal 0.0007070
    eccentricity = st.eccentricityStandardizer(s10)
    eccentricity = float(eccentricity)
    #print(repr(eccentricity))

    s7 = line2[34:42] # degrees
    argPerigree = float(s7)
    
    #print(repr(argPerigree))

    s8 = line2[43:51] # degrees
    meanAnomaly = float(s8)
    #print(repr(meanAnomaly))

    s9 = line2[52:63] # revolution per day
    meanMotion = float(s9)
    #print(repr(meanMotion))

    revNumatEpoch = line2[63:68] # revolution number at epoch
    #print(repr(revNumatEpoch))

    checksum2 = line2[68:69]
    #print(repr(checksum2))

