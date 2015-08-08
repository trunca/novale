#Modulo falso para compatibilidad con Oe-Alliance

def getMachineBuild():
    return "gb800ueplus"

def getMachineProcModel():
    return "gb800ueplus"

def getMachineBrand():
    return "GigaBlue"

def getMachineName():
    return "800 UE plus"

def getMachineMtdKernel():
    return "mtd2"

def getMachineKernelFile():
    return "kernel.bin"

def getMachineMtdRoot():
    return "mtd0"

def getMachineRootFile():
    return "rootfs.bin"

def getMachineMKUBIFS():
    return "-m 2048 -e 126976 -c 4096"

def getMachineUBINIZE():
    return "-m 2048 -p 128KiB"

def getBoxType():
    return "gb800ueplus"

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
    return "gigablue/ueplus"

def getImageFileSystem():
    return "ubi"