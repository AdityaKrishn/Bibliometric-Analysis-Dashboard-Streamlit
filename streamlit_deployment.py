# import subprocess
import sys

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
        st.bar_chart(dict['author_db_grouped'], x = 'year', y = 'counts')
    with col2:
        st.subheader("Papers published each year - OUI Elders' citers publications")
        st.bar_chart(dict['citation_db_grouped'], x = 'year', y = 'counts')


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
            filters_option1 = [ 5, 2, 1]   
            filter_option1 = st.selectbox('Select the filter option', filters_option1, key='filter_option1')
            filter_option1 = str(filter_option1)
            st.info("The filter option is the minimum number of times a keyword should occur in the publications to be considered for the graph.")

            try:
                path = '/Scopus Iteration'
                HtmlFile6 = open(os.getcwd()+r"/OUI Authors Network/authkeywords_combined_" + option +r"_"+filter_option1+ r".html", 'r')
                components.html(HtmlFile6.read(), height=700)
            except:
                st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
            try:
                df_html6 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/authkeywords_combined_' + option +r"_"+filter_option1+ r'.html_communities.csv')
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
            filters_option2 = [5, 2, 1]   
            filter_option2 = st.selectbox('Select the filter option', filters_option2, key='filter_option2')
            filter_option2 = str(filter_option2)  
            st.info("The filter option is the minimum number of publications an author should have to be added in the graph.") 
            try:
                HtmlFile3 = open(os.getcwd()+r"/OUI Authors Network/author_names_combined_" + option +r"_"+filter_option2+ r".html", 'r')
                components.html(HtmlFile3.read(), height=700)            
            except:
                st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
            try:
                df_html3 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/author_names_combined_' + option +r"_"+filter_option2+ r'.html_communities.csv')
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
            filters_option3 = [5, 2, 1]   
            filter_option3 = st.selectbox('Select the filter option', filters_option3, key='filter_option3')
            filter_option3 = str(filter_option3)
            st.info("The filter option is the minimum number of times a keyword should occur in the publications to be considered for the graph.")
            try:
                path = 'Scopus Iteration'
                HtmlFile4 = open(os.getcwd()+r"/OUI Authors Network/authkeywords_OUI_" + option +r"_"+filter_option3+ r".html", 'r')
                components.html(HtmlFile4.read(), height=700)
            except:
                st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
            try:
                df_html4 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/authkeywords_OUI_' + option +r"_"+filter_option3+ r'.html_communities.csv')
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
            filters_option4 = [5, 2, 1]   
            filter_option4 = st.selectbox('Select the filter option', filters_option4, key='filter_option4')
            filter_option4 = str(filter_option4)
            st.info("The filter option is the minimum number of publications an author should have to be added in the graph.") 
            try:
                path = 'Scopus Iteration'
                HtmlFile1 = open(os.getcwd()+r"/OUI Authors Network/author_names_OUI_" + option +r"_"+filter_option4+ r".html", 'r')
                components.html(HtmlFile1.read(), height=700)
            except:
                st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
            try:
                df_html1 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/author_names_OUI_' + option +r"_"+filter_option4+ r'.html_communities.csv')
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
            filters_option5 = [ 5, 2, 1]   
            filter_option5 = st.selectbox('Select the filter option', filters_option5, key='filter_option5')
            filter_option5 = str(filter_option5)
            st.info("The filter option is the minimum number of times a keyword should occur in the publications to be considered for the graph.")
            try:
                path = '/Scopus Iteration'
                HtmlFile5 = open(os.getcwd()+r"/OUI Authors Network/authkeywords_citations_" + option +r"_"+filter_option5+ r".html", 'r')
                components.html(HtmlFile5.read(), height=700)
            except:
                st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
            try:
                df_html5 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/authkeywords_citations_' + option +r"_"+filter_option5+ r'.html_communities.csv')
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
            filters_option6 = [5, 2, 1]   
            filter_option6 = st.selectbox('Select the filter option', filters_option6, key='filter_option6')
            filter_option6 = str(filter_option6)
            st.info("The filter option is the minimum number of publications an author should have to be added in the graph.") 
            try:
                path = '/Scopus Iteration'
                HtmlFile2 = open(os.getcwd()+r"/OUI Authors Network/author_names_citation_" + option +r"_"+filter_option6+ r".html", 'r')
                components.html(HtmlFile2.read(), height=700)
                
            except:
                st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
            try:
                df_html2 = pd.read_csv(os.getcwd()+r'/OUI Authors Network/author_names_citation_' + option +r"_"+filter_option6+ r'.html_communities.csv')
                # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
                df_html2.columns = ['cluster ' + str(col) for col in df_html2.columns]
                df_html2 = df_html2.dropna(how='all')
                df_html2 = df_html2.fillna('')
                st.dataframe(df_html2, hide_index=True)
            except:

                print(sys.exc_info()[0])


with st.container():   
    st.subheader("Bibliographic coupling Network of Publication Journals")   
    st.info("Two articles are said to be bibliographically coupled if at least one cited source appears in the bibliographies or reference lists of both articles (Kessler, 1963)")  
    filters_option7 = [5, 2, 1]   
    filter_option7 = st.selectbox('Select the filter option', filters_option7, key='filter_option7')
    filter_option7 = str(filter_option7)
    st.info("The filter option is the minimum number of publications a journal should have to be added in the graph.") 
    try:
        path = '/Scopus Iteration'
        # HtmlFile2 = open(os.getcwd()+r"\Scopus Iteration\citers_names_with_all_ranking.html", 'r')
        HtmlFile7 = open(os.getcwd()+r"/publicationJournalBibliographiccoupling_" + filter_option7 + r".html", 'r')  
        components.html(HtmlFile7.read(), height=700) 
        
    except:
        st.text("Due to insufficient data points for the selected option, graph could not be generated. Please select a different filter option.")
        
    try:
        df_html7 = pd.read_csv(os.getcwd()+r'/publicationJournalBibliographiccoupling_' + filter_option7 + r'.html_communities.csv')
        # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
        df_html7.columns = ['cluster ' + str(col) for col in df_html7.columns]
        df_html7 = df_html7.dropna(how='all')
        df_html7 = df_html7.fillna('')
        st.dataframe(df_html7, hide_index=True)
    except:

        print(sys.exc_info()[0])




top5_papers_author_db = dict['top5_papers_author_db']
top5_papers_citation_db = dict['top5_papers_citation_db']

#change datatype of cover_year to string in both dataframes
top5_papers_author_db['cover_year'] = top5_papers_author_db['cover_year'].astype(str)
top5_papers_citation_db['cover_year'] = top5_papers_citation_db['cover_year'].astype(str)


authors = list(set([item for sublist in top5_papers_author_db.author_names.tolist() for item in sublist]))
authors = [x for x in authors if x != '']
all_authors = ['All'] + sorted(authors)
all_years = ['All'] + sorted(top5_papers_author_db['cover_year'].unique().tolist())
all_journals = ['All'] + sorted(top5_papers_author_db['publicationName'].unique().tolist())
author_keywords = list(set([item for sublist in top5_papers_author_db.authkeywords.tolist() for item in sublist]))
author_keywords = [x for x in author_keywords if x != '']
all_keywords = ['All'] + sorted(author_keywords)


#create select boxes for Author name, year, journal, keywords to filter the above dataframes, also add All as an option to the select boxes and if all is selected, show all the data

def filter_author_db(df, author, year, journal, keyword):
    if author != 'All':
        df = df[df['author_names'].apply(lambda x: author in x)]
    if year != 'All':
        df = df[df['cover_year'] == year]
    if journal != 'All':
        df = df[df['publicationName'] == journal]
    if keyword != 'All':
        df = df[df['authkeywords'].apply(lambda x: keyword in x)]
    return df


with st.container():
    st.subheader("Below are the details of publications authored/co-authored by the OUI Elders")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        author_filter1 = st.selectbox('Filter by Author', all_authors, key='author_filter1')
    with col2:
        year_filter1 = st.selectbox('Filter by Year', all_years, key='year_filter1')
    with col3:
        journal_filter1 = st.selectbox('Filter by Journal', all_journals, key='journal_filter1')
    with col4:
        keyword_filter1 = st.selectbox('Filter by Keyword', all_keywords, key='keyword_filter1')

    if author_filter1 == 'All' and year_filter1 == 'All' and journal_filter1 == 'All' and keyword_filter1 == 'All':
        filtered_author_db = top5_papers_author_db
    else:
        filtered_author_db = filter_author_db(top5_papers_author_db,author_filter1, year_filter1, journal_filter1, keyword_filter1)
    filtered_author_db = filtered_author_db.rename(columns={'cover_year': 'Year', 'citedby_count': 'Citations', 'authkeywords': 'Keywords', 'publicationName': 'Journal', 'author_names': 'Authors', 'affilname': 'Affiliations', 'title': 'Title', 'doi': 'DOI', 'description': 'Abstract'})
    st.dataframe(filtered_author_db, hide_index=True)


authors = list(set([item for sublist in top5_papers_citation_db.author_names.tolist() for item in sublist]))
authors = [x for x in authors if x != '']
all_authors = ['All'] + sorted(authors)
all_years = ['All'] + sorted(top5_papers_citation_db['cover_year'].unique().tolist())
all_journals = ['All'] + sorted(top5_papers_citation_db['publicationName'].unique().tolist())
citation_keywords = list(set([item for sublist in top5_papers_citation_db.authkeywords.tolist() for item in sublist]))
citation_keywords = [x for x in citation_keywords if x != '']
all_keywords = ['All'] + sorted(citation_keywords)



with st.container():
    st.subheader("Below are the details of publications authored/co-authored by the OUI Elder's Citers")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        author_filter2 = st.selectbox('Filter by Author', all_authors, key='author_filter2')
    with col2:
        year_filter2 = st.selectbox('Filter by Year', all_years, key='year_filter2')
    with col3:
        journal_filter2 = st.selectbox('Filter by Journal', all_journals, key='journal_filter2')
    with col4:
        keyword_filter2 = st.selectbox('Filter by Keyword', all_keywords, key='keyword_filter2')

    if author_filter2 == 'All' and year_filter2 == 'All' and journal_filter2 == 'All' and keyword_filter2== 'All':
        filtered_citation_db = top5_papers_citation_db
    else:
        filtered_citation_db = filter_author_db(top5_papers_citation_db,author_filter2, year_filter2, journal_filter2, keyword_filter2)
    filtered_citation_db = filtered_citation_db.rename(columns={'cover_year': 'Year', 'citedby_count': 'Citations', 'authkeywords': 'Keywords', 'publicationName': 'Journal', 'author_names': 'Authors', 'affilname': 'Affiliations', 'title': 'Title', 'doi': 'DOI', 'description': 'Abstract'})
    st.dataframe(filtered_citation_db, hide_index=True)


# @st.cache(allow_output_mutation=True)
# def biblio_graph():
#     path = '/Scopus Iteration'
#     HtmlFile7 = open(r"publicationJournalBibliographiccoupling.html", 'r')
#     return HtmlFile7
     
# @st.cache_data
# def biblio_table():
#     df_html7 = pd.read_csv(r'publicationJournalBibliographiccoupling.html_communities.csv')
#     # df_html2 = df_html2.reindex(sorted(df_html2.columns), axis=1)
#     df_html7.columns = ['cluster ' + str(col) for col in df_html7.columns]
#     df_html7 = df_html7.dropna(how='all')
#     df_html7 = df_html7.fillna('')
#     return df_html7
     

# with st.container():   
#     st.subheader("Bibliographic coupling Network of Publication Journals")   
#     st.info("Two articles are said to be bibliographically coupled if at least one cited source appears in the bibliographies or reference lists of both articles (Kessler, 1963)")  
#     st.caption("Note: Due to lack of publication journals for OUI Elders sub-communities, the graph could only be created for a few OUI Elders and thus only the overall graph is presented.")
#     HtmlFile7 = biblio_graph()
#     df_html7 = biblio_table()
#     try:
#         components.html(HtmlFile7.read(), height=700)
        
#     except: 
#         path = '/OUI Authors Network'
#         HtmlFile7 = open(f'{path}/citers_names_with_all_ranking.html','r',encoding='utf-8')

#     try:

#         st.dataframe(df_html7, hide_index=True)
#     except:
#         print(sys.exc_info()[0])


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