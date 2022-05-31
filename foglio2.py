from math import ceil
from utility import *
import numpy as np
import mip


def MPS(periods,mix,domanda,M,work_time,costo_scorta,setup_cost,prods,scorte_in,scorte_fin1,scorte_fin2,period_cap):




    m=mip.Model()
    m.verbose=0

    scorte=[m.add_var(var_type=mip.INTEGER) for i in range(prods)]

    production=[m.add_var(var_type=mip.INTEGER) for i in range(periods) for j in range(prods) ]
    production=np.reshape(production,(periods,prods))


    has_production=[m.add_var(var_type=mip.BINARY) for i in range(periods) for j in range(prods) ]
    has_production=np.reshape(has_production,(periods,prods))

    n_setup=[m.add_var(var_type=mip.INTEGER) for i in range(periods)]

    scorte=[m.add_var( var_type=mip.INTEGER) for i in range(periods+1) for j in range(prods)]
    scorte=np.reshape(scorte,(periods+1,prods))

    tot_scorte=[m.add_var(var_type=mip.INTEGER) for i in range(prods)]


    for i in range(prods):
        pass
        for j in range(periods):
            pass
            m.add_constr(scorte[j,i]>=0)
            m.add_constr(has_production[j,i]<=production[j,i])#ok
            m.add_constr(has_production[j,i]*M>=production[j,i])#ok

    for i in range(periods):
        m.add_constr(mip.xsum(production[i,j]*work_time[j] for j in range(prods))<=period_cap[0])#######
        if i>0:
            m.add_constr(n_setup[i]==(mip.xsum(has_production[i,j] for j in range(prods))))#ok
        else:
            m.add_constr(n_setup[i]==(mip.xsum(has_production[i,j] for j in range(prods))-1))#ok
        for j in range(prods):
            pass
            m.add_constr(scorte[i+1,j]==(production[i,j] + scorte[i,j] - ceil(domanda[0]*mix[j]/periods) ))#ok
    for i in range(prods):
        pass
        m.add_constr(tot_scorte[i]==mip.xsum(scorte[j,i] for j in range(1,periods+1)))#ok
    m.add_constr(mip.xsum(scorte[0,i] for i in range(prods))==scorte_in)
    m.add_constr(mip.xsum(scorte[periods,i] for i in range(prods))==scorte_fin1)



    ########SECONDO TRIMESTRE

    scorte1=[m.add_var(var_type=mip.INTEGER) for i in range(prods)]

    production1=[m.add_var(var_type=mip.INTEGER) for i in range(periods) for j in range(prods) ]
    production1=np.reshape(production1,(periods,prods))


    has_production1=[m.add_var(var_type=mip.BINARY) for i in range(periods) for j in range(prods) ]
    has_production1=np.reshape(has_production1,(periods,prods))

    n_setup1=[m.add_var(var_type=mip.INTEGER) for i in range(periods)]

    scorte1=[m.add_var( var_type=mip.INTEGER) for i in range(periods+1) for j in range(prods)]
    scorte1=np.reshape(scorte1,(periods+1,prods))

    tot_scorte1=[m.add_var(var_type=mip.INTEGER) for i in range(prods)]


    for i in range(prods):
        pass
        for j in range(periods):
            pass
            m.add_constr(scorte1[j,i]>=0)
            m.add_constr(has_production1[j,i]<=production1[j,i])#ok
            m.add_constr(has_production1[j,i]*M>=production1[j,i])#ok

    for i in range(periods):
        m.add_constr(mip.xsum(production1[i,j]*work_time[j] for j in range(prods))<=period_cap[1])#######
        if i>0:
            m.add_constr(n_setup1[i]==(mip.xsum(has_production1[i,j] for j in range(prods))))#ok
        else:
            m.add_constr(n_setup1[i]==(mip.xsum(has_production1[i,j] for j in range(prods))-1))#ok
        for j in range(prods):
            pass
            m.add_constr(scorte1[i+1,j]==(production1[i,j] + scorte1[i,j] - ceil(domanda[1]*mix[j]/periods) ))#ok
    for i in range(prods):
        m.add_constr(scorte1[0,i]==scorte[periods,i])
        m.add_constr(tot_scorte1[i]==mip.xsum(scorte1[j,i] for j in range(1,periods+1)))#ok
    m.add_constr(mip.xsum(scorte1[periods,i] for i in range(prods))==scorte_fin2)


    m.objective=mip.minimize(mip.xsum(costo_scorta[i]*tot_scorte[i] for i in range(prods))+mip.xsum(n_setup[i] for i in range(periods))*setup_cost+mip.xsum(costo_scorta[i]*tot_scorte1[i] for i in range(prods))+mip.xsum(n_setup1[i] for i in range(periods))*setup_cost)
    m.optimize()
    print(m.objective_value)
    costo_scorte_tot=sum(costo_scorta[i]*tot_scorte[i].x for i in range(prods))
    costo_scorte_tot1=sum(costo_scorta[i]*tot_scorte1[i].x for i in range(prods))

    print ("tot scorte:")
    for i in range(prods):
        print(tot_scorte[i].x)
    print("production:")
    prodprint=np.zeros_like(production)
    has_prodprint=np.zeros_like(has_production)
    scorte_print=np.zeros_like(scorte)
    for i in range(periods):
        for j in range(prods):
            prodprint[i,j]=production[i,j].x
            has_prodprint[i,j]=has_production[i,j].x
    
            
    for i in range(periods+1):
        for j in range(prods):
            scorte_print[i,j]=scorte[i,j].x
    print(prodprint)
    print(has_prodprint)
    print("scorte:")
    print(scorte_print)
    print ("setup:")
    for i in range(periods):
        print(n_setup[i].x)
    print("costo scorte:",costo_scorte_tot)
    print("setup cost:",sum(n_setup[i].x for i in range(periods))*setup_cost)


    costo_scorte_tot=sum(costo_scorta[i]*tot_scorte1[i].x for i in range(prods))
    print ("tot scorte1:")
    for i in range(prods):
        print(tot_scorte1[i].x)
    print("production:")
    prodprint=np.zeros_like(production1)
    has_prodprint=np.zeros_like(has_production1)
    scorte_print=np.zeros_like(scorte1)
    for i in range(periods):
        for j in range(prods):
            prodprint[i,j]=production1[i,j].x
            has_prodprint[i,j]=has_production1[i,j].x
            
    for i in range(periods+1):
        for j in range(prods):
            scorte_print[i,j]=scorte1[i,j].x
    print(prodprint)
    print(has_prodprint)
    print("scorte1:")
    print(scorte_print)
    print ("setup1:")
    for i in range(periods):
        print(n_setup[i].x)
    print("costo scorte1:",costo_scorte_tot)
    print("setup cost1:",sum(n_setup1[i].x for i in range(periods))*setup_cost)


    return(toMatrix(scorte),toMatrix(scorte1),toMatrix(production),toMatrix(production1),costo_scorte_tot,costo_scorte_tot1,m.objective_value)