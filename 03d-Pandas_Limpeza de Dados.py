#!/usr/bin/env python
# coding: utf-8

# # Limpeza de Dados
# 
# Os processos de limpeza e preparação de dados são muito importantes. Dados limpos, completos e organizados tornam as análises mais fáceis e confiáveis. Abaixo descrevemos alguns dos principais mecanismos para tratar dados que tenham algum problema.
# 
# Execute cada célula de código abaixo para ver o resultado.

# ## Leitura e análise inicial dos dados
# 

# In[1]:


#importação de bibliotecas
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')

# lê o arquivo CSV
df = pd.read_csv('../data/aluguel-com-erros.csv')


# O primeiro passo ao se analisar dados desconhecidos é visualizar algumas linhas de dados:

# In[2]:


df.head(10)


# O método `info` é útil para vermos quais colunas do DataFrame tiveram seus tipos de dados corretamente identificados pelo Pandas. No caso abaixo já é possível identificar alguns problemas. As colunas *quartos, suite, area, aluguel e condomínio* foram interpretadas como objetos genéricos enquanto deveriam ser numéricas. A coluna *data* deveria ser do tipo `datetype`.
# 
# O método `info` também nos informa quantos valores cada coluna tem. Veja abaixo que a coluna *endereço* tem apenas 19 valores.

# In[3]:


df.info()


# ## Localizando e tratando valores inválidos

# Se você quer eliminar as linhas com valores nulos em uma determinada coluna, basta usar o `.isna()` especificando a coluna.

# In[4]:


df_sem_nulos = df[df['endereco'].isna() == False]

df_sem_nulos


# Podemos usar o método `fillna` para substituir os valores em branco por um valor definido, neste caso a *String* "Desconhecido". Após a substituição não há mais linhas com valores em branco.

# In[5]:


df['endereco'] = df['endereco'].fillna("Desconhecido")

df[df.isna().any(axis=1)]


# Podemos também fazer substituições de partes das *strings* no DataFrame. Por exemplo, podemos padronizar ruas e avenidas com as abreviações R. e Av. O código abaixo faz isto:

# In[6]:


df['endereco'] = df['endereco'].str.replace('Rua', 'R.')
df['endereco'] = df['endereco'].str.replace('Avenida', 'Av.')

df.head()


# Ainda não sabemos por que diversas colunas numéricas foram identificadas com o tipo genérico *object*. Uma forma de averiguar é listar todos os valores não repetidos de uma coluna. O método `unique` é útil neste caso. Abaixo podemos ver que a coluna *aluguel* contém uma ou mais interrogações (?) entre os valores.

# In[7]:


df['aluguel'].unique()


# Vamos então exibir todas as linhas com interrogações em alguma coluna. O comando abaixo identificou que a linha de índice 19 contém vários valores representados com uma interrogação.

# In[8]:


df[df['aluguel'] == '?']


# Como a linha identificada acima tem muitos valores inválidos, podemos decidir retirá-la do DataFrame. Para isso, usamos o método `drop`. Perceba que a linha não aparece mais no DataFrame.

# In[9]:


df = df.drop(19)

df


# ## Conversão de tipos

# Como pode ser visto pela execução do método `info` abaixo, as colunas ainda possuem tipos incorretos. Precisamos então fazer a conversão manual dos tipos.

# In[10]:


df.info()


# Para converter as colunas para os tipos adequados, usamos o método `astype`. Podemos tanto aplicar a uma coluna por vez ou em várias colunas representadas por um dicionário. O código abaixo exemplifica as duas abordagens:

# In[11]:


df['suite'] = df['suite'].astype(int)

df = df.astype({'area': int, 'aluguel': float, 'condominio': float})


# Para uma coluna com datas, precisamos usar um comando diferente, o `to_datetime`. Ao executar o comando abaixo obtemos um erro informando que há um valor de data contendo 'janeiro 17', que não pode ser interpretado pelo método.

# In[12]:


df['data'] = pd.to_datetime(df['data'])


# Abaixo substituimos o valor com problema e com isso conseguimos converter corretamente a coluna.

# In[13]:


df['data'] = df['data'].str.replace('janeiro 17', '01/01/17')

df['data'] = pd.to_datetime(df['data'], format='%d/%m/%y')


# Agora podemos conferir os tipos e verificar que estão todos corretos:

# In[14]:


df.info()


# Com todos os tipos convertidos corretamente, podemos aplicar funções estatísticas e exibir corretamente os valores em gráficos como mostrado abaixo:

# In[15]:


print('Média do aluguel: ', df['aluguel'].mean())

df.set_index('data')['aluguel'].plot()


# ## Identificando outliers

# Outliers são valores fora da faixa esperada para uma observação. Um forma conveniente de identificar outliers é usando BoxPlots. Abaixo podemos perceber que existem dois valores de condomínio fora do que seria esperado (mostrados como círculos abaixo e acima da caixa).

# In[16]:


df[['aluguel', 'condominio']].plot.box()


# Outra forma de identificar outliers é calcular os *z-scores* para uma variável. O z-score fornece informação sobre o quão inesperado um valor é considerando os demais valores presentes. Abaixo calculamos os z-scores para a variável condomínio. Veja que um valor 'inesperado' é o 120 com z-score -1.3, indicando que é um valor mais baixo que o esperado. O outro outlier é o de condomínio 1100 com z-score 3.7 indicando que está muito acima do esperado. Em geral valores de z-score abaixo de -3 e acima de +3 são fortes candidados a serem outliers.

# In[17]:


df['condominio_zscore'] = (df['condominio'] - df['condominio'].mean())/df['condominio'].std()

df.sort_values('condominio_zscore')


# Uma possibilidade para eliminar o valor que está muito acima seria excluir a linha que o contém. O problema disso é que perderíamos todos os dados da linha, que inclui dados aparentemente corretos. Uma forma de manter os dados corretos e ao mesmo tempo minimizar a influência do valor incorreto é substituir o valor incorreto pela média dos demais valores para a variável, como fazemos abaixo. Veja que agora o valor de condomínio para a linha problemática é 379.84.

# In[18]:


df.loc[2, 'condominio'] = df['condominio'].mean()

df


# ## Escrevendo os dados limpos no disco
# 
# Para salvar os dados limpos em um arquivo, usamos o método `to_csv`, como no exemplo abaixo:

# In[19]:


df.to_csv('../data/aluguel-limpo.csv', index=False)

