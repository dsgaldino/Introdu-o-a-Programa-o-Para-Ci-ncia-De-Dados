#!/usr/bin/env python
# coding: utf-8

# # Pandas - Manipulação e Agregação de Dados
# 
# Manipulação e agregação de dados são funcionalidades essenciais no Pandas. O Pandas possui diversos métodos para transformação, agrupamento e agregação dos dados. Execute cada célula de código abaixo para ver o resultado.
# 

# In[1]:


#importing libraries
import pandas as pd
import numpy as np


# ## Lendo dados de um arquivo
# 
# O DataFrame carregado contém dados de apartamentos para alugar na cidade de Curitiba.

# In[2]:


# lê o arquivo CSV
df = pd.read_csv('../data/aluguel.csv')

# mostra o conteúdo do DataFrame
df


# Para ordenar um DataFrame de acordo com uma coluna, usa-se o método `sort_values()`. Abaixo ordenamos o DataFrame pela coluna *aluguel* em ordem decrescente:

# In[3]:


df.sort_values("aluguel", ascending=False)


# ## Analisando dados do DataFrame
# 

# ### Agrupamento
# 
# Uma funcionalidade muito útil é o agrupamento de valores. No exemplo abaixo os valores são agrupados de acordo com o número de quartos. A média é calculada para cada valor distinto de número de quartos. Neste caso, apartamentos de 1 quarto têm valor médio de aluguel 701 enquanto os de 2 quartos têm valor médio 1095.

# In[4]:


df_grouped = df.groupby(['quartos']).mean()
df_grouped


# Podemos também agrupar por mais de um valor. Abaixo calculamos a média de valor do aluguel agrupando por número de quartos e também o número de vagas. Neste caso, o valor médio de aluguel para apartamentos de 2 quartos sem vaga é de R$ 1216.

# In[5]:


df_grouped = df.groupby(['quartos', 'vaga']).mean()[['aluguel']]

df_grouped


# No DataFrame anterior, quartos e vagas fazem parte do índice do DataFrame. Podemos usar o método *reset_index()* para tranformá-los em colunas: 

# In[6]:


df_grouped = df.groupby(['quartos', 'vaga']).mean()['aluguel'].reset_index()

df_grouped


# Podemos usar outras funções de agregação, como `max`, `min`, etc. Para contar as ocorrências em cada grupo, usamos a função `size()`. Para dar um novo nome para a nova coluna criada, podemos usar o parâmetro `name` no método `reset_index`, como mostrado abaixo.

# In[7]:


df_grouped_size = df.groupby(['quartos', 'vaga']).size().reset_index(name='count')

df_grouped_size


# ### Pivot
# 
# E podemos usar o método *pivot()* para rearranjar as linhas e colunas. Abaixo fazemos com que o DataFrame seja rearranjado de forma a ter o número de vagas como colunas. Como na visualização anterior, aqui também podemos ver que o valor médio de aluguel para um apartamento com um quarto e sem vaga é de R$ 601.

# In[8]:


df_grouped.pivot(index='quartos', columns='vaga', values='aluguel')


# O método *pivot_table* é parecido com o *pivot()* mas permite também que se especifique uma função para a agregação de valores. Com ele podemos obter os mesmos resultados sem precisar agrupar o DataFrame, como é mostrado abaixo:

# In[9]:


df.pivot_table(index='quartos', columns='vaga', values='aluguel', aggfunc=np.mean)


# ### Crosstab
# 
# O comando *crosstab* relaciona duas colunas para criar um novo DataFrame com valores nas células representando a quantidade de instâncias de cada tipo. Por exemplo, abaixo podemos ver que o DataFrame original tem 6 ofertas de aluguel com 1 quarto e 0 vagas.

# In[10]:


pd.crosstab(df['quartos'], df['vaga'])


# ## Junção de Dados

# Quando temos dois DataFrames e precisamos uni-los, usamos as funcionalidades de junção de dados. Existem vários métodos para fazer junção, dependendo do resultado esperado. Para os exemplos desta seção vamos continuar usando o DataFrame de apartamentos (repetido abaixo) e vamos também definir um novo DataFrame (na célula seguinte) contendo códigos de apartamentos e imobiliárias fictícias respensáveis por eles.

# In[11]:


df


# In[12]:


# Criando um novo DataFrame para ser usado na junção
df_imobiliarias = pd.DataFrame()
df_imobiliarias['codigo'] = [469,74,59375, 2381, 34]
df_imobiliarias['imobiliaria'] = ['Apollo', 'ImobiOne', 'ImobiOne', 'Apollo', 'ImobiTwo']

df_imobiliarias


# O método mais usado para junção de duas colunas é o *merge*. No exemplo abaixo a aplicação do método retorna um novo DataFrame com as colunas dos dois DataFrames originais unidas e com as linhas associadas de acordo com a coluna em comum (código).

# In[13]:


df_joined = pd.merge(df, df_imobiliarias)

df_joined


# Também podemos fazer a união das linhas de dois DataFrames diferentes (de preferência contendo as mesmas colunas). Abaixo definimos um novo DataFrame com duas novas ofertas de aluguel para unirmos ao DataFrame original.

# In[14]:


df_mais_apartamentos = pd.DataFrame([[734, 'Rua Nova', 2, 1, 84, 0, 1250, 490, '02/11/17'],
                                     [4124, 'Rua Nova 2', 1, 1, 60, 0, 850, 310, '30/09/17']],
                                     columns = df.columns)

df_mais_apartamentos


# O método usado para a união das linhas de dois DataFrames é o *concat*:

# In[15]:


pd.concat([df, df_mais_apartamentos])


# ### Referências
# 
# - Documentção do Pandas: [pandas.DataFrame.merge](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html)
# - Documentção do Pandas: [pandas.DataFrame.join](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html)
# - Documentção do Pandas: [pandas.concat](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html)
# 
