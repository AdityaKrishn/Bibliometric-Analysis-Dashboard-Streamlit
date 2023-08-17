# import subprocess
import sys

# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Example usage:
# install('streamlit==1.9.0')
# install('openpyxl')


import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import os
import pickle
# import openpyxl

# author_df = pd.read_excel(r'Village Elders_id.xlsx', sheet_name='Scopus ID DB')
author_df = pd.read_csv(r'Village Elders_id.csv')


#read the pickle file streamlit_data_prep into a dictionary
with open(r'streamlit_data_prep.pickle', 'rb') as handle:
    dict = pickle.load(handle)



st.set_page_config(layout = "wide", page_title = "Scopus Dashboard", page_icon = "📊", menu_items={'About': 'https://www.time.rwth-aachen.de/cms/TIME/Die-Research-Area/~ehfb/Technologie-und-Innovationsmanagement-/?lidx=1'})

# The main window

st.title("Bibliometric Analysis of Open User Innovation(OUI) Community Publications")
st.info("Compare the publications of Open User Innovation Elders with the publications of their citers(authors who have cited their publications)")


with st.container():
     col1, col2, col3 = st.columns(3)
     number_of_OUI_Elders = 27
    #  col1.metric("Number of OUI Elders", dict['author_df.shape[0]'])
     col1.metric("Number of OUI Elders", number_of_OUI_Elders)
     col2.metric("Total number of authors listed in OUI Elders publications", dict['authorss.__len__()'])
     col3.metric("Total number of authors listed in OUI Elders citations", dict['citerss.__len__()'])


with st.container():
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Top 15 authors by number of papers listed in OUI Elder's publications")
        st.altair_chart(alt.Chart(dict['top_authors']).mark_bar().encode(x=alt.X('creator', sort=None), y='count'), use_container_width=True)
    with col2:
        st.subheader("Top 15 citers by number of papers listed in OUI Elder's citations")
        st.altair_chart(alt.Chart(dict['top_citers']).mark_bar().encode(x=alt.X('creator', sort=None), y='count'), use_container_width=True)

with st.container():
     #create bar chart for top 30 keywords in author_keywords and citers_keywords in two columns
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Top 15 keywords in OUI Elders' publications")
        st.altair_chart(alt.Chart(dict['author_keywords']).mark_bar().encode(x=alt.X('keyword', sort=None), y='count'), use_container_width=True)
    with col2:
        st.subheader("Top 15 keywords in OUI Elders' citers publications")
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
st.info("Select a graph visualisation type to view.  \nThe graphs are interactive and can be zoomed in and out and dragged around.  \nThe graphs are of three types: \n1. Open User Innovation(OUI) Elders(publications authored or co-authored by the OUI Elders community) \n2. Citers of OUI Elder's papers(All authors who have cited the publications of OUI Elders) \n3. Combination of both OUI Elders' publications and their Citers' publications  \n\nNote: The graphs are made of a filtered set of user-innovation focussed research papers.")
#st.caption("Note: The graphs are made of a filtered set of user-innovation focussed research papers.")

path = r'OUI Authors Network'
files = os.listdir(path)
files = [i for i in files if i.endswith('.html')]
#get all the ending numbers of the files which occur after the last underscore and beqfore the .html
files = [i.split('_')[-1].split('.')[0] for i in files]
files = [int(i) for i in files]
author_names = author_df[author_df['Value'].isin(files)]['Full Name'].tolist()
author_names = list(set(author_names))
#sort the list alphabetically
author_names.sort()

options = st.selectbox('Select the OUI elder to view the network', author_names)

#select the exact name from the array
author_name = str(options)

# st.write('You selected:', author_name)

#select the corresponding scopus id from author_df based on the selected author name
scopus_id = author_df[author_df['Full Name'] == author_name]['Value'].unique()
#select the exact scopus id from the array
scopus_id = scopus_id[0]


#convert option to string
option = str(scopus_id)

option_3 = st.selectbox('Select the graph type', ['Combination of OUI Elders and their Citers publications combined','OUI Elders publications only', 'OUI Elders Citers publications only'])

if option_3 == 'Combination of OUI Elders and their Citers publications combined':

    with st.container():   
            st.subheader("Co-occurrence Keyword Network of combined OUI Elders and their Citers") 
            st.info("Scientific collaboration network(keyword type) is a network where nodes are keywords and links are co-occurence of the respective keywords in the same paper")   
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
            st.info("Scientific collaboration network(author type) is a network where nodes are authors and links are co-authorships as the latter is one of the most well-documented forms of scientific collaboration (Glanzel, 2004)")     
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

elif option_3 == 'OUI Elders publications only':

    with st.container():
            
            st.subheader("Co-occurrence Keyword Network of OUI Elder Papers")
            st.info("Scientific collaboration network(keyword type) is a network where nodes are keywords and links are co-occurence of the respective keywords in the same paper")
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
            st.info("Scientific collaboration network(author type) is a network where nodes are authors and links are co-authorships as the latter is one of the most well-documented forms of scientific collaboration (Glanzel, 2004)")
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
            st.info("Scientific collaboration network(keyword type) is a network where nodes are keywords and links are co-occurence of the respective keywords in the same paper")    
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
            st.info("Scientific collaboration network(author type) is a network where nodes are authors and links are co-authorships as the latter is one of the most well-documented forms of scientific collaboration (Glanzel, 2004)") 
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
#     st.subheader("Bibliographic coupling Network of Publication Journals")   
#     st.info("Two articles are said to be bibliographically coupled if at least one cited source appears in the bibliographies or reference lists of both articles (Kessler, 1963)")  
#     try:
#         path = '/OUI Authors Network'
#         HtmlFile7 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')
        
#     except:
#         path = '/Scopus Iteration'
#         # HtmlFile2 = open(os.getcwd()+r"\Scopus Iteration\citers_names_with_all_ranking.html", 'r')
#         HtmlFile7 = open(os.getcwd()+r"/OUI Authors Network/publicationJournalBibliographiccoupling_" + option + r".html", 'r')   
#     components.html(HtmlFile7.read(), height=700)
#     try:
#         df_html7 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/publicationJournalBibliographiccoupling_' + option + r'.html_communities.csv')
#         # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
#         df_html7.columns = ['cluster ' + str(col) for col in df_html7.columns]
#         df_html7 = df_html7.dropna(how='all')
#         df_html7 = df_html7.fillna('')
#         st.dataframe(df_html7, hide_index=True)
#     except:
#         print(sys.exc_info()[0])


@st.cache(allow_output_mutation=True)
def biblio_graph():
    path = '/Scopus Iteration'
    HtmlFile7 = open(r"publicationJournalBibliographiccoupling.html", 'r')
    return HtmlFile7
     
@st.cache_data
def biblio_table():
    df_html7 = pd.read_csv(r'publicationJournalBibliographiccoupling.html_communities.csv')
    # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
    df_html7.columns = ['cluster ' + str(col) for col in df_html7.columns]
    df_html7 = df_html7.dropna(how='all')
    df_html7 = df_html7.fillna('')
    return df_html7
     

with st.container():   
    st.subheader("Bibliographic coupling Network of Publication Journals")   
    st.info("Two articles are said to be bibliographically coupled if at least one cited source appears in the bibliographies or reference lists of both articles (Kessler, 1963)")  
    st.caption("Note: Due to lack of publication journals for OUI Elders sub-communities, the graph could only be created for a few OUI Elders and thus only the overall graph is presented.")
    HtmlFile7 = biblio_graph()
    df_html7 = biblio_table()
    try:
        components.html(HtmlFile7.read(), height=700)
        
    except: 
        path = '/OUI Authors Network'
        HtmlFile7 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')

    try:

        st.dataframe(df_html7, hide_index=True)
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

# with st.container():   
#         st.subheader("Topic Modelling of OUI Elders Citers Papers abstracts")   
#         try:
#             path = '/tmp'
#             HtmlFile6 = open(f'{path}/authkeywords_citers.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
#         except:
#             path = '/Scopus Iteration'
#             # HtmlFile4 = open(os.getcwd()+r"\Scopus Iteration\authkeywords_citers.html", 'r')
          
#             HtmlFile6 = open(r"LDA10.html", 'r')
#         components.html(HtmlFile6.read(), height=750)

# with st.container():   
#     st.subheader("Co-citation Network of Publication Journals")     
#     try:
#         path = '/OUI Authors Network'
#         HtmlFile7 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')
        
#     except:
#         path = '/Scopus Iteration'
#         HtmlFile7 = open(r"publicationJournalCocitation.html", 'r')
#     components.html(HtmlFile7.read(), height=700)
#     try:
#         df_html7 = pd.read_csv(r'publicationJournalCocitation.html_communities.csv')
#         # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
#         df_html7.columns = ['cluster ' + str(col) for col in df_html7.columns]
#         df_html7 = df_html7.dropna(how='all')
#         df_html7 = df_html7.fillna('')
#         st.dataframe(df_html7, hide_index=True)
#     except:
#         print(sys.exc_info()[0])