import numpy as np
import mip
from utility import *



'''
produzione=np.array([   [60, 0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0],
                        [0, 0, 45, 0, 45, 0, 0, 0, 0, 0, 0, 0],
                        [0, 60, 0, 60, 0, 0, 60, 60, 60, 60, 60, 60]])
'''
def MRP(produzione,distinta,periodi,costo_ordine,materie_grezze,prodotti_finiti,costo_scorta):


    fabbisogno=np.zeros((materie_grezze, periodi))
    for i in range(periodi):
        for j in range(materie_grezze):
            fabbisogno[j,i]=sum(produzione[k,i]*distinta[k,j] for k in range(prodotti_finiti))
    print(fabbisogno)

 
    m=mip.Model()
    m.verbose=0

    scorte=[m.add_var(var_type=mip.INTEGER) for i in range(materie_grezze) for i in range(periodi+1)]
    scorte=np.reshape(scorte, (materie_grezze, periodi+1))

    ordine=[m.add_var(var_type=mip.INTEGER) for i in range(materie_grezze) for i in range(periodi)]
    ordine=np.reshape(ordine, (materie_grezze, periodi))

    has_ordine=[m.add_var(var_type=mip.BINARY) for i in range(materie_grezze) for i in range(periodi)]
    has_ordine=np.reshape(has_ordine, (materie_grezze, periodi))

    has_giacenza=[m.add_var(var_type=mip.BINARY) for i in range(materie_grezze)]

    costi=[m.add_var(var_type=mip.INTEGER) for i in range(materie_grezze)]

    M=1000000
    for i in range(materie_grezze):
        m.add_constr(scorte[i,0]<=300)
        for j in range(periodi):
            m.add_constr(scorte[i,j]>=0)
            m.add_constr(has_ordine[i,j]<=ordine[i,j])#ok
            m.add_constr(has_ordine[i,j]*M>=ordine[i,j])#ok
            m.add_constr(scorte[i,j+1]==ordine[i,j]+scorte[i,j]-fabbisogno[i,j])#ok
    for i in range(materie_grezze):
        m.add_constr(has_ordine[i,0]==0)
        m.add_constr(has_giacenza[i]<=scorte[i,0])#ok
        m.add_constr(has_giacenza[i]*M>=scorte[i,0])#ok

    m.add_constr(has_ordine[2,1]==0)


    for i in range (materie_grezze):
        m.add_constr(costi[i]==(costo_scorta[i]*mip.xsum(scorte[i,j] for j in range(1,periodi))+costo_ordine*mip.xsum(has_ordine[i,j] for j in range(periodi))+costo_ordine*has_giacenza[i]))

    m.objective=mip.minimize(mip.xsum(costi[i] for i in range (materie_grezze)))
    m.optimize()
    print(m.objective_value)
    print("costi=")
    for i in range (materie_grezze):
        print(costi[i].x)

    return (toMatrix(scorte),toMatrix(ordine),toArray(costi))


