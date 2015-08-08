#Modulo falso para compatibilidad con Oe-Alliance

def getMachineBuild():
    return "gbquadplus"

def getMachineProcModel():
    return "gbquadplus"

def getMachineBrand():
    return "GigaBlue"

def getMachineName():
    return "quadplus"

def getMachineMtdKernel():
    return "mtd2"

def getMachineKernelFile():
    return "kernel.bin"

def getMachineMtdRoot():
    return "mtd0"

def getMachineRootFile():
    return "rootfs.bin"

def getMachineMKUBIFS():
    return "-m 2048 -e 126976 -c 4000"

def getMachineUBINIZE():
    return "-m 2048 -p 128KiB"

def getBoxType():
    return "gbquadplus"

def getBrandOEM():
    return "gigablue"

def getOEVersion():
    return "OE-SFteam 2.0"

def getDriverDate():
    return "20150610"

def getImageVersion():
    return "4"

def getImageBuild():
    return "1"

def getImageDistro():
    return "sfteam"

def getImageFolder():
    return "gigablue/quadplus"

def getImageFileSystem():
    return "ubi"