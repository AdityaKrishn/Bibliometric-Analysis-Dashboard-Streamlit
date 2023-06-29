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
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Top 10 authors by number of papers listed in OUI Elder's publications")
        st.altair_chart(alt.Chart(dict['top_authors']).mark_bar().encode(x=alt.X('creator', sort=None), y='count'), use_container_width=True)
    with col2:
        st.subheader("Top 10 citers by number of papers listed in OUI Elder's citations")
        st.altair_chart(alt.Chart(dict['top_citers']).mark_bar().encode(x=alt.X('creator', sort=None), y='count'), use_container_width=True)

with st.container():
     #create bar chart for top 30 keywords in author_keywords and citers_keywords in two columns
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Top 10 keywords in OUI Elders' publications")
        st.altair_chart(alt.Chart(dict['author_keywords']).mark_bar().encode(x=alt.X('keyword', sort=None), y='count'), use_container_width=True)
    with col2:
        st.subheader("Top 10 keywords in OUI Elders' citers publications")
        st.altair_chart(alt.Chart(dict['citers_keywords']).mark_bar().encode(x=alt.X('keyword', sort=None), y='count'), use_container_width=True)

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


options = st.selectbox('Select the OUI elder to view the network', author_names)

#select the exact name from the array
author_name = str(options)

st.write('You selected:', author_name)

#select the corresponding scopus id from author_df based on the selected author name
scopus_id = author_df[author_df['Full Name'] == author_name]['Value'].unique()
#select the exact scopus id from the array
scopus_id = scopus_id[0]


#convert option to string
option = str(scopus_id)

option_3 = st.selectbox('Select the graph type', ['OUI Elders and their Citers combined','OUI Elders', 'OUI Elders Citers'])

if option_3 == 'OUI Elders and their Citers combined':

    with st.container():   
            st.subheader("Co-occurrence Keyword Network of combined OUI Elders and their Citers")    
            try:
                path = '/OUI Authors Network'
                HtmlFile6 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
            except:
                path = '/Scopus Iteration'
                # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
            
                HtmlFile6 = open(os.getcwd()+r"/OUI Authors Network/authkeywords_combined_" + option + r".html", 'r')
            components.html(HtmlFile6.read(), height=700)
            try:
                df_html6 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/authkeywords_combined_' + option + r'.html_communities.csv')
                # df_html6 = df_html6.reindex(sorted(df_html6.columns), axis=1)
                df_html6.columns = ['cluster ' + str(col) for col in df_html6.columns]
                df_html6 = df_html6.dropna(how='all')
                df_html6 = df_html6.fillna('')
                st.dataframe(df_html6, hide_index=True)
            except:
                print(sys.exc_info()[0])

    with st.container():   
            st.subheader("Co-authorship Network of combined OUI Elders and their Citers")     
            try:
                path = '/OUI Authors Network'
                HtmlFile3 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')
                
            except:
                path = '/Scopus Iteration'
                # HtmlFile2 = open(os.getcwd()+r"\Scopus Iteration\citers_names_with_all_ranking.html", 'r')
            
                HtmlFile3 = open(os.getcwd()+r"/OUI Authors Network/author_names_combined_" + option + r".html", 'r')
            components.html(HtmlFile3.read(), height=700)
            try:
                df_html3 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/author_names_combined_' + option + r'.html_communities.csv')
                # df_html3 = df_html3.reindex(sorted(df_html3.columns), axis=1)
                df_html3.columns = ['cluster ' + str(col) for col in df_html3.columns]
                df_html3 = df_html3.dropna(how='all')
                df_html3 = df_html3.fillna('')
                st.dataframe(df_html3, hide_index=True)
            except:
                print(sys.exc_info()[0])

elif option_3 == 'OUI Elders':

    with st.container():
            
            st.subheader("Co-occurrence Keyword Network of OUI Elder Papers")
            try:
                path = '/OUI Authors Network'
                HtmlFile4 = open(f'{path}/authkeywords_OUI_Elders.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
            except:
                path = 'Scopus Iteration'
                # HtmlFile3 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_OUI_Elders.html", 'r')
                
                HtmlFile4 = open(os.getcwd()+r"/OUI Authors Network/authkeywords_OUI_" + option + r".html", 'r')
            components.html(HtmlFile4.read(), height=700)
            try:
                df_html4 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/authkeywords_OUI_' + option + r'.html_communities.csv')
                # df_html4 = df_html4.reindex(sorted(df_html4.columns), axis=1)
                df_html4.columns = ['cluster ' + str(col) for col in df_html4.columns]
                df_html4 = df_html4.dropna(how='all')
                df_html4 = df_html4.fillna('')
                st.dataframe(df_html4, hide_index=True)
            except:
                print(sys.exc_info()[0])

    with st.container():


            st.subheader("Co-authorship Network of OUI Elders")
            try:
                path = '/OUI Authors Network'
                HtmlFile1 = open(f'{path}/author_names.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
            except:
                path = 'Scopus Iteration'
                # HtmlFile1 = open(os.getcwd()+r"\Scopus Iteration\author_names.html", 'r')

                HtmlFile1 = open(os.getcwd()+r"/OUI Authors Network/author_names_OUI_" + option + r".html", 'r')
            components.html(HtmlFile1.read(), height=700)
            try:
                df_html1 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/author_names_OUI_' + option + r'.html_communities.csv')
                # df_html1 = df_html1.reindex(sorted(df_html1.columns), axis=1)
                df_html1.columns = ['cluster ' + str(col) for col in df_html1.columns]
                df_html1 = df_html1.dropna(how='all')
                df_html1 = df_html1.fillna('')
                st.dataframe(df_html1, hide_index=True)
            except:
                print(sys.exc_info()[0])

else: 

    with st.container():   
            st.subheader("Co-occurrence Keyword Network of OUI Elders Citers Papers")    
            try:
                path = '/OUI Authors Network'
                HtmlFile5 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
            except:
                path = '/Scopus Iteration'
                # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
            
                HtmlFile5 = open(os.getcwd()+r"/OUI Authors Network/authkeywords_citations_" + option + r".html", 'r')
            components.html(HtmlFile5.read(), height=700)
            try:
                df_html5 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/authkeywords_citations_' + option + r'.html_communities.csv')
                # df_html5 = df_html5.reindex(sorted(df_html5.columns), axis=1)
                df_html5.columns = ['cluster ' + str(col) for col in df_html5.columns]
                df_html5 = df_html5.dropna(how='all')
                df_html5 = df_html5.fillna('')
                st.dataframe(df_html5, hide_index=True)
            except:
                print(sys.exc_info()[0])

    with st.container():   
            st.subheader("Co-authorship Network of OUI Elders Citers")     
            try:
                path = '/OUI Authors Network'
                HtmlFile2 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')
                
            except:
                path = '/Scopus Iteration'
                # HtmlFile2 = open(os.getcwd()+r"\Scopus Iteration\citers_names_with_all_ranking.html", 'r')
            
                HtmlFile2 = open(os.getcwd()+r"/OUI Authors Network/author_names_citation_" + option + r".html", 'r')
            components.html(HtmlFile2.read(), height=700)
            try:
                df_html2 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/author_names_citation_' + option + r'.html_communities.csv')
                # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
                df_html2.columns = ['cluster ' + str(col) for col in df_html2.columns]
                df_html2 = df_html2.dropna(how='all')
                df_html2 = df_html2.fillna('')
                st.dataframe(df_html2, hide_index=True)
            except:
                print(sys.exc_info()[0])





# with st.container():   
#         st.subheader("Bibliographic coupling of Journals of OUI Elders Citers Papers")    
#         try:
#             path = '/OUI Authors Network'
#             HtmlFile5 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
#         except:
#             path = '/Scopus Iteration'
#             # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
          
#             HtmlFile5 = open(r"publicationNames_Citers1.html", 'r')
#         components.html(HtmlFile5.read(), height=700)

with st.container():   
        st.subheader("Topic Modelling of OUI Elders Citers Papers abstracts")   
        try:
            path = '/tmp'
            HtmlFile6 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
        except:
            path = '/Scopus Iteration'
            # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
          
            HtmlFile6 = open(r"LDA10.html", 'r')
        components.html(HtmlFile6.read(), height=750)
