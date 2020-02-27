import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import matplotlib.animation as animation
from copy import copy, deepcopy


class modele(object):
	def __init__(self,H=100,L=100,n=6,I0=37,mwm=1,mmw=1,mww=0,mmm=0,bw=1,aw=1,R0w=2,bm=1,am=1,R0m=1.8,gl=False,loc=True, showMe=False,T=100):
		self.mat=[[0 for i in range (L)] for j in range (H)]

		self.n=n
		self.H=H
		self.L=L
		self.mwm=mwm
		self.mmw=mmw
		self.mww=mww
		self.mmm=mmm
		self.bw=bw
		self.aw=aw
		self.R0w=R0w
		self.bm=bm
		self.am=am
		self.R0m=R0m
		self.gl=gl
		self.loc=loc
		self.giveupafter=10
		self.square_min=0

		while ((self.square_min)**2)<n:
			self.square_min=self.square_min+1
		print(self.square_min)

		lc=int(I0**0.5)

		i0=int(H/2)-int(lc/2)
		j0=int(L/2)-int(lc/2)

		for i in range (I0):
			self.mat[i0][j0]=1
			j0=j0+1
			if j0>int(H/2)+int(lc/2):
				j0=int(H/2)-int(lc/2)
				i0=i0+1
		if showMe:
			for t in range (T):
				self.heatmap()
				self.spread()
				time.sleep(1)
	def restart(self):
		# ajouter le fait de changer des parametres ?
		self.mat=[[0 for i in range (self.L)] for j in range (self.H)]
		self.mat[random.randrange(0,self.H)][random.randrange(0,self.L)] = 1 #random place
	
	def gen_bool(self,prob):
		res=False
		temp=random.randint(0,10000)/100
		if temp<prob:
			res=True
		return res

	def kill_people(self):
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				
				#Wild
				if self.mat[i][j]==1 and self.gen_bool(self.aw):
					self.mat[i][j]=3

				#Virulent
				if self.mat[i][j]==2 and self.gen_bool(self.am):
					self.mat[i][j]=3

	def mute_strains(self):
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				if self.mat[i][j]==2:
					temp=self.gen_bool(self.mmw)
					if temp:
						self.mat[i][j]=1

				elif self.mat[i][j]==1:
					temp=self.gen_bool(self.mwm)
					if temp:
						self.mat[i][j]=2

	def gn_pos(self,i,j):
		new_i=random.randint(i-self.square_min,i+self.square_min)
		new_j=random.randint(j-self.square_min,j+self.square_min)
		return (new_i,new_j)
		
	def spread_loc(self):
		ancienne=deepcopy(self.mat)
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):

				#Virulent
				if self.mat[i][j]==2:
					for gens in range (self.n):
						temp=self.gen_bool(self.bm)
						if temp:
							compteur=0
							while compteur<self.giveupafter:
								tempi,tempj=self.gn_pos(i,j)
								try:
									if ancienne[tempi][tempj]==0:
										self.mat[tempi][tempj]=2
								except:
									compteur=self.giveupafter+1
									
								compteur=compteur+1
			
				#Wild
				elif self.mat[i][j]==1:
					for gens in range (self.n):
						temp=self.gen_bool(self.bw)
						if temp:
							compteur=0
							while compteur<self.giveupafter:
								tempi=i+random.randint(-1,1)
								tempj=j+random.randint(-1,1)
								try:
									if ancienne[tempi][tempj]==0:
										self.mat[tempi][tempj]=1
								except:
									compteur=self.giveupafter+1
									
								compteur=compteur+1

	def spread_gl(self):
		ancienne=deepcopy(self.mat)
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):

				#Virulent
				if self.mat[i][j]==2:
					temp=self.gen_bool(self.bm)
					if temp: 
						new_i=random.randint(0,self.H-1)
						new_j=random.randint(0,self.L-1)
						while ancienne[new_i][new_j]!=0:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
						self.mat[new_i][new_j]=2
						
				#Wild
				elif self.mat[i][j]==1:
					temp=self.gen_bool(self.bw)
					if temp:
						new_i=random.randint(0,self.H-1)
						new_j=random.randint(0,self.L-1)
						while ancienne[new_i][new_j]!=0:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
						self.mat[new_i][new_j]=1

	def spread(self):
		self.kill_people()
		
		self.mute_strains()
				
		if self.loc:
			self.spread_loc()
		
		if self.gl:
			self.spread_gl()
	
	def heatmap(self):
		res=''
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				if self.mat[i][j]==0:
					res=res+'.'
				elif self.mat[i][j]==1:
					res=res+'°'
				elif self.mat[i][j]==2:
					res=res+'*'
				elif self.mat[i][j]==3:
					res=res+'^'
				else:
					print('Erreur 404')
					res=res+'X'
					
			res=res+'\n'
		print(res)
					
		
if __name__ == '__main__':
	x=modele(showMe=True,H=50,L=50,gl=False,loc=True)
