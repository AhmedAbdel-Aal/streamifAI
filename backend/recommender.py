import numpy as np
from copy import deepcopy
import math
import pandas as pd
import sklearn
import pandas_profiling
from datetime import datetime
from sklearn.svm import SVC
import missingno as msno
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.manifold import MDS
from sklearn.decomposition import PCA
from argparse import ArgumentParser
import numpy as np
from scipy import spatial
import torch
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.base import clone
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from pathlib import Path

pubinput=[['the lord of the rings: the two towers',0.2],['the lord of the rings: the two towers',0.7],['the lord of the rings: the two towers',0.1]]

def prepare_dataframe(company_data, movie_data, rating_data):
    df0 = pd.read_json(company_data)
    df0=df0.drop(['tmdb', 'tvdb' ,'imdb_episode_id','airtime','banners','posters','publication','modified','timestamp','expires'], axis=1)
    df_movies = pd.read_csv(r'{}'.format(movie_data), thousands=',')
    df_ratings= pd.read_csv(r'{}'.format(rating_data), thousands=',')
    df_ratings=df_ratings.drop(columns=['votes_1','votes_2','votes_3','votes_4','votes_5','votes_10', 'votes_9',
        'votes_8', 'votes_7', 'votes_6'])
    df_ratings_na=df_ratings.isna().sum().tolist()
    order_ratings=sorted(range(len(df_ratings_na)), key=lambda k: df_ratings_na[k])
    cols_ratings = df_ratings.columns.tolist()
    cols_ratings = [cols_ratings[i] for i in order_ratings]
    df_ratings=df_ratings[cols_ratings]
    df1 = pd.merge(df_movies, df_ratings, on='imdb_title_id',  how='outer')
    df1=df1.rename(columns={'year': 'year of release', 'imdb_title_id': 'imdb_id' })
    df1['imdb_id'] = df1['imdb_id'].str.replace("tt","").astype(int)
    df1['index']=[i for i in range(len(df1))]
    numerical_col=df1.select_dtypes(include='number').columns
    df1.sort_values("index", inplace = True)
    df1_na=df1.isna().sum().tolist()
    order=sorted(range(len(df1_na)), key=lambda k: df1_na[k])
    cols = df1.columns.tolist()
    cols = [cols[i] for i in order]
    df1=df1[cols]
    L_genre=df1['genre'].value_counts()
    df1['title']=df1['title'].str.lower()
    df1['original_title']=df1['original_title'].str.lower()
    df1['genre']=df1['genre'].str.lower()
    df1['production_company']=df1['production_company'].str.lower()
    df1.drop('usa_gross_income', inplace=True, axis=1)
    df1.drop('worlwide_gross_income', inplace=True, axis=1)
    df1=df1.drop(columns={'date_published','year of release'})
    df=df1.merge(df0,on='imdb_id')
    df.drop_duplicates(subset='imdb_id', keep='first', inplace=True, ignore_index=True)
    features = ['original_title', 'writer', 'production_company']
    def combine_features(row):
        return row['original_title']+' '+row['writer']+' '+row['production_company']
    for feature in features:
        df1[feature] = df1[feature].fillna('')
    df1['combined_features'] = df1.apply(combine_features, axis = 1)
    df1.head()
    vector= TfidfVectorizer(max_features=500)
    vectorized_data = vector.fit_transform(df1['combined_features'].values)
    vectorized_dataframe = pd.DataFrame(vectorized_data.toarray(), index=df1['combined_features'].index.tolist())
    svd = TruncatedSVD(n_components=10)
    reduced_vector = svd.fit_transform(vectorized_dataframe)
    reduced_dataframe = pd.DataFrame(reduced_vector, index=df1['combined_features'].index.tolist())
    for i in range(len(reduced_dataframe.columns)):
        reduced_dataframe.rename(columns = {i:'str_{}'.format(i)}, inplace = True)
    df=pd.concat([df, reduced_dataframe], axis=1)
    df=df.drop(['votes', 'weighted_average_vote', 'total_votes', 'mean_vote',
        'median_vote', 'index', 'males_allages_avg_vote', 'males_allages_votes',
        'non_us_voters_rating', 'non_us_voters_votes','allgenders_30age_avg_vote', 'allgenders_30age_votes','males_30age_votes', 'country', 'actors_x',
        'allgenders_45age_avg_vote', 'allgenders_45age_votes',
        'females_allages_avg_vote', 'females_allages_votes', 'males_45age_votes', 'us_voters_rating',
        'us_voters_votes', 'top1000_voters_rating', 'top1000_voters_votes',
        'allgenders_18age_avg_vote', 'allgenders_18age_votes', 'language_x',
        'females_30age_votes', 
        'males_18age_votes', 
        'females_45age_votes', 'production_company', 
        'females_18age_votes', 
        'allgenders_0age_avg_vote', 'allgenders_0age_votes',
            'males_0age_votes', 
        'females_0age_votes', ], axis=1)
    df_num = df._get_numeric_data()
    df_num.replace(np.nan,0)
    df_genres = df.genres.str.get_dummies(' und ').add_prefix('genre_')
    df_num = pd.concat([df_num, df_genres], axis=1, sort=False)
    df_no_rating=df_num.copy(deep=True)
    scaler = MinMaxScaler()
    df_no_rating=df_no_rating.drop(["males_0age_avg_vote",'avg_vote', 'males_30age_avg_vote',
        'males_45age_avg_vote', 'females_30age_avg_vote',
        'males_18age_avg_vote', 'females_45age_avg_vote',
        'females_18age_avg_vote', 'reviews_from_users', 'reviews_from_critics',
        'males_0age_avg_vote', 'females_0age_avg_vote','males_0age_avg_vote'] , axis=1)

    df_no_rating[['duration', 'metascore', 'id', 'available', 'original',
        'serie', 'season', 'episode', 'year', 'price', 'stereoscopic',
        'runtime', 'fsk', 'genre_Action', 'genre_Anime',
        'genre_Ausländische Filme', 'genre_Bollywood', 'genre_Dokumentarfilme',
        'genre_Dokumentationen, TV-Sendungen', 'genre_Drama',
        'genre_Drama, TV-Sendungen', 'genre_Familie',
        'genre_Familie, TV-Sendungen', 'genre_Familie, TV-Sendungen, Animation',
        'genre_Fantasy', 'genre_Filme', 'genre_Filme für die Feiertage',
        'genre_Horror', 'genre_Independent-Filme', 'genre_Indien Regional',
        'genre_Kinder', 'genre_Klassiker', 'genre_Komödien',
        'genre_Komödien, TV-Sendungen', 'genre_Konzertfilme',
        'genre_Koreanisches Kino', 'genre_Kurzfilme', 'genre_Liebesfilme',
        'genre_Musicals', 'genre_Musik-Filme', 'genre_Science-Fiction',
        'genre_Special Interest', 'genre_Thriller', 'genre_Türkei',
        'genre_Western']] = scaler.fit_transform(df_no_rating[['duration', 'metascore', 'id', 'available', 'original',
        'serie', 'season', 'episode', 'year', 'price', 'stereoscopic',
        'runtime', 'fsk', 'genre_Action', 'genre_Anime',
        'genre_Ausländische Filme', 'genre_Bollywood', 'genre_Dokumentarfilme',
        'genre_Dokumentationen, TV-Sendungen', 'genre_Drama',
        'genre_Drama, TV-Sendungen', 'genre_Familie',
        'genre_Familie, TV-Sendungen', 'genre_Familie, TV-Sendungen, Animation',
        'genre_Fantasy', 'genre_Filme', 'genre_Filme für die Feiertage',
        'genre_Horror', 'genre_Independent-Filme', 'genre_Indien Regional',
        'genre_Kinder', 'genre_Klassiker', 'genre_Komödien',
        'genre_Komödien, TV-Sendungen', 'genre_Konzertfilme',
        'genre_Koreanisches Kino', 'genre_Kurzfilme', 'genre_Liebesfilme',
        'genre_Musicals', 'genre_Musik-Filme', 'genre_Science-Fiction',
        'genre_Special Interest', 'genre_Thriller', 'genre_Türkei',
        'genre_Western']])
    df.to_csv('clean_data.csv') 
    df_num.to_csv('clean_numerical_data.csv') 
    df_no_rating.to_csv('clean_no_rating_data.csv') 
    return df,df_num,df_no_rating

def Similarity(movieId1, movieId2,df_num):
    row1=df_num[df_num['imdb_id'] == movieId1].fillna(0).to_numpy()
    row2=df_num[df_num['imdb_id'] == movieId2].fillna(0).to_numpy()
    return 1 - spatial.distance.cosine(row1[0], row2[0])

def recommendation(query,movie_entry):
    file1 = Path("clean_data.csv")
    file2 = Path("clean_numerical_data.csv")
    file3= Path("clean_no_rating_data.csv")
    if file1.is_file() and file2.is_file() and file3.is_file():
        df = pd.read_csv(r'{}'.format(file1), thousands=',')
        df_num = pd.read_csv(r'{}'.format(file2), thousands=',')
        df_no_rating = pd.read_csv(r'{}'.format(file3), thousands=',')
    else:
        df,df_num,df_no_rating=prepare_dataframe('ap.json','IMDb movies.csv','IMDb ratings.csv')
    query_vector=[[(element['age_range_high']+element['age_range_low'])/2,str.lower(element['gender'])] for element in query]
    for s in query_vector:
        if s[0]<18:
            s[0]=0
        elif s[0]<30:
            s[0]=18
        elif s[0]<45:
            s[0]=30
        else:
            s[0]=45
    y_string= ['{}s_{}age_avg_vote'.format(s[1],s[0]) for s in query_vector]
    y=[df_num[str].replace(np.nan,0).to_numpy() for str in y_string ]
    X=[df_no_rating[[c for c in df_no_rating.columns]].replace(np.nan,0).to_numpy() for i in range(len(y))]
    what_to_pop=[]
    for i in range(len(y)):
        regressor = GradientBoostingRegressor(n_estimators= 1, min_samples_split = 2, min_samples_leaf=1, max_depth=1, verbose= 1)
        regressor = deepcopy(regressor)
        regressor.fit(X[i], y[i])
        feature_importance = regressor.feature_importances_
        print(feature_importance)
        sorted_idx = np.abs(np.argsort(feature_importance))
        print(feature_importance)
        #what_to_pop+=[df_no_rating.columns[np.argmax(feature_importance[sorted_idx])]]
        what_to_pop+=[df_no_rating.columns[np.argpartition(feature_importance[sorted_idx], -2)[-2:]]]
    rows=[]
    for i in range(len(what_to_pop)):
        for j in range(len((what_to_pop[i]))):
            if (df_num[y_string[0]].corr(df_num[what_to_pop[i][j]])<0):
                rows+=[df_num[df_num[y_string[i]]<=df_num.quantile(.7, axis = 0)[y_string[i]]].index]
            else:
                if(df_num[y_string[0]].corr(df_num[what_to_pop[i][j]])>0):
                    rows+=[df_num[df_num[y_string[i]]>=df_num.quantile(.3, axis = 0)[y_string[i]]].index]
    rows_to_keep=set.intersection(*map(set,rows))
    distances=[]
    if(len(movie_entry)==0):
        sample = df.sample(n=1, weights='avg_vote', axis=0).reset_index()
        movie_entry=[[str(sample.loc[0]['original_title']),1]]
    for index in rows_to_keep:
        calculation=0
        for c in movie_entry:
            calculation+=c[1]*Similarity(df_no_rating.loc[df[df['original_title']==c[0]].index[0]]['imdb_id'], df_no_rating.loc[index]['imdb_id'],df_num)
        distances += [calculation]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:10]
    l=[]
    for i in movie_list:
        l+=[[df.iloc[i[0]]['original_title'],df.iloc[i[0]]['url']]]
    return l
