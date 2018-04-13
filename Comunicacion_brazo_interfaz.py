import serial
import matplotlib.pyplot as plt
import numpy as np

# Configuración del puerto Serial y parámetros para la impresión por pantalla
port= serial.Serial('COM4', 115200, timeout=1.0)

#plt.ion()                                                                                           #Esto indica de manera indirecta que vamos a tener un gráfico interactivo
y1 = []
y2 = []
y3 = []
plt.ylim(0, 3.5)
plt.xlim(0, 100)

port.set_buffer_size(5, 1)

# Si, al crear el objeto, el puerto no esta abierto: lo abrimos con el metodo
#port.open() #Para mi estaba abierto el puerto serial
port.flushInput()                                                                                   # Limpiamos lo que haya podido estar en el Buffer



with port:
    while True: #Mientras el puerto reciba información

        ch = port.read(5)                                                                           # Lee n número de bytes. 3 para nuestro caso

        #Extracción de datos del protocolo de comunicación

        p1 = format((ch[1] & 31) ,'05b')   # Hacemos and con 31 para extraer los 5 bits que nos interesan

        p2 = format((ch[2] & 127),'07b')    # Hacemos and con 127 para extraer los 7 bits que nos interesan

        p3 = format((ch[3] & 31) ,'05b')   # Hacemos and con 31 para extraer los 5 bits que nos interesan

        p4 = format((ch[4] & 127),'07b')   # Hacemos and con 31 para extraer los 5 bits que nos interesan

        D1 = format((ch[1] & 64) ,'07b')   # Hacemos and con  para extraer el bit del canal digital que nos interesan

        mensaje_1 = p1 + p2                 # Super caiman esta manera de concatenar binarios, pero así es Python

        mensaje_2 = p3 + p4  # Super caiman esta manera de concatenar binarios, pero así es Python

        mensaje_1int = int(mensaje_1, 2)*(3/4095) # llevamos el valor medido al valor de voltaje equivalente POTENCIOMETRO

        mensaje_2int = int(mensaje_2, 2)*(3/4095)#int(mensaje_2, 2)*(7/4095)  # llevamos el valor medido al valor de voltaje equivalente SHARP

        mensaje_3int = int(D1, 2)*(3/64)

        print(D1)


        #if len(y)%20 is 0:
        print(mensaje_2) #Esto solo pra visualizar el voltaje medido en consola
            #port.reset_input_buffer()

        #Graficar la señal
        #if len(y) % 100 is 0:
        y1.append(mensaje_1int)
        y2.append(mensaje_2int)
        y3.append(mensaje_3int)


        plt.plot(y1,'b')
        plt.hold
        plt.plot(y2,'r')
        plt.hold
        plt.plot(y3, 'g')
        plt.pause(0.00000000000000000001)

        if len(y1) is 100:
                y1.clear()
                y2.clear()
                y3.clear()
                port.reset_input_buffer()
                plt.clf()
                plt.ylim(0, 3.5)
                plt.xlim(0, 100)


