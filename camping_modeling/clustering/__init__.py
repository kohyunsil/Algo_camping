import nlp_clustering as nc
import pandas as pd

if __name__ == '__main__':
    nlp = nc.NlpCluster()
    # data = nlp.nlp_cleansing()
    # data.to_csv("../../datas/nlp_cleansed_data.csv", encoding="utf-8-sig")
    nlp.nlp_clustering(vec='tfidf', min_cluster_size=30)