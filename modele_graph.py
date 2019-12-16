import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import matplotlib.animation as animation


class modele(object):
	def __init__(self,H=100,L=100,n=6,I0=37,mwm=1,mmw=1,mww=0,mmm=0,bw=2,aw=1,R0w=2,bm=7.2,am=4,R0m=1.8,gl=False,loc=True, showMe=False):
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



	def spread(self):
		#Wild 1
		#Virulent 2

		#Deces
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				#Wild
				if self.mat[i][j]==1:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.aw)
					if temp:
						self.mat[i][j]=3

				#Virulent
				if self.mat[i][j]==2:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.am)
					if temp:
						self.mat[i][j]=3
			#temp=self.gen_bool_from_a_certian_probability_out_of_100(self.am)

		#Mutation
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				if self.mat[i][j]==2:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.mmw)
					if temp:
						self.mat[i][j]=1

				if self.mat[i][j]==1:
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.mwm)
					if temp:
						self.mat[i][j]=2

		#Local
		if self.loc:
			for i in range (len(self.mat)):
				for j in range (len(self.mat[0])):
					#Virulent
					if self.mat[i][j]==2:
						for gens in range (self.n):
							temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bm)
							if temp:
								new_i=j
								new_j=i
								ite=0
								k=1
								while self.mat[new_i][new_j]==2:
									ite=ite+1
									new_i=max(0,min((len(self.mat))-1,(i+random.randint(-k,k))))
									new_j=max(0,min((len(self.mat[0]))-1,j+random.randint(-k,k)))
									if ite==25:
										k=k+1
										ite=0
								self.mat[new_i][new_j]=2
					#Wild
					if self.mat[i][j]==1:
						for gens in range (self.n):
							temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bw)
							if temp:
								new_i=j-1
								new_j=i-1
								ite=0
								k=1
								while self.mat[new_i][new_j]==1:
									ite=ite+1
									new_i=max(0,min((len(self.mat))-1,i+random.randint(-k,k)))
									new_j=max(0,min((len(self.mat[0]))-1,j+random.randint(-k,k)))
									if ite==25:
										k=k+1
										ite=0
								self.mat[new_i][new_j]=1



		#Global
		if self.gl:
			for i in range (len(self.mat)):
				for j in range (len(self.mat[0])):
					#Virulent
					if self.mat[i][j]==2:
						temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bm)
						if temp:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
							self.mat[new_i][new_j]=2

					#Wild
					if self.mat[i][j]==1:
						temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bw)
						if temp:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
							self.mat[new_i][new_j]=1

	def heatmap(self):
		self.fig, ax_lst = plt.subplots(1,1)
		heatmap = ax_lst.pcolor(self.mat)
		self.fig.canvas.draw()
		self.fig.show()

		while True:
			self.spread()

			heatmap = ax_lst.pcolor(self.mat)
			ax_lst.draw_artist(ax_lst.patch)
			ax_lst.draw_artist(heatmap)
			self.fig.canvas.blit(ax_lst.bbox)
			self.fig.canvas.flush_events()

if __name__ == '__main__':
	x=modele(showMe=True)
