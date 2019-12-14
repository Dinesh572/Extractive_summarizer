from nltk.corpus import stopwords
from nltk.stem import PorterStemmer# is used to convert faster fastest to its root word fast
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4
import requests
url='https://en.wikipedia.org/wiki/20th_century'
res=requests.get(url)
soup = bs4.BeautifulSoup(res.text, 'lxml')
paragraphs=soup.find_all('p')
#print(paragraphs)
article_content=''
for p in paragraphs:
    article_content  += p.text # here .text is used to get only text e.g; <p> hello <b> friends!</b> </p> ----->  hello friends! (note <b> & </b> is not included)
#print(article_content)

def create_frequency_table(text_string) -> dict: # here  -> dict is return annotation of function create_dictionary_table  can also be retrived by create_dictionary_table.__annotations__
    stop_words=set(stopwords.words("english"))
    word_tokens = word_tokenize(text_string)
    stem=PorterStemmer()
    freq_tbl= dict()
    for wd in word_tokens:
        wd=stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in freq_tbl:
            freq_tbl[wd]+=1
        else:
            freq_tbl[wd]=1
    return freq_tbl

def calculate_sentence_scores (sentences, frequency_table)-> dict:
    sentence_weight=dict()
    for sentence in sentences :
        sentence_wordcount = 0
        for word_weight in frequency_table :
            if word_weight in sentence.lower():
                sentence_wordcount +=1
                if sentence[:7] in sentence_weight :
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] =frequency_table[word_weight]
        sentence_weight[sentence[:7]] /= sentence_wordcount
    return sentence_weight
def calculate_avg_score(sentence_weight) -> int:
    sum_val=0
    for value in sentence_weight :
        sum_val += sentence_weight[value];

    avg_score =sum_val /len(sentence_weight)

    return avg_score

def article_summary(sentence_weight,threshold ,sentences) :
    article_summary =''
    for sentence in sentences :
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] > threshold :
            article_summary += ' ' +sentence

    return article_summary

def run_article_summary(article):
    freq_tbl = create_frequency_table(article)
    sentences = sent_tokenize(article)
    sentence_score =calculate_sentence_scores(sentences, freq_tbl)
    threshold = calculate_avg_score(sentence_score)
    summary = article_summary(sentence_score, 1.5*threshold, sentences)
    return summary

if __name__ == "__main__" :
    summary =run_article_summary(article_content)
    print(summary)
