import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_dataset():
    df = pd.read_excel("VERİSETLERİ/KITAP/bkmkitap_10.xlsx")
    df = df.iloc[:, 1:]

    return df


df = load_dataset()
df.shape


def create_tfidf(dataframe):
    with open('VERİSETLERİ/turkce-stop-words.txt') as f:
        lines = f.readlines()

    tfidf = TfidfVectorizer(stop_words=lines)
    dataframe['description'] = dataframe['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe['description'])

    return tfidf_matrix


def create_cosinsimilartiy(tfidf_matrix):
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim


def convertbook(dataframe):
    indices = pd.Series(dataframe.index, index=dataframe['title'])
    indices = indices[~indices.index.duplicated(keep='last')]

    return indices


def bookrecommendation(dataframe, bookname, indices, cosine_sim, filtre):
    movie_index = indices[bookname]
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:filtre].index
    recomendation_books = dataframe['title'].iloc[movie_indices]

    return recomendation_books


def search_book_name(dataframe, searchname):
    for i, name in enumerate(dataframe["title"]):
        if searchname in name:
            print(name)


tfidf_matrix = create_tfidf(df)
cosine_sim = create_cosinsimilartiy(tfidf_matrix)
indices = convertbook(df)
recomendation_books = bookrecommendation(df, "Hayvan Çiftliği", indices, cosine_sim, 4)

