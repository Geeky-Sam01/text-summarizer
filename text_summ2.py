#Text summarization basic Steps:
#  1.Tokenizaiton
# 2. Stopword removal
# 3. Lemmatization and WordFrequency Removal
# 4. Normalization
# 5. Sentence Scores

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from sklearn.feature_extraction.text import TfidfVectorizer



def calculating_tfidf_scores(tokens):
    stopwords=list(STOP_WORDS)
    cleaned_tokens= [token.lemma_.lower() for token in tokens if token.text.lower() not in stopwords and token.text.lower() not in punctuation]
    cleaned_tokens=' '.join(cleaned_tokens)
    tfidf=TfidfVectorizer()
    result=tfidf.fit_transform([cleaned_tokens])
    tridf_scores={}
    for word , score in zip(tfidf.get_feature_names_out(),result.toarray()[0]):
        tridf_scores[word]=score
    return tridf_scores

def score_sentences(select_tokens, tfidf_scores):
    sent_scores = {}
    for sent in select_tokens:
        score = sum(tfidf_scores.get(token.lemma_.lower(), 0) for token in sent)
        sent_scores[sent] = score
    return sent_scores



def generate_summzary(rawdocs,selection_percentage=0.3):
    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)
    
    tfidf_scores= calculating_tfidf_scores(doc)
    
    sent_tokens=[sent for sent in doc.sents]
    sent_scores=score_sentences(sent_tokens,tfidf_scores)
    select_length=int(len(sent_tokens)*selection_percentage)
    summary=nlargest(select_length,sent_scores,key=sent_scores.get)
    final_summary=' '.join([sent.text for sent in summary])
    len_of_doc=len(rawdocs.split())
    len_of_summary=len(final_summary.split())

    return final_summary,doc,len_of_doc,len_of_summary



#TEST CODE
'''
text="""Climate change is a pressing global issue that is primarily driven by human activities, such as the burning of fossil fuels, deforestation, and industrial processes. The increase in greenhouse gas emissions, such as carbon dioxide and methane, leads to a gradual rise in global temperatures, causing widespread impacts including melting ice caps, rising sea levels, more frequent and severe heatwaves, and disrupted weather patterns. Urgent international cooperation is required to mitigate the effects of climate change through transitioning to renewable energy sources, implementing sustainable land-use practices, and adopting policies to reduce emissions. Failure to take substantial action could result in irreversible and catastrophic consequences for ecosystems, economies, and human societies across the world
"""
summary,original,a,b=generate_summzary(text)
print(summary)

#summary=' '.join([sent for sent in summary])
'''
