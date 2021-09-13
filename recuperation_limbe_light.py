# -*- coding: utf-8 -*-
import numpy as np
import time
import matplotlib.pyplot as plt
filename = "moon_lite.txt"

#observateur est le point (x,y,z) de l'observateur dans l'espace à 3 dimensions (x,y,z) orthonormé de centre O
#observateur regardant en direction de la lune de centre O, par définition observateur est aussi son propre vecteur
#Pour obtenir un limbe equatorial, placer observateur sur l'axe des Y tel que observateur = [0.0, 1.0, 0.0]
#Pour obtenir un limbe polaire passant par la latitude 0, placer observateur sur l'axe des Z tel que T = [0.0, 0.0, 1.0]

observateur = [0.0,1.0,0.0]

#O origine du repère, également le centre de la Lune
O = [0, 0, 0]

#vecteur_en_partie_Fixe : vecteur x,y,z avec x,y fixé pour résolution d'équation cas 1 > un vecteur dans le plan

vecteur_en_partie_Fixe = [1.0,1.0]

#A vecteur x,y,z avec x fixé pour résolution determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux
vecteur_orthogonal_en_partie_Fixe = [2.0]

#Rayon de la lune en mètre / lunar reference radius
R = 1737400

Scaling_Factor = 0.5

tabVecteur = []

def recuperation_matrice_Lune(namefile):
    matrice_Lune = []
    f = open(namefile, "r")
    
    for line in f:
        stock = line.split(" ")
        
        for x in range(len(stock)):
            stock[x] = int(stock[x])
            stock[x] = 255 - stock[x]

        matrice_Lune.append(stock)
        
    f.close
    
    #il est nécessaire d'inverser les lignes de la matrice pour ne pas obtenir une image à l'envers
    for x in range(len(matrice_Lune)/2):
        tmp = matrice_Lune[x]
        matrice_Lune[x] = matrice_Lune[len(matrice_Lune)-1-x]
        matrice_Lune[len(matrice_Lune)-1-x] = tmp
        
    return matrice_Lune

#cas particulier de l'observateur
def verification_position_observateur(vecteur_observateur):
    if( vecteur_observateur[0] == 0 and vecteur_observateur[1] == 0 and vecteur_observateur[2] != 0):
        print "L'observateur se situe sur l'axe Z"
        return 1
    elif( vecteur_observateur[0] == 0 and vecteur_observateur[1] != 0 and vecteur_observateur[2] == 0):
        print "L'observateur se situe sur l'axe Y"
        return 2
    elif( vecteur_observateur[0] != 0 and vecteur_observateur[1] == 0 and vecteur_observateur[2] == 0):
        print "L'observateur se situe sur l'axe X"
        return 3
    elif( vecteur_observateur[0] != 0 and vecteur_observateur[1] != 0 and vecteur_observateur[2] == 0):
        print "L'observateur se situe sur le plan XY"
        return 4
    elif( vecteur_observateur[0] != 0 and vecteur_observateur[1] == 0 and vecteur_observateur[2] != 0):
        print "L'observateur se situe sur le plan XZ"
        return 5
    elif( vecteur_observateur[0] == 0 and vecteur_observateur[1] != 0 and vecteur_observateur[2] != 0):
        print "L'observateur se situe sur le plan YZ"
        return 6
    elif( vecteur_observateur[0] == 0 and vecteur_observateur[1] == 0 and vecteur_observateur[2] == 0):
        print "ERREUR dans verification_position_observateur. Vecteur observateur NULL, impossible d'obtenir un limbe depuis un tel observateur"
        return -1
    else:
        print "L'observateur se situe dans l'espace 3D sans cas particulier"
        return 0

    
def traitement_en_fonction_du_cas_observateur(cas):
    if(cas == 0):
        print "========"
        print "==CAS=0="
        print "========"
        vecteur1 = determiner_un_vecteur_dans_le_plan_normal_passant_par_0_du_vecteur_observateur(observateur) #vecteur1 étant un vecteur du plan normal à observateur, par definition vecteur1 est vecteur normal à observateur
        vecteur2 = determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux(observateur,vecteur1)
        
        
    elif(cas == 1):
        print "========"
        print "==CAS=1="
        print "========"
        vecteur1 = [1,0,0]
        vecteur2 = [0,1,0]
        
    elif(cas == 2):
        print "========"
        print "==CAS=2="
        print "========"
        vecteur1 = [1,0,0]
        vecteur2 = [0,0,1]
        
    elif(cas == 3):
        print "========"
        print "==CAS=3="
        print "========"
        vecteur1 = [0,1,0]
        vecteur2 = [0,0,1]
    
    elif(cas == 4):
        print "========"
        print "==CAS=4="
        print "========"
        vecteur1 = [0,0,1]
        vecteur2 = determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux(observateur,vecteur1)
        
    elif(cas == 5):
        print "========"
        print "==CAS=5="
        print "========"
        vecteur1 = [1,0,0]
        vecteur2 = determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux_cas5(observateur)
        
    elif(cas == 6):
        print "========"
        print "==CAS=6="
        print "========"
        vecteur1 = [0,1,0]
        vecteur2 = determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux_cas6(observateur)
        
    elif(cas == -1):
        print "ERREUR dans traitement_en_fonction_du_cas_observateur, cas de l'observateur NULL (-1), impossible de traiter cette donnée."
        exit
    return vecteur1, vecteur2

#orthogonalité sur le meme plan XZ
def determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux_cas5(observateur):
    vecteur_solution = []
    vecteur_solution.append(observateur[0])
    vecteur_solution.append(0)
    vecteur_solution.append(-(vecteur_solution[0]*observateur[0])/observateur[2])    
    return vecteur_solution

#orthogonalité sur le meme plan YZ
def determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux_cas6(observateur):
    vecteur_solution = [0]
    vecteur_solution.append(observateur[1])
    vecteur_solution.append(-(vecteur_solution[1]*observateur[1])/observateur[2])    
    return vecteur_solution

#soit p un plan normal à observateur tel que p[0]*x + p[1]*y + p[2]*z + d = 0, d = 0 car le plan passe par l'origine et p = vecteur_observateur (theoreme)
#soit vecteur_en_partie_Fixe un vecteur du plan p, dont vecteur_plan[0] et vecteur_plan[1] déjà fixés (pour résoudre équation)
def determiner_un_vecteur_dans_le_plan_normal_passant_par_0_du_vecteur_observateur(vecteur_observateur):
    z = -( vecteur_observateur[0] * vecteur_en_partie_Fixe[0] + vecteur_observateur[1] * vecteur_en_partie_Fixe[1] ) / vecteur_observateur[2]
    vecteur_solution = vecteur_en_partie_Fixe
    vecteur_solution.append(z)
    return vecteur_solution

#v1 et v2 vecteur orthogonaux, donc v1 observateur
def determiner_un_vecteur_orthogonal_a_deux_vecteurs_orthogonaux(v1, v2):
    vecteur_solution = vecteur_orthogonal_en_partie_Fixe
    
    y = -vecteur_solution[0] * (v1[0] * v2[2] - v2[0] * v1[2]) / (v1[1] * v2[2] - v2[1] * v1[2])
    vecteur_solution.append(y)
    
    z = -(v2[0] * vecteur_solution[0] + v2[1] * vecteur_solution[1]) / v2[2]
    vecteur_solution.append(z)
    
    return vecteur_solution

def calculerNorme(vecteur):
    norme = 0
    for i in vecteur:
        norme += i * i
    norme = np.sqrt(norme)
        
    return norme

def calculer_Delta_entre_vecteur_et_R(vecteur):
    a = vecteur[0] * vecteur[0] + vecteur[1] * vecteur[1] + vecteur[2] * vecteur[2]
    b = R * R
    delta = np.sqrt(b / a)
    
    return delta
#v1 et v2 vecteur orthogonaux, qui forment un plan dont le cercle appartient, teta angle entre deux points, r rayon de référence du cercle, o centre du cercle
def vecteur_du_cercle_dorigine_o_rayon_r(v1, v2, teta, o, r):
    vecteur = []
    x = o[0] + v1[0] * r * np.cos(teta) + v2[0] * r * np.sin(teta)
    y = o[1] + v1[1] * r * np.cos(teta) + v2[1] * r * np.sin(teta)
    z = o[2] + v1[2] * r * np.cos(teta) + v2[2] * r * np.sin(teta)
    
    vecteur.append(x)
    vecteur.append(y)
    vecteur.append(z)
    norme = calculerNorme(vecteur)
    
    return vecteur, norme

"""solution alternative avec DELTA"""
def vecteur_du_cercle_dorigine_o_rayon_r_avec_delta(v1, v2, teta, o, r):
    vecteur = []
    x = o[0] + v1[0] * r * np.cos(teta) + v2[0] * r * np.sin(teta)
    y = o[1] + v1[1] * r * np.cos(teta) + v2[1] * r * np.sin(teta)
    z = o[2] + v1[2] * r * np.cos(teta) + v2[2] * r * np.sin(teta)
    
    vecteur.append(x)
    vecteur.append(y)
    vecteur.append(z)
    delta = calculer_Delta_entre_vecteur_et_R(vecteur)
    print "==========================================="
    print "==========================================="
    print "==========================================="
    
    print("VECTEUR: ")
    print vecteur
    
    print "NORME: "
    print calculerNorme(vecteur)
    print "DELTA : "
    print delta
    
    
    vecteur[0] = vecteur[0]*delta
    vecteur[1] = vecteur[1]*delta
    vecteur[2] = vecteur[2]*delta
    print("VECTEUR APRES MULTIPLICATION AVEC DELTA: ")
    print vecteur
    print "NORME APRES MULTIPLICATION AVEC DELTA: "
    print calculerNorme(vecteur)
    print "==========================================="
    print "==========================================="
    print "==========================================="
    return vecteur

def points_du_cercle(v1, v2, r, o, nb_valeurs):
    intervalle = 2*np.pi/nb_valeurs
    points = []
    rayon_points = []
    for i in range(nb_valeurs):
        vecteur, norme = vecteur_du_cercle_dorigine_o_rayon_r(v1, v2, i*intervalle, o, r)
        points.append(vecteur)
        rayon_points.append(norme)
        
    
    return points, rayon_points

"""solution alternative avec DELTA"""
def points_du_cercle_avec_delta(v1, v2, r, o, nb_valeurs):
    intervalle = 2*np.pi/nb_valeurs
    points = []
    for i in range(nb_valeurs):
        points.append(vecteur_du_cercle_dorigine_o_rayon_r_avec_delta(v1, v2, i*intervalle, o, r))
    
    return points

#un point est un point x,y,z convertible en un couple [latitude, longitude]
def conversion_points_en_latitude_longitude(points, rayon_points):
    
    tab_couples = []
    couple = []
    
    for i in range(len(points)):
        couple = []
        latitude = np.arcsin(points[i][1]/rayon_points[i])
        longitude = np.arctan2(points[i][2] , points[i][0])
        latitude = latitude * 180 / np.pi
        longitude = longitude * 180 / np.pi
        couple.append(latitude)
        couple.append(longitude)
        tab_couples.append(couple)
        
    return tab_couples

def conversion_points_en_latitude_longitude_avec_delta(points):
    
    tab_couples = []
    couple = []
    
    for point in points:
        couple = []
        latitude = np.arcsin(point[1]/R)
        longitude = np.arctan2(point[2] , point[0])
        latitude = latitude * 180 / np.pi
        longitude = longitude * 180 / np.pi
        couple.append(latitude)
        couple.append(longitude)
        tab_couples.append(couple)
        
    return tab_couples

def conversion_latitude_longitude_positif(tab):
    for p in tab:
        p[0] = np.abs(p[0]-90)
        p[1] += 180
    return tab
    

def interpolation_dans_matrice(matriceLune, matriceLatitude_Longitude):
    
    
    hauteurLune = len(matriceLune)
    largeurLune = len(matriceLune[0])
    
    #len_Latitude_Longitude = len(matriceLatitude_Longitude)
    
    pas_x = hauteurLune / 180.0
    pas_y = largeurLune / (2.0 * 180.0)
    
    #couple latitude Y longitude X
    for p in matriceLatitude_Longitude:
        p[0] = p[0] * pas_x
        if p[0] == hauteurLune :
            p[0] = 0;
        p[1] = p[1] * pas_y
        if p[1] == largeurLune :
            p[1] = 0;
    compteur = 0
    liste_points = []
    for points in matriceLatitude_Longitude:
        ##print compteur
        compteur += 1
        #print points
        bl = matriceLune[int(np.floor(points[0]))][int(np.floor(points[1]))]
        #print np.floor(points[0]), np.floor(points[1])
        if int(np.ceil(points[1])) == len(matriceLune[0]):
            br = matriceLune[int(np.floor(points[0]))][0]
        else:
            br = matriceLune[int(np.floor(points[0]))][int(np.ceil(points[1]))]
        #print np.floor(points[0]), np.ceil(points[1])
        if int(np.ceil(points[0])) == len(matriceLune):
            tl = matriceLune[0][int(np.floor(points[1]))]
        else:
            tl = matriceLune[int(np.ceil(points[0]))][int(np.floor(points[1]))]
        #print np.ceil(points[0]), np.floor(points[1])
        if (int(np.ceil(points[0])) == len(matriceLune)) and (int(np.ceil(points[1])) == len(matriceLune[0])):
            tr = matriceLune[0][0]
        elif (int(np.ceil(points[0])) == len(matriceLune)) and (int(np.ceil(points[1])) != len(matriceLune[0])):
            tr = matriceLune[0][int(np.ceil(points[1]))]
        elif (int(np.ceil(points[0])) != len(matriceLune)) and (int(np.ceil(points[1])) == len(matriceLune[0])):
            tr = matriceLune[int(np.ceil(points[0]))][0]
        elif (int(np.ceil(points[0])) != len(matriceLune)) and (int(np.ceil(points[1])) != len(matriceLune[0])):
            tr = matriceLune[int(np.ceil(points[0]))][int(np.ceil(points[1]))]
        #print np.ceil(points[0]), np.ceil(points[1])
        moyenne = (bl + br + tl + tr) / 4
        liste_points.append(moyenne)
    
    return liste_points
    
def draw_limbe(tab):
    ##CERCLE
    #===========================
    theta = np.linspace(0, 2*np.pi, len(tab) + 1)

    X1 = np.cos(theta)
    Y1 = np.sin(theta)
    
    for i in range(0, len(tab)):
        tab[i] = tab[i] - 127 #-127 pour le cas du moonlight codé sur [0-255], l'original est entre -32000 et 32000
    
    
    for i in range(0, len(tab)):

        X1[i] = X1[i] * (R + (tab[i])*Scaling_Factor*np.power(2,16)/255) #mise à l'echelle, Bit Type 16
        Y1[i] = Y1[i] * (R + (tab[i])*Scaling_Factor*np.power(2,16)/255)
       
    
    X1[len(X1)-1] = X1[0]
    Y1[len(Y1)-1] = Y1[0]
    
    liste_compteur = [i for i in range(len(tab))]
    plt.plot(X1,Y1) #tracer le cercle à l'echelle représentatif du limbe
    
    plt.axis("equal")
    plt.show()
    
    liste_compteur = [i for i in range(len(tab))]
    plt.plot(liste_compteur, tab) #tracer la courbe représentative du limbe
    plt.show()
    
    return tab

def limbe_equateur(matrice_Lune):
    
    theta = np.linspace(0, 2*np.pi, len(matrice_Lune[0]) + 1)

    X1 = np.cos(theta)
    Y1 = np.sin(theta)
    
    len_matrice_lune = len(matrice_Lune)
    len_ligne_matrice_lune = len(matrice_Lune[0])
    
    tab = []
    for i in range(0, len_ligne_matrice_lune):
        tab.append(matrice_Lune[int(len_matrice_lune/2)][i] - 127)#-127 pour le cas du moonlight codé sur [0,255] (2^8 valeurs possible), l'original codé sur [-32768, 32767] (2^16 valeurs possibles)
    
    
    for i in range(0, len(tab)):

        X1[i] = X1[i] * (R + (tab[i])*Scaling_Factor*np.power(2,16)/255) #mise à l'echelle 16 bit, scaling factor le ratio prescrit par le fichier source. Ex : 1 = +0.5m par rapport au rayon de la Lune R
        Y1[i] = Y1[i] * (R + (tab[i])*Scaling_Factor*np.power(2,16)/255)
       
    
    X1[len(X1)-1] = X1[0]
    Y1[len(Y1)-1] = Y1[0]
    
    liste_compteur = [i for i in range(len(tab))]
    plt.plot(X1,Y1)
    
    plt.axis("equal")
    plt.show()
    
    liste_compteur = [i for i in range(len(tab))]
    plt.plot(liste_compteur, tab)
    plt.show()
    
    return tab

def limbe_polaire_latitude_0(matrice_Lune):
    theta = np.linspace(0, 2*np.pi, len(matrice_Lune[0]) + 1)

    X1 = np.cos(theta)
    Y1 = np.sin(theta)
    
    len_matrice_lune = len(matrice_Lune)
    len_ligne_matrice_lune = len(matrice_Lune[0])
    
    tab1 = []
    tab2 = []
    for i in range(0, len_matrice_lune):
        tab1.append(matrice_Lune[i][0] - 127)#-127 pour le cas du moonlight codé sur [0-255] (2^8 valeurs possible), l'original est codé sur [-32768, 32767] (2^16 valeurs possibles)
        tab2.append(matrice_Lune[(len_matrice_lune-1)-i][int(len_ligne_matrice_lune/2)] - 127)
    
    tab = tab1 + tab2 #concaténation de tab1 et tab2
    
    for i in range(0, len(tab)):

        X1[i] = X1[i] * (R + (tab[i])*Scaling_Factor*np.power(2,16)/255) #mise à l'echelle 16 bit, scaling factor le ratio prescrit par le fichier source. Ex : 1 = +0.5m +0.5m par rapport au rayon de la Lune R
        Y1[i] = Y1[i] * (R + (tab[i])*Scaling_Factor*np.power(2,16)/255)
       
    
    X1[len(X1)-1] = X1[0]
    Y1[len(Y1)-1] = Y1[0]
    
    liste_compteur = [i for i in range(len(tab))]
    plt.plot(X1,Y1)
    
    plt.axis("equal")
    plt.show()
    
    liste_compteur = [i for i in range(len(tab))]
    plt.plot(liste_compteur, tab)
    plt.show()
    return tab

def correlation(a,b):
    len_a = len(a)
    len_b = len(b)
    numerateur = 0
    denominateur = 0
    somme_a_carre = 0
    somme_b_carre = 0
    if len_a == len_b:
        for i in range(len_a):
            numerateur += a[i]*b[i]
            somme_a_carre += (a[i] * a[i])
            somme_b_carre += (b[i] * b[i])
        denominateur = np.sqrt(somme_a_carre*somme_b_carre)
        correlation = numerateur / denominateur
        return correlation
    else:
        print "ERREUR dans la fonction correlation : a et b ne font pas la même taille"
        return -1
    return -1

def decalage(a, len_a):
    tmp = a[0]
    for i in range(len_a-1):
        a[i] = a[i+1]
    a[len_a-1]=tmp
    return a

def shift_verification(a,b):
    len_a = len(a)
    len_b = len(b)
    decalage_compteur = 0
    valeur_correlation = -1
    valeur_correlation_max = -1
    if len_a == len_b:
        valeur_correlation = correlation(a,b)
        if (valeur_correlation < 0.99):
            print "a et b n'ont pas de correlation directe, tentative de décalage de b"
            print valeur_correlation
            for i in range(len_a):
                decalage_compteur += 1
                b = decalage(b, len_b)
                valeur_correlation = correlation(a,b)
                if valeur_correlation_max < valeur_correlation:
                    valeur_correlation_max = valeur_correlation
                if valeur_correlation > 0.99:
                    print "Correlation trouvee entre a et b apres ", decalage_compteur, " decalages de b"
                    print "Valeur correlation acceptee (>0.99) : ", valeur_correlation_max
                    return True
                    
        else:
            print "a et b ont deja une correlation directe (>0.99)"
            return True
        print "Aucune correlation trouvee entre a et b apres", decalage_compteur, "tentative(s) de decalage"
        print "Valeur correlation max : ", valeur_correlation_max
        return False
    else:
        print "ERREUR dans la fonction correlation : a et b ne font pas la même taille"
        return False
    return False

def exportation_limbe_fichier_texte(points):
    f = open("limbe.txt", "w")
    
    for i in range(len(points)):
        for j in range(len(points[i])):
            f.write(str(points[i][j])+" ")
        if i != len(points)-1:
            f.write("\n")
    
    f.close()
    return 0

def main():

    start_time = time.time()
    
    matrice_Lune = recuperation_matrice_Lune(filename)    
    plt.pcolormesh(matrice_Lune, cmap='Greys')
    plt.show()
    
    cas = verification_position_observateur(observateur)
    V1, V2 = traitement_en_fonction_du_cas_observateur(cas)
    print V1, V2
    
    points = []
    
    
    points, rayon_points = points_du_cercle(V1,V2,R,O,len(matrice_Lune[0])) #matrice_Lune[0] correspond à la précision maximale
    matriceLatitude_Longitude = conversion_points_en_latitude_longitude(points, rayon_points)
    matriceLatitude_Longitude_positif = conversion_latitude_longitude_positif(matriceLatitude_Longitude) #transformation nécessaire pour interpoler dans la matrice
    
   
    matrice_limbe = interpolation_dans_matrice(matrice_Lune, matriceLatitude_Longitude_positif)
    
    
    limbe = draw_limbe(matrice_limbe)
    
    #Version alternative, utile pour vérification et exporter le limbe
    points_delta = []
    points_delta = points_du_cercle_avec_delta(V1,V2,R,O,len(matrice_Lune[0])) #matrice_Lune[0] correspond à la précision maximale
    matriceLatitude_Longitude_avec_delta = conversion_points_en_latitude_longitude_avec_delta(points_delta)
    matriceLatitude_Longitude_avec_delta_positif = conversion_latitude_longitude_positif(matriceLatitude_Longitude_avec_delta)
    matrice_limbe_avec_delta = interpolation_dans_matrice(matrice_Lune, matriceLatitude_Longitude_avec_delta_positif)
    limbe_delta = draw_limbe(matrice_limbe_avec_delta)
    shift_verification(limbe,limbe_delta)
    
    exportation_limbe_fichier_texte(points_delta)
    
    
    #limbe_equateur_reference = limbe_equateur(matrice_Lune)
    #limbe_polaire_latitude_0_reference = limbe_polaire_latitude_0(matrice_Lune)
        
    #shift_verification(limbe,limbe_equateur_reference) #verification cohérence de donnée entre la fonction générique et un limbe particulier, l'equateur
    #shift_verification(limbe,limbe_polaire_latitude_0_reference) #verification cohérence de donnée entre la fonction générique et un limbe particulier, l'equateur
    
    
    
    print "temps d'execution : ", (time.time()-start_time)
    return 0

main()