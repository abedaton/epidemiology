import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import matplotlib.animation as animation
from copy import copy, deepcopy


class modele(object):
	def __init__(self,H=100,L=100,n=6,I0=37,mwm=1,mmw=1,mww=0,mmm=0,bw=1,aw=1,R0w=2,bm=1,am=1,R0m=1.8,gl=False,loc=True, showMe=False):
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
		self.minimum_lenght_of_a_square_to_fit_all_n_in_it=0
		while ((self.minimum_lenght_of_a_square_to_fit_all_n_in_it/2)**2)<n:
			self.minimum_lenght_of_a_square_to_fit_all_n_in_it=self.minimum_lenght_of_a_square_to_fit_all_n_in_it+1
		print(self.minimum_lenght_of_a_square_to_fit_all_n_in_it)
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
			self.heatmap()

	def gen_bool_from_a_certian_probability_out_of_100(self,prob):
		res=False
		temp=random.randint(0,10000)/100
		if temp<prob:
			res=True
		return res

	def kill_people(self):
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				#Wild
				if self.mat[i][j]==1 and self.gen_bool_from_a_certian_probability_out_of_100(self.aw):
					self.mat[i][j]=3

				#Virulent
				if self.mat[i][j]==2 and self.gen_bool_from_a_certian_probability_out_of_100(self.am):
					self.mat[i][j]=3
			#temp=self.gen_bool_from_a_certian_probability_out_of_100(self.am)

	def mute_strains(self):
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				if self.mat[i][j]==2:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.mmw)
					if temp:
						self.mat[i][j]=1

				elif self.mat[i][j]==1:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.mwm)
					if temp:
						self.mat[i][j]=2

	def gn_pos(self,i,j):
		#new_i=random.randint(i-self.minimum_lenght_of_a_square_to_fit_all_n_in_it,i+self.minimum_lenght_of_a_square_to_fit_all_n_in_it)
		#new_j=random.randint(j-self.minimum_lenght_of_a_square_to_fit_all_n_in_it,j+self.minimum_lenght_of_a_square_to_fit_all_n_in_it)
		new_i=i+random.randint(-1,1)
		new_j=j+random.randint(-1,1)
		return (new_i,new_j)
		
	def spread_loc(self):
		ancienne=deepcopy(self.mat)
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				#Virulent
				if self.mat[i][j]==2:
					for gens in range (self.n):
						temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bm)
						if temp:
							compteur=0
							while compteur<self.giveupafter:
								#tempi=i+random.randint(-1,1)
								#tempj=j+random.randint(-1,1)
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
						temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bw)
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
		#self.mat=deepcopy(ancienne)
	def spread_gl(self):
		ancienne=deepcopy(self.mat)
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				#Virulent
				if self.mat[i][j]==2:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bm)
					if temp: 
						new_i=random.randint(0,self.H-1)
						new_j=random.randint(0,self.L-1)
						while ancienne[new_i][new_j]!=0:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
						self.mat[new_i][new_j]=2
						
				#Wild
				elif self.mat[i][j]==1:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bw)
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
		
if __name__ == '__main__':
	x=modele(showMe=True)
