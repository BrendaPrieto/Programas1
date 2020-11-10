from gurobipy import *
model_tela= Model("ProgramarProduccion")
Telas=[1,2,3,4,5]
TelasR=[3,4,5]
VelocidadJ=[4.63,4.63,5.23,5.23,4.17]
VelocidadR=[5.23,5.23,4.17]

#Variables de decisión
CantTelaLJ = model_tela.addVars(Telas,vtype=GRB.CONTINUOUS, name="Cantidad de tela (m)J")
CantTelaLR = model_tela.addVars(TelasR,vtype=GRB.CONTINUOUS, name="Cantidad de tela (m)R")
CantTelaP = model_tela.addVars(Telas,vtype=GRB.CONTINUOUS, name="Cantidad de tela (m) a comprar")

#Restricciones de demanda
model_tela.addConstr(CantTelaLJ[Telas[0]]+CantTelaP[Telas[0]]>=16500)
model_tela.addConstr(CantTelaLJ[Telas[1]]+CantTelaP[Telas[1]]>=22000)
model_tela.addConstr(CantTelaLJ[Telas[2]]+CantTelaLR[TelasR[0]]+CantTelaP[Telas[2]]>=62000)
model_tela.addConstr(CantTelaLJ[Telas[3]]+CantTelaLR[TelasR[1]]+CantTelaP[Telas[3]]>=7500)
model_tela.addConstr(CantTelaLJ[Telas[4]]+CantTelaLR[TelasR[2]]+CantTelaP[Telas[4]]>=62000)

#Restricciones de capacidad de horas de trabajo
model_tela.addConstr(quicksum((1/(VelocidadJ[i]*24*30))*CantTelaLJ[Telas[i]] for i in range(5)) <= 8)
model_tela.addConstr(quicksum((1/(VelocidadR[i]*24*30))*CantTelaLR[TelasR[i]] for i in range(3)) <= 30)


#Función objetivo

#FuncionObjetivo =1.33*CantTelaLJ[Telas[0]]+1.13*CantTelaP[Telas[0]]+1.31*CantTelaLJ[Telas[1]]+1.16*CantTelaP[Telas[1]]+1.61*(CantTelaLJ[Telas[2]]+CantTelaLR[TelasR[0]])+1.5*CantTelaP[Telas[2]]+1.73*(CantTelaLJ[Telas[3]]+CantTelaLR[TelasR[1]])+1.54*CantTelaP[Telas[3]]+1.2*(CantTelaLJ[Telas[4]]+CantTelaLR[TelasR[2]])+CantTelaP[Telas[4]]
FuncionObjetivo=0

model_tela.setObjective(FuncionObjetivo, GRB.MAXIMIZE)

model_tela.write("PlanProduccionTela.lp")
model_tela.optimize()
if model_tela.SolCount > 0:
    model_tela.printAttr("x")
    print("FO: %g" % FuncionObjetivo.getValue())


