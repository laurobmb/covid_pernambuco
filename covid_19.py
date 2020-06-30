# -*- coding: utf-8 -*-
"""covid-19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V5mIHo8x243fSDbV1a9AOs0VvZUtVm16
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import gzip
import urllib.request
from requests import get
from datetime import datetime
from IPython.display import display, HTML

def unzip(out_file):
    try:
        print('Descompactando arquivo',out_file)
        with gzip.GzipFile(out_file,'rb') as uncompressed:
            file_content = uncompressed.read()
        with open(out_file, 'wb') as f:
            f.write(file_content)
            return 0

    except Exception as e:
        print(e)
        return 1

def download(url, file_name):
    try:
        with open(file_name, "wb") as file:
            response = get(url)
            file.write(response.content)
        print('Download file',file_name)            
        return 0
    except Exception as e:
        print(e)
        return 1


cvs = glob.glob('*.cvs')
print('Tentando remover arquivos antigos')
for i in cvs:
    print('Removendo arquivos antigos')
    os.remove(i)
    
download('https://data.brasil.io/dataset/covid19/caso_full.csv.gz','caso_full.csv.gz')
unzip('caso_full.csv.gz')
download('https://brasil.io/dataset/covid19/caso/?is_last=True&place_type=city&state=PE&format=csv','pernambuco.csv')
download('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv','cases-brazil-cities-time.csv')
download('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv','cases-brazil-states.csv')
download('https://brasil.io/dataset/covid19/caso_full/?format=csv','brasil.csv')

now = datetime.now() 
print(now)
print(os.listdir('.'))

diretorio='files'
if not os.path.exists(diretorio):
    os.makedirs(diretorio)
    print("Pasta",diretorio,"criada ")
else:    
    print("Pasta",diretorio,"já existe")

df_municipio = pd.read_csv('cases-brazil-cities-time.csv')
display(df_municipio.tail())

df_estado = pd.read_csv('cases-brazil-states.csv')
display(df_estado.tail())

#Selecionando total de mortes no estado de Pernambuco
df_estado_pernambuco = df_estado[ ['date','state', 'deaths']]
df_estado_pernambuco = df_estado_pernambuco.loc[ (df_estado_pernambuco["state"]=="PE") & (df_estado_pernambuco["deaths"]>0) & (df_estado_pernambuco["date"] >= "2020-06-01") ]
df_estado_pernambuco.head()

sns.set_style('darkgrid')
plt.figure(figsize=(60,10))
g = sns.barplot(data=df_estado_pernambuco, x='date',y='deaths',palette="ch:.25")
plt.xticks(rotation=90)
plt.text(0,4500, "Gráfico de mortes acumuladas da COVID-19 em Pernambuco", fontsize = 60, color='Black', fontstyle='italic')

cont=0
for index, row in df_estado_pernambuco.iterrows():
  g.text(cont,row.deaths, row.deaths, color='black', ha="center",fontsize=20)
  cont = cont+1

g.figure.savefig('files/novos_mortes_pernambuco_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/novos_mortes_pernambuco_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

#Selecionando total de mortes por dia no estado de Pernambuco
df_estado_pernambuco = df_estado[ ['date','state', 'newDeaths']]
df_estado_pernambuco = df_estado_pernambuco.loc[(df_estado_pernambuco["state"]=="PE") & (df_estado_pernambuco["newDeaths"]>0)]
df_estado_pernambuco.tail()

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(data=df_estado_pernambuco, x='date',y='newDeaths',palette="BuGn_d",linewidth=2)
plt.xticks(rotation=90)
plt.title('Estudo de dados da COVID-19') 
plt.text(0,100, "Mortes por dia no estado de Pernambuco", fontsize = 40, color='Black', fontstyle='italic')

cont=0
for index, row in df_estado_pernambuco.iterrows():
  g.text(cont,row.newDeaths, row.newDeaths, color='black', ha="center",fontsize=9)
  cont = cont+1

g.figure.savefig('files/novos_mortes_pernambuco_por_dia.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/novos_mortes_pernambuco_por_dia.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
sns.distplot(df_estado_pernambuco['newDeaths'],color="y")
plt.title('Mortes por dia no estado de Pernambuco')

#Selecionando total de mortes no estado de Pernambuco
#print(df_estado.columns.values)
df_estado_pernambuco = df_estado[ ['date','state', 'newCases']]
df_estado_pernambuco = df_estado_pernambuco.loc[(df_estado_pernambuco["state"]=="PE")]
df_estado_pernambuco.tail()

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(data=df_estado_pernambuco, x='date',y='newCases',palette="Blues_d",linewidth=2)
plt.xticks(rotation=90)
plt.title('Estudo de dados da COVID-19') 
plt.text(0,2000, "Novos casos de COVID-19 por dia", fontsize = 40, color='Black', fontstyle='italic')
plt.text(0,1700, "em estado de Pernambuco", fontsize = 40, color='Black', fontstyle='italic')

cont=0
for index, row in df_estado_pernambuco.iterrows():
  g.text(cont,row.newCases, row.newCases, color='black', ha="center",fontsize=9)
  cont = cont+1

g.figure.savefig('files/novos_casos_pernambuco_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/novos_casos_pernambuco_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

#Selecionando total de mortes no estado de Pernambuco
#print(df_estado.columns.values)
df_estado_pernambuco = df_estado[ ['date','state', 'newCases']]
df_estado_pernambuco = df_estado_pernambuco.loc[(df_estado_pernambuco["state"]=="PE")]
df_estado_pernambuco.tail()

df_municipio = pd.read_csv('cases-brazil-cities-time.csv')
# Selecionando as colunas desejadas
df_paulista = df_municipio[ ['date','state','city','newCases']]
# Selecionando estado
df_paulista = df_paulista.loc[(df_paulista["state"]=="PE")]
# Selecionando municipio de Paulista
df_paulista = df_paulista.loc[(df_paulista["city"]=="Paulista/PE")]


display(df_paulista.tail())

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(data=df_paulista, x='date',y='newCases',palette="cubehelix",linewidth=2)
plt.xticks(rotation=90)
plt.title('Estudo de dados da COVID-19') 
plt.text(0,120, "Novos casos de COVID-19 por dia", fontsize = 25, color='Black', fontstyle='italic')
plt.text(0,100, "em Paulista/PE", fontsize = 25, color='Black', fontstyle='italic')

cont=0
for index, row in df_paulista.iterrows():
  g.text(cont,row.newCases, row.newCases, color='black', ha="center",fontsize=9)
  cont = cont+1

g.figure.savefig('files/novos_casos_paulista_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/novos_casos_paulista_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

#Selecionando total de mortes no estado de Pernambuco
#print(df_estado.columns.values)
df_estado_pernambuco = df_estado[ ['date','state', 'newCases']]
df_estado_pernambuco = df_estado_pernambuco.loc[(df_estado_pernambuco["state"]=="PE")]
df_estado_pernambuco.tail()

df_municipio = pd.read_csv('cases-brazil-cities-time.csv')
# Selecionando as colunas desejadas
df_paulista = df_municipio[ ['date','state','city','newCases']]
# Selecionando estado
df_paulista = df_paulista.loc[(df_paulista["state"]=="PE")]
# Selecionando municipio de Recife
df_paulista = df_paulista.loc[(df_paulista["city"]=="Recife/PE")]


display(df_paulista.tail())

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(data=df_paulista, x='date',y='newCases',palette="cubehelix",linewidth=2)
plt.xticks(rotation=90)
plt.title('Estudo de dados da COVID-19') 
plt.text(0,1000, "Novos casos de COVID-19 por dia", fontsize = 25, color='Black', fontstyle='italic')
plt.text(0,900, "em Recife/PE", fontsize = 25, color='Black', fontstyle='italic')

cont=0
for index, row in df_paulista.iterrows():
  g.text(cont,row.newCases, row.newCases, color='black', ha="center",fontsize=9)
  cont = cont+1

g.figure.savefig('files/novos_casos_recife_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/novos_casos_recife_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

#Selecionando total de mortes no estado de Pernambuco
#print(df_estado.columns.values)
df_estado_pernambuco = df_estado[ ['date','state', 'newCases']]
df_estado_pernambuco = df_estado_pernambuco.loc[(df_estado_pernambuco["state"]=="PE")]
df_estado_pernambuco.tail()

df_municipio = pd.read_csv('cases-brazil-cities-time.csv')
# Selecionando as colunas desejadas
df_paulista = df_municipio[ ['date','state','city','newCases']]
# Selecionando estado
df_paulista = df_paulista.loc[(df_paulista["state"]=="PE")]
# Selecionando municipio de Olinda
df_paulista = df_paulista.loc[(df_paulista["city"]=="Olinda/PE")]


display(df_paulista.tail())

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(data=df_paulista, x='date',y='newCases',palette="cubehelix",linewidth=2)
plt.xticks(rotation=90)
plt.title('Estudo de dados da COVID-19') 
plt.text(0,150, "Novos casos de COVID-19 por dia", fontsize = 25, color='Black', fontstyle='italic')
plt.text(0,100, "em Olinda/PE", fontsize = 25, color='Black', fontstyle='italic')

cont=0
for index, row in df_paulista.iterrows():
  g.text(cont,row.newCases, row.newCases, color='black', ha="center",fontsize=9)
  cont = cont+1

g.figure.savefig('files/novos_casos_olinda_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/novos_casos_olinda_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

#Selecionando total de mortes no estado de Pernambuco
#print(df_estado.columns.values)
#df_estado_pernambuco = df_estado[ ['date','state', 'deaths']]
#df_estado_pernambuco = df_estado_pernambuco.loc[(df_estado_pernambuco["state"]=="PE")]
#df_estado_pernambuco.tail()

# Carregando dataframe
df_municipio = pd.read_csv('cases-brazil-cities-time.csv')
#display(df_municipio.tail())

# Selecionando as colunas desejadas
df_paulista = df_municipio[ ['date','state','city','newDeaths']]
# Selecionando estado e datas
df_paulista_deaths_03 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-03-01") & (df_paulista["date"] <= "2020-03-31") ]
df_paulista_deaths_04 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-04-01") & (df_paulista["date"] <= "2020-04-31") ]
df_paulista_deaths_05 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-05-01") & (df_paulista["date"] <= "2020-05-31") ]
df_paulista_deaths_06 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-06-01") & (df_paulista["date"] <= "2020-06-31") ]

# Selecionando as colunas desejadas
df_paulista = df_municipio[ ['date','state','city','newCases']]
# Selecionando estado e datas
df_paulista_totalCases_03 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-03-01") & (df_paulista["date"] <= "2020-03-31") ]
df_paulista_totalCases_04 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-04-01") & (df_paulista["date"] <= "2020-04-31") ]
df_paulista_totalCases_05 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-05-01") & (df_paulista["date"] <= "2020-05-31") ]
df_paulista_totalCases_06 = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-06-01") & (df_paulista["date"] <= "2020-06-31") ]

# Número de mortes por mês
sum_row = df_paulista_deaths_05.sum(axis=0)
print(sum_row.newDeaths)

# Número de casos por mês
sum_row = df_paulista_totalCases_03.sum(axis=0)
print(sum_row.newCases)


data = {'month': ['Mar ','Apr ','May ','Jun '],
        'deaths': [
                   df_paulista_deaths_03.sum(axis=0).newDeaths,
                   df_paulista_deaths_04.sum(axis=0).newDeaths,
                   df_paulista_deaths_05.sum(axis=0).newDeaths,
                   df_paulista_deaths_06.sum(axis=0).newDeaths,
                   ],
        'cases': [
                  df_paulista_totalCases_03.sum(axis=0).newCases,
                  df_paulista_totalCases_04.sum(axis=0).newCases,
                  df_paulista_totalCases_05.sum(axis=0).newCases,
                  df_paulista_totalCases_06.sum(axis=0).newCases,
                  ]
        }

df = pd.DataFrame(data)
display(df)

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(x="month", y="deaths", data=df,palette="hot",linewidth=2);
plt.title('Estudo de dados da COVID-19') 
plt.text(0,2000, "Gráfico de mortes por mês", fontsize = 40, color='Black', fontstyle='italic')
plt.text(0,1800, "no estado de Pernumbuco", fontsize = 40, color='Black', fontstyle='italic')


cont=0
for index, row in df.iterrows():
  g.text(cont,row.deaths, row.deaths, color='black', ha="center",fontsize=30)
  cont = cont+1

g.figure.savefig('files/mortes_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/mortes_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

df = pd.DataFrame(data)
display(df)

sns.set_style('darkgrid')
plt.figure(figsize=(31,8))
g = sns.barplot(x="month", y="cases", data=df,palette="Reds",linewidth=2);
plt.title('Estudo de dados da COVID-19') 
plt.text(0,25000, "Gráfico de casos por mês", fontsize = 40, color='Black', fontstyle='italic')
plt.text(0,23000, "no estado de Pernumbuco", fontsize = 40, color='Black', fontstyle='italic')

cont=0
for index, row in df.iterrows():
  g.text(cont,row.cases, row.cases, color='black', ha="center",fontsize=30)
  cont = cont+1

g.figure.savefig('files/casos_por_mes.png',dpi=200,bbox_inches='tight',orientation='landscape',quality=90)
#g.figure.savefig('files/casos_por_mes.pdf',dpi=600,bbox_inches='tight',orientation='landscape',quality=90)

#df_municipio = pd.read_csv('cases-brazil-cities-time.csv')
#display(df_municipio.tail())

df_estado = pd.read_csv('cases-brazil-states.csv')
#display(df_estado.tail())

df_paulista = df_estado[ ['date','state','recovered']]

# Selecionando estado e datas
df_paulista_recovered = df_paulista.loc[ (df_paulista["state"]=="PE") & (df_paulista["date"] >= "2020-06-15") & (df_paulista["date"] <= "2020-06-31") ]
#print(df_paulista_recovered.tail() )
sns.set_style('darkgrid')
plt.figure(figsize=(30,8))
plt.xticks(rotation=90)
g = sns.barplot(x="date", y="recovered",palette = 'hot',data=df_paulista_recovered)
g.text(0,39000, "Números de recuperados em Pernambuco da COVID-19", fontsize = 35, color='Black', fontstyle='italic')
plt.title('Estudo de dados da COVID-19') 

cont=0
for index, row in df_paulista_recovered.iterrows():
  g.text(cont,row.recovered, row.recovered, color='black', ha="center",fontsize=12)
  cont = cont+1


g.figure.savefig('files/recuperados_pernambuco.png',dpi=200,quality=90)

download('https://dados.seplag.pe.gov.br/apps/basegeral.csv','basegeral.csv')
df_basegeral = pd.read_csv('basegeral.csv',sep=';')
display(df_basegeral.tail())
df_basegeral = df_basegeral[ ['Sexo','Resultado','evolucao','faixa_etaria']]
display(df_basegeral.tail())

display(df_basegeral['evolucao'].drop_duplicates())
display(df_basegeral['Sexo'].drop_duplicates())
display(df_basegeral['faixa_etaria'].drop_duplicates())
display(df_basegeral['Resultado'].drop_duplicates())




#ax = sns.barplot(x="Resultado", y="faixa_etaria", hue="Sexo", data=df_basegeral)

import matplotlib.pyplot as plt

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
