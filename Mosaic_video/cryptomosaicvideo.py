#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import matplotlib.pyplot as plt
import random
import os


# In[2]:


LICENSE_TEXT = """
SOFTWARE LICENSE

This software is licensed under the following terms:
- You may not distribute it without explicit permission.
- Free for non-commercial use only.
- You may not modify or reverse engineer the code.

(Additional license terms...)
 
Created by: CutVonDrake
"""

# Display the license at startup
print(LICENSE_TEXT)
user_input = input("\nDo you accept the terms of the license? (y/n): ").strip().lower()

if user_input != 'y':
    print("You cannot use the program without accepting the license terms.")
    exit(1)

# Proceed with the rest of the program
print("Welcome to the program!")


# In[ ]:


# Specifica il percorso del file video
#video_path = C:\Users\andre\Python notebooks\Media\video\battle_game.mp4
crypto_number=(input('Enter a decryption password: minimum 10 characters:'))
crypto_number=int(''.join(str(ord(c)) for c in crypto_number))
video_path=input('Paste video path: no quotes:')
# Ottieni la cartella in cui si trova il video
output_folder = os.path.dirname(video_path)
output_video = os.path.join(output_folder, 'mosaic_video.mp4')
#specifica quanti secondi del video prendere
seconds= int(input('Cut video in seconds:'))
n=int(input('Mosaic complexity: insert a number from 2 to 100 (lower number higher complexity; suggested=10):'))


# In[ ]:


# Specifica un fattore di scala per il ridimensionamento
#resize_scale = 0.5
cap = cv2.VideoCapture(video_path)
d=0
frames=[]
while d<(seconds*30):
    # Legge un fotogramma dal file video
    ret, frame = cap.read()

    #Qui sta leggendo il fotogramma quindi per modificare l'immagine fare tutto qui
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    img=frame.copy()
    random.seed(int(f'{crypto_number}'*4))
    img=img[0:img.shape[0]//n*n,0:img.shape[1]//n*n,:]
    img1=img.copy()
    A = [(x, y) for x in range(0,img.shape[0],n) for y in range(0,img.shape[1],n)]
    random.shuffle(A)
    D=[]
    for a in range(0,img.shape[0],n):
        for b in range(0,img.shape[1],n):
            C=A.pop()
            x=C[0]
            y=C[1]
            img1[a:a+n,b:b+n]=img[x:x+n,y:y+n]
    frame=img1.copy()
    #FINE MODIFICHE
    frames.append(frame)
    d+=1
    # Aggiorna la barra manuale
    percent = (d / (seconds * 30)) * 100
    bar = ('#' * int(percent // 2)).ljust(50, '-')
    print(f"\r[{bar}] {percent:.2f}%", end='')
    # Se non ci sono più fotogrammi, esci dal ciclo
    if not ret:
        print("Fine del video.")
        break
    # Percorso della cartella in cui vuoi salvare l'immagine
    #output_folder = output_folder
    #output_folder = r'C:\Users\andre\Python notebooks\Media\frames'
    # Nome del file di output
    #output_file = os.path.join(output_folder, f'{d:020d}.jpg')
    # Salva l'immagine
    #cv2.imwrite(output_file, frame)



#----------------------------------------------------------------------------------------




#Riconverti i frames in video
import cv2
import os
# Carica la prima immagine per ottenere le dimensioni
prima_immagine = frames[0]
# Ottieni le dimensioni (larghezza, altezza) della prima immagine
altezza, larghezza, _ = prima_immagine.shape

# Crea l'oggetto VideoWriter per scrivere il video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Usa il codec mp4v per creare il video .mp4
fps = 30  # Frame rate per il video
video_writer = cv2.VideoWriter(output_video, fourcc, fps, (larghezza, altezza))

total_frames=len(frames)

# Aggiungi ogni immagine al video
for img in frames:    
    # Carica l'immagine
    # Aggiungi l'immagine al video
    video_writer.write(img)
# Rilascia il VideoWriter e chiudi
video_writer.release()
print('\n'f'Video creato con successo come {output_video}')

