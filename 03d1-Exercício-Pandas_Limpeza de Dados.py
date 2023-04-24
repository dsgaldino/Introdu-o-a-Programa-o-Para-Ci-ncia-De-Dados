#!/usr/bin/env python
# coding: utf-8

# # Limpeza de Dados - Exercícios
# 
# Resolva os exercícios propostos abaixo. Os exercícios usam um dataset de reclamações registradas por cidadãos. O detaset foi derivado de dados do [Portal de Dados Abertos da Prefeitura de Curitiba](https://www.curitiba.pr.gov.br/DADOSABERTOS/).

# ## Leitura e análise inicial dos dados
# 
# Inicie um DataFrame a partir do arquivo `2017-02-01_156_-_Base_de_Dados_sample.csv`. Exiba algumas linhas e informações sobre os tipos identificados automaticamente pelo Pandas.
# 
# **Dica:** Caso o arquivo não seja separado por vírgulas, o Pandas não conseguirá reconhecer os campos adequadamente. Você precisará fornecer o parâmetro `sep=';'` para indicar o separador correto (neste caso, o `;`).
# 
# **Dica:** Aplicativos modernos tendem a armazenar arquivos no formato UTF-8, mas é comum encontrar arquivos codificados em outros formatos. Caso você tenha problemas para ler o arquivo, utilize o parâmetro `encoding='latin-1'` para selecionar o encoding correto (*latin-1* neste exemplo).

# In[1]:


# Resposta:
import pandas as pd

# lê o arquivo CSV
df = pd.read_csv('../data/2017-02-01_156_-_Base_de_Dados_sample.csv', sep=';', encoding='latin-1')


# Visualize algumas linhas de dados:

# In[2]:


# Resposta:
df.head()


# Use o método `info` para exibir as colunas e os tipos identificados.

# In[3]:


# Resposta:
df.info()


# Estamos interessados apenas nos seguintes campos: 'DATA', 'HORARIO', 'ASSUNTO', 'BAIRRO_ASS', 'SEXO', 'DATA_NASC', 'RESPOSTA_FINAL'
# 
# Crie (ou substitua) um DataFrame contendo apenas os campos acima.

# In[4]:


# Resposta:

df_new = df[['DATA', 'HORARIO', 'ASSUNTO', 'BAIRRO_ASS', 'SEXO', 'DATA_NASC', 'RESPOSTA_FINAL']]
df_new


# ## Localizando e tratando valores inválidos

# Exiba todas as linhas com valores em branco (*NaN*).

# In[5]:


# Resposta:
df_new[df_new.isna().any(axis=1)]


# Exclua todas as linhas que contenham algum valor nulo (*NaN*). Verifique se todas as linhas com valores em branco foram excluídas corretamente.

# In[6]:


# Resposta:
df_new = df_new.dropna()
print(df_new.isnull().sum())


# Faça com que todos os nomes de bairros fiquem em letras minúsculas.

# In[7]:


# Resposta:
df_new['BAIRRO_ASS'] = df_new['BAIRRO_ASS'].str.lower()
df_new


# ## Conversão de tipos, criação de coluna e escrita em CSV

# Exiba os tipos das colunas do DataFrame.

# In[8]:


# Resposta:
df_new.dtypes


# - Converta os campos de data para o formato DateTime. 
# - Crie uma nova coluna chamada HORA, contendo apenas o componete hora do horário da reclamação (dica: use os comandos str.split e str.get)
# - Converta a coluna HORA para Inteiro

# In[9]:


# Resposta:

# converter colunas de data para DateTime
df_new['DATA'] = pd.to_datetime(df_new['DATA'], format='%d/%m/%Y')
df_new['DATA_NASC'] = pd.to_datetime(df_new['DATA_NASC'], format='%d/%m/%Y')

# criar coluna HORA
df_new['HORA'] = df_new['HORARIO'].str.split().str.get(0)

# converter coluna HORA para inteiro
df_new['HORA'] = df_new['HORA'].str.split(':').str[0].astype(int)

df_new


# Crie uma coluna chamada `IDADE` contendo a diferença entre o ano da reclamação e o ano de nascimento da pessoa.
# 
# **Dica:** Para extrair o ano de uma coluna do tipo data, use a propriedade `dt.year`. Por exemplo: `df['DATA'].dt.year`.

# In[10]:


# Resposta:

df_new['IDADE'] = (df_new['DATA'].dt.year) - (df_new['DATA_NASC'].dt.year)


# Verifique se as colunas foram corretamente convertidas para os tipos corretos.

# In[11]:


# Resposta:
df_new.info()


# Identifique outliers na coluna `IDADE`. Remova do DataFrame todas as reclamações de pessoas com idades muito baixas.

# In[12]:


# Resposta:
df_new['IDADE'].hist(bins=20)

df_new = df_new[df_new['IDADE'] >= 18]


# In[13]:


df_new['IDADE'].hist(bins=20)


# Salve o DataFrame em um arquivo CSV chamado `../data/2017-02-01_156_-_Base_de_Dados_sample-limpo.csv`. Use o parâmetro `index=False` para não incluir o índice no aquivo gerado.

# In[14]:


# Resposta:
df_new.to_csv('../data/2017-02-01_156_-_Base_de_Dados_sample-limpo2.csv', index=False)
