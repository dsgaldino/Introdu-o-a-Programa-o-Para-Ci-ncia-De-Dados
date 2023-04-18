#!/usr/bin/env python
# coding: utf-8

# # Manipulação e Agregação de Dados - Exercícios
# 
# Resolva os exercícios propostos abaixo. Os exercícios usam um dataset de reclamações registradas por cidadãos. O detaset foi derivado de dados do [Portal de Dados Abertos da Prefeitura de Curitiba](https://www.curitiba.pr.gov.br/DADOSABERTOS/).

# ## Leitura e análise inicial dos dados
# 
# Inicie um DataFrame a partir do arquivo `2017-02-01_156_-_Base_de_Dados_sample.csv`. 
# 
# **Dica:** Caso o arquivo não seja separado por vírgulas, o Pandas não conseguirá reconhecer os campos adequadamente. Você precisará fornecer o parâmetro `sep=';'` para indicar o separador correto (neste caso, o `;`).
# 
# **Dica:** Aplicativos modernos tendem a armazenar arquivos no formato UTF-8, mas é comum encontrar arquivos codificados em outros formatos. Caso você tenha problemas para ler o arquivo, utilize o parâmetro `encoding='latin-1'` para selecionar o encoding correto (*latin-1* neste exemplo).

# In[1]:


# Resposta:
#importing libraries
import pandas as pd

df = pd.read_csv('../data/2017-02-01_156_-_Base_de_Dados_sample.csv', sep=';', encoding='latin-1')


# Visualize algumas linhas de dados:

# In[2]:


# Resposta:
df.head()


# Use o método `df.describe(include="all")` para exibir informações sobre as colunas.

# In[3]:


# Resposta:
df.describe(include="all")


# Crie um novo DataFrame chamado `df_elogios` contendo apenas as linhas cujos valores na coluna `TIPO` são iguais a 'ELOGIO'. Este DataFrame deve ter as colunas TIPO, ASSUNTO, e BAIRRO_CIDADAO.

# In[6]:


# Resposta:
df_elogios = df.groupby('TIPO').get_group('ELOGIO')[['TIPO', 'ASSUNTO', 'BAIRRO_CIDADAO']]
df_elogios


# Quais são os 5 bairros com mais elogios? Agrupe pelo `BAIRRO_CIDADAO` e ordene o resultado para responder.

# In[9]:


# Resposta:
df_elogios.groupby("BAIRRO_CIDADAO").size().sort_values(ascending=False).head(5)


# Crie dois novos DataFrames, um contendo as linhas de reclamações de pessoas do sexo masculino e outra do sexo feminino. Use estes DataFrames para responder:
# 
# Qual é a proporção de reclamações entre homens e mulheres? (total de reclamações de homens dividido pelo total de reclamações de mulheres)

# In[32]:


# Resposta:
df_Masculino = df[df['SEXO'] == 'M']
df_Feminino = df[df['SEXO'] == 'F']

proporcao = len(df_Masculino)/ len(df_Feminino['SEXO'])
proporcao = proporcao *100
print("Proporção de reclamações entre homens e mulheres: {:.0f}%".format(proporcao))


# Concatene os dois DataFrames criados acima para criar um DataFrame chamado `df_todos`. Verifique se este DataFrame tem o mesmo número de linhas do DataFrame lido do CSV.

# In[37]:


# Resposta:
# Concatenando os DataFrames
df_todos = pd.concat([df_Masculino, df_Feminino])

print("Linhas em df:", len(df))
print("Linhas em df_todos:", len(df_todos))

# Verificando o número de linhas
if len(df_todos) == len(df):
    print("\nOs DataFrames possuem o mesmo número de linhas.")
else:
    print("\nOs DataFrama não possuem o mesmo número de linhas.")


# Crie um novo DataFrame chamado `df_sexo` contendo a contagem de reclamações para cada sexo. A coluna com a contagem deve se chamar `contagem`.

# In[62]:


# Resposta:
df_sexo = df.groupby(['SEXO']).count()[['TIPO']]
df_sexo.columns = ['contagem']
df_sexo


# Crie um novo DataFrame chamado `df_sexo_tipo` contendo a contagem de reclamações para cada sexo e tipo. A coluna com a contagem deve se chamar `total`.

# In[63]:


# Resposta:
df_sexo_tipo = df.groupby(['SEXO', 'TIPO'])['TIPO'].count().reset_index(name='total')
df_sexo_tipo


# Faça uma junção dos DataFrames `df_sexo, df_sexo_tipo` para criar um novo DataFrame chamado `df_juncao` contendo as contagens por sexo e também por sexo/tipo.

# In[64]:


# Resposta:
df_juncao = pd.merge(df_sexo, df_sexo_tipo, on = "SEXO")
df_juncao


# Crie uma nova coluna no DataFrame `df_juncao` chamada `proporcao` contendo a porcentagem de homens e mulheres que fizeram cada tipo de reclamação. Responda: qual sexo faz mais elogios? Qual faz mais solicitações? Qual faz mais reclamações?

# In[84]:


# Resposta:
df_juncao['proporcao'] = (df_juncao['total'] / df_juncao['contagem']) * 100
df_juncao


# In[96]:


# Sexo que faz mais elogios
elogios = df_juncao[df_juncao['TIPO'] == 'ELOGIO'].groupby('SEXO')['proporcao'].max()
sexo_max_elogios = elogios.idxmax()
proporcao_max_elogios = elogios.max()
print("Sexo que faz mais elogios: ", sexo_max_elogios, "({:.2f}%)".format(proporcao_max_elogios))

# Sexo que faz mais solicitações
solicitacoes = df_juncao[df_juncao['TIPO'] == 'SOLICITAÇÃO'].groupby('SEXO')['proporcao'].max()
sexo_max_solicitacoes = solicitacoes.idxmax()
proporcao_max_solicitacoes = solicitacoes.max()
print("Sexo que faz mais solicitações: ", sexo_max_solicitacoes, "({:.2f}%)".format(proporcao_max_solicitacoes))

# Sexo que faz mais reclamações
reclamacoes = df_juncao[df_juncao['TIPO'] == 'RECLAMAÇÃO'].groupby('SEXO')['proporcao'].max()
sexo_max_reclamacoes = reclamacoes.idxmax()
proporcao_max_reclamacoes = reclamacoes.max()
print("Sexo que faz mais reclamações: ", sexo_max_reclamacoes, "({:.2f}%)".format(proporcao_max_reclamacoes))


# In[ ]:




