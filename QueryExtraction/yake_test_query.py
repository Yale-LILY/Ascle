'''
YAKE: https://github.com/LIAAD/yake

YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text.
We compare it against ten state-of-the-art unsupervised approaches (TF.IDF, KP-Miner, RAKE, TextRank, SingleRank, ExpandRank, TopicRank, TopicalPageRank, PositionRank and MultipartiteRank), and one supervised method (KEA).
'''


import yake


language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1


def yake_extract(text,topk=30):

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=topk, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    results = []
    for kw in keywords:
        results.append(kw[0])

    return results

