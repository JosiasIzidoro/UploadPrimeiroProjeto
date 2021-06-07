import usb
import numpy as np

def lt():
    dev = usb.core.find(idVendor = 0x13ba, idProduct = 0x0018)
    ep = dev[0].interfaces()[0].endpoints()[0]
    i = dev[0].interfaces()[0].bInterfaceNumber
    dev.reset()
    
    if dev.is_kernel_driver_active(i):
        dev.detach_kernel_driver(i)
        
    #dev.set_configuration()
    eaddr = ep.bEndpointAddress
    
    while True:
        
        r = dev.read(eaddr, 9600)
        print(len(r))
        print(r)
        dev.reset()
            
        r1, soma = bip(r)
        #r1 = int(r1)
        print('')
        print('Código de barra: ',r1)
        
        if soma != 0:
            
            print('Break: ', soma)
            break
    
    return r1

lt()


def bip(r):
    
    dec = []
    dec1 = []
    c = []
    soma = []
    d = {2:'', 8:'A', 9:'B', 10:'C', 11:'D', 12:'E', 13:'F', 14:'G', 15:'H',
         16:'I', 17:'J', 18:'K', 19:'L', 20:'M', 21:'N', 22:'O', 23:'P', 24:'Q',
         25:'R', 26:'S', 27:'T', 28:'U', 29:'V',
         30:1, 31:2, 32:3, 33:4, 34:5, 35:6, 36:7, 37:8, 38:9, 39:0, 40:""}
    #r = np.arange(16)
        
    x = int(len(r)/16) +1
        
    for j in range(x):
        
        y = (j * 16) - 1
        z = -16
        z = z + y
        #z = 0
        
        for i in range(len(r)):
            
            if i != y and y != -1 and i >= z:
                dec1.append(r[i])
                #print(dec1)
    
            
            if i == y:
                dec1.append(r[i])
                dec.append(dec1)
                dec1 = []
                
                break
            
    
    for i in dec:
        
        decimal = 0
        for byte in i:
            decimal += byte
            
        cod = d[decimal]
        c.append(str(cod))
        
        if type(cod) == int:
            
            soma.append(cod)
        
    print(soma)
    x = len(soma) - 1
    
    if x != -1:
    
        s = sum(soma)
        
    else:
        
        s = 0        
        print(x)
            
    c1 = ''.join(c)
    
    return c1, s



def LSerial():
    
    ser = serial.Serial('/dev/ttyACM0', 9600)	#Configurando e abrindo a porta
    
    x = []
    for i in range(7):
        
        s = ser.read()
        x.append(s)
        
    #ser.close()
    
    y = x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6]
    
    y = str(y)
    y = y.split("b'")
    y = y[1]
    y = y.split(str("'"))
    y = y[0]
    
    return y