
def elread():
    #inion
    file.seek(256, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #cz
    file.seek(192, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #nas
    file.seek(112, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #lpa
    file.seek(0, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #rpa
    file.seek(64, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)


    #coil 1
    file.seek(320, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #coil 2
    file.seek(384, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)


    #coil 3
    file.seek(488, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #coil 4
    file.seek(512, os.SEEK_SET) #24bytes
    fread(file, 3, 'd', 'd', 0)
    #coil 5
    file.seek(576, os.SEEK_SET)
    fread(file, 3, 'd', 'd', 0)