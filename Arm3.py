"""Librerias para comunicación Serial"""
import serial
import matplotlib.pyplot as plt
"""Librerias para Interfaz gráfica"""
import sys
import numpy as np
import pygame
import pygame.locals
from armpart import ArmPart
import tkinter as tk
from tkinter import ttk

"""Parámetros para Comunicación Serial"""
port= serial.Serial('COM4', 115200, timeout=1.0)
port.set_buffer_size(5, 1)
port.flushInput()

"""Parametros para Pygame"""
black = (0, 0, 0)
white = (255, 255, 255)
pygame.init()
width = 850
height = 750
display = pygame.display.set_mode((width, height))
fpsClock = pygame.time.Clock()
upperarm = ArmPart('upperarm.png', scale=.7)
forearm = ArmPart('forearm.png', scale=.8)
hand = ArmPart('hand.png', scale=1.0)
origin = (width / 2, height / 2)
m = 0
n = 0


"""Funciones a utilizar"""
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    ttk.Label()
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


"""Inicio de la recepción de datos y la interfaz gráfica"""
    while True: #Mientras el puerto reciba información

        ch = port.read(5)  # Lee n número de bytes. 5 para nuestro caso

        """ Extracción de datos del protocolo de comunicación """

        p1 = format((ch[1] & 31), '05b')  # Hacemos and con 31 para extraer los 5 bits que nos interesan

        p2 = format((ch[2] & 127), '07b')  # Hacemos and con 127 para extraer los 7 bits que nos interesan

        p3 = format((ch[3] & 31), '05b')  # Hacemos and con 31 para extraer los 5 bits que nos interesan

        p4 = format((ch[4] & 127), '07b')  # Hacemos and con 31 para extraer los 5 bits que nos interesan

        D1 = format((ch[1] & 64), '07b')  # Hacemos and con  para extraer el bit del canal digital que nos interesan

        D2 = format((ch[1] & 32), '07b')  # Hacemos and con  para extraer el bit del canal digital que nos interesan

        mensaje_1 = p1 + p2  # Concatenamos los bits correspondientes al canal analógico 1

        mensaje_2 = p3 + p4  # Concatenamos los bits correspondientes al canal analógico 2

        mensaje_1int = int(mensaje_1, 2) * ( 3 / 4095)  # llevamos el valor medido al valor de voltaje equivalente Sharp

        mensaje_2int = int(mensaje_2, 2);  # Llevamos el valor medido al valor enviado por el Giroscopio

        mensaje_3int = int(D1, 2) * (3 / 64)
        mensaje_4int = int(D2, 2) * (3 / 32)



#-----------------------------------Codigo del brazo------------------------------------------

        display.fill(white)

        """Pruebas del movimiento del brazo con comandos por el teclado"""
        """
        # rotate our joints
        #ua_image, ua_rect = upperarm.rotate(.03)
        while 1:
            tecla = sys.stdin.read(1)
            if tecla == 'a' or 'q' or 'w' or 'e' or 'r':
                break


        if tecla == 'a':
            n=0
            m=0
        if tecla == 'q':
            n=0.1
            m=0
        if tecla == 'w':
            n = -0.1
            m = 0
        if tecla == 'e':
            n = 0
            m = 0.1
        if tecla == 'r':
            n = 0
            m = -0.1
        """

        """Movimiento del brazo por señales recibidas por comunicación serial"""
        medida1 = mensaje_1int - medida_anterior1
        medida2 = mensaje_2int - medida_anterior2

        #prueba = prueba+1
        n=0
        m=0

        if abs(medida1) > 0.03 and abs(medida1)<.11:
            m=2*medida1
        if abs(medida2) > 3 and abs(medida2)<40:# and abs(medida2) < 10:
            n=medida2/40
            if inicio == True:
                n=-medida2/5
                inicio = False
        if mensaje_3int == 3.0:
            msg="Se ha detectado un golpe en el dispositivo"
            popupmsg(msg)
        if mensaje_4int == 3.0 and mensaje_anterior4 == 0.0:
            if Sensor_d2==False:
                msg = "Se ha inhabilitado el movimiento del brazo"
                popupmsg(msg)

            if Sensor_d2 == True:
                msg = "Se ha habilitado el movimiento del brazo"
                popupmsg(msg)
            Sensor_d2 = not Sensor_d2
        if Sensor_d2 == True:
            n=0; m=0


        ua_image, ua_rect = upperarm.rotate(n)
        ua_rect.center += np.asarray(origin)
        ua_rect.center -= np.array([-np.cos(upperarm.rotation) * upperarm.offset,
                                    np.sin(upperarm.rotation) * upperarm.offset])
        fa_image, fa_rect = forearm.rotate((n+m))
        h_image, h_rect = hand.rotate((n+m))

        # generate (x,y) positions of each of the joints
        joints_x = np.cumsum([0,
                              upperarm.scale * np.cos(upperarm.rotation),
                              forearm.scale * np.cos(forearm.rotation),
                              hand.length * np.cos(hand.rotation)]) + origin[0]
        joints_y = np.cumsum([0,
                              upperarm.scale * np.sin(upperarm.rotation),
                              forearm.scale * np.sin(forearm.rotation),
                              hand.length * np.sin(hand.rotation)]) * -1 + origin[1]
        joints = [(int(x), int(y)) for x,y in zip(joints_x, joints_y)]

        def transform(rect, base, arm_part):
            rect.center += np.asarray(base)
            rect.center += np.array([np.cos(arm_part.rotation) * arm_part.offset,
                                  -np.sin(arm_part.rotation) * arm_part.offset])

        #transform(ua_rect, joints[0], upperarm)
        transform(fa_rect, joints[1], forearm)
        transform(h_rect, joints[2], hand)
        # transform the hand a bit more because it's weird
        h_rect.center += np.array([np.cos(hand.rotation),
                                  -np.sin(hand.rotation)]) * -10

        display.blit(ua_image, ua_rect)
        display.blit(fa_image, fa_rect)
        display.blit(h_image, h_rect)

        medida_anterior1 = mensaje_1int
        medida_anterior2 = mensaje_2int
        mensaje_anterior4 = mensaje_4int

    # check for quit
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(30)
