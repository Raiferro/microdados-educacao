from pandas.core.indexes.base import Index
from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
import numpy as np
import pandas as pd
import xmltodict
from pandas import json_normalize
import urllib.request
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
from PIL import Image
import requests
import matplotlib.pyplot as plt

#-- Configura o estilo da pagina
st.set_page_config(layout="wide", page_title= "Microdados Educação")
matplotlib.use("agg")
_lock = RendererAgg.lock

#-- Estilo dos Gráficos
sns.set_style('darkgrid')
sns.set_palette("dark:blue")

#-- Carrega dos dados
@st.cache
def get_data():
     return(pd.read_csv('2020.csv'))
df = get_data()

st.sidebar.header("Filtrar Dados")
#-- Filtro - Define o ano da pesquisa
select_ano = st.sidebar.selectbox('Qual ano do deseja analisar?', ['2020'])

#-- Filtro - Escolhe a faixa etaria
faixa_etaria = st.sidebar.slider('Faixa Etaria', min_value=0, max_value=100, value=(0,100))
df = df.query("NU_IDADE >= @faixa_etaria[0] and NU_IDADE <= @faixa_etaria[1]")

#-- Filtro - Sexo
expander_sexo = st.sidebar.beta_expander("Sexo", expanded=False)
with expander_sexo:
    masculino = expander_sexo.checkbox('Masculino', value=True)
    feminino = expander_sexo.checkbox('Feminino', value=True)
    if(masculino and feminino):
        pass
    if(masculino and not feminino):
        df = df.query("TP_SEXO == 1")
    if(not masculino and feminino):
        df = df.query("TP_SEXO == 2")
    if(not masculino and not feminino):
        df = df.query("TP_SEXO != 1 and TP_SEXO != 2")
    
#-- Filtro - Cor/Raça
expander_raça = st.sidebar.beta_expander("Cor/Raça", expanded=False)
with expander_raça:
    #st.sidebar.markdown('#### Cor/Raça')
    preta = expander_raça.checkbox('Preta', value=True)
    if not preta: df = df.query("TP_COR_RACA != 2 ")
    parda = expander_raça.checkbox('Parda', value=True)
    if not parda: df = df.query("TP_COR_RACA != 3 ")
    amarela = expander_raça.checkbox('Amarela', value=True)
    if not amarela: df = df.query("TP_COR_RACA !=  4")
    indigena = expander_raça.checkbox('Indígena', value=True)
    if not indigena: df = df.query("TP_COR_RACA != 5 ")
    branca = expander_raça.checkbox('Branca', value=True)
    if not branca: df = df.query("TP_COR_RACA != 1 ")
    nao_declarada = indigena = expander_raça.checkbox('Não declarada', value=True)
    if not nao_declarada: df = df.query("TP_COR_RACA != 0 ")

#-- Filtro - Ensino Público/Privado
expander_publiparti= st.sidebar.beta_expander("Ensino Público/Privado")
with expander_publiparti:
    #expander_modalidade.sidebar.markdown('#### Ensino Público/Privado')
    publico = expander_publiparti.checkbox('Público', value = True)
    if not publico: df = df.query("TP_DEPENDENCIA == 4")
    privado = expander_publiparti.checkbox('Privado', value = True)
    if not privado: df = df.query("TP_DEPENDENCIA != 4")

#-- Filtro - Necessidade Especial
expander_especial = st.sidebar.beta_expander("Necessidade Especial")
with expander_especial:
    check_nao_necessidade = expander_especial.checkbox('Não Possui Necessidade Especial', value = True)
    if not check_nao_necessidade: df = df.query("IN_NECESSIDADE_ESPECIAL != 0")
    check_cegueira = expander_especial.checkbox('Cegueira', value = True)
    if not check_cegueira: df = df.query("IN_CEGUEIRA != 1")
    check_baixa_visao = expander_especial.checkbox('Baixa Visão', value = True)
    if not check_baixa_visao: df = df.query("IN_BAIXA_VISAO != 1")
    check_def_auditiva = expander_especial.checkbox('Deficiência Auditiva', value = True)
    if not check_def_auditiva: df = df.query("IN_DEF_AUDITIVA != 1")
    check_def_fisica = expander_especial.checkbox('Deficiência Física', value = True) 
    if not check_def_fisica: df = df.query("IN_DEF_FISICA != 1")
    check_def_int = expander_especial.checkbox('Deficiência Intelectual', value = True) 
    if not check_def_int: df = df.query("IN_DEF_INTELECTUAL != 1")
    check_surdez = expander_especial.checkbox('Surdez', value = True) 
    if not check_surdez: df = df.query("IN_SURDEZ != 1")
    check_super = expander_especial.checkbox('Super Dotação', value = True) 
    if not check_super: df = df.query("IN_SUPERDOTACAO != 1")
    check_autismo = expander_especial.checkbox('Autismo', value = True) 
    if not check_autismo: df = df.query("IN_AUTISMO != 1")
    check_def_mult = expander_especial.checkbox('Deficiência Múltipla', value = True) 
    if not check_def_mult: df = df.query("IN_DEF_MULTIPLA != 1")
    check_surdo_ceg = expander_especial.checkbox('Surdocegueira', value = True)
    if not check_surdo_ceg: df = df.query("IN_SURDOCEGUEIRA != 1")

#-- Filtro - Etapa de Ensino
expander_modalidade = st.sidebar.beta_expander("Etapa de Ensino")
with expander_modalidade:
    check_creche = expander_modalidade.checkbox("Educação Infantil - Creche", value = True)
    if not check_creche: df = df.query("TP_ETAPA_ENSINO != 1")
    check_preescola = expander_modalidade.checkbox("Educação Infantil - Pré-escola", value = True)
    if not check_preescola: df = df.query("TP_ETAPA_ENSINO != 2")
    check_1ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 1º Ano", value = True)
    if not check_1ano: df = df.query("TP_ETAPA_ENSINO != 14")
    check_2ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 2º Ano", value = True)
    if not check_2ano: df = df.query("TP_ETAPA_ENSINO != 15")
    check_3ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 3º Ano", value = True)
    if not check_3ano: df = df.query("TP_ETAPA_ENSINO != 16")
    check_4ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 4º Ano", value = True)
    if not check_4ano: df = df.query("TP_ETAPA_ENSINO != 17")
    check_5ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 5º Ano", value = True)
    if not check_5ano: df = df.query("TP_ETAPA_ENSINO != 18")
    check_6ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 6º Ano", value = True)
    if not check_6ano: df = df.query("TP_ETAPA_ENSINO != 19")
    check_7ano =  expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 7º Ano", value = True)
    if not check_7ano: df = df.query("TP_ETAPA_ENSINO != 20")
    check_8ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 8º Ano", value = True)
    if not check_8ano: df = df.query("TP_ETAPA_ENSINO != 21")
    check_9ano = expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 9º Ano", value = True)
    if not check_9ano: df = df.query("TP_ETAPA_ENSINO != 41")
    check_1a_medio = expander_modalidade.checkbox("Ensino Médio - 1º ano/1ª Série", value = True)
    if not check_1a_medio: df = df.query("TP_ETAPA_ENSINO != 25")
    check_2a_medio = expander_modalidade.checkbox("Ensino Médio - 2º ano/2ª Série", value = True)
    if not check_2a_medio: df = df.query("TP_ETAPA_ENSINO != 26")
    check_3a_medio = expander_modalidade.checkbox("Ensino Médio - 3ºano/3ª Série", value = True)
    if not check_3a_medio: df = df.query("TP_ETAPA_ENSINO != 27")
    check_4a_medio =  expander_modalidade.checkbox("Ensino Médio - 4º ano/4ª Série", value = True)
    if not check_4a_medio: df = df.query("TP_ETAPA_ENSINO != 28")
    check_ns_medio = expander_modalidade.checkbox("Ensino Médio - Não Seriada", value = True)
    if not check_ns_medio: df = df.query("TP_ETAPA_ENSINO != 29")
    check_cti_1a = expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 1ª Série", value = True)
    if not check_cti_1a: df = df.query("TP_ETAPA_ENSINO != 30")
    check_cti_2a = expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 2ª Série", value = True)
    if not check_cti_2a: df = df.query("TP_ETAPA_ENSINO != 31")
    check_cti_3a = expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 3ª Série", value = True)
    if not check_cti_3a: df = df.query("TP_ETAPA_ENSINO != 32")
    check_cti_4a = expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 4ª Série", value = True)
    if not check_cti_4a: df = df.query("TP_ETAPA_ENSINO != 33")
    check_cti_ns = expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) Não Seriada", value = True)
    if not check_cti_ns: df = df.query("TP_ETAPA_ENSINO != 34")
    check_medio_mag_1a = expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 1ª Série", value = True)
    if not check_medio_mag_1a: df = df.query("TP_ETAPA_ENSINO != 35")
    check_medio_mag_2a = expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 2ª Série", value = True)
    if not check_medio_mag_2a: df = df.query("TP_ETAPA_ENSINO != 36")
    check_medio_mag_3a = expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 3ª Série", value = True)
    if not check_medio_mag_3a: df = df.query("TP_ETAPA_ENSINO != 37")
    check_medio_mag_4a = expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 4ª Série", value = True)
    if not check_medio_mag_4a: df = df.query("TP_ETAPA_ENSINO != 38")
    check_ct_conco = expander_modalidade.checkbox("Curso Técnico - Concomitante", value = True)
    if not check_ct_conco: df = df.query("TP_ETAPA_ENSINO != 39")
    check_ct_sub = expander_modalidade.checkbox("Curso Técnico - Subsequente", value = True)
    if not check_ct_sub: df = df.query("TP_ETAPA_ENSINO != 40")
    check_fic_eja_medio = expander_modalidade.checkbox("Curso FIC integrado na modalidade EJA  - Nível Médio", value = True)
    if not check_fic_eja_medio: df = df.query("TP_ETAPA_ENSINO != 67")
    check_fic = expander_modalidade.checkbox("Curso FIC Concomitante", value = True)
    if not check_fic: df = df.query("TP_ETAPA_ENSINO != 68")
    check_eja_fundamental_inicial = expander_modalidade.checkbox("EJA - Ensino Fundamental - Anos Iniciais", value = True)
    if not  check_eja_fundamental_inicial: df = df.query("TP_ETAPA_ENSINO != 69")
    check_eja_fundamental_final = expander_modalidade.checkbox("EJA - Ensino Fundamental - Anos Finais", value = True)
    if not  check_eja_fundamental_final: df = df.query("TP_ETAPA_ENSINO != 70")
    check_eja_medio = expander_modalidade.checkbox("EJA - Ensino Médio", value = True)
    if not  check_eja_medio: df = df.query("TP_ETAPA_ENSINO != 71")
    check_eja_fic_fundamental = expander_modalidade.checkbox("Curso FIC integrado na modalidade EJA - Nível Fundamental (EJA integrada à Educação Profissional de Nível Fundamental)", value = True)
    if not  check_eja_fic_fundamental: df = df.query("TP_ETAPA_ENSINO != 73")
    check_eja_cti_medio = expander_modalidade.checkbox("Curso Técnico Integrado na Modalidade EJA (EJA integrada à Educação Profissional de Nível Médio)", value = True)
    if not  check_eja_cti_medio: df = df.query("TP_ETAPA_ENSINO != 74")

#-- Funcao que carrega a contagem de cada necessidade especial
def get_dados_necessidades_especiais(df):
    df_necessidade_especial = df.query("IN_NECESSIDADE_ESPECIAL == 1")
    cegueira = df_necessidade_especial.IN_CEGUEIRA.sum()
    baixa_visao = df_necessidade_especial.IN_BAIXA_VISAO.sum()
    auditiva = df_necessidade_especial.IN_DEF_AUDITIVA.sum()
    def_fisica = df_necessidade_especial.IN_DEF_FISICA.sum()
    def_inte = df_necessidade_especial.IN_DEF_INTELECTUAL.sum()
    surdez = df_necessidade_especial.IN_SURDEZ.sum()
    surdocegueira = df_necessidade_especial.IN_SURDOCEGUEIRA.sum()
    def_multipla = df_necessidade_especial.IN_DEF_MULTIPLA.sum()
    autismo = df_necessidade_especial.IN_AUTISMO.sum()
    superd = df_necessidade_especial.IN_SUPERDOTACAO.sum()
    return cegueira, baixa_visao, auditiva, def_fisica, def_inte, surdez, superd, autismo, def_multipla, surdocegueira


#-- Cabeçalho
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2, .2, 1, .1))
row0_1.title('Microdados Educação do Municipio da Caucaia')

with row0_2:
    st.write('')

row0_2.subheader(
    'Dados disponiveis pelo INPEP e visualização desenvolvida pela BlockchainOne (https://blockchainone.com.br/)')

row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((.1, 3.2, .1))

#-- Indrodução
with row1_1:
    total = len(df)
    st.markdown(
        """
        Esta aplicacão tem como objetivo gerar uma melhor visualização dos dados da educação básica do município de Caucaia-CE. Os dados são referentes ao ano de 2020. 
        Para os filtros aplicados foram encontrados: **{}** alunos.
        """.format(total)
    )


row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))


#-- Grafico Distirbuição de Idade
with row3_1, _lock:
    st.subheader('Distribuição de Idade')
    media = df['NU_IDADE'].mean()
    std = df['NU_IDADE'].std()
    mediana = df['NU_IDADE'].median()
    moda = df['NU_IDADE'].mode()
    if df['NU_IDADE'].mode().size > 0:
        moda = moda[0]
    else:
        moda = 0  
    
    hist_idade, ax_hist_idade = plt.subplots()
    ax_hist_idade = sns.histplot(data=df, x="NU_IDADE_REFERENCIA")
    ax_hist_idade.set_xlabel('Idade')
    ax_hist_idade.set_ylabel('Quantidade')
    st.pyplot(hist_idade)
    st.markdown("A média da idade dos alunos filtrados é **{0:.2f}**, com devio padrão de **{1:.2f}**, mediana **{2:.0f}** e moda **{3:.0f}**".format(media, std, mediana, moda))

#-- Gráfico Boxplot
with row3_2, _lock:
    st.subheader("Análise dos Quartis - Idade")
    boxplot, ax_boxplot = plt.subplots()
    ax_boxplot = sns.boxplot(x=df["NU_IDADE"])
    ax_boxplot.set_xlabel("Idade")
    st.pyplot(boxplot)
    Q1 = df['NU_IDADE'].quantile(.25)
    Q2 = df['NU_IDADE'].quantile(.5)
    Q3 = df['NU_IDADE'].quantile(.75)
    MAX = df['NU_IDADE'].quantile(1)
    st.markdown("O primeiro quartil das idades dos alunos foi **{0:.2f}**. O segundo quartil **{1:.2f}**. O terceiro **{2:.2f}** e o valor máximo foi de **{3:.2f}**".format(Q1,Q2,Q3,MAX)) 


st.write('')
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

#-- Gráfico Cor/Raça
with row4_1, _lock:
    index = (0,1,2,3,4, 5)
    st.subheader("Distribuição de Raça/Cor declarada")
    data_raca = pd.Series(data = df.groupby("TP_COR_RACA")['TP_COR_RACA'].count(), index = index)
    total = data_raca.sum()
    labels_raca = ['Não declarada', 'Branca', 'Preta', 'Parda', 'Amarela', 'Indigena']
    graf_raca, ax_raca = plt.subplots()
    ax_raca = sns.barplot(x=data_raca, y = labels_raca)
    ax_raca.set_xlabel("Contagem")
    st.pyplot(graf_raca)
    st.markdown(
        """
        **{:.0f}**(**{:.2f}**%) dos alunos não declararam cor/raça, 
        **{:.0f}**(**{:.2f}**%) declararam como 'preta'. 
        **{:.0f}**(**{:.2f}**%) declararam como 'branca'. 
        **{:.0f}**(**{:.2f}**%) declararam como 'parda'. 
        **{:.0f}**(**{:.2f}**%) como 'amarela' e 
        **{:.0f}**(**{:.2f}**%) como 'indigena'.
        """.format(data_raca[0], data_raca[0] / total * 100, data_raca[1], data_raca[1] / total * 100,data_raca[2], (data_raca[2] / total * 100), data_raca[3], (data_raca[3] / total * 100), data_raca[4], (data_raca[4] / total * 100), data_raca[5],(data_raca[5] / total * 100)))
        

#-- Gráfico Gênero
with row4_2, _lock:
    index = (1,2)
    st.subheader("Distribuição de Gênero Declarado ")
    data_sexo = pd.Series(df.groupby("TP_SEXO")['TP_SEXO'].count(), index = index)
    masc = data_sexo[1]
    fem = data_sexo[2]
    total = masc+fem
    graf_sexo, ax_sexo = plt.subplots()
    labels_sexo = ["Masculino", "Feminino"]
    ax_sexo = sns.barplot(x=data_sexo, y=labels_sexo)
    ax_sexo.set_xlabel("Contagem")
    st.pyplot(graf_sexo)
    st.markdown("Foram declarados **{0}** alunos do sexo masculino, o que representa **{1:.2f}**% dos alunos e foram declarados **{2}** alunos do sexo feminino o que corresponde a **{3:.2f}**% do total de alunos.".format(masc, (masc / total * 100),fem, (fem / total * 100))) 


st.write('')
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

#-- Gráfico Zona Residencial
with row5_1, _lock:
    index = (1,2)
    st.subheader("Distribuição por Zona Residêncial")
    data_regiao = pd.Series(df.groupby("TP_ZONA_RESIDENCIAL")['TP_ZONA_RESIDENCIAL'].count(),index=index)
    graf_regiao, ax_regiao = plt.subplots()
    labels = ["Urbana ", "Rural"]
    ax_regiao = sns.barplot(x=data_regiao, y = labels)
    ax_regiao.set_xlabel("Contagem")
    st.pyplot(graf_regiao)
    st.markdown("**{:.0f}**(**{:.2f}**%) dos alunos declaram que vivem em zona urbana e **{:.0f}**(**{:.2f}**%) declaram viver em zona rural".format(data_regiao[1], data_regiao[1] / total * 100, data_regiao[2], data_regiao[2]/total * 100))

#-- Gráfico Localização Diferenciada
with row5_2, _lock:
    index = (0,1,2,3)
    st.subheader("Distribuição por Estudo em Localização Diferenciada")
    data_local_diferenciado = pd.Series(df.groupby("TP_LOCALIZACAO_DIFERENCIADA")['TP_LOCALIZACAO_DIFERENCIADA'].count(), index=index)
    labels = ["Não diferenciada ", "Área de assentamento", "Terra indígena", "Comunidade remanescente de quilombos"]

    graf_diferenciado, ax_diferenciado = plt.subplots()
    ax_diferenciado = sns.barplot(x=data_local_diferenciado, y = labels)
    ax_diferenciado.set_xlabel("Contagem")
    st.pyplot(graf_diferenciado)

    st.markdown("""
        **{:.0f}**(**{:.2f}**%) dos alunos não estudam em localização diferenciada, **{:.0f}**(**{:.2f}**%) estudam em escola localizada em área de assentamento, 
        **{:.0f}**(**{:.2f}**%) estudam em escola localizada em terra indígena, **{:.0f}**(**{:.2f}**%) estudam em escola localizada em comunidade remanescente de quilombos.
    """.format(data_local_diferenciado[0], data_local_diferenciado[0]/total*100,data_local_diferenciado[1], data_local_diferenciado[1]/total*100,data_local_diferenciado[2],data_local_diferenciado[2]/total*100, data_local_diferenciado[3], data_local_diferenciado[3]/total*100))


st.write('')
row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

#-- Gráfico Localização Diferenciada
with row6_1, _lock:
    index = (0, 1)
    st.subheader("Alunos com Necessidades Especiais")
    data_necessidade = pd.Series(df.groupby("IN_NECESSIDADE_ESPECIAL")['IN_NECESSIDADE_ESPECIAL'].count(), index=index)
    labels = ["Não ", "Sim"]
    graf_necessidade_1, ax_necessidade_1 = plt.subplots()
    ax_necessidade_1 = sns.barplot(x=data_necessidade, y = labels)
    ax_necessidade_1.set_xlabel("Contagem")
    st.pyplot(graf_necessidade_1)
    st.markdown(
        """
        **{:.0f}**(**{:.2f}**)% dos alunos não possuem necessidades especiais e **{:.0f}**(**{:.2f}**)%  dos alunos possuem algum tipo de necessidade especial
        """.format(data_necessidade[0], data_necessidade[0]/total * 100, data_necessidade[1],data_necessidade[1]/total * 100) )

#-- Gráfico Necessidade Especial
with row6_2, _lock:
    st.subheader("Distribuição por Necessidade Especial")
    cegueira, baixa_visao, auditiva, def_fisica, def_inte, surdez, superd, autismo, def_multipla, surdocegueira = get_dados_necessidades_especiais(df)
    d = {
        'Necessidade Esp.': ['Cegueira', "Baixa Visão", "Deficiência Auditiva", "Deficiência Física", "Deficiência Intelectual", "Surdez", "Super Dotação", "Autismo", "Deficiência Múltipla", "Surdocegueira"],
        'Quantidade': [cegueira, baixa_visao, auditiva, def_fisica, def_inte, surdez, superd, autismo, def_multipla, surdocegueira]
    }   
    quantidades_ne = pd.DataFrame(d)
    graf_necessidade_2, ax_necessidade_2 = plt.subplots()
    ax_necessidade_2 = sns.barplot(data = quantidades_ne, x = 'Quantidade', y='Necessidade Esp.', palette = "dark:blue")
    st.pyplot(graf_necessidade_2)
    st.markdown("**{}** alunos apresentam cegueira, **{}** alunos apresentam baixa visão, **{}** alunos apresentam deficiência auditiva, **{}** alunos apresentam deficiência física, **{}** alunos apresentam deficiência instelectual, **{}** alunos apresentam surdez, **{}** alunos apresentam superdotação, **{}** alunos apresentam autismo,**{}** alunos apresentam deficiência múltipla e **{}** alunos apresentam surdocegueira.".format(cegueira, baixa_visao, auditiva, def_fisica, def_inte, surdez, superd, autismo, def_multipla, surdocegueira))

st.write('')
row7_space1, row7_1, row7_space2, row7_2, row7_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

#-- Gráfico Dependencia Escola
with row7_1, _lock:
    index = (1,2,3,4)
    st.subheader("Distribuição por Depêndencia Administrativa da Escola")
    labels = ["Federal", "Estadual", "Municipal", "Privada"]
    data_particular = pd.Series(df.groupby("TP_DEPENDENCIA")['TP_DEPENDENCIA'].count(), index=index)
    total = data_particular.sum()
    graf_dep, ax_dep = plt.subplots()
    ax_dep = sns.barplot(x= data_particular, y=labels)
    ax_dep.set_xlabel("Contagem")
    st.pyplot(graf_dep)
    st.markdown(
        """
        **{:.0f}**(**{:.2f}%**) dos alunos estudam em escola administrada pelo governo federal, 
        **{:.0f}**(**{:.2f}%**) dos alunos estudam em escola administrada pelo governo do estado, 
        **{:.0f}**(**{:.2f}%**) dos alunos estudam em escola administrada pelo governo do municipal e 
        **{:.0f}**(**{:.2f}%**) dos alunos estudam em escola particular.
        """.format(data_particular[1], data_particular[1] / total * 100, data_particular[2], data_particular[2] / total * 100, data_particular[3], data_particular[3] / total * 100, data_particular[4], data_particular[4] / total * 100)
    )

#-- #-- Gráfico Creche/Pré-Escola
with row7_2, _lock:
    index = (1,2)
    st.subheader("Distribuilção alunos de Educação Infantil")
    labels = ["Creche", "Pré-escola"]
    data_infantil = pd.Series(df.groupby("TP_ETAPA_ENSINO")["TP_ETAPA_ENSINO"].count(), index = index)
    total = data_infantil.sum()
    graf_inf, ax_inf = plt.subplots()
    ax_inf = sns.barplot(x=data_infantil, y=labels)
    ax_inf.set_xlabel("Contagem")
    st.pyplot(graf_inf)
    st.markdown(
        """
        **{:.0f}** alunos estão na creche e 
        **{:.0f}** dos alunos estão na pré-escola.
         """.format(data_infantil[1], data_infantil[2])
    )

st.write('')
row8_space1, row8_1, row8_space2 = st.beta_columns(
    (.1, 1, .1))


#-- Gráfico Ensino Fundamental - Regular
with row8_1, _lock:
    st.subheader("Distribuilção alunos de Ensino Fundamental(9 anos) - Regular")
    index = (14,15,16,17,18,19,20,21,41)
    labels = ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano", "6º ano", "7º ano", "8º ano", "9º ano"]
    data_fundamental = pd.Series(df.groupby("TP_ETAPA_ENSINO")["TP_ETAPA_ENSINO"].count(), index = index)
    graf_fund, ax_fund = plt.subplots()
    ax_fund = sns.barplot(x=data_fundamental, y=labels, palette = sns.color_palette())
    ax_fund.set_xlabel("Contagem")
    st.pyplot(graf_fund)
    st.markdown(
        """
        **{:.0f}** alunos filtrado estão no 1º ano do fundamental, 
        **{:.0f}** alunos estão no 2º ano, **{:.0f}** alunos estão no 3º ano, **{:.0f}** alunos estão no 4º ano, **{:.0f}** alunos estão no 5º ano, 
        **{:.0f}** alunos estão no 6º ano, 
        **{:.0f}** alunos estão no 7º ano, 
        **{:.0f}** alunos estão no 8º ano, 
        **{:.0f}** alunos estão no 9º ano, 
         """.format(data_fundamental[14], data_fundamental[15], data_fundamental[16], data_fundamental[17], data_fundamental[18], data_fundamental[19], data_fundamental[20], data_fundamental[21], data_fundamental[41],)
    )

st.write('')
row9_space1, row9_1, row9_space2 = st.beta_columns(
    (.1, 1, .1))

#-- Gráfico Ensino Medio - Regular
with row9_1, _lock:
    st.subheader("Distribuilção alunos de Ensino Médio - Regular")
    index = (25,26,27,28,29,30,31,32,33,34,35,36,37,38)
    labels = ["1º ano", "2º ano", "3º ano", "4º ano", "Não Seriado", "Técnico Integrado - 1º Ano", "Técnico Integrado - 2º Ano", "Técnico Integrado - 3º Ano", "Técnico Integrado - 4º Ano", "Técnico Integrado - Não Seriado", "Normal/Magisterio - 1º Ano", "Normal/Magisterio - 2º Ano", "Normal/Magisterio - 3º Ano", "Normal/Magisterio - 4º Ano"]
    data_medio = pd.Series(df.groupby("TP_ETAPA_ENSINO")["TP_ETAPA_ENSINO"].count(), index = index)
    graf_med, ax_med = plt.subplots()
    ax_med = sns.barplot(x=data_medio, y=labels, palette = sns.color_palette())
    ax_med.set_xlabel("Contagem")
    st.pyplot(graf_med)
    st.markdown(
        """
        **{:.0f}** alunos filtrado estão no 1º ano do ensino médio, **{:.0f}** alunos estão no 2º ano, **{:.0f}** alunos estão no 3º ano, **{:.0f}** alunos estão no 4º ano e **{:.0f}** alunos estão no ensino médio não seriado. 
        **{:.0f}** alunos estão no 1º ano do ensino médio com curso técnico integrado, **{:.0f}** alunos estão no 2º ano, **{:.0f}** alunos estão no 3º ano,**{:.0f}** alunos estão no 4º ano e **{:.0f}** alunos então no ens. médio com curso técnico integrado - não seriado.
        **{:.0f}** alunos estão no 1º ano do ensino médio modalidade normal/magistério, **{:.0f}** alunos estão no 2º ano, **{:.0f}** alunos estão no 3º ano e **{:.0f}** alunos então no ens. médio modalidade normal/magistério.
        
         """.format(data_medio[25], data_medio[26],data_medio[27],data_medio[28],data_medio[29],data_medio[30],data_medio[31],data_medio[32],data_medio[33],data_medio[34],data_medio[35],data_medio[36],data_medio[37],data_medio[38])
    )


st.write('')
row10_space1, row10_1, row10_space2 = st.beta_columns(
    (.1, 1, .1))

#-- Gráfico EJA
with row10_1, _lock:
    st.subheader("Distribuilção alunos de EJA")
    index = (65,67,69,70,71,73,74)
    labels = ["Ensino Fundamental - Projovem Urbano", "FIC integrado - Nível Médio", "Ensino Fundamental - Anos Iniciais", "Ensino Fundamental - Anos Finais", "Ensino Médio", "FIC integrado - Nível Fundamental", "Técnico Integrado de Nível Médio"]
    data_eja = pd.Series(df.groupby("TP_ETAPA_ENSINO")["TP_ETAPA_ENSINO"].count(), index = index)
    graf_eja, ax_eja = plt.subplots()
    ax_eja = sns.barplot(x=data_eja, y=labels, palette = sns.color_palette())
    ax_eja.set_xlabel("Contagem")
    st.pyplot(graf_eja)
    st.markdown(
        """
        **{:.0f}**  alunos filtrados estão cursando 'Ensino Fundamental - Projovem Urbano', **{:.0f}** cursam a modalidade 'FIC integrado - Nível Médio', **{:.0f}** cursam a modalidade 'Ensino Fundamental - Anos Iniciais', 
        **{:.0f}**  cursam a modalidade 'Ensino Fundamental - Anos Finais', **{:.0f}**  cursam a modalidade "Ensino Médio", **{:.0f}**  cursam a modalidade 'FIC integrado - Nível Fundamental', **{:.0f}**  e cursam a modalidade 'Técnico Integrado de Nível Médio'.
        """.format(data_eja[65], data_eja[67], data_eja[69], data_eja[70], data_eja[71], data_eja[73], data_eja[74])
    )

st.write('')
row11_space1, row11_1, row10_space2 = st.beta_columns(
    (.1, 1, .1))

#-- Gráfico Curso técnico
with row11_1, _lock:
    st.subheader("Distribuilção alunos de Curso Técnico não Integrado")
    index = (39,40)
    labels = ["Concomitante", "Subsequente"]
    data_tec = pd.Series(df.groupby("TP_ETAPA_ENSINO")["TP_ETAPA_ENSINO"].count(), index = index)
    graf_tec, ax_tec = plt.subplots()
    ax_tec = sns.barplot(x=data_tec, y=labels, palette = sns.color_palette())
    ax_tec.set_xlabel("Contagem") 
    st.pyplot(graf_tec)
    st.markdown(
        """
        **{:.0f}**  alunos filtrados estão fazendo curso técnico concomitante e **{:.0f}** fazem a modalidade subsequente.
        """.format(data_tec[39], data_tec[40])
    )

def get_dados_local_diferenciado(df):
    data_local_diferenciado = df.groupby("TP_LOCALIZACAO_DIFERENCIADA")['TP_LOCALIZACAO_DIFERENCIADA'].count()
    size = data_local_diferenciado
    return data_local_diferenciado


def get_dados_zona(df):
    data_regiao = df.groupby("TP_ZONA_RESIDENCIAL")['TP_ZONA_RESIDENCIAL'].count()
    return data_regiao, data_regiao[1], data_regiao[2]    
    

def get_dados_idade(df):
    media = df['NU_IDADE'].mean()
    std = df['NU_IDADE'].std()
    mediana = df['NU_IDADE'].median()
    moda = df['NU_IDADE'].mode()
    return media, std, mediana ,moda[0]


def get_dados_quartil(df):
    pri_quartil = df['NU_IDADE'].quantile(.25)
    seg_quartil = df['NU_IDADE'].quantile(.5)
    ter_quartil = df['NU_IDADE'].quantile(.75)
    qua_quartil = df['NU_IDADE'].quantile(1)
    return pri_quartil, seg_quartil,ter_quartil, qua_quartil


def capturar_filtros(df):
    #-- Define o ano da pesquisa
    select_ano = st.sidebar.selectbox('Qual ano do deseja analisar?', ['2020'])
    
    #-- Escolhe a faixa etaria
    faixa_etaria = st.sidebar.slider('Faixa Etaria', min_value=0, max_value=100, value=(0,100))

    #-- Sexo
    expander_sexo = st.sidebar.beta_expander("Sexo", expanded=False)
    with expander_sexo:
        #expander_sexo.markdown('#### Sexo')
        masculino = expander_sexo.checkbox('Masculino', value=True)
        feminino = expander_sexo.checkbox('Feminino', value=True)

    #-- Cor/Raça
    expander_raça = st.sidebar.beta_expander("Cor/Raça", expanded=False)
    with expander_raça:
        #st.sidebar.markdown('#### Cor/Raça')
        preta = expander_raça.checkbox('Preta', value=True)
        parda = expander_raça.checkbox('Parda', value=True)
        amarela = expander_raça.checkbox('Amarela', value=True)
        indigena = expander_raça.checkbox('Indígena', value=True)
        branca = expander_raça.checkbox('Branca', value=True)
        nao_declarada = indigena = expander_raça.checkbox('Não declarada', value=True)
    

    #--Ensino Público/Privado
    expander_publiparti= st.sidebar.beta_expander("Ensino Público/Privado")
    with expander_publiparti:
        #expander_modalidade.sidebar.markdown('#### Ensino Público/Privado')
        publico = expander_publiparti.checkbox('Público', value = True)
        privado = expander_publiparti.checkbox('Privado', value = True)

    #Etapa de Ensino
    expander_modalidade = st.sidebar.beta_expander("Etapa de Ensino")
    with expander_modalidade:
        expander_modalidade.checkbox("Educação Infantil - Creche", value = True)
        expander_modalidade.checkbox("Educação Infantil - Pré-escola", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 1º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 2º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 3º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 4º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 5º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 6º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 7º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 8º Ano", value = True)
        expander_modalidade.checkbox("Ensino Fundamental de 9 anos - 9º Ano", value = True)
        expander_modalidade.checkbox("Ensino Médio - 1º ano/1ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - 2º ano/2ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - 3ºano/3ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - 4º ano/4ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - Não Seriada", value = True)
        expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 1ª Série", value = True)
        expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 2ª Série", value = True)
        expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 3ª Série", value = True)
        expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) 4ª Série", value = True)
        expander_modalidade.checkbox("Curso Técnico Integrado (Ensino Médio Integrado) Não Seriada", value = True)
        expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 1ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 2ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 3ª Série", value = True)
        expander_modalidade.checkbox("Ensino Médio - Modalidade Normal/Magistério 4ª Série", value = True)
        expander_modalidade.checkbox("Curso Técnico - Concomitante", value = True)
        expander_modalidade.checkbox("Curso Técnico - Subsequente", value = True)
        expander_modalidade.checkbox("Curso FIC integrado na modalidade EJA  - Nível Médio", value = True)
        expander_modalidade.checkbox("Curso FIC Concomitante", value = True)
        expander_modalidade.checkbox("EJA - Ensino Fundamental - Anos Iniciais", value = True)
        expander_modalidade.checkbox("EJA - Ensino Fundamental - Anos Finais", value = True)
        expander_modalidade.checkbox("EJA - Ensino Médio", value = True)
        expander_modalidade.checkbox("Curso FIC integrado na modalidade EJA - Nível Fundamental (EJA integrada à Educação Profissional de Nível Fundamental)", value = True)
        expander_modalidade.checkbox("Curso Técnico Integrado na Modalidade EJA (EJA integrada à Educação Profissional de Nível Médio)", value = True)


    #Necessidade Especial
    #st.sidebar.markdown("### Necessidade Especial")
    expander_especial = st.sidebar.beta_expander("Necessidade Especial")
    with expander_especial:
       check_cegueira = expander_especial.checkbox('Cegueira', value = True)
       check_baixa_visao = expander_especial.checkbox('Baixa Visão', value = True)
       check_def_auditiva = expander_especial.checkbox('Deficiência Auditiva', value = True)
       check_def_fisica = expander_especial.checkbox('Deficiência Física', value = True) 
       check_def_int = expander_especial.checkbox('Deficiência Intelectual', value = True) 
       check_surdez = expander_especial.checkbox('Surdez', value = True) 
       check_super = expander_especial.checkbox('Super Dotação', value = True) 
       check_autismo = expander_especial.checkbox('Autismo', value = True) 
       check_def_mult = expander_especial.checkbox('Deficiência Múltipla', value = True) 
       check_surdo_ceg = expander_especial.checkbox('Surdocegueira', value = True)    
    
    
    
