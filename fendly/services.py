def convertToBinaryData(file):
    # Convert digital data to binary format
    
    blobData = file.read()
    return blobData

def convertToImage(data,filename):
    with open(filename, 'wb') as file:
        file.write(data)
    return filename