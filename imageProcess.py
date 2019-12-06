import base64
def convertToString(location):
    with open(location,"rb") as file:
        imageString=base64.b64encode(file.read())
    return imageString
