from inc_noesis import *


def registerNoesisTypes():
    handle = noesis.register("Venom Codename Outbtreak images", ".mt")
    noesis.setHandlerLoadRGBA(handle, itdLoadRGBA)
    noesis.setHandlerTypeCheck(handle, itdCheckType)
    
    return 1


class MTImage:
    def __init__(self, reader):
        self.reader = reader
        self.width = 0
        self.height = 0
        self.type = 0 
        self.data = None     
        self.palette = None     
        
    def readHeader(self):
        self.reader.seek(12)
        
    def readData(self):
        self.width = self.reader.readUShort()
        self.height = self.reader.readUShort()
        self.type = self.reader.readUShort()
        
        if self.type == 8:
            self.palette = self.reader.readBytes(768)
            self.data = self.reader.readBytes(self.width * self.height)
        else:
            self.data = self.reader.readBytes(self.width * self.height * (self.type >> 3))       
    
    def read(self):
        self.readHeader()    
        self.readData()
        
        
def itdCheckType(data):
    #
    return 1
    
    
def itdLoadRGBA(data, texList):   
    image = MTImage(NoeBitStream(data))       
    image.read()

    if image.type == 8:
        data = rapi.imageDecodeRawPal(image.data, image.palette, image.width, image.height, 8, "b8g8r8")
        texList.append(NoeTexture(os.path.basename(rapi.getInputName()), image.width, image.height, data, noesis.NOESISTEX_RGBA32))         
    else:
        #data = rapi.imageDecodeRaw(data, image.width, image.height, "r8g8b8p8")    
        texList.append(NoeTexture(os.path.basename(rapi.getInputName()), image.width, image.height, data, noesis.NOESISTEX_RGBA32)) 
                   
    return 1

