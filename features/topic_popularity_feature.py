from utils.plot_utils import create_simple_histogram
from utils.table_utils import *
from paths import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
##import seaborn as sns
import statsmodels.api as sm

def create_topics_popularity(main_table,with_confidence = True):
    #------------------------------Clicks per topic----------------------
    #TODO update to correct columns names
    relavent_ads_ands_docs = pd.read_csv(main_table ,usecols=["document_id_y", "ad_id", "clicked"])
    relavent_ads_ands_docs.rename(index=str, columns={"document_id_y": "document_id"},inplace=True)

    topics = pd.read_csv(DOC_TOPICS_YAIR, usecols=["document_id", "confidence_level", "topic_id"])

    relavent_ads_docs_and_topics = relavent_ads_ands_docs.merge(topics,on='document_id')

    clicks_per_topic = relavent_ads_docs_and_topics.groupby(["topic_id"],as_index=False).agg({"clicked":np.sum})\
        .rename(index=str,columns={'clicked': 'clicks_No'})

    '''
    #creates histogram
    topicArr = np.array(clicks_per_topic[["topic_id"]])
    clicksArr = np.array(clicks_per_topic[["clicked"]])
    create_simple_histogram(topicArr,clicksArr,"Clicks Per topic","Topics","Clicks","clicks_per_topics.png")
    '''

    #-----------------------Topic per Document Histogram------------------------

    docs_per_topic = topics.groupby(["topic_id"],as_index=False).agg({"document_id":np.count_nonzero})\
        .rename(index=str, columns={"document_id": "doc_No"})
    '''
    topic_ids = np.array(docs_per_topic[["topic_id"]])
    number_of_documents = np.array(docs_per_topic[["document_id"]])
    create_simple_histogram(topic_ids,number_of_documents,"Docs_per_topics","Topics","Docs","docs_per_topics.png")
    '''

    topic_popularity = relavent_ads_docs_and_topics.merge(clicks_per_topic, on="topic_id").merge(docs_per_topic, on="topic_id")

    if with_confidence:
        topic_popularity['topic_popularity_conf'] = (topic_popularity['clicks_No']*topic_popularity['confidence_level'])/topic_popularity['doc_No']
    else:
        topic_popularity['topic_popularity'] = topic_popularity['clicks_No'] / topic_popularity['doc_No']

    topic_popularity.drop(['clicked','document_id','topic_id','confidence_level','clicks_No','doc_No'],axis=1,inplace=True)

    return topic_popularity


T = create_topics_popularity(MAIN_TABLE_YAIR)
print(T.head(10))