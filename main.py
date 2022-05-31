import mip
import numpy as np
from math import ceil
from eq_alexandra import *
from foglio2 import *
from foglio3 import *
from utility import *

###PARAMETRI PRODUCTION CAP

scarto=[0.0, 0.00, 0.0 ,0.0]        #scarto rispetto alla domanda prevista
cl_or=10            #costo orario regolare
cl_os=15            #costo orario straordinario
cms=6               #costo mantenimento a scorta unità/trimestre
cs_in=45           #costo inserimento scorta iniziale per pezzo
nm=3                #numero medio di lavoro per pezzo
tr=4                #numero di trimestri
sc_max=300          #scorta massima iniziale
prz=70              #prezzo unitario di vendita prodotto

domanda_raw=[240,600,360,240] #domanda prevista per ogni trimestre

domanda=[ceil(domanda_raw[i]*(1+scarto[i])) for i in range(tr)]

###PARAMETRI MPS


setup_cost=40
periodi=12 
prods=3
mix=[0.2,0.2,0.6]

costo_scorta=[0.8,1.20,1] #costo scorta per ogni trimestre disaggregato
acqu_in=[30,60,45]        #costo acquisizione iniziale per ogni trimestre
vendita=[55,85,70]        #prezzo unitario di vendita prodotto
work_time=[2,4,3]         #tempo di lavoro per pezzo disaggregato

M=100000


###PARAMETRI MRP

distinta=np.array([[1, 1, 0, 0],
                  [0, 1, 1, 0],
                  [1, 0, 0, 1]])


costo_scorta=np.array([0.15, 0.15, 0.45, 0.30]) #costo mantemiento a scorta unità/periodo
LT=np.array([1, 1, 2, 1])                       #lead time per ogni prodotto (da modificare a mano nei constraint)

costo_ordine=12
materie_grezze=4
prodotti_finiti=3






result=PCAP(tr,domanda,sc_max,prz,cs_in,cl_or,cl_os,cms,nm)
o_r,o_s,scortePCAP,qtapr,objPCAP=result
scorte_in=scortePCAP[0]
scorte_fin1=scortePCAP[1]
scorte_fin2=scortePCAP[2]

capacity=[(o_r+o_s[i])*nm for i in range(tr)]
period_cap=[capacity[i]/(periodi/2) for i in range(tr)]
print("period",period_cap)
result=MPS(int(periodi/2),mix,domanda,M,work_time,costo_scorta,setup_cost,prods,scorte_in,scorte_fin1,scorte_fin2,period_cap)
scorteMPS,scorte1MPS,productionMPS,production1MPS,cs_tot,cs_tot1,objMPS=result

print(result)

produzione=np.concatenate((productionMPS,production1MPS))
print(produzione)
produzione=np.transpose(produzione)
result=MRP(produzione, distinta,periodi,costo_ordine,materie_grezze,prodotti_finiti,costo_scorta)
scorteMRP,ordini,costiMRP=result


#print some matrices to a text file
with open("optimization_results.txt","w+") as file:
    file.write("Scorte Production Cap\n")
    file.write(np.array2string(scortePCAP))
    file.write("\n\nLavoro regolare={}".format(o_r))
    file.write("\n\nLavoro straordinario:")
    file.write(np.array2string(o_s))
    file.write("\n\nScorte MPS trimestre1:\n")
    file.write(np.array2string(np.transpose(scorteMPS),separator='\t'))
    file.write("\n\nScorte MPS trimestre2:\n")
    file.write(np.array2string(np.transpose(scorte1MPS),separator='\t'))
    file.write("\n\nProduzione MPS:\n")
    file.write(np.array2string(produzione,separator='\t'))
    file.write("\n\nScorte MRP:\n")
    file.write(np.array2string(scorteMRP,separator='\t'))
    file.write("\n\nOrdini MRP:\n")
    file.write(np.array2string(ordini,separator='\t'))
    file.write("\n\nCosti MRP:\n")
    file.write(np.array2string(costiMRP,separator='\t'))