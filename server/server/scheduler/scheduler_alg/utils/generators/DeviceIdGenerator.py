def generateId(apartmentNo, serialNo):
    return f"{apartmentNo:02d}{serialNo:02d}"

def getApartmentNo(id):
    return int(id[:2])

def getSerialNo(id):
    return int(id[2:])
