#Reprend les données trouvées ainsi que leur source
import numpy as np
import random

class Data(object):
    """docstring for Data."""

    def __init__(self):
        """

        """
        self.I_0 = 1
        #Inconnu mais techniquement une seule personne
        self.ageGroups = \
        ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44',\
        '45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85-89',\
        '90-94','95-99']
        self.agePyramid = \
        {'0-4' : 314124 + 299950,'5-9' : 339657 + 324571,'10-14' : 335209 + 319591,
        '15-19' : 321799 + 306978,'20-24' : 338535 + 328480,'25-29' : 372076 + 370967,\
        '30-34' : 366079 + 367695,'35-39' : 375382 + 373952,'40-44' : 367726 + 362357,\
        '45-49' : 393030 + 383781,'50-54' : 406065 + 396423,'55-59' : 395680 + 395329,\
        '60-64' : 349903 + 360317,'65-69' : 298531 + 316977,'70-74' : 249917 + 281584,\
        '75-79' : 165270 + 206033,'80-84' : 131151 + 188231,'85-89' : 76744 + 138525,\
        '90-94' : 26049 + 63748,'95-99' : 4641 + 16412}
        #https://statbel.fgov.be/fr/themes/population/structure-de-la-population (01/01/19)

        self.ageBracketToGroupBracket = \
        {'0-4': ('0-4','5-9','10-14','15-19'), '5-9' : ('0-4','5-9','10-14','15-19'),\
        '10-14' : ('0-4','5-9','10-14','15-19'), '15-19' : ('0-4','5-9','10-14','15-19'),\
        '20-24' : ('20-24','25-29','30-34','35-39','40-44'),\
         '25-29' : ('20-24','25-29','30-34','35-39','40-44'), '30-34' : ('20-24','25-29','30-34','35-39','40-44'),\
         '35-39' : ('20-24','25-29','30-34','35-39','40-44'), '40-44' : ('20-24','25-29','30-34','35-39','40-44'),\
         '45-49' : ('45-49','50-54'), '50-54' : ('45-49','50-54'),\
         '55-59': ('55-59,60-64'), '60-64' : ('55-59,60-64'),\
         '65-69' : ('65-69,70-74'), '70-74' :('65-69,70-74'),\
         '75-79' : ('75-79,80-84'), '80-84' : ('75-79,80-84'),\
         '85-89' : ('85-89','90-94','95-99'), '90-94': ('85-89','90-94','95-99'), '95-99' : ('85-89','90-94','95-99')}

        self.N = 0 #Population Belgique
        for key in self.ageGroups:
            self.N += self.agePyramid[key]

        self.probabilityAgeWeight =\
        [self.agePyramid[self.ageGroups[0]]/self.N,\
        self.agePyramid[self.ageGroups[1]]/self.N,\
        self.agePyramid[self.ageGroups[2]]/self.N,\
        self.agePyramid[self.ageGroups[3]]/self.N,\
        self.agePyramid[self.ageGroups[4]]/self.N,\
        self.agePyramid[self.ageGroups[5]]/self.N,\
        self.agePyramid[self.ageGroups[6]]/self.N,\
        self.agePyramid[self.ageGroups[7]]/self.N,\
        self.agePyramid[self.ageGroups[8]]/self.N,\
        self.agePyramid[self.ageGroups[9]]/self.N,\
        self.agePyramid[self.ageGroups[10]]/self.N,\
        self.agePyramid[self.ageGroups[11]]/self.N,\
        self.agePyramid[self.ageGroups[12]]/self.N,\
        self.agePyramid[self.ageGroups[13]]/self.N,\
        self.agePyramid[self.ageGroups[14]]/self.N,\
        self.agePyramid[self.ageGroups[15]]/self.N,\
        self.agePyramid[self.ageGroups[16]]/self.N,\
        self.agePyramid[self.ageGroups[17]]/self.N,\
        self.agePyramid[self.ageGroups[18]]/self.N,\
        self.agePyramid[self.ageGroups[19]]/self.N]

        #Taux d'hospitalisation sachant touché par la maladie
        self.hospitalizationRate = \
        {('0-4','5-9','10-14','15-19') : 1.6,\
         ('20-24','25-29','30-34','35-39','40-44') : 14.3,\
         ('45-49','50-54') : 21.2, ('55-59,60-64') : 20.5,\
         ('65-69,70-74') : 28.6, ('75-79,80-84') : 30.5,\
         ('85-89','90-94','95-99'): 31.3}

        #Taux d'admissions en soin intensif sachant touché par la maladie
        self.ICURate = \
        {('0-4','5-9','10-14','15-19') : 0,\
         ('20-24','25-29','30-34','35-39','40-44') : 2,\
         ('45-49','50-54') : 5.4, ('55-59,60-64') : 4.7,\
         ('65-69,70-74') : 8.1, ('75-79,80-84') : 10.5,\
         ('85-89','90-94','95-99'): 6.3}

        #Taux de mort sachant touché par la maladie
        self.deathRate = \
        {('0-4','5-9','10-14','15-19') : 0,\
        ('20-24','25-29','30-34','35-39','40-44') : 0.1,\
        ('45-49','50-54') : 0.5, ('55-59,60-64') : 1.4,\
        ('65-69,70-74') : 2.7, ('75-79,80-84') : 4.3,\
        ('85-89','90-94','95-99'): 10.4}
        #Source : https://www.cdc.gov/mmwr/volumes/69/wr/mm6912e2.htm#F1_down (12/02/20->16/03/20)

        self.noConsequenceRate = \
        {('0-4','5-9','10-14','15-19') : 100-self.hospitalizationRate[('0-4','5-9','10-14','15-19')]-self.ICURate[('0-4','5-9','10-14','15-19')]-self.deathRate[('0-4','5-9','10-14','15-19')],\
        ('20-24','25-29','30-34','35-39','40-44') : 100-self.hospitalizationRate[('20-24','25-29','30-34','35-39','40-44')]-self.ICURate[('20-24','25-29','30-34','35-39','40-44')]-self.deathRate[('20-24','25-29','30-34','35-39','40-44')],\
        ('45-49','50-54') : 100-self.hospitalizationRate[('45-49','50-54')]-self.ICURate[('45-49','50-54')]-self.deathRate[('45-49','50-54')],\
        ('55-59,60-64') : 100-self.hospitalizationRate[('55-59,60-64')]-self.ICURate[('55-59,60-64')]-self.deathRate[('55-59,60-64')],\
        ('65-69,70-74') : 100-self.hospitalizationRate[('65-69,70-74')]-self.ICURate[('65-69,70-74')]-self.deathRate[('65-69,70-74')],\
        ('75-79,80-84') : 100-self.hospitalizationRate[('75-79,80-84')]-self.ICURate[('75-79,80-84')]-self.deathRate[('75-79,80-84')],\
        ('85-89','90-94','95-99'): 100-self.hospitalizationRate[('85-89','90-94','95-99')]-self.ICURate[('85-89','90-94','95-99')]-self.deathRate[('85-89','90-94','95-99')]}

        #Vérification des données
        for key in self.noConsequenceRate.keys():
            total = self.hospitalizationRate[key] + self.ICURate[key] + self.deathRate[key] + self.noConsequenceRate[key]
            if not (99.99 < total < 100.01):
                print("Error calculating data")


        #FORTE HYPOTHESE : les deux suivent une loi normale
        self.medianViralShedding = 20 #https://doi.org/10.1016/S0140-6736(20)30566-3
        self.SDViralShedding = 7/1.35 #https://doi.org/10.1016/S0140-6736(20)30566-3
        # divide by 1.35 : https://www.researchgate.net/post/Is_there_any_way_to_get_mean_and_SD_from_median_and_IQR_interquartile_range
        self.medianR0 = 2.79 #https://doi.org/10.1093/jtm/taaa021
        self.SDR0 = 1.16/1.35 #https://doi.org/10.1093/jtm/taaa021

        self.medianIncubationTime = 6.4 #https://doi.org/10.2807/1560-7917.ES.2020.25.5.2000062
        self.SDIncubationTime = 2.3 #https://doi.org/10.2807/1560-7917.ES.2020.25.5.2000062



    def getTimeViralShedding(self, nb=1):
        #Minimum observé dans https://doi.org/10.1016/S0140-6736(20)30566-3 : 8
        #HYPOTHESE : A la fin du viral shedding, la personne est soit rétablie soit morte ( pas de mort plus rapide si état critique)
        #HYPOTHESE PAR MANQUE D'INFORMATION : Une fois qu'une personne est infectée, elle peut immédiatement (le jour même) transmettre le virus
        #Ce qui est une forte hypothèse qui nous fait dériver des observations
        return np.random.normal(self.medianViralShedding, self.SDViralShedding, size=nb)

    def getR0(self, nb=1):
        #Pas de nombre de transmission négatif
        return np.random.normal(self.medianR0,self.SDR0, size=nb)

    def getIncubationPeriod(self, nb=1):
        #Le modèle est beaucoup trop loin de la réalité à cause de ce manque d'information. Selon https://doi.org/10.1016/j.ijantimicag.2020.105924,
        #la période d'incubation est en moyenne de 6.4 jours avec un écart type de 2.3 jours
        return np.random.normal(self.medianIncubationTime, self.SDIncubationTime, size=nb)
