import cPickle as pickle
from sklearn import preprocessing

with open('dataset.pickle', 'rb') as handle:
    data_set = pickle.load(handle)

train_data = []
question_wise = {}
for data in data_set:
    if data[-1] in question_wise:
        question_wise[data[-1]].append(data)
    else:
        question_wise[data[-1]] = [data]

max_ans_per_question = 0
for question in question_wise:
    if max_ans_per_question < len(question_wise[question]):
        max_ans_per_question = len(question_wise[question])

def thread_answer_count(id):
    return len(question_wise[id])

def thread_max_vote_on_answer_count(id):
    max = -1000
    for data in question_wise[id]:
        if data[1] > max:
            max = data[1]
    return max

def normalize_attributes(data):
    coloum_to_normalize = [1,2,3,4,5,6,7,8,9]
    data_to_normalize = [[float(l[i]) for i in coloum_to_normalize] for l in data]
    min_max_scaler = preprocessing.MinMaxScaler()
    train_minmax = min_max_scaler.fit_transform(data_to_normalize)
    return train_minmax

attr = normalize_attributes(data_set)

weight = {
    'answer_vote_count': 100,
    'is_accepted': 12,
    'thread_has_accepted': -3,
    'question_vote_count': 8,
    'reviewer_repo': 0,
    # 'ratio_ans_and_best_ans': 1,
    'avg_repo_question_people_involved': 2,
    'avg_repo_answer_people_involved': 1,
    'people_involved_question': 1,
    'people_involved_answer': -1,
    # 'people_involved_ratio': 3,
    'ans_count': 1
}

index = 0
for data in data_set:
    this_row = []
    this_row.append(data[0])
    score = 0.000
    score += data[6] * weight['is_accepted']
    score += data[5] * weight['thread_has_accepted']
    score += attr[index][0] * weight['answer_vote_count']
    score += attr[index][1] * weight['question_vote_count']
    score += attr[index][2] * weight['people_involved_question']
    score += attr[index][3] * weight['people_involved_answer']
    # score += (attr[2]/attr[3]) * weight['people_involved_ratio']
    score += attr[index][6] * weight['reviewer_repo']
    score += attr[index][7] * weight['avg_repo_question_people_involved']
    score += attr[index][8] * weight['avg_repo_answer_people_involved']
    # score += (data[1]/thread_max_vote_on_answer_count(data[-1])) * weight['ratio_ans_and_best_ans']
    score += (thread_answer_count(data[-1])/max_ans_per_question) * weight['ans_count']
    this_row.append(score)
    this_row.append(data[-1])
    train_data.append(this_row)
    index += 1

train_data.sort(key=lambda x: x[1])


def find_in_train(id):
    index = len(train_data)
    last = -1
    for data in train_data:
        if data[2] == id:
            last = index
        index -= 1
    return last

label_data = []
for i in train_data[-1000:]:
    label_data.append([i[0], 1])
for i in train_data[:500]:
    label_data.append([i[0], 0])

with open('dataset_labelled.pickle', 'wb') as handle:
    pickle.dump(label_data, handle)

import csv
with open("dataset_labelled.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(label_data)