# simulation craprojetprojet #

from tkinter import*
from functools import*
import random, time, math, hote, animal, caca

class simulation:

	def __init__(self):
		
		self._larg=1000
		self._haut=800
		
		self._Pmax= int(self._larg*self._haut/2000)
		
		#création fenetre avec la titre "Gastro tueuse"
		self._fenetre=Tk()
		self._fenetre.title("Gastro tueuse")
		
		#Creation du canevas
		self.canevas=Canvas(self._fenetre,width=self._larg,height=self._haut, bg="#3EB317")
		self.canevas.pack(side=LEFT,padx=5,pady=5)
		
		#creation d'un boite définissant le nombre de souris saines "hotes"
		Label(self._fenetre, text="Souris saines").pack()
		hote=StringVar()
		self._nbhote=Spinbox(self._fenetre, from_=10, to=5000, width=4, increment=10, textvariable=hote)
		self._nbhote.pack()	
		
		#création d'une boite définissant le nombre de souris malades
		Label(self._fenetre, text="Souris malades").pack()
		parasite=StringVar()
		self._nbmala=Spinbox(self._fenetre, from_=10, to=5000, width=4, increment=10, textvariable=parasite)
		self._nbmala.pack()
		
		#création d'une boite définissant le temps de la simultation
		Label(self._fenetre, text="Temps").pack()
		temps=StringVar()
		temps.set("100")
		self._nbpas=Spinbox(self._fenetre, from_=1000, to=5000, width=4, increment=100, textvariable=temps)
		self._nbpas.pack()
		
		#creation d'un bouton lançant la simulation
		self._boutonS=Button(self._fenetre, text="Lancer simulation",command=self.vieanimaux)
		self._boutonS.pack()
		
		#création d'un bouton effaçant la limulation
		self._boutonE=Button(self._fenetre, text="Effacer la simulation",command=self.effacer)
		self._boutonE.pack()
		
		#creation d'un bouton fermant la fenetre
		self._boutonF=Button(self._fenetre, text="Fermer la fenêtre", command=self._fenetre.destroy)
		self._boutonF.pack()
				
	#fait vivre chaques animaux chaque jours
	def vieanimaux(self):
		self.canevas.delete(ALL)
		self._listanim=[] 																																								#crée une liste vide d'animaux
		nbh=int(self._nbhote.get()) 																																					#associe nbh au nombre d'hotes définis plus haut
		nbm=int(self._nbmala.get()) 																																					#associe nbm au nombre de malades définis plus haut
		tmax=int(self._nbpas.get()) 																																					#associe tmax au temps définis plus haut
		t=0
		for l in range(nbh):
				self._listanim.append(hote.hote(self.canevas)) 																															#ajoute les hôtes sains à la liste
		for l in range(nbm):
				self._listanim.append(hote.hote(self.canevas, m=1))  																													#ajoute les souris malades à la liste
		while len(self._listanim)>0 and t<tmax:
			baby=[] 																																									#crée une liste vide de bébés
			i=0 																																										#indice de l'animal que l'on va regarder à ce tour
			cc=0  																																										#nombre de caca sain du tour
			ccm=0 																																										#nombre de caca malsain du tour
			while i<len(self._listanim):
				animi=self._listanim[i] 																																				#sélectionne un animal de la liste
				nbb, cci, ccmi=animi.vit(self._listanim) 																																#ajoute les individus de la liste de bébés et fait vivre tout les animaux
				cc+=cci
				ccm+=ccmi
				for l in range(nbb):
					self._listanim.append(hote.hote(self.canevas)) 																														#fais apparaitre les souris dans le canevas
				if not animi.est_vivant(): 																																				#regarde si l'animal est mort
					self._listanim.pop(i) 																																				#supprime l'individus de la liste
				else: 																																									#met en place la reproduction des animaux en passant par la gestation de ces derniers
					if animi.get_sexe()=="F" and isinstance(animi, hote.hote) and animi.get_age()>hote.hote.maturite and not animi.estgestante(): 										#on teste que les femelles mature et non enceinte et non malade
						j=0
						fin=0 																																							#si fin vaut 1, la boucle s'arrête pour ne pas tester tous les partenaires alors qu'elle est tombée enceinte du deuxiéme de la liste
						while j <len(self._listanim) and fin==0: 																														#tant que j n'est pas le dernier de la liste et que le femelle n'est pas enciente
							animj=self._listanim[j] 																																	#on regarde l'animla j
							if j !=i and type(animi)==type(animj) and animj.get_sexe()=="M" and self.dist(i,j)<hote.hote.vitessemax/2 and animj.get_age()>hote.hote.maturite: 			#on teste si un partenaire sain et mature est dans la place pour se reproduire (remarque si i = j on a "2" femelle donc pas de bébé, on pourrait retirer  ?Optimiser en changeant l'ordre?
								animi.devientgestante()																																	#appel de la fonnction qui fait tomber enceinte la femelle
								fin=1 																																					#la femelle est enceinte, la boucle peut s'arreter
							j+=1 																																						#j augmente, on regarde l'animla suivant de la liste
				i+=1 																																									#l'indice augmente de un, on va regardr l'animal suivant de la liste
			for l in range(cc):
				self._listanim.append(caca.caca(self.canevas)) 																															#ajoute les cacas sains à la liste des animaux
			cc=0
			for l in range(ccm):
				self._listanim.append(caca.caca(self.canevas, m=1)) 																													#ajoute les cacas malades à la liste des animaux
			ccm=0
			self.canevas.update_idletasks() 																																			#met à jour le canevas
			self._listanim+=baby 																																						#ajoute les bébés à la liste des animaux
			print("day:",t)
			time.sleep(0.1) 																																							#pause de'une demi seconde
			t+=1
			
	#efface toute la simulation
	def effacer(self):
		self.canevas.delete(ALL)
	
	#calcule la distance entre l'individus i et l'individus j	
	def dist(self,i,j):
		xi,yi=self._listanim[i].get_x(),self._listanim[i].get_y()
		xj,yj=self._listanim[j].get_x(),self._listanim[j].get_y()
		return math.sqrt((xi-xj)**2+(yi-yj)**2)
	
	#boucle du programme
	def main(self):
		self._fenetre.mainloop()

prgr= simulation()
prgr.main()
