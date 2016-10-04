import csv
import markdown
import bs4
import os
import cPickle as pickle
from textpreprocess import textpreprocess
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

tool_name_to_number_mapping = {
    'Bitbucket': 1,
    'Github': 2,
    'CodeBrag': 3,
    'Phabricater': 4,
    'GamifiedSD': 5
}

if not os.path.isfile('dataset_processed.pickle'):

    file_reader = open('/home/shivam/study/monsoon15/honors/data/random_2500_shuffled.csv', 'r')
    r = csv.reader(file_reader)

    data_set = []
    for row in r:
        data_set.append(row)

    only_corpus = []
    only_labels = []
    for data in data_set:
        data_ = markdown.markdown(data[0].encode('utf-8'))
        data_ = bs4.BeautifulSoup(data_)
        [s.extract() for s in data_('pre')]
        [s.extract() for s in data_('code')]
        data_ = textpreprocess(data_.get_text(), converthtml=False)
        data[0] = ' '.join(data_.split())
        data[1] = tool_name_to_number_mapping[data[1]]
        only_corpus.append(data[0])
        only_labels.append(data[2])

    with open('dataset_processed.pickle', 'wb') as handle:
        pickle.dump([only_corpus, only_labels], handle)

else:
    with open('dataset_processed.pickle', 'rb') as handle:
        only_corpus, only_labels = pickle.load(handle)

################################################################
# from IPython.display import Image
# from sklearn.externals.six import StringIO
# import pydot
# dot_data = StringIO()
# tree.export_graphviz(clf, out_file=dot_data)
# graph = pydot.graph_from_dot_data(dot_data.getvalue())
# graph.write_pdf("visualize.pdf")


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn import ensemble
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
svd = ""

# file_reader = open('android_complete_stemmed.csv', 'r')
# r = csv.reader(file_reader)
# android_csv_data = []
# for row in r:
#     android_csv_data.append(row)
# with open('comment_android_dataset.pickle', 'rb') as handle:
#     data_set = pickle.load(handle)
# c=0
# for data in android_csv_data:
#     if c>=200:
#         break
#     c += 1
#     only_corpus.append(data[0])
#     only_labels.append(int(data[1]))
    # only_labels.append(1)

######################
##################
#######################
vectorizer = TfidfVectorizer(min_df=1)
# vectorizer = CountVectorizer(analyzer='char', min_df=1)
X =  vectorizer.fit_transform(only_corpus[:2000])
X_ = vectorizer.transform(only_corpus[2000:])

# svd = TruncatedSVD(n_components=20, random_state=42, )
# X = svd.fit_transform(X)
# X_ = svd.transform(X_)


# clf = GaussianNB()
# clf = tree.DecisionTreeClassifier()
# clf = ensemble.RandomForestClassifier()
clf = svm.LinearSVC()
# clf = MLPClassifier(solver='lbgfs')

# X = X.tolist()
# X_ = X_.tolist()
X = X.toarray()
X_ = X_.toarray()


clf.fit(X[:2000], only_labels[:2000])

with open('trained_model.pickle', 'wb') as handle:
    pickle.dump([vectorizer, clf, svd], handle)

y_predict = clf.predict(X_)
labels_ = only_labels[2000:]
print classification_report(labels_, y_predict)

# clf = KMeans(n_clusters=2)
# clf.fit(X[:1600].toarray(), only_labels[:1600])
# y_predict = clf.predict(X_.toarray())
# labels_ = only_labels[1500:]
# print classification_report(labels_, y_predict)
#
# index = 0
# for y in y_predict:
#     if y==0:
#             print only_corpus[index+1500]
#     index +=1
