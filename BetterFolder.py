import os
import shutil
import re
from os import path
import json
import time
from watchdog.observers import Observer
#from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileSystemEventHandler
from datetime import date
from datetime import datetime

#.crdownload, .tmp

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        for filename in os.listdir(folderToTrack):
            #print(filename)
            src = folderToTrack + '/' + filename
            name, extension = os.path.splitext(src)
            #print(name,str(extension))
            if os.path.isdir(src):
                #print('Soy un folder y no me muevo!!!')
                algo = 0
            elif str(extension) == ".crdownload" or str(extension) == ".tmp" or str(extension) == "":
                #print('Me estoy descargando o soy archivo temporal')
                algo = 0
            else:
                name, extension = os.path.splitext(src)
                extension = re.findall("(?i)(?<=\.)\w+",str(extension))
                dirName = "".join(extension) + "-Folder"
                print(dirName)
                #checamos si existe una carpeta si es asi no hacemos nada y si no existe creamos otra
                newDestination = folderDestination + '/' + dirName
                newDestinationAux = folderDestination + '/' + dirName
                if os.path.isdir(newDestination):
                    print("Este folder ya existe: ",dirName)
                else:
                    print("no existe el folder llamado ",dirName," se creara uno")
                    try:
                        os.makedirs(newDestination, exist_ok = True)
                        print("Directory '%s' created successfully" % dirName)
                    except OSError as error:
                        print("Directory '%s' can not be created" % dirName)
                #movemos los archivos
                print('Me movi a1: ', newDestination)
                newDestination = newDestination + '/' + filename

                i=1
          
                while True:
                    if os.path.exists(newDestination) == True:
                        today = date.today()
                        now = datetime.now()
                        newDestination = "".join(name) + " " + str(today.strftime("%d-%m-%Y")) + " " +str(now.strftime("%H-%M-%S")) + "." + "".join(extension)
                        #newDestination = "".join(name) + " (%d)." % (i) + "".join(extension)
                        print("Cambie de nombre: ",newDestination)
                        i = i+1
                    if os.path.exists(newDestination) == False:
                        break
                    


                time.sleep(1)
                print('Me movi a2: ', newDestination)
                os.rename(src, newDestination)

# Parent Directory path
folderToTrack = '/Users/Martín/Documents/prueba'
#extencion = "yolo"
folderDestination  = '/Users/Martín/Documents/prueba'

event_handler = EventHandler()
observer = Observer()
observer.schedule(event_handler, folderToTrack, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
