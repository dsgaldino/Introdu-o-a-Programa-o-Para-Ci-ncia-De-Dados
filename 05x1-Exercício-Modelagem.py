#!/usr/bin/env python
# coding: utf-8

# # Exercícios de Modelagem - Dados de Reclamações
# 
# Resolva os exercícios propostos abaixo.

# ## Leitura e análise inicial dos dados
# 
# Abra o arquivo `../data/2017-02-01_156_-_Base_de_Dados_sample-limpo.csv` disponibilizado pelo professor e faça as exibições iniciais do conteúdo.

# In[1]:


# Resposta:

# Import libraries 
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import nltk
from nltk.tokenize import word_tokenize
import unicodedata
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('../data/2017-02-01_156_-_Base_de_Dados_sample-limpo.csv')

df.head()


# ## Análise Estatística
# 
# Analise a diferença entre idades de homens e mulheres no dataset. A diferença é estatisticamente significativa?

# In[2]:


# Resposta:

df_masculino = df[df['SEXO'] == 'M']['IDADE']
df_feminino = df[df['SEXO'] == 'F']['IDADE']

media_masculino = df_masculino.mean()
media_feminino = df_feminino.mean()

print(f"Média de idade dos homens: {media_masculino:.2f}")
print(f"Média de idade das mulheres: {media_feminino:.2f}")

t_stat, p_value = stats.ttest_ind(df_masculino, df_feminino, equal_var=False)
alpha = 0.05


# In[3]:


# Resposta:

if p_value < alpha:
    print(f"A diferença entre as médias de idade é estatisticamente significativa (p-value = {p_value:.4f})")
else:
    print(f"A diferença entre as médias de idade não é estatisticamente significativa (p-value = {p_value:.4f})")


# ## Clusterização
# 
# Nosso objetivo é agrupar bairros pela similaridade dos tipos de reclamação. Use o método crosstab() para gerar um novo DataFrame com os bairros nas linhas e os assuntos nas colunas.

# In[4]:


# Resposta:

df_crossed = pd.crosstab(df['BAIRRO_ASS'], df['ASSUNTO'])
df_crossed


# Normalize o DataFrame criado acima.

# In[5]:


# Resposta:

df_normalized = pd.DataFrame(
                  MinMaxScaler().fit_transform(df_crossed),
                  index = df_crossed.index,
                  columns=df_crossed.columns)

df_normalized


# Aplique o algoritmo KMeans sobre os dados normalizados para separar os bairros em 6 classes. 

# In[6]:


# Resposta:

kmeans = KMeans(n_clusters=6, random_state=42)
labels = kmeans.fit_predict(df_normalized)


# A partir do resultado da clusterização, crie um DataFrame chamado `df_agrupamentos` contendo os bairros como índice e uma coluna chamada `Agrupamento` contendo a classe encontrada pelo K-Means.

# In[7]:


# Resposta:

df_agrupamentos = pd.DataFrame(df_crossed.index).set_index('BAIRRO_ASS')
df_agrupamentos['Agrupamento'] = labels

df_agrupamentos


# ## Análise de texto

# Vamos agora analisar os textos da coluna `RESPOSTA_FINAL` para cada grupo encontrado pelo K-means. Primeiramente, crie uma nova coluna com os textos normalizados (use a função `normaliza_texto()` para remover acentos e stopwords).

# In[8]:


# Resposta:
nltk.download('stopwords')
nltk.download('punkt')

stopwords = nltk.corpus.stopwords.words('portuguese')
print(stopwords)

def remove_acentos(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

stopwords = [remove_acentos(palavra) for palavra in stopwords]

def normaliza_texto(txt):
    return ' '.join([word for word in word_tokenize(str.lower(remove_acentos(txt))) if word not in stopwords])

#criando nova coluna
                 
df['RESPOSTA_NORMALIZADA'] = df.apply(lambda linha: normaliza_texto(str(linha['RESPOSTA_FINAL'])), axis = 1)

df.head()


# Crie um novo DataFrame chamado `df_texto` contendo duas colunas: o bairro da reclamação (`BAIRRO_ASS`) e o texto normalizado.

# In[9]:


# Resposta:

df_texto = df[['BAIRRO_ASS', 'RESPOSTA_NORMALIZADA']]
df_texto


# Crie um novo DataFrame, chamado `df_merge` contendo a junção das informações dos DataFrames `df_texto` e `df_agrupamentos`. Após a junção este DataFrame deve ter, para cada recalamação, o bairro, resposta final (normalizada) e a classe do bairro identificada pelo k-means.

# In[10]:


# Resposta:

df_merge = pd.merge(df_texto, df_agrupamentos, left_on='BAIRRO_ASS', right_index=True)
df_merge.head()


# Agrupe as reclamações das mesmas classes (coluna `Agrupamento` determinada pelo k-means) concatenando todo os textos individuais. No fim você deve ter um DataFrame (ou Series) contendo os 6 agrupamentos como índice e para cada agrupamento uma grande string com todos os textos registrados para o agrupamento.

# In[11]:


# Resposta:

df_grouped = df_merge.groupby('Agrupamento')['RESPOSTA_NORMALIZADA'].apply(lambda x: ' '.join(x))
df_grouped


# Gere gráficos de distribuição de frequência de palavras e wordclouds para cada agrupamento. Tente identificar padrões para os agrupamentos, por exemplo, que tipo de problema cada um costuma ter.
# 
# Para instalar o pacote de criação de wordclous, é necessário executar o seguinte comando no terminal:
# 
# `conda install -c conda-forge wordcloud`

# In[12]:


# Resposta:

for agrupamento, texto in df_grouped.items():
    print("############## {} ##############".format(agrupamento))
    freqDist = FreqDist(texto.split(" "))
    freqDist.plot(10)


# In[13]:


# Resposta:

for agrupamento, texto in df_grouped.items():
    print("############## {} ##############".format(agrupamento))
    # Cria a imagem da nuvem de palavras:
    wordcloud = WordCloud().generate(texto)

    # Exibe a imagem gerada
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# Existem seis grupos distintos, cada um com suas próprias áreas de atuação. O grupo 0 concentra-se em fornecer atendimento e
# serviços, enquanto o grupo 1 lida com a remoção de entulhos e resíduos por meio da coleta e queima a céu aberto de materiais
# em terrenos baldios. O grupo 2 se dedica ao transporte e coleta de materiais, com semelhanças ao grupo 1. O grupo 3 
# concentra-se principalmente na coleta de detritos, entulhos e resíduos vegetais. O grupo 4 é especializado em receber 
# solicitações, contatos e abordagens. Por fim, o grupo 5 é semelhante ao grupo 3 em termos de foco, concentrando-se em coletar
# detritos, entulhos e resíduos vegetais.
