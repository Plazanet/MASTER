# animal craprojet #

from tkinter import*
import math
import random


class animal:
	
	vitessemax=0.1
	dattrac=0.1
	prairie= None 
	fiching="mmorty.png"
	dureedevie=1
	maturite=1
	gestation=1	       																												#temps de gestation des femelles des animaux
	gestationM=1 																													#temps de gestation de la maladie dans les animaux
	chiasse=0
	chiasseMax=25 																													#temps au bout du quel l'animal déféque
	
	def __init__ (self,cnv,abscisse=-1,ordonnee=-1,direction=random.random()*(2*math.pi),age=-1, m=0): 								#m = 0 pas malade
		
		self._direction=direction 																									#définit la dérection que prends l'animal en se déplaçant
		
		#place l'animal dans la prairie
		if animal.prairie is None:
			animal.prairie=cnv
			animal.xmax=int(animal.prairie.cget("width"))
			animal.ymax=int(animal.prairie.cget("height"))	

		#détermine les coordonnées de l'animal
		if abscisse==-1:
			abscisse=random.randint(0,animal.xmax-1)
		if ordonnee==-1:
			ordonnee=random.randint(0,animal.ymax-1)
		self.positionne(abscisse,ordonnee)
			
		self._vivant=True
		self.est_malade=False 
		self._attrait=False
				
		self._tgest=-1
		self._sexe=random.choice(["F","M"]) 																						#définir le sexe de l'animal
		
		#associe une image à un animal avec des coordonnées propres
		self._fiching="mmorty.png"
		self._photo=PhotoImage(file=self._fiching).subsample(10,10)
		self._img=animal.prairie.create_image(self._x,self._y,image=self._photo)
		
		#définit l'age de l'animal
		if age>=0:
			self._age=age
		else:
			self._age=random.randint(0,200)
	
	#méthode définissant les nouvelles positions de l'animal	
	def positionne(self, nouvx, nouvy):
		self._x = nouvx
		if self._x<0:
			self._x=animal.xmax-1
		if self._x>=animal.xmax:
			self._x=0
		
		self._y = nouvy
		if self._y<0:
			self._y=animal.ymax-1
		if self._y>=animal.ymax:
			self._y=0
			
	#méthode définissant le déplacement de l'animal		
	def dep(self):
		vitesse=self.vitessemax*random.random()
		self._direction+=random.normalvariate(0,math.pi/8)
		x1=self._x+vitesse*math.cos(self._direction)
		y1=self._y+vitesse*math.sin(self._direction)
		self.positionne(x1,y1)
		self.redessine()
	
	#méthode définissant le sexe de l'animal	
	def get_sexe(self):
		return self._sexe
	
	#mathode définissant le x de l'animal
	def get_x(self):
		return self._x
	
	#mathode définissant de y de l'animal
	def get_y(self):
		return self._y
	
	#méthode définissant l'age de l'animal	
	def get_age(self):
		return self._age
	
	#méthode faisaintdevenir gestante l'animal
	def devientgestante(self):
		self._tgest=self.gestation
	
	#méthode définisssant l'état de gestation de l'animal	
	def estgestante(self):
		return self._tgest>=0	
	
	#méthode calculant la distance entre les animaux i et j	
	def distance(self, a):
		xi,yi = a.get_x(),a.get_y()
		xj,yj = self.get_x(),self.get_y()
		return math.sqrt((xi-xj)**2+(yi-yj)**2)
	
	#méthode regardant si un animal est vivant
	def est_vivant(self):
		return self._vivant

	#méthode définissant si un animal meurt
	def meurt(self):
		vivant=False
		animal.prairie.delete(self._img)
		
	#méthode faisant crotter l'animal
	def OopsieDoopsie(self, cc):
		if self._m == 0 :
			if self._chiasse==self.chiasseMax: 																										#si le temps de défaquer atteint son maximum fait passer à un l'indice de caca
				cc=1
				self._chiasse=0 																													#refaire venir le temps de défécation à zero
			else:
				self._chiasse+=1 																													#ajoute un temps de plus à la défécation
		else: 
			if self._chiasse==self.chiasseMax: 																										#si le temps de défaquer atteint son maximum fait passer à deux l'indice de caca
				cc=2
				self._chiasse=0 																													#refaire venir le temps de défécation à zero
			else:
				self._chiasse+=1 																													#ajoute un temps de plus à la défécation
		return cc
	
	#méthode redessinant un animal aprés son déplacement
	def redessine(self):
		animal.prairie.coords(self._img,self._x,self._y)

