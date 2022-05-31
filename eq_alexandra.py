import mip
import numpy as np
from math import ceil

from utility import toArray

def PCAP(tr,domanda,sc_max,prz,cs_in,cl_or,cl_os,cms,nm):

    m=mip.Model()
    m.verbose=0

    
    o_r=m.add_var( var_type=mip.INTEGER)
    o_s=[m.add_var( var_type=mip.INTEGER) for i in range(tr)]
    scorte=[m.add_var( var_type=mip.INTEGER) for i in range(tr+1)]
    qtapr=[m.add_var( var_type=mip.INTEGER) for i in range(tr)]

    for i in range(tr):
        m.add_constr(o_s[i]<=0.5*o_r)
        m.add_constr(qtapr[i]+scorte[i]>=domanda[i])
        m.add_constr(qtapr[i]==(o_r+o_s[i]))
        m.add_constr(scorte[i+1]==qtapr[i]+scorte[i]-domanda[i])
    


    m.add_constr(scorte[0]<=sc_max)
    m.add_constr(scorte[4]>=scorte[0])


    m.objective=mip.maximize(mip.xsum(domanda[i]*prz for i in range(tr))+scorte[4]*cs_in-(cs_in*scorte[0]+mip.xsum(scorte[i]*cms for i in range(1,tr+1))+cl_or*o_r*nm*tr+mip.xsum(o_s[i]*cl_os*nm for i in range(tr))+mip.xsum(qtapr[i]*15 for i in range(tr))))
    m.optimize()

    return (o_r.x,toArray(o_s),toArray(scorte),toArray(qtapr),m.objective_value)

    




