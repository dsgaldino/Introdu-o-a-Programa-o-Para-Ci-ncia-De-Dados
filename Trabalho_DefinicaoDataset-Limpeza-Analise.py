#!/usr/bin/env python
# coding: utf-8

# # Análise de consumo de energia de diversos setores

# ## Informações sobre o dataset
# 
# #### Data e Hora
# * Begin - Datatime inicial
# * End - Datatime final
# 
# #### Preço da Energia Elétrica
# * Import (EUR/kWh) - O valor da energia elétrica consumida pelos clientes da rede
# * Export (EUR/kWh) - O valor da energia retornada dos consumidores a rede
# 
# #### Consumo de energia elétrica por empresa (Siglas)
# * CCF - Consumo de energia elétrica de uma fábrica de chocolate
# * CHT - Consumo de energia elétrica de um Hotel com 60 quartos, 20 saunas, 15 piscinas e 20 salas para beleza e relaxamento
# * CMS - Consumo de energia elétrica de empresa de equipamentos hospitalares
# * CPT - Consumo de energia elétrica de uma fábrica de comida para animais
# * CSB - Consumo de energia elétrica de uma empresa de logística
# 
# #### Clima
# * Temperature - Temperatura média na Holanda em °C
# * CDD - Cooling Degree-Days a 18°C baseado na temperatura média
# * HDD - Heating Degree-Days a 16°C baseado na temperatura média

# ### Importando Bibliotecas

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np


# ### Leitura inicial dos dados

# In[2]:


# lê o arquivo CSV
df = pd.read_csv('../trabalho final/Energy.csv',sep=';', encoding='latin-1')

df.head()


# In[3]:


df.info()


# ### Limpeza dos dados

# In[4]:


# Copy the data to a new DataFrame
df_new = df.copy()

# split Timestamp column into Date and Hour columns
df_new[['Data', 'Hora']] = df_new['Begin'].str.split('T', expand=True)
df_new['Hora'] = pd.to_datetime(df_new['Hora']).dt.time

# Delete the columns 'Period', 'Begin' and 'End'
df_new = df_new.drop(['ï»¿Period', 'Begin', 'End'], axis=1)

# Converting some columns to crrect type
df_new['Data'] = pd.to_datetime(df_new['Data'])
df_new['Export (EUR/kWh)'] = pd.to_numeric(df_new['Export (EUR/kWh)'], errors='coerce')
df_new['CCF (kWh)'] = pd.to_numeric(df_new['CCF (kWh)'], errors='coerce')
df_new['CHT (kWh)'] = pd.to_numeric(df_new['CHT (kWh)'], errors='coerce')
df_new['CMS (kWh)'] = pd.to_numeric(df_new['CMS (kWh)'], errors='coerce')
df_new['CPT (kWh)'] = pd.to_numeric(df_new['CPT (kWh)'], errors='coerce')
df_new['CSB (kWh)'] = pd.to_numeric(df_new['CSB (kWh)'], errors='coerce')
df_new['Air temperature (Â°C)'] = pd.to_numeric(df_new['Air temperature (Â°C)'], errors='coerce')
df_new['CDD-18 (Â°C)'] = pd.to_numeric(df_new['CDD-18 (Â°C)'], errors='coerce')
df_new['HDD-16 (Â°C)'] = pd.to_numeric(df_new['HDD-16 (Â°C)'], errors='coerce')

# Rename some columns
df_new = df_new.rename(columns={'Air temperature (Â°C)': 'Air temperature (°C)', 'CDD-18 (Â°C)': 'CDD-18 (°C)', 'HDD-16 (Â°C)': 'HDD-16 (°C)'})

# Delete all rows that contain any null (NaN) value
df_new[df_new.isna().any(axis=1)]
df_new = df_new.dropna()


# In[5]:


df_new.info()


# In[6]:


print('Maior data:', df_new['Data'].max())
print('Menor data:', df_new['Data'].min())


# ### Verificando a média de consumo por empresa, a média de preço da energia elétrica (importação e exportação) e a temperatura média

# In[7]:


print('Consumo médio por hora de uma fábrica de chocolate:', df_new['CCF (kWh)'].mean())
print('Consumo médio por hora de um Hotel:', df_new['CHT (kWh)'].mean())
print('Consumo médio por hora de uma empresa de equipamentos hospitalares:', df_new['CMS (kWh)'].mean())
print('Consumo médio por hora de uma fábrica de comida para pet:', df_new['CPT (kWh)'].mean())
print('Consumo médio por hora de uma empresa de logística:', df_new['CSB (kWh)'].mean())


# In[8]:


print('Preço médio de importação de energia elétrica:', df_new['Import (EUR/kWh)'].mean())
print('Preço médio de importação de energia elétrica:', df_new['Export (EUR/kWh)'].mean())


# In[9]:


print('Temperatura média na Holanda:', df_new['Air temperature (°C)'].mean())


# In[10]:


df_new.describe()


# ## Análise de consumo de energia Elétrica

# In[11]:


# Grouping the consumption by day
grouped_data = df_new.groupby(['Data']).agg({'CCF (kWh)': 'mean', 'CHT (kWh)': 'mean', 'CMS (kWh)': 'mean', 'CPT (kWh)': 'mean', 'CSB (kWh)': 'mean'})

plt.style.use('ggplot')
grouped_data.plot(kind='hist', alpha=0.5, bins=20, figsize=(10,6))
plt.title('Distribuição da Média Diária de Consumo por Tipo de Empresa')
plt.xlabel('Consumo (kWh)')
plt.ylabel('Frequência')
plt.legend(loc='upper right')
plt.show()


#  Pode ser observar que em 80% das empresas analisadas o consumo de energia médio diário é de no máximo 150 kWh.

# In[12]:


# Grouping the consumption by hour
grouped_hora = df_new.groupby(['Hora']).agg({'CCF (kWh)': 'mean', 'CHT (kWh)': 'mean', 'CMS (kWh)': 'mean', 'CPT (kWh)': 'mean', 'CSB (kWh)': 'mean'})

plt.style.use('ggplot')
grouped_hora.plot(kind='line', figsize=(10,6))
plt.title('Perfil de Consumo')
plt.xlabel('Hora')
plt.ylabel('Consumo (kWh)')
plt.show()


# Podemos oberservar a diferença entre os perfis de concusmo das empresas. Nota-se que:
# 
# - CCF (Fábrica de Chocolate)  tem um perfil enérgico grande de noite até de manhã e que durante a tarde cai. Isso mostra que a empresa deve possuir Painéis solares que supram partes das suas necessidades energéticas.
# 
# - CSB (Logística) deve possuir equipamento que rodam 24h por dia deixando o seu consumo acima de 50 kWh e que conforme se aproxima do horário comercial, seu consumo aumenta, devido o maior numero de quipamentos ligado por conta dos funcionarios.
# 
# - Demais empresas possuem uma curva de perfil enérgitico tipico, que aumenta conforme o inicio do horário comercial e que diminui até o final do dia, exceto pelo Hotel (CHT) que possui hospedes que utilizando suas dependecias até o perído das 22-23h.

# ## Análise do preço da energia Elétrica

# In[13]:


# Grouping the prices by day
grouped_Pdata = df_new.groupby(['Data']).agg({'Import (EUR/kWh)': 'mean', 'Export (EUR/kWh)': 'mean'})

plt.style.use('ggplot')
grouped_Pdata.plot(kind='box', figsize=(10,6))
plt.title('Variação dos Preços de Importação e Exportação')
plt.ylabel('Preço (EUR/kWh)')
plt.show()


# In[14]:


plt.style.use('ggplot')
grouped_Pdata.plot(kind='hist', alpha=0.5, bins=20, figsize=(10,6))
plt.title('Distribuição de Importação e Exportação de Energia Elétrica')
plt.xlabel('Preço (EUR/kWh)')
plt.ylabel('Frequência')
plt.legend(loc='upper right')
plt.show()


# In[15]:


# Grouping the prices by hour
grouped_Phora = df_new.groupby(['Hora']).agg({'Import (EUR/kWh)': 'mean', 'Export (EUR/kWh)': 'mean'})

plt.style.use('ggplot')
grouped_Phora.plot(kind='line', figsize=(10,6))
plt.title('Importação X Exportação')
plt.xlabel('Hora')
plt.ylabel('Preço (EUR/kWh)')
plt.show()


# ## Análise da Temperatura

# In[16]:


grouped_Temp = df_new.groupby(pd.Grouper(key='Data', freq='M')).agg({'Air temperature (°C)': 'mean'})

plt.style.use('ggplot')
grouped_Temp.plot(kind='line', figsize=(10,6))
plt.title('Variação da Temperatura')
plt.xlabel('Data')
plt.ylabel('Temperatura (C)')
plt.show()


# In[17]:


grouped_CH = df_new.groupby(pd.Grouper(key='Data', freq='M')).agg({'CDD-18 (°C)': 'mean', 'HDD-16 (°C)': 'mean'})

plt.style.use('ggplot')
grouped_CH.plot(kind='line', figsize=(10,6))
plt.title('Heating X Cooling')
plt.xlabel('Data')
plt.ylabel('Temperatura (C)')
plt.show()


# In[18]:


hdd_16 = df_new.groupby('Air temperature (°C)')['HDD-16 (°C)'].mean()


# In[19]:


grouped_ccf = df_new.groupby('Air temperature (°C)')['CCF (kWh)'].mean()

plt.scatter(grouped_ccf.index, grouped_ccf.values, c=hdd_16)
z_ccf = np.polyfit(grouped_ccf.index, grouped_ccf.values, 1)
p_ccf = np.poly1d(z_ccf)
plt.plot(grouped_ccf.index, p_ccf(grouped_ccf.index), "r--")
plt.title('Consumo de CCF em função da temperatura ambiente')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Consumo de energia elétrica (kWh)')
plt.colorbar(label='HDD-16 (°C)')
plt.show()


# In[20]:


grouped_cht = df_new.groupby('Air temperature (°C)')['CHT (kWh)'].mean()

plt.scatter(grouped_cht.index, grouped_cht.values, c=hdd_16)
z_cht = np.polyfit(grouped_cht.index, grouped_cht.values, 1)
p_cht = np.poly1d(z_cht)
plt.plot(grouped_cht.index, p_cht(grouped_cht.index), "r--")
plt.title('Consumo de CHT em função da temperatura ambiente')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Consumo de energia elétrica (kWh)')
plt.colorbar(label='HDD-16 (°C)')
plt.show()


# In[21]:


grouped_cms = df_new.groupby('Air temperature (°C)')['CMS (kWh)'].mean()

plt.scatter(grouped_cms.index, grouped_cms.values, c=hdd_16)
z_cms = np.polyfit(grouped_cms.index, grouped_cms.values, 1)
p_cms = np.poly1d(z_cms)
plt.plot(grouped_cms.index, p_cms(grouped_cms.index), "r--")
plt.title('Consumo de CMS em função da temperatura ambiente')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Consumo de energia elétrica (kWh)')
plt.colorbar(label='HDD-16 (°C)')
plt.show()


# In[22]:


grouped_cpt = df_new.groupby('Air temperature (°C)')['CPT (kWh)'].mean()

plt.scatter(grouped_cpt.index, grouped_cpt.values, c=hdd_16)
z_cpt = np.polyfit(grouped_cpt.index, grouped_cpt.values, 1)
p_cpt = np.poly1d(z_cpt)
plt.plot(grouped_cpt.index, p_cpt(grouped_cpt.index), "r--")
plt.title('Consumo de CPT em função da temperatura ambiente')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Consumo de energia elétrica (kWh)')
plt.colorbar(label='HDD-16 (°C)')
plt.show()


# In[23]:


grouped_csb = df_new.groupby('Air temperature (°C)')['CSB (kWh)'].mean()

plt.scatter(grouped_csb.index, grouped_csb.values, c=hdd_16)
z_csb = np.polyfit(grouped_csb.index, grouped_csb.values, 1)
p_csb = np.poly1d(z_csb)
plt.plot(grouped_csb.index, p_csb(grouped_csb.index), "r--")
plt.title('Consumo de CSB em função da temperatura ambiente')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Consumo de energia elétrica (kWh)')
plt.colorbar(label='HDD-16 (°C)')
plt.show()


# In[25]:


df_numeric = df_new[['Import (EUR/kWh)', 'Export (EUR/kWh)', 'CCF (kWh)', 'CHT (kWh)', 'CMS (kWh)', 'CPT (kWh)', 'CSB (kWh)', 'Air temperature (°C)', 'CDD-18 (°C)', 'HDD-16 (°C)']]
df_corr = df_numeric.corr()
df_corr = df_corr.style.background_gradient(cmap='RdBu')
df_corr


# In[ ]:




