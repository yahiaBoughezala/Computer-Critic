import nltk.classify.util
import glob
from nltk.classify import NaiveBayesClassifier
import json
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
stop_words = set(stopwords.words('english'))
# small algorithmn to calculate rating(out of 5) based on the sentiment result of comment and its summary
def calcRating(neg_review_avg,neu_review_avg,pos_review_avg,neg_summary_avg,neu_summary_avg,pos_summary_avg):
    if pos_review_avg > neg_review_avg and pos_summary_avg > neg_summary_avg:
        
        rate = (2/3*(pos_review_avg - neg_review_avg) + 1/3*(pos_summary_avg - neg_summary_avg))/(1- (2/3*neu_review_avg + 1/3* neu_summary_avg)+0.000001)
        
    elif pos_review_avg > neg_review_avg and  pos_summary_avg <= neg_summary_avg:
        
        rate = (2/3*(pos_review_avg - neg_review_avg) + 1/3*(pos_summary_avg - neg_summary_avg))/(1- (2/3*neu_review_avg + 1/3* neu_summary_avg)+0.000001)
      
    elif pos_review_avg <= neg_review_avg and  pos_summary_avg > neg_summary_avg: 
        
       rate = (2/3*(pos_review_avg - neg_review_avg) + 1/3*(pos_summary_avg - neg_summary_avg))/(1- (2/3*neu_review_avg + 1/3* neu_summary_avg)+0.000001)
        
    elif pos_review_avg <= neg_review_avg and  pos_summary_avg <= neg_summary_avg:   
        
        rate = (2/3*(pos_review_avg - neg_review_avg) + 1/3*(pos_summary_avg - neg_summary_avg))/(1- (2/3*neu_review_avg + 1/3* neu_summary_avg)+0.000001)

    return (rate*5+5)/2


out = open('single_sentiment_output.json','r+')

# open wach file in the cluster folder
with open("reviews.json") as file:  
         neg_review = 0
         neu_review = 0
         pos_review = 0
         neg_summary = 0
         neu_summary = 0
         pos_summary = 0
         rate=0
         for line in file:
              data = json.loads(line)
             
              # using nltk library , sentimentanalyser module we can find the sentiment values of a sentence.
              sid = SentimentIntensityAnalyzer()
              sreview = sid.polarity_scores(data['reviewText'])
              # this assigns the negative , positive and neutral rating of the comments.
              neg_review = sreview['neg'] 
              neu_review = sreview['neu']
              pos_review = sreview['pos']
                
              ssummary = sid.polarity_scores(data['summary'])
              # this assigns the negative , positive and neutral rating of the summary of the reviews 
              neg_summary = ssummary['neg']
              neu_summary = ssummary['neu']
              pos_summary = ssummary['pos']
              
              # passing the sentiment values to the calcRating Function and then printing it in JSON format.
              rate = calcRating(neg_review,neu_review,pos_review,neg_summary,neu_summary,pos_summary)
              out.write("{ \"ProductID\" : \""+ str(data['asin'])+"\" , \"neg_review_avg\" : "+ str(neg_review)+" , \"neu_review_avg\" : "+str(neu_review)+" , \"pos_review_avg\" : "+str(pos_review)+" , \"neg_summary_avg\" : "+str(neg_summary)+" , \"neu_summary_avg\" : "+str(neu_summary)+" , \"pos_summary_avg\" : "+str(pos_summary)+" , \"float_rating\" : "+str(rate)+" , \"round_rating\" : "+str(round(rate))+" }\n")

              
out.close()
    





      
        