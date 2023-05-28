import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Example usage:
install('openpyxl')

import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import os
import pickle
import openpyxl

author_df = pd.read_excel(r'Village Elders_id.xlsx', sheet_name='Scopus ID DB')


#read the pickle file streamlit_data_prep into a dictionary
with open(r'streamlit_data_prep.pickle', 'rb') as handle:
    dict = pickle.load(handle)



st.set_page_config(layout = "wide", page_title = "Scopus Dashboard", page_icon = "📊", menu_items={'About': 'https://www.time.rwth-aachen.de/cms/TIME/Die-Research-Area/~ehfb/Technologie-und-Innovationsmanagement-/?lidx=1'})

# The main window

st.title("Bibliometric Analysis of OUI Elders' Publications")
st.info("Compare the publications of OUI Elders with the publications of other authors in the same field")


with st.container():
     col1, col2, col3 = st.columns(3)
     col1.metric("Number of OUI Elders", dict['author_df.shape[0]'])
     col2.metric("Total number of authors listed in OUI Elders publications", dict['authorss.__len__()'])
     col3.metric("Total number of authors listed in OUI Elders citations", dict['citerss.__len__()'])


with st.container():

    st.subheader("Top 5 authors by number of papers listed in OUI Elder's publications")
    st.table(dict['top_authors'])

    st.subheader("Top 5 citers by number of papers listed in OUI Elder's citations")
    st.table(dict['top_citers'])

with st.container():
     #create bar chart for top 30 keywords in author_keywords and citers_keywords in two columns
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Top 30 keywords in OUI Elders' publications")
        st.bar_chart(data = dict['author_keywords'], x = 'keyword', y = 'count')
    with col2:
        st.subheader("Top 30 keywords in OUI Elders' citers publications")
        st.bar_chart(data = dict['citers_keywords'], x = 'keyword', y = 'count')

with st.container():
     #create bar chart for top 30 keywords in author_keywords and citers_keywords in two columns
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Papers published each year - OUI Elders' publications")
        st.bar_chart(dict['author_db_grouped'], x = 'cover_year', y = 'counts')
    with col2:
        st.subheader("Papers published each year - OUI Elders' citers publications")
        st.bar_chart(dict['citation_db_grouped'], x = 'cover_year', y = 'counts')


st.header("Network analysis of bibliographic data")  
st.info("Select a graph visualisation type to view")

path = r'OUI Authors Network'
files = os.listdir(path)
files = [i for i in files if i.endswith('.html')]
#get all the ending numbers of the files which occur after the last underscore and beqfore the .html
files = [i.split('_')[-1].split('.')[0] for i in files]
files = [int(i) for i in files]
author_names = author_df[author_df['Value'].isin(files)]['Full Name'].tolist()


option = st.selectbox('Select the OUI elder to view the network', author_names)

#select the exact name from the array
author_name = author_names[0]

st.write('You selected:', author_name)

#select the corresponding scopus id from author_df based on the selected author name
scopus_id = author_df[author_df['Full Name'] == author_name]['Value'].unique()
#select the exact scopus id from the array
scopus_id = scopus_id[0]


#convert option to string
option = str(scopus_id)



with st.container():


        st.subheader("Co-authorship Network of OUI Elders")
        try:
            path = '/OUI Authors Network'
            HtmlFile1 = open(f'{path}/author_names.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
        except:
            path = 'Scopus Iteration'
            # HtmlFile1 = open(os.getcwd()+r"\Scopus Iteration\author_names.html", 'r')

            HtmlFile1 = open(os.getcwd()+r"OUI Authors Network/author_names_OUI_" + option + r".html", 'r')
        components.html(HtmlFile1.read(), height=700)

with st.container():   
        st.subheader("Co-authorship Network of OUI Elders Citers")     
        try:
            path = '/OUI Authors Network'
            HtmlFile2 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')
            
        except:
            path = '/Scopus Iteration'
            # HtmlFile2 = open(os.getcwd()+r"\Scopus Iteration\citers_names_with_all_ranking.html", 'r')
        
            HtmlFile2 = open(os.getcwd()+r"OUI Authors Network/author_names_citation_" + option + r".html", 'r')
        components.html(HtmlFile2.read(), height=700)


with st.container():
        
        st.subheader("Co-occurrence Keyword Network of OUI Elder Papers")
        try:
            path = '/OUI Authors Network'
            HtmlFile3 = open(f'{path}/authkeywords_OUI_Elders.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
        except:
            path = 'Scopus Iteration'
            # HtmlFile3 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_OUI_Elders.html", 'r')
            
            HtmlFile3 = open(os.getcwd()+r"OUI Authors Network/authkeywords_OUI_" + option + r".html", 'r')
        components.html(HtmlFile3.read(), height=700)

with st.container():   
        st.subheader("Co-occurrence Keyword Network of OUI Elders Citers Papers")    
        try:
            path = '/OUI Authors Network'
            HtmlFile4 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
        except:
            path = '/Scopus Iteration'
            # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
          
            HtmlFile4 = open(os.getcwd()+r"OUI Authors Network/authkeywords_citations_" + option + r".html", 'r')
        components.html(HtmlFile4.read(), height=700)

with st.container():   
        st.subheader("Bibliographic coupling of Journals of OUI Elders Citers Papers")    
        try:
            path = '/OUI Authors Network'
            HtmlFile5 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
        except:
            path = '/Scopus Iteration'
            # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
          
            HtmlFile5 = open(os.getcwd()+r"publicationNames_Citers1.html", 'r')
        components.html(HtmlFile5.read(), height=700)


