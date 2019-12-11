import random



class modele(object):
	def __init__(self,H=100,L=100,n=6,I0=37,mwm=1,mmw=1,mww=0,mmm=0,bw=2,aw=1,R0w=2,bm=7.2,am=4,R0m=1.8,gl=False,loc=True):
		self.mat=[['S' for i in range (L)] for j in range (H)]

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
			self.mat[i0][j0]='W'
			j0=j0+1
			if j0>int(H/2)+int(lc/2):
				j0=int(H/2)-int(lc/2)
				i0=i0+1

	def gen_bool_from_a_certian_probability_out_of_100(self,prob):
		res=False
		temp=random.randint(0,10000)/100
		if temp<prob:
			res=True
		return res



	def spread(self):
		#Mutation
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				if self.mat[i][j]=='M':
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.mmw)
					if temp:
						self.mat[i][j]='W'

				if self.mat[i][j]=='W':
					temp=self.gen_bool_from_a_certian_probability_out_of_100(self.mwm)
					if temp:
						self.mat[i][j]='M'

		#Local
		if self.loc:
			for i in range (len(self.mat)):
				for j in range (len(self.mat[0])):
					#Virulent
					if self.mat[i][j]=='M':
						for gens in range (self.n):
							temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bm)
							if temp:
								new_i=j
								new_j=i
								ite=0
								k=1
								while self.mat[new_i][new_j]=='M':
									ite=ite+1
									new_i=i+random.randint(-k,k)
									new_j=j+random.randint(-k,k)
									if ite==25:
										k=k+1
										ite=0
								self.mat[new_i][new_j]='M'
					#Wild
					if self.mat[i][j]=='W':
						for gens in range (self.n):
							temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bw)
							if temp:
								new_i=j
								new_j=i
								ite=0
								k=1
								while self.mat[new_i][new_j]=='W':
									ite=ite+1
									new_i=i+random.randint(-k,k)
									new_j=j+random.randint(-k,k)
									if ite==25:
										k=k+1
										ite=0
								self.mat[new_i][new_j]='W'
						#temp=self.gen_bool_from_a_certian_probability_out_of_100(self.)
						#Faire un truc avc la virulence ?
					

		#Global
		if self.gl:
			for i in range (len(self.mat)):
				for j in range (len(self.mat[0])):
					#Virulent
					if self.mat[i][j]=='M':
						temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bm)
						if temp:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
							self.mat[new_i][new_j]='M'

					#Wild
					if self.mat[i][j]=='W':
						temp=self.gen_bool_from_a_certian_probability_out_of_100(self.bw)
						if temp:
							new_i=random.randint(0,self.H-1)
							new_j=random.randint(0,self.L-1)
							self.mat[new_i][new_j]='W'


						#temp=self.gen_bool_from_a_certian_probability_out_of_100(self.aw)
						#temp=self.gen_bool_from_a_certian_probability_out_of_100(self.am)
						#Faire un truc avc la virulence ?


	def display(self):
		print()
		for i in range (len(self.mat)):
			for j in range (len(self.mat[0])):
				print(self.mat[i][j],end='')
			print()


x=modele()
x.display()

for i in range (100):
	x.spread()
	x.display()
