# hote craprojet #

from tkinter import*
import math, random
from animal import*

class hote(animal):
	prairie=None
	vitessemax=15 																																					#vitesse  maximale de base des souris
	dureedevie=750 																																					#durée de vie de base des souris
	maturite=25 																																					#maturité des souris
	gestation=19 																																					#temps de gestation des souris
	gestationM=8 																																					#temps de gestation de la maladie dans les souris
	chiasse=0
	chiasseMax=25 																																					#temps au bout du quel l'animal déféque
	
	def __init__ (self,cnv,abscisse=-1,ordonnee=-1,direction=random.random()*(2*math.pi),age=-1, m=0): 																#m = 0 pas malade
		super().__init__(cnv,abscisse,ordonnee,direction,age)
		
		self.vitessemax=random.randint(10,15) 																														#définit la vitesse de l'hôte
		
		self._direction=direction 																																	#définit la dérection que prends l'hôte en se déplaçant
		
		#place l'hôte dans la prairie
		if hote.prairie is None:
			hote.prairie=cnv
			hote.xmax=int(hote.prairie.cget("width"))
			hote.ymax=int(hote.prairie.cget("height"))
		
		#détermine les coordonnées de l'hôte	
		if abscisse==-1:
			abscisse=random.randint(0,hote.xmax-1)
		if ordonnee==-1:
			ordonnee=random.randint(0,hote.ymax-1)
		self.positionne(abscisse,ordonnee)
		
		self.est_malade=False 																																		#constante de base de l'état de maladie
		
		self._chiasse=0 																																			#constante de base de la défécation
		
		self._angle=random.random()*2*(math.pi) 																													#calcule  un angle
		
		self._tgest=-1 																																				#définit le temps de gestation par défaut
		
		
		#définit l'age de l'hôte
		if age>=0:
			self._age=age
		else:
			self._age=random.randint(1,24)
		if m==0:	
			self._sexe=random.choice(["F","M"]) 																													#définir le sexe de l'hote sain
			self._m=0
		else:
			self._sexe=random.choice(["FM","MM"]) 																													#définir le sexe de l'hôte malade
			self._m=1
		
		#associe une image à un hôte avec des coordonnées propres
		self._fiching="baby_cute_mouse.png"
		self._photo=PhotoImage(file=self._fiching).subsample(30,30)
		self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)
	
	#fait vivre chaques hôtes
	def vit(self,listanim):
		nbb=0 																																						#constante de base du nombre de bébé par tours
		age=self._age
		cc=0 																																						#constante de base du nombre de cacas sains par tours
		ccm=0 																																						#constante de base du nombre de cacas malades par tours
		if self.est_vivant():
			vitesse=(self.vitessemax*random.random()) 																												#définit la vitesse de déplacement de l'hôte
			Pmourir=math.log(age)																																	#calcule la probabilité de mourir
			hasard=random.random()*1+random.randint(5,100)
			if hasard<Pmourir: 																																		#fait mourir l'hôte si sa probabilité de mourir est suppérieure à un nombre au hasard
				self._vivant=False 																																	#change la constante de vie de la souris
			self.Coprophagie(listanim) 																																#appel la méthode de coprophagie (deplacement + manger caca)
			self._age+=1 																																			#calcule l'age de l'hôte
			if isinstance(self, hote) and self._age == self.maturite: 																								#méthode faisant devenir adulte les souris
				hote.prairie.delete(self._img,self._x, self._y) 																									#suprimme l'image de bebe souris
				if self._sexe=="M": 																																#si c'est un male sain on change d'image
					self._fiching="mickey_mouse_01.png"
					self._photo=PhotoImage(file=self._fiching).subsample(7,7)
					self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)	
				elif self._sexe=="F": 																																#si s'est une femelle sains on change d'image
					self._fiching="minnie_mouse_01.png"
					self._photo=PhotoImage(file=self._fiching).subsample(40,40)
					self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)
				elif self._sexe=="MM": 																																#si c'est un male malade de base on change d'image
					self._fiching="mickey_mouse.para_01.png"
					self._photo=PhotoImage(file=self._fiching).subsample(9,9)
					self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)
				else: 																																				#si c'est une femelle malade de base on change d'image
					self._fiching="minnie_mouse.para_01.png"
					self._photo=PhotoImage(file=self._fiching).subsample(40,40)
					self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)
				
			
			#calcule le temps de gestatin de l'hôte
			if self._tgest>=0:
				self._tgest-=1
			if self._tgest==0:
				nbb=random.randint(5,12) 																															#définit un nombre de bébés
				self._tgest-=1
				
			#fait faire un caca à l'animal malade
			cc=self.OopsieDoopsie(cc)
			if cc == 2:
				cc=0
				ccm=1
		return nbb, cc, ccm


	def miammiam(self, listanim): 																																	#fait manger la caca à la souris et devanir malade si la caca était malade
		for caca in listanim : 
			dist = self.distance(caca) 																														#calcule la distance au caca
			if not isinstance(caca,hote) and dist < self.vitessemax and caca.est_vivant : 																			#regarde la nature de l'objet, la distance de la souris au caca et si le caca est vivant
				if caca._m == 1 and self._m == 0: 																													#si le caca est un caca malade et que que la souris est saine
					self.devient_malade() 																															#fait devenir la souris malade
				caca.meurt() 																																		#le caca meurt et disparait
				listanim.pop(listanim.index(caca)) 																													#le caca sort de la liste
		
	def Coprophagie(self, listanim): 																																#fait se déplacer la souris vers le caca, et manger le caca par la souris ; comportement assez normal chez ces petites bête
		for caca in listanim : 
			distList = [] 																																			#crée un liste vide des distances entre la souris et les cacas
			Xi = [] 																																				#crée un liste vide de coordonnées X
			Yi = [] 																																				#crée un liste vide de coordonnées Y
			if not isinstance(caca,hote) and caca.est_vivant():
				dist = self.distance(caca) 																													#calcule la distance au caca
				Xi.append(animal.get_x(self)) 																														#ajoute le x du caca à la liste des coordonnées X
				Yi.append(animal.get_y(self)) 																														#ajoute le y du caca à la liste des coordonnées Y
				distList.append(dist) 																																#ajoute la distance souris/caca à la liste des distances
			if len(distList)!=0: 																																	#regarde la liste si elle contiens au moins une valeur
				distmin = min(distList) 																															#regarde la plus petite distance soursi/caca de la liste
				if distmin < 100 : 																																	#ne s'actionne que si la distance souris/caca est inférieure à 100
					self.nouvelangle(Xi[distList.index(distmin)], Yi[distList.index(distmin)]) 																		#donne un nouvel angel de déplancement à la souris
					x = self._x + self.vitessemax*math.cos(self._nouvangle)																							#donne un nouvel x à la souris
					y = self._y + self.vitessemax*math.sin(self._nouvangle) 																						#donne un nouvel y à la souris
					self.positionne(x,y) 																													#appel la méthode positionne sur les nouvelles coordonnées de la souris
					self.redessine() 																															#appel la méthode pour redessiner la souris dans le canevas
					self.miammiam(listanim) 																														#appel la méthode faisant manger les cacas à la souris
				else:
					self.dep() 																																		#appel la méthode de déplacement de la souris
					self.miammiam(listanim) 																														#appel la méthode faisant manger les cacas à la souris
			else:
				self.dep() 																																			#appel la méthode de déplacement de la souris
				self.miammiam(listanim) 																															#appel la méthode faisant manger les cacas à la souris
			
	def nouvelangle(self, xcaca, ycaca): 																															#recalcule l'angle de déplancement de la souris
		delta_x = xcaca - self._x
		delta_y = ycaca - self._y
		if delta_x == 0: 																																			# si delta x ou y =0, la tangente est infini (angle droit)
			if delta_y > 0:
				self._nouvangle = math.pi/2
			else: 
				self._nouvangle = -math.pi/2
		else:
			self._nouvangle = math.atan(delta_y/delta_x)
			if delta_x < 0:
				self._nouvangle += math.pi
				
	#méthode rendant un animal malade
	def devient_malade(self):
		self.vitessemax=random.randint(5,10) 																														#baisse vitesse 
		self.dureedevie=500     																																	#baisse durée de vie
		self.gestationM=1 																																			#temps de gestation de la maladie dans la souris
		self.chiasseMax=25																																			#actuellement inchangée des données de base
		if self._sexe=="F": 																																		#change l'image de la souris femelle malade
			self._fiching="minnie_mouse.para_01.png"
			self._photo=PhotoImage(file=self._fiching).subsample(40,40)
			self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)
			self._sexe="FM"
			self._m=1
		elif self._sexe=="M": 																																		#change l'image de la souris mâle malade
			self._fiching="mickey_mouse.para_01.png"
			self._photo=PhotoImage(file=self._fiching).subsample(9,9)
			self._img=hote.prairie.create_image(self._x,self._y,image=self._photo)
			self._sexe="MM"
			self._m=1
		return 
