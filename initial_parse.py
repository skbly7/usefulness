##################################################
############# LIBRARIES AND STUFF ################
##################################################

import os
import cPickle as pickle
import xmltodict
import html2text

if not os.path.isfile('dataset.pickle'):

##################################################
############# LOADING CODEREVIEW DATA ############
##################################################

    if not os.path.isfile('posts.pickle'):
        print "posts.pickle not found, recalculating from xml file..."
        dump_ptr = open('Posts.xml')
        dump_xml = dump_ptr.read()
        posts_dump = xmltodict.parse(dump_xml)['posts']['row']
        with open('posts.pickle', 'wb') as handle:
            pickle.dump(posts_dump, handle)
    else:
        print "posts.pickle found, and loading..."
        with open('posts.pickle', 'rb') as handle:
            posts_dump = pickle.load(handle)

    if not os.path.isfile('user_repo.pickle'):
        print "user_repo.pickle not found, recalculating from xml file..."
        if not os.path.isfile('users.pickle'):
            print "users.pickle not found, recalculating from xml file..."
            dump_ptr = open('Users.xml')
            dump_xml = dump_ptr.read()
            users_dump = xmltodict.parse(dump_xml)['users']['row']
            with open('users.pickle', 'wb') as handle:
                pickle.dump(users_dump, handle)
        else:
            print "users.pickle found, and loading..."
            with open('users.pickle', 'rb') as handle:
                users_dump = pickle.load(handle)

        user_repo = {}
        userId_repo = {}
        for user in users_dump:
            user_repo[user['@DisplayName']] = int(user['@Reputation'])
            userId_repo[user['@Id']] = int(user['@Reputation'])
        del users_dump
        with open('user_repo.pickle', 'wb') as handle:
            pickle.dump([user_repo, userId_repo], handle)
    else:
        print "user_repo.pickle found, and loading..."
        with open('user_repo.pickle', 'rb') as handle:
            user_repo, userId_repo = pickle.load(handle)

    if not os.path.isfile('comments.pickle'):
        print "comments.pickle not found, recalculating from xml file..."
        dump_ptr = open('Comments.xml')
        dump_xml = dump_ptr.read()
        comments_dump = xmltodict.parse(dump_xml)['comments']['row']
        with open('comments.pickle', 'wb') as handle:
            pickle.dump(comments_dump, handle)
    else:
        print "comments.pickle found, and loading..."
        with open('comments.pickle', 'rb') as handle:
            comments_dump = pickle.load(handle)

    ###################################################
    ############# DATA SET CREATION ###################
    ###################################################

    # Adding comments according to postId in dict
    comments = {}
    for var in comments_dump:
        if var['@PostId'] not in comments:
            comments[var['@PostId']] = []
        required_data = []
        try:
            required_data.append(var['@Score'])
            required_data.append(var['@Id'])
            required_data.append(var['@UserId'])
            required_data.append(userId_repo[var['@UserId']])
            comments[var['@PostId']].append(required_data)
        except:
            pass

    del comments_dump

    filtered_question_ids = {}
    for data in posts_dump:
        if data['@PostTypeId'] == '1':
            if data['@Tags'].find("python") > -1:
                filtered_question_ids[data['@Id']] = []
                filtered_question_ids[data['@Id']].append(int(data['@Score']))
                try:
                    filtered_question_ids[data['@Id']].append(int(data['@AcceptedAnswerId']))
                except KeyError:
                    filtered_question_ids[data['@Id']].append(-1)

    answer_user_involvement = {}
    answer_avg_rating_involvement = {}
    question_user_involvement = {}
    question_avg_rating_involvement = {}

    for data in posts_dump:
        if data['@PostTypeId'] == '2':
            try:
                comments_this = comments[data['@Id']]
            except KeyError:
                comments_this = []
            users_map = {}
            try:
                users_map[data['@OwnerUserId']] = userId_repo[data['@OwnerUserId']]
            except KeyError:
                try:
                    users_map[data['@OwnerDisplayName']] = user_repo[data['@OwnerDisplayName']]
                except KeyError:
                    # Rare case, but true :(
                    users_map[-1] = 0
            for comment in comments_this:
                users_map[comment[2]] = userId_repo[comment[2]]
            answer_user_involvement[data['@Id']] = len(users_map)
            answer_avg_rating_involvement[data['@Id']] = sum(users_map.values()) / len(users_map)
            try:
                question_user_involvement[data['@ParentId']].update(users_map)
            except KeyError:
                question_user_involvement[data['@ParentId']] = users_map

    for questionId in question_user_involvement:
        question_avg_rating_involvement[questionId] = sum(question_user_involvement[questionId].values()) / len(question_user_involvement[questionId])

    del comments

    data_set = []
    for data in posts_dump:
        if data['@PostTypeId'] == '2':
            if data['@ParentId'] in filtered_question_ids:
                required_data = []
                required_data.append(html2text.html2text(data['@Body']).encode('utf-8'))
                required_data.append(int(data['@Score']))
                # Score of question
                required_data.append(filtered_question_ids[data['@ParentId']][0])
                required_data.append(len(question_user_involvement[data['@ParentId']]))
                # User involved in answer
                try:
                    required_data.append(len(answer_user_involvement['@Id']))
                except KeyError:
                    required_data.append(1)
                # is_accepted
                if filtered_question_ids[data['@ParentId']][1] == -1:
                    required_data.append(0)
                    required_data.append(0)
                else:
                    required_data.append(1)
                    if filtered_question_ids[data['@ParentId']][1] == int(data['@Id']):
                        required_data.append(1)
                    else:
                        required_data.append(0)
                self_repo = 0
                try:
                    self_repo = int(userId_repo[data['@OwnerUserId']])
                except KeyError:
                    try:
                        self_repo = int(user_repo[data['@OwnerDisplayName']])
                    except KeyError:
                        # Rare case, but true :(
                        self_repo = 0
                required_data.append(self_repo)
                required_data.append(question_avg_rating_involvement[data['@ParentId']])
                try:
                    required_data.append(answer_avg_rating_involvement[data['@Id']])
                except:
                    required_data.append(self_repo)
                required_data.append(int(data['@ParentId']))
                data_set.append(required_data)

    with open('dataset.pickle', 'wb') as handle:
            pickle.dump(data_set, handle)

else:
    with open('dataset.pickle', 'rb') as handle:
        data_set = pickle.load(handle)

print len(data_set), ' generated..'


if not os.path.isfile('comment_android.pickle'):
    print "comment_android.pickle not found, recalculating from xml file..."
    dump_ptr = open('comment_android.xml')
    dump_xml = dump_ptr.read()
    cc_android_dump = xmltodict.parse(dump_xml)['table']['row']
    cc_android_dump_ = []
    for comment in cc_android_dump:
        cc_android_dump_.append(comment['Message'])
    with open('comment_android.pickle', 'wb') as handle:
        pickle.dump(cc_android_dump_, handle)
else:
    print "comment_android.pickle found, and loading..."
    with open('comment_android.pickle', 'rb') as handle:
    cc_android_dump_ = pickle.load(handle)