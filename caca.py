# caca craprojet #

from tkinter import*
import math, random
from animal import*

class caca(animal):
    prairie=None
    vitessemax=0 																																				#les cacas ne se déplacent pas, il n'ont pas de vitesse
    dureedevie=25 																																				#on donne une durée de vie aux cacas

    def __init__ (self,cnv,abscisse=-1,ordonnee=-1,direction=random.random()*(2*math.pi),age=-1, m=0): 															#m = 0 pas malade
        super().__init__(cnv,abscisse,ordonnee,direction,age)

        #place le caca dans la prairie
        if caca.prairie is None:
            caca.prairie=cnv
            caca.xmax=int(caca.prairie.cget("width"))
            caca.ymax=int(caca.prairie.cget("height"))
    
        #détermine les coordonnées du caca	
        if abscisse==-1:
            abscisse=random.randint(0,caca.xmax-1)
        if ordonnee==-1:
            ordonnee=random.randint(0,caca.ymax-1)
        self.positionne(abscisse,ordonnee)
            
        self.est_contagieux=False

        #définit l'age de du caca
        if age>=0:
            self._age=age
        else:
            self._age=0
        if m == 1 :
            self._fiching="caca_sarko.png" 																														#définit l'image des cacas malades ; n'y voyez auccun message politique biensur
            self._photo=PhotoImage(file=self._fiching).subsample(20,20)
            self._img=animal.prairie.create_image(self._x,self._y,image=self._photo)
            self._m=1
        else:
            self._fiching="chocolat_poop.png" 																													#définit l'image des cacas sains ; histoire de rendre le tout un peu plus apétissant
            self._photo=PhotoImage(file=self._fiching).subsample(20,20)
            self._img=animal.prairie.create_image(self._x,self._y,image=self._photo)
            self._m=0
            
    #fait vivre chaques caca
    def vit(self, listanim):
        nbb = 0
        cc = 0
        ccm = 0
        age=self._age
        if age==self.dureedevie:
            self._vivant=False 																																	#fait mourir le caca
        else:
            self._age+=1 																																		#calcule l'age du caca
        return nbb, cc, ccm

