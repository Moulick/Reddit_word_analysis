from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re
from pprint import pprint
import praw
import string

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def preprocess(s, lowercase=False):
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


#tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
#pprint(preprocess(tweet))



reddit = praw.Reddit('XD')
print('Read only:', reddit.read_only)  # Check if read_only

print('Ok')

count = 0
word_dict = {}
for comment in reddit.redditor('chhopsky').comments.hot(limit=None):
    count +=1
    comment_tokens = preprocess(comment.body)


    for word in comment_tokens:
        word = word.casefold()
        if word not in string.punctuation:
            if word not in stopwords.words('english'):
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1


pprint(word_dict)
most_common_word = max(word_dict, key=word_dict.get)

print(most_common_word, word_dict[most_common_word])
print(count)

