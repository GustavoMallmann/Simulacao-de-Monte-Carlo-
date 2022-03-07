from numpy import random, empty, full, meshgrid, round
from math import sqrt, log
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


def resistencia_G1(apss):
    a = -4578.78  # pra que o resultado com aps medio fosse 10060.76
    return aps[0]*fps*(dp - a/2)  # FORM
    # return apss*fps*(dp - a/2) # MC

    # return 10060.76 # valor fixo de mu


def resistencia_G2(fcc):
    return 16 * sqrt(fc[0])  # FORM
    # return 16 * sqrt(fcc) # MC


def solicitacao_G1(dcc, mve):
    return (dc[0]*l*l/8) + mdw + (mve*(1+im)+mca)*dfm  # FORM
    # return (dc*l*l/8) + mdw + (mve*(1+im)+mca)*dfm # MC


def solicitacao_G2(dcc, mve):
    # FORM
    return (fpb + (dc[0]*l*l/8)/sgi + mdw/sgi + (mve*(1+im)+mca)*dfm/sgi)
    # return (fpb + (dcc*l*l/8)/sgi + mdw/sgi + (mve*(1+im)+mca)*dfm/sgi) # MC


simulacoes = 10000  # quantidade de simulacoes desejadas
# valores da tabela 3 (media e desvio padrao)
aps = [0.00276, 0.0000345]
ybs = [0.103, 0.0082]
ygc = [0.95, 0.009]
b = [1.63, 0.006]
fc = [45234.14, 6785.12]
fpu = [1969949.30, 49248.73]
hviga = [1.25, 0.010]
pinicial = [4268.49, 213.42]
dc = [16.33, 1.63]
mve = [1575.59, 393.90]
l = 25.2
mdw = 1679
fps = 1516.25
dp = 140.2
a = 0  # valor desconhecido
im = 1.28
#mca = 1213
mca = 396.9
dfm = 1
fpb = -19822.18
sgi = 0.2601

# inicializando variáveis auxiliares

falhasG1 = 0
falhasG2 = 0
g1 = empty(simulacoes)
g2 = empty(simulacoes)
resis_g1 = empty(simulacoes)
resis_g2 = empty(simulacoes)
solic_g1 = empty(simulacoes)
solic_g2 = empty(simulacoes)

# gerando os valores aleatorios com as correspondentes distribuiçoes
rAps = round(random.normal(aps[0], aps[1], simulacoes), 3)
rYbs = round(random.normal(ybs[0], ybs[1], simulacoes), 3)
rYgc = round(random.normal(ygc[0], ygc[1], simulacoes), 3)
rB = round(random.normal(b[0], b[1], simulacoes), 3)
rFc = round(random.lognormal(log(fc[0]), log(fc[1]), simulacoes), 3)
rFpu = round(random.lognormal(log(fpu[0]), log(fpu[1]), simulacoes), 3)
rHviga = round(random.normal(hviga[0], hviga[1], simulacoes), 3)
rPinicial = round(random.normal(pinicial[0], pinicial[1], simulacoes), 3)
rDc = round(random.normal(dc[0], dc[1], simulacoes), 3)
rMve = round(random.gumbel(mve[0], mve[1], simulacoes), 3)

# calcula as funções G1 e G2 para cada valor aleatório gerado, e acrescenta o contador de falhas
for i in range(0, simulacoes):
    resis_g1[i] = resistencia_G1(rAps[i])
    solic_g1[i] = solicitacao_G1(rDc[i], rMve[i])
    g1[i] = resis_g1[i] - solic_g1[i]
    if g1[i] < 0:
        falhasG1 += 1
    resis_g2[i] = resistencia_G2(rFc[i])
    solic_g2[i] = solicitacao_G2(rDc[i], rMve[i])
    g2[i] = resis_g2[i] - solic_g2[i]
    if g2[i] < 0:
        falhasG2 += 1

# probabilidade de falha das funções G
prob_falhaG1 = falhasG1/simulacoes
prob_falhaG2 = falhasG2/simulacoes
resis_g1 = round(resis_g1, 3)
solic_g1 = round(solic_g1, 3)
g1 = round(g1, 3)
resis_g2 = round(resis_g2, 3)
solic_g2 = round(solic_g2, 3)
g2 = round(g2, 3)
for i in range(0, 10):  # trocar o 10 por quantos valores se quer visualizar
    print(
        f"ResistênciaG1:{resis_g1[i]}  SolicitaçãoG1:{solic_g1[i]}  G1:{g1[i]}\nResistênciaG2:{resis_g2[i]}  SolicitaçãoG2:{solic_g2[i]}  G2:{g2[i]}")
print(
    f"\nProbabilidade de falha de G1:{prob_falhaG1}\nProbabilidade de falha de G2:{prob_falhaG2}\n")
# grafico G1
fig1 = plt.figure()
ax = plt.axes(projection='3d')
plt.xlabel("Resistência")
plt.ylabel("Solicitação")
Res1, Sol1 = meshgrid(resis_g1, solic_g1)
zG1 = Res1 - Sol1
ax.plot_surface(Res1, Sol1, zG1, cmap='viridis', edgecolor='none')

fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
plt.xlabel("Resistência")
plt.ylabel("Solicitação")
Res2, Sol2 = meshgrid(resis_g2, solic_g2)
zG2 = Res2 - Sol2
ax2.plot_surface(Res2, Sol2, zG2, cmap='viridis', edgecolor='none')

for j in range(0, 10):  # trocar o 10 por quantos valores se quer visualizar
    print(f"aps:{rAps[j]}  ybs:{rYbs[j]}  ygc:{rYgc[j]}  b:{rB[j]}  fc:{rFc[j]}  fpu:{rFpu[j]}  hviga:{rHviga[j]}  pinicial:{rPinicial[j]}  dc:{rDc[j]}  mve:{rMve[j]}")
# plt.show()
