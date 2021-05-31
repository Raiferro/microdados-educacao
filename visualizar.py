import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns




st.set_page_config(page_title='Microdados Educação Caucaia')


def main(df):
    st.title('Visualização dos microdados do censo da educação básica de 2020')
    st.subheader('Dados disponiveis pelo INPEP e visualização desenvolvida pela BlockchainOne (https://blockchainone.com.br/)')
    st.markdown(
    """
    
    <br><br/>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla dolor sapien,
    gravida a tellus non, tempus hendrerit mauris. Suspendisse non interdum libero.
    Nulla vel porttitor erat, ac auctor ligula. Ut suscipit neque et semper pretium. Nunc quis ultrices nisi.
    Pellentesque in lectus ut leo vestibulum fringilla vitae non quam. Duis tempus faucibus nisi, a mollis est scelerisque non.
    Vivamus porta at eros vel vestibulum. Nullam eget egestas mi.
    """
    , unsafe_allow_html=True)
    capturar_filtros(df)
    #st.write(df.head())

    
    col1, col2 = st.beta_columns(2)

    #-- Histograma de Idade
    col1.markdown(
        """
        ### Distribuição de idade dos alunos filtrados
    
        """
    )
    
    fig, ax1 = plt.subplots()
    sns.histplot(data=df, x="NU_IDADE_REFERENCIA")
    col1.pyplot(fig)
    media, desvio, mediana, moda = get_dados_idade(df)
    col1.write("A média da idade dos alunos filtrados é {0:.2f}, com devio padrão de {1:.2f}, mediana {2:.0f} e moda {3:.0f}".format(media, desvio, mediana, moda))

    ##-- Boxplot com a Disitribuicao
    col2.markdown(
        """
        ### Análise dos Quartis - Idade

        """
    )
    boxplot, axbp = plt.subplots()
    sns.boxplot(x=df["NU_IDADE"])
    col2.pyplot(boxplot)

    Q1, Q2, Q3, MAX = get_dados_quartil(df)
    col2.write("O primeiro quartil das idades dos alunos foi {0:.2f}. O segundo quartil {1:.2f}. O terceiro {2:.2f} e o valor máximo foi de {3:.2f}".format(Q1,Q2,Q3,MAX))    


    st.write("---")


    #-- Histograma de Raca
    col1.markdown(
        """

        ### Distribuição de Raça/Cor declarada

        """
    )
    labels = ['Não declarada', 'Branca', 'Preta', 'Parda', 'Amarela', 'Indigena']
    race, ax2 = plt.subplots()
    sns.histplot(data=df, x="TP_COR_RACA", )
    col1.pyplot(race)
    
    #--Pizza do Sexo
    col2.markdown(
        """
        ### Distribuição de Gênero Declarado 

        """
    )
    data_sexo = df.groupby("TP_SEXO")['TP_SEXO'].count()
    pie_sexo, ax3 = plt.subplots()
    labels = ["Masculino", "Feminino"]
    sns.barplot(x=data_sexo, y=labels)
    #plt.pie(x=data_sexo, autopct="%.1f%%", labels=labels, pctdistance=0.5)
    #plt.title("Sexo dos Alunos", fontsize=14)
    col2.pyplot(pie_sexo)

    #--Zona Rural/Urbana
    col1.markdown(
        """
        ### Distribuição por Tipo de Zona Residêncial
    
        """
    )
    data_regiao, n_urb, n_rural = get_dados_zona(df)
    pie_regiao, ax4 = plt.subplots()
    labels = ["Urbana ", "Rural"]
    sns.barplot(x=data_regiao, y=labels)
    col1.pyplot(pie_regiao)    
    col1.write("{0} alunos declararam viver em zona urbana e {1} declararam viver em zona rural".format(n_urb, n_rural))

    #--Estudam em Local Diferenciado
    col2.markdown(
        """
        ### Distribuição por Localização Diferênciada da Escola

        """
    )
    data_diferenciado = get_dados_local_diferenciado(df)
    img_dif, ax_dif = plt.subplots()
    labels = ["Não diferenciada ", "Área de assentamento", "Terra indígena", "Comunidade remanescente de quilombos"]
    ax_dif = sns.barplot(y=data_diferenciado, x=labels)
    #ax_dif.bar_label(img_dif, fmt='%.2f')
    col2.pyplot(img_dif)


    



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
    
    
    filtros_aplicados = st.sidebar.button('Filtrar')
    #if filtros_aplicados:
    #    if (masculino and feminino): pass
    #    if(masculino and not feminino):
    #        df = df.where(TP_SEXO == 1)
    #    if(not masculino and feminino):
    #        df = df.where(TP_SEXO == 2)
    #    #df = df.where(df.NU_IDADE >= faixa_etaria[0] and df.NU_IDADE <= faixa_etaria[1])
    #    filtrar_dados(df)


#def filtrar_dados(df):
    #-- Filtra o Ano
    #if(select_ano != '2020'):
    #    pass
    
    #-- Filtra a faixa Etaria
    
    
    #Filtra o Sexo
    
     
    #Filtra Raça/Cor
    #racas = []
    #if nao_declarada: raca.append('0')
    pass

  
if __name__ == '__main__':

    #logging.basicConfig(level=logging.CRITICAL)

    #df = load_data()
    df = pd.read_csv('2020.csv')
    main(df)
























