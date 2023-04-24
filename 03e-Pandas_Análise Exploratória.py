#!/usr/bin/env python
# coding: utf-8

# # Análise Exploratória
# 
# A Análise Exploratória é uma fase importante de uma tarefa de Ciência de Dados. É nesta fase que buscamos entender os dados com os seguintes objetivos:
# 
# - Identificar padrões iniciais
# - Formular perguntas de pesquisa e hipóteses
# - Identificar dados incompletos ou não confiáveis
# 
# Para atingir os objetivos, em geral usa-se uma combinação de análises estatísticas com uma grande ênfase em geração e interpretação de gráficos.

# ## Leitura e análise inicial dos dados
# 

# In[1]:


# Importação de Bibliotecas
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')

# lê o arquivo CSV
df = pd.read_csv('../data/aluguel.csv')


# O primeiro passo ao se analisar dados desconhecidos é visualizar algumas linhas de dados:

# In[2]:


df.head(10)


# O método `describe` é útil para se ter uma idéia de estatísticas básicas para as variáveis numéricas. Por exemplo, abaixo podemos ver que a média dos valores de aluguel é 898 enquanto a mediana (50 percentil) é 900.

# In[3]:


df.describe()


# ## Visualização da distribuição de variáveis

# Visualizar as distribuições das variaveis nos ajuda a identificar os primeiros padrões. Abaixo exibimos os histogramas para `aluguel` e `condomínio`. É possivel ver que a maior concentração de apartamentos é de aluguéis entre 600 e 900. Há também uma concentração menor em aluguéis em torno de 1200. Já a distribuição dos condomínios é mais homogênea, com a maior parte dos valores por volta de 370.
# 
# Faz sentido este comportamento? Aparentemente o condomínio não varia na mesma proporção do valor do aluguel. Ou seja, se um apartamento de 600 paga 300 de condomínio, não se espera que um apartamento de 1200 pague 600 de condomínio. Esta pode ser uma questão a se explorar em passos futuros das análises.

# In[4]:


df['aluguel'].hist(bins=7)


# In[5]:


df['condominio'].hist(bins=7)


# Podemos também exibir as distribuições usando KDEs:

# In[6]:


df['aluguel'].plot.kde()


# In[7]:


df['condominio'].plot.kde()


# Outra forma de visualizar a distribuição de variáveis é através de Box Plots. Abaixo exibimos uma gráfico para aluguéis e condomínios. Novamente, podemos perceber que a variação nos aluguéis é maior que nos condomínios. Nos condomínios podemos ver tambem um outlier (círculo abaixo da barra). Verifique os dados e identifique qual apartamento tem este valor de condomínio tão diferente.

# In[8]:


df[['aluguel', 'condominio']].plot.box()


# ## Análise da correlação entre as variáveis

# Para identificar associações entre as variáveis podemos utilizar diversas ferramentas estatísticas e visuais. Para calcular a correlação (Pearson) entre todos os pares de variáves, podemos usar o método `corr`. Abaixo podemos ver que a maior correlação está entre a área do apartamento e o aluguel. Isto significa que, aparentemente, o tamanho do apartamento é o que mais influencia no valor total.

# In[9]:


df.corr()


# Uma forma interessante de visualizar a matrix de correlações é usar um Heatmap. No caso abaixo usamos cores azuis para identificar as correlações maiores e cores vermelhas para as menores.

# In[10]:


df_corr = df.corr()
df_corr = df_corr.style.background_gradient(cmap='RdBu')
df_corr


# A correlação é uma boa medida de associação entre variáveis, mas ela não oferece detalhes sobre a distribuição ou sobre a presença de outliers. Para se ter uma ideia melhor das associações, é interessante visualizar os dados no plano cartesiano. Para isto podemos construir uma matriz com as visualizações dos pontos para todas as combinações de variáveis. Abaixo fazemos isto para área, aluguel e condomínio. Veja que entre aluguel e área há realmente uma tendência de associação (maior concentração de pontos próximos à diagonal).

# In[11]:


from pandas.plotting import scatter_matrix

scatter_matrix(df[['area','aluguel','condominio']], figsize=(10, 10), diagonal='kde')


# Podemos também construir um gráfico isolando apenas duas variáveis para explorar com mais detalhes:

# In[12]:


df.plot.scatter(x='area', y='aluguel')


# Uma visualização útil para comparar mais de duas variáveis é o Parallel Coordinates. Abaixo plotamos linhas em azul representando apartamentos com 2 quartos e linhas verdes para os de 1 quarto. É possivel observar que apartamentos de dois quartos tendem a ter área e valor de aluguel mais altos. Já o valor do condomínio não demonstra uma superioridade tão marcante para os apartamentos de 2 quartos.

# In[13]:


from pandas.plotting import parallel_coordinates

parallel_coordinates(df[['area','aluguel','condominio', 'quartos']], 'quartos', colormap='winter')


# ## Comparando proporções

# Podemos usar gráficos de pizza para comparar proporções de partes. Abaixo calculamos o total de ofertas de apartamentos por número de vagas e exibimos o resultado em um gráfico de pizza.

# In[14]:


df_vagas = df.groupby('vaga').size().rename('Total vagas')
df_vagas


# In[15]:


df_vagas.plot.pie()


# Poderíamos também ter usado um gráfico de barras:

# In[16]:


df_vagas.plot.bar()


# Gráficos de barras também são úteis para comparar valores individuais, como abaixo. É fácil identificar quais são os apartamentos com valores maiores e menores.

# In[17]:


df.plot.barh(x='codigo', y=['aluguel', 'condominio'])


# ## Analisando tendências de crescimento
# 
# 

# Quando analisamos dados sequenciais (por exemplo dados temporais), é interessante plotar linhas que demonstrem a tendência de crescimento ao longo do tempo. Abaixo exibimos os valores de apartamentos de acordo com a data de registro da oferta. Esta não é uma boa visualização porque ela não deixa claro se a variação é referente ao período ou a fatores específicos do apartamento (como área ou número de quartos).

# In[18]:


# converte coluna data para o tipo datetime
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%y')

df.set_index('data').sort_index()[['aluguel', 'condominio']].plot()


# Uma visualização temporal mais interessante pode ser obtida se calcularmos a média dos valores de aluguel para cada mês. Abaixo calculamos e exibimos os valores médios de aluguel e condomínio por mês. Agora sim podemos identificar que aparentemente há um aumento nos valores no mês de agosto.

# In[19]:


periodo = df.data.dt.to_period("M")  # transforma datas em mês/ano

df.groupby(periodo)[['aluguel', 'condominio']].mean().plot()


# ### Referências
# 
# - Documentação do Pandas: [Visualization](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html)
# 
