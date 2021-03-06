{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.svm import SVC\n",
    "import pickle\n",
    "\n",
    "def get_mood_api():\n",
    "    \n",
    "    reviewmood = pickle.load(open('review.pkl','rb'))\n",
    "    \n",
    "    def mood_data_api(reviewmood,data):\n",
    "        df ={}\n",
    "        df[0] = data\n",
    "        return pd.DataFrame.from_dict(df, orient='index')\n",
    "        \n",
    "        df_suprv = df.drop(df.columns[[2,3,4,5,6,9,10,11]], axis =1)\n",
    "        #df_suprv.loc[:,'reviewType']=df_suprv['overall'].apply(lambda x: 1 if x >= 4.0 else 0 )\n",
    "        df_suprv.loc[:,'verified'] = [1 if x=='True' else 0  for x in df_suprv['verified']]\n",
    "        def count_punct(text):\n",
    "            count = sum([1 for char in text if char in string.punctuation])\n",
    "            ratio = count/(len(text) - text.count(\" \"))\n",
    "            return round(ratio, 4)*100\n",
    "\n",
    "        df_suprv['punct%'] = df_suprv['reviewText'].apply(lambda x: count_punct(x))\n",
    "        df_suprv['body_len'] = df_suprv['reviewText'].apply(lambda x: len(x) - x.count(\" \"))\n",
    "        df_suprv.rename(columns ={'summary' :'Summary', 'overall' :'Overall'},inplace = True)\n",
    "        tfidf_vect = TfidfVectorizer(ngram_range=(2,2))\n",
    "        tfidf_vect1 = TfidfVectorizer(ngram_range=(2,2))\n",
    "        X_tfidf = tfidf_vect.fit_transform(df_suprv['cleaned_text'])\n",
    "        XS_tfidf = tfidf_vect1.fit_transform(df_suprv['cleaned_summ'])\n",
    "        X_tfidf_df = pd.DataFrame(X_tfidf.toarray())\n",
    "        X_tfidf_df.columns = tfidf_vect.get_feature_names()\n",
    "        X_tfidf_df1 = pd.DataFrame(XS_tfidf.toarray())\n",
    "        X_tfidf_df1.columns = tfidf_vect1.get_feature_names()\n",
    "        df_new = pd.concat([df_suprv, X_tfidf_df,X_tfidf_df1],axis=1,sort=False)\n",
    "        df_new.fillna(value =0, inplace = True)\n",
    "        \n",
    "        ReviewType = reviewmood.predict(df_new)\n",
    "        return ReviewType\n",
    "    \n",
    "    return mood_data_api\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
