#!/usr/bin/env python
# coding: utf-8

# # Análise Exploratória - Dados de Reclamações
# 
# Resolva os exercícios propostos abaixo.

# ## Leitura e análise inicial dos dados
# 
# Inicialize um DataFrame a partir do arquivo `../data/2017-02-01_156_-_Base_de_Dados_sample-limpo.csv` disponibilizado pelo professor.
# 
# Responda: Qual a média das idades das pessoas que reclamaram? Qual a idade máxima? Quantos valores únicos possuímos para a coluna `BAIRRO_ASS`?
# 
# **Dica:** A função len() pode ser usada para se obter o tamanho de listas, séries ou dataframes. Por exemplo, `len([1,3,9])` retorna 3.

# In[1]:


# Resposta:
# Importação de Bibliotecas
import pandas as pd
import matplotlib.pyplot as plt


# lê o arquivo CSV
df = pd.read_csv('../data/2017-02-01_156_-_Base_de_Dados_sample-limpo3.csv')

df.tail()


# In[2]:


idade_media =df["IDADE"].mean()
print("Média das idades das pessoas que reclamaram:", int(idade_media))

idade_maxima = df["IDADE"].max()
print("Idade máxima:", idade_maxima)

valores_unicos = df["BAIRRO_ASS"].nunique()
print("Quantidade de valores únicos na coluna BAIRRO_ASS:", valores_unicos)


# O primeiro passo ao se analisar dados desconhecidos é visualizar algumas linhas de dados:

# In[3]:


# Resposta:
df.describe()


# ## Visualização da distribuição das variáveis

# Exiba histogramas para visualizar a distribuição de idades para homens e mulheres.
# 
# Responda: Existe alguma diferença na distribuição das idades entre homens e mulheres?

# In[4]:


# Resposta:
df_sexo = df.groupby("SEXO")
df_homens = df_sexo.get_group("M")
df_mulheres = df_sexo.get_group("F")


df.groupby('SEXO')['IDADE'].describe()


# In[5]:


# Resposta:

plt.hist(df_homens["IDADE"], alpha=0.5, label="Homens")
plt.hist(df_mulheres["IDADE"], alpha=0.5, label="Mulheres")
plt.legend(loc="upper right")
plt.show()


# In[6]:


# É possível verificar que as mulheres realizaram mais reclamações que os homens, a difrença média nas idades é de 1 ano,
# tendo a média de mulheres 48,77 anos e homens 47,65.

# Analisando a distribuição por meio do histograma é possível verificar que entre os 25 e 65 anos de idade a média de 
# reclamações feitas por mulheres é acima de 500, enquanto que para homens essa média se mantem entre 35 e 60. 
# Tendo um pico entre os 40 e 50 e para as muloheres esse pico ocorre entre 45 e 55 anos.

# o Histograma masculino segue um padrão normal, enquanto o das mulheres não.


# Exiba um BoxPlot das idades de acordo com o sexo do reclamante para ver se as diferenças ficam mais óbvias. 
# 
# **Dica:** Para exibir boxplots agrupados por categoria, use o método `boxplot` como no exemplo: `df.boxplot(column='IDADE', by = 'SEXO')`.

# In[7]:


# Resposta:
df.boxplot(column='IDADE', by='SEXO', figsize=(8,6))
plt.title('Idades por sexo')
plt.ylabel('Idade')
plt.show()


# ## Seleção dos dados
# 
# Nesta etapa vamos filtrar apenas linhas com os tipos de relamação (assuntos) mais comuns.
# 
# - Faça uma contagem dos assuntos mais comuns (usando `groupby`). Revise o procedimento no tutorial de Manipulação e Agregação de Dados, se necessário.
# - Crie uma lista contendo os assuntos com mais de 60 reclamações. Armazene a lista em uma variável para uso posterior.
# 
# **Dica:** Para criar uma lista a partir de uma coluna de valores, use o comando `list()` como no exemplo: `list(df_grouped_top['ASSUNTO'])`

# In[8]:


# Resposta:
# Contagem dos assuntos mais comuns
df_count_reclamacoes = df.groupby('ASSUNTO')['ASSUNTO'].count()

# Filtrando apenas assuntos com mais de 60 reclamações
df_assuntos_mais_comuns = list(df_count_reclamacoes[df_count_reclamacoes > 60].index)


# In[9]:


df_assuntos_mais_comuns


# Crie um novo DataFrame contendo apenas reclamações contidas na lista das reclamações mais comuns.
# 
# **Dica:** Para filtrar linhas que contêm valores de uma lista, use o método `isin()`. Por exemplo, `df['ASSUNTO'].isin(lista_top)` retorna uma lista de valores True/False que pode ser usada para selecionar as linhas de interesse.

# In[10]:


# Resposta:

# criação do novo DataFrame
df_top_reclamacoes = df[df['ASSUNTO'].isin(df_assuntos_mais_comuns)]

df_top_reclamacoes


# ## Análise de similaridades entre reclamações de bairros
# 
# Queremos agora identificar bairros com problemas similares. Use o método `crosstab()` para gerar um novo DataFrame com os bairros nas colunas e os assuntos (os mais comuns, filtrados acima) nas linhas. 

# In[11]:


# Resposta:
df_crossed = pd.crosstab(df_top_reclamacoes['ASSUNTO'], df['BAIRRO_ASS'])
df_crossed


# Usando o DataFrame obtido anteriormente, gere a matriz de correlações entre bairros (método `corr()`).

# In[12]:


# Resposta:
df_crossed.corr()


# Use um Heatmap para exibir as correlações com cores.

# In[13]:


# Resposta:

df_corr = df_crossed.corr()
df_corr = df_corr.style.background_gradient(cmap='RdBu')
df_corr


# É possível perceber algum padrão entre os bairros baseando-se nas correlações obtidas?

# In[14]:


# Não foi identificado um padrão, porém existem alguns bairros com forte correlação como: Abranches, Alto Boqueirão, Cachoeira, 
# Cajuru, Capão da Imbuia, Cidade induatrialPilarzinho, Santa Candida,Sitio Cercado, Uberaba e Xaxim.


# ## Análise de bairros mais problemáticos
# 
# Agora nosso interesse é determinar os bairros com mais reclamações.
# 
# - Crie um DataFrame com a contagem de reclamações por bairro (usando a coluna BAIRRO_ASS).
# - Exiba os dados usando um gráfico de barras para visualizarmos os bairros com mais reclamações

# In[15]:


# Resposta:
contagem = df.groupby('BAIRRO_ASS')['BAIRRO_ASS'].count().rename('Reclamacoes')


# In[16]:


# Resposta:

contagem.sort_values().plot.barh(figsize=(5, 15))
plt.title('Rreclamações por bairro')
plt.xlabel('Contagem')
plt.ylabel('Bairro')
plt.show()


# O problema de considerar apenas o total de reclamações é que não estamos considerando a população dos bairros. Então o ideal é calcular a *taxa* de reclamações, ou seja, o número de reclamações por habitante do bairro.
# 
# - Crie um novo DataFrame a partir dos dados do arquivo `../data/dados_bairros.csv`.
# - Converta os nomes dos bairros deste DataFrame para caixa-baixo (minúsculo).
# - Faça uma junção do DataFrame de totais por bairro com o novo DataFrame.
# 
# **Dica:** Para especificar as colunas contendo os valores base para a junção, especifique os parâmetros `left_on` e `right_on` no método `merge`.

# In[17]:


# Resposta:

# Lendo o arquivo com os dados dos bairros
df_bairros = pd.read_csv('../data/dados_bairros.csv')

df_bairros.head()


# In[18]:


# Convertendo os nomes dos bairros para caixa-baixo
df_bairros['Bairro'] = df_bairros['Bairro'].str.lower()

# Fazendo a junção dos DataFrames
df_final = pd.merge(df_bairros[['Bairro', 'Total']], contagem, left_on='Bairro', right_index=True)

df_final.head()


# Crie uma nova coluna chamada *taxa* contendo o resultado da divisão da coluna de contagem de reclamações pela coluna de total de habitantes.

# In[19]:


# Resposta:

# Calculando a taxa de reclamações por habitante
df_final['taxa_reclamacoes'] = df_final['Reclamacoes'] / df_final['Total']

df_final.head()


# Exiba um gráfico de barras mostrando os bairros de acordo com a taxa de reclamações.

# In[20]:


# Resposta:

df_final.set_index("Bairro", inplace=True)
df_final[["taxa_reclamacoes"]].sort_values(by="taxa_reclamacoes").plot.barh(figsize=(7, 20))
plt.title('Taxa de Reclamações')
plt.xlabel('Taxa')
plt.ylabel('Bairro')
plt.show()


# ## Analisando tendências temporais
# 
# Vamos agora identificar os meses com mais reclamações. 
# 
# - Usando o DataFrame completo (lido a partir do CSV), converta a coluna *DATA* para o tipo `datetime`. Revise o tutorial de Limpeza de Dados se necessário.
# - Agrupe as linhas contando as reclamações por mês. Revise o tutorial de Análise Exploratória se necessário.
# - Exiba um gráfico de linha com a evolução da contagem.
# 

# In[21]:


# Resposta:

# Convertendo a coluna DATA para o tipo datetime
df['DATA'] = pd.to_datetime(df['DATA'])

# Agrupando as linhas contando as reclamações por mês
df_mes = df.groupby(pd.Grouper(key='DATA', freq='M'))['DATA'].count().rename("Reclamacoes")


# In[22]:


# Resposta:
df_mes.plot.line()

