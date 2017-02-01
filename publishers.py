import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#ads per publishers. each ad is connected to a publisher through the document it is leading to.
ad_doc = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/promoted_content.csv",
                     usecols=["ad_id","document_id"],iterator = True, chuncksize = 20000)

doc_publisher = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_meta.csv",
                            usecols=["document_id","publisher_id"],iterator = True, chuncksize = 20000)

clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     usecols=["ad_id","clicked"],iterator = True, chuncksize = 20000)

#returns a block of relavent docs, ads and displays
relavent_docs = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/fifth_merge_w_top_sim.csv",
                           usecols = ["document_id_y"])
relavent_docs = pd.Series(np.array(relavent_docs.document_id_y)).unique()

relavent_ad = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/fifth_merge_w_top_sim.csv",
                           usecols = ["ad_id"])
relavent_ad = pd.Series(np.array(relavent_ad.ad_id)).unique()

relavent_disp = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/fifth_merge_w_top_sim.csv",
                           usecols = ["display_id"])
relavent_disp = pd.Series(np.array(relavent_disp.display_id)).unique()


#returns filtered tavles of doc_piblisher, clicks and ad_doc by document_id, display_id and ad_id
relavent_doc_publisher =  pd.concat([chunk[chunk['document_id'].isin(relavent_docs)]for chunk in doc_publisher])
relavent_clicks =  pd.concat([chunk[chunk['display_id'].isin(relavent_disp)]for chunk in clicks])
relavent_ad = pd.concat([chunk[chunk['ad_id'].isin(relavent_disp)]for chunk in ad_doc])
ad_publisher = relavent_ad.merge(relavent_docs, on="document_id")
relavent_ad = relavent_ad.drop("document_id",1)
skdsk
ad_publisher_g = ad_publisher.groupby(["publisher_id"],as_index=False).agg({"ad_id":np.count_nonzero})

publishers = np.array(ad_publisher_g["publisher_id"])
ads = np.array(ad_publisher_g["ad_id"])

fig = plt.figure()
fig.suptitle('ads per publisher', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Publishers")
ax.set_ylabel("Ads")
plt.bar(left=publishers, height=ads)
plt.show()

#now clicks per publisher
#we need to agragate first in order to prevent multiplies (many ads in different displays)
clicks_g = clicks.groupby(["ad_id"], as_index = False).agg({"clicked":np.sum})
clicks_publishers = clicks_g.merge(ad_publisher,on = "ad_id")
clicks_publishers = clicks_publishers.drop("ad_id",1)
clicks_publishers_g = clicks_publishers.groupby(["publisher_id"], as_index = False).agg({"clicked":np.sum})

clks = np.array(clicks_publishers_g["clicked"])
pblshs = np.array(clicks_publishers_g["publisher_id"])

fig = plt.figure()
fig.suptitle('clicks per publisher', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Publishers")
ax.set_ylabel("Clicks")
plt.bar(left=pblshs, height=clks)
plt.show()



#remarks:
#some document_id's who appears in doc_meta does not appear on promoted content, and the opposite.