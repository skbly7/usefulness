import cPickle as pickle
import collections
import csv
import bs4
import re
import markdown
from textpreprocess import textpreprocess
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
with open('trained_model.pickle', 'rb') as handle:
    vectorizer, clf, svd = pickle.load(handle)

android = False

file_reader = open('marks.csv', 'r')

r = csv.reader(file_reader)
data__ = []
for row in r:
    data__.append(row)

data_set = []
auto_count = 0
for row in data__:
    data = row[0]
    if len(data) == 0:
        continue
    data_ = markdown.markdown(data.encode('utf-8'))
    data_ = bs4.BeautifulSoup(data_)
    [s.extract() for s in data_('pre')]
    [s.extract() for s in data_('code')]
    data_ = data_.get_text()
    re.sub(r'[^\s\w_]+', '', data_)
    data_ = textpreprocess(data_, converthtml=False)
    content = ' '.join(data_.split())
    data_set.append(content)
    row.append(content)

# with open('comment_android_dataset.pickle', 'wb') as handle:
#     pickle.dump(data_set, handle)

X_ = vectorizer.transform(data_set)
# X_ = svd.transform(X_)

# X_ = X_.toarray()
# X_ = X_.tolist()
# clf.partial_fit([X_[34],X_[33],X_[31],X_[40],X_[41],X_[43],X_[44],X_[45],X_[48],X_[49]],[1,1,1,1,1,1,1,1,1,1])
y_predict = clf.predict(X_)
counter=collections.Counter(y_predict)
print(counter)
print (counter[1]/float(counter[0]+counter[1]))*100, "% useful comments"

if android:
    print "-------------------------------------"
    print "Automatic count : ", auto_count
    print "New percentage : ", (counter[1]/float(counter[0]+counter[1]-auto_count))*100, "% useful comments"

############################
### IGNORE THIS
###########################
#
# index = 0
# c = 0
# for y in y_predict:
#     if y==1:
#         if c>500:
#             print index, data_set[index]
#         c += 1
#         if c>550:
#             break
#     index+=1

def get_classificable_comment_android(data):
    import markdown
    import bs4
    import cPickle as pickle
    from textpreprocess import textpreprocess
    out = []
    for test in data:
        temp_ = test
        temp = ' '.join(test.split('\n')[1:] if test.startswith("Patch Set") else '')
        if temp != '':
            temp = markdown.markdown(temp.encode('utf-8'))
            temp = bs4.BeautifulSoup(temp)
            [s.extract() for s in temp('pre')]
            [s.extract() for s in temp('code')]
            temp = temp.get_text()
            re.sub(r'[^\s\w_]+', '', temp)
            temp = textpreprocess(temp, converthtml=False)
            if temp != '':
                out.append([temp_, 0])
    return out


def save_to_csv(var, name_csv):
    import csv
    out = []
    for i in var:
        temp = []
        temp.append(int(i))
        temp.append(1)
        out.append(temp)
    with open(name_csv, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(out)


