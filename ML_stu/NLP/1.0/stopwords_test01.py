from nltk.corpus import stopwords

word_list = ["the", "is"]
filtered_words = [word for word in word_list if word not in stopwords.words('english')]
print(stopwords.words("english"))