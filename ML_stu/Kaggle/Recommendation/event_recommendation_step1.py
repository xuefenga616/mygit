#coding:utf-8
import itertools
import pickle
import datetime
import hashlib
import locale
import numpy as np
import pycountry
import scipy.io as sio
from scipy import sparse    # 稀疏矩阵
from scipy.spatial import distance as ssd
from collections import defaultdict
from sklearn.preprocessing import normalize

# jupyter notebook

# 处理user和event关联数据，只关心train和test中出现的user和event
class ProgramEntities():
    def __init__(self):
        uniqueUsers = set()
        uniqueEvents = set()
        eventsForUser = defaultdict(set)
        usersForEvent = defaultdict(set)
        for filename in [r"D:\kaggle_data\event_recommendation\train.csv", r"D:\kaggle_data\event_recommendation\test.csv"]:
            f = open(filename, 'r')
            for line in f.readlines()[1:]:
                cols = line.strip().split(",")
                uniqueUsers.add(cols[0])
                uniqueEvents.add(cols[1])
                eventsForUser[cols[0]].add(cols[1])
                usersForEvent[cols[1]].add(cols[0])
            f.close()
        self.userEventScores = sparse.dok_matrix((len(uniqueUsers), len(uniqueEvents)))
        self.userIndex = dict()
        self.eventIndex = dict()
        for i,u in enumerate(uniqueUsers):  # 枚举
            self.userIndex[u] = i
        for i,e in enumerate(uniqueEvents):
            self.eventIndex[e] = i
        # print(self.userIndex)
        # print(self.eventIndex)

        ftrain = open(r"D:\kaggle_data\event_recommendation\train.csv", 'r')
        for line in ftrain.readlines()[1:]:
            cols = line.strip().split(",")
            i = self.userIndex.get(cols[0])
            j = self.eventIndex.get(cols[1])
            self.userEventScores[i,j] = int(cols[4]) - int(cols[5])
        ftrain.close()
        # print(len(userEventScores))
        # 保存下来
        # sio.mmwrite("PE_userEventScores", userEventScores)

        # 再把所有关联的user和event找出来，并保存
        # 关联用户，指的是在同一个event上有行为的用户pair（两两组合）
        # 关联event，指的是在同一个user有行为的event pair
        self.uniqueUserPairs = set()
        self.uniqueEventPairs = set()
        for event in uniqueEvents:
            users = usersForEvent[event]
            if len(users) > 2:
                self.uniqueUserPairs.update(itertools.combinations(users, 2))    # 把1个list中所有元素两两组合
        for user in uniqueUsers:
            events = eventsForUser[user]
            if len(events) > 2:
                self.uniqueEventPairs.update(itertools.combinations(events, 2))
        # pickle.dump(userIndex, open("PE_userIndex.pkl", 'wb'))
        # pickle.dump(eventIndex, open("PE_eventIndex.pkl", 'wb'))


# 数据清洗
class DataCleaner(object):
    def __init__(self):
        # 载入locale包
        self.localeIdMap = defaultdict(int)     # value类型是int
        for i,l in enumerate(locale.locale_alias.keys()):
            self.localeIdMap[l] = i + 1

        # 载入country
        self.countryIdMap = defaultdict(int)
        ctryIdx = defaultdict(int)
        for i,c in enumerate(pycountry.countries):
            self.countryIdMap[c.name.lower()] = i + 1
            if c.name.lower() == "usa":
                ctryIdx["US"] = i
            elif c.name.lower() == "canada":
                ctryIdx["CA"] = i
        for cc in ctryIdx.keys():
            for s in pycountry.subdivisions.get(country_code=cc):
                self.countryIdMap[s.name.lower()] = ctryIdx[cc] + 1

        # gender id
        self.genderIdMap = defaultdict(int, {"male": 1, "female": 2})

    def getLocaleId(self, loc_str):
        return self.localeIdMap[loc_str.lower()]

    def getGenderId(self, gender_str):
        return self.genderIdMap[gender_str]

    def getJoinedYearMonth(self, date_str):
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return "".join([str(dt.year), str(dt.month)])

    def getCountryId(self, location):
        if (isinstance(location,str) and len(location.strip())>0 and location.rfind("  ")>-1):
            return self.countryIdMap[location[location.rindex("  ")+2: ].lower()]
        else:
            return 0

    def getBirthYearInt(self, birthYear):
        try:
            return 0 if birthYear is None else int(birthYear)
        except:
            return 0

    def getTimezoneInt(self, timezone):
        try:
            return int(timezone)
        except:
            return 0

    def getFeatureHash(self, value):
        if len(value.strip()) == 0:
            return -1
        else:
            return int(hashlib.sha224(value.encode("utf8")).hexdigest()[0:4], 16)

    def getFloatValue(self, value):
        if len(value.strip()) == 0:
            return 0.0
        else:
            return float(value)


# 用户与用户相似度矩阵
def Users():
    pr = ProgramEntities()
    nusers = len(pr.userIndex)
    sim = ssd.correlation

    cleaner = DataCleaner()
    fin = open(r"D:\kaggle_data\event_recommendation\users.csv", 'r')
    colnames = fin.readline().strip().split(",")
    userMatrix = sparse.dok_matrix((nusers, len(colnames)-1))   # 稀疏矩阵
    for line in fin:
        cols = line.strip().split(",")
        # 只考虑train.csv中出现的用户
        if cols[0] in pr.userIndex.keys():
            i = pr.userIndex[cols[0]]
            userMatrix[i, 0] = cleaner.getLocaleId(cols[1])
            userMatrix[i, 1] = cleaner.getBirthYearInt(cols[2])
            userMatrix[i, 2] = cleaner.getGenderId(cols[3])
            userMatrix[i, 3] = cleaner.getJoinedYearMonth(cols[4])
            userMatrix[i, 4] = cleaner.getCountryId(cols[5])
            userMatrix[i, 5] = cleaner.getTimezoneInt(cols[6])
    fin.close()
    # print(userMatrix)

    # 归一化用户矩阵，并存起来
    userMatrix_N = normalize(userMatrix, norm='l1', axis=0)     # axis=0 沿着列归一化
    # sio.mmwrite("US_userMatrix", userMatrix_N)
    # 生成一个用户相似度矩阵
    userSimMatrix = sparse.dok_matrix((nusers, nusers))
    for i in range(nusers):
        userSimMatrix[i, i] = 1.0
    for u1,u2 in pr.uniqueUserPairs:
        i = pr.userIndex[u1]
        j = pr.userIndex[u2]
        if (i not in userSimMatrix.keys() and j not in userSimMatrix.keys()):
            usim = sim(userMatrix_N.getrow(i).todense(), userMatrix_N.getrow(j).todense())
            userSimMatrix[i, j] = usim
            userSimMatrix[j, i] = usim
    sio.mmwrite("US_userSimMatrix", userSimMatrix)

# 用户社交关系挖掘
def UserFriends():
    # 找出某用户的那些朋友
    pr = ProgramEntities()
    nusers = len(pr.userIndex)
    numFriends = np.zeros((nusers))
    userFriends = sparse.dok_matrix((nusers, nusers))

    fin = open(r"D:\kaggle_data\event_recommendation\user_friends.csv", 'r')
    ln = 0
    for line in fin.readlines()[1:]:
        # print(line)
        if ln % 200 == 0:
            print("Loading line: ", ln)
        cols = line.strip().split(",")
        user = cols[0]
        if user in pr.userIndex.keys():
            friends = cols[1].split(" ")
            i = pr.userIndex[user]
            numFriends[i] = len(friends)
            for friend in friends:
                if friend in pr.userIndex.keys():
                    j = pr.userIndex[friend]
                    eventsForUser = pr.userEventScores.getrow(j).todense()  # todense()恢复
                    score = eventsForUser.sum() / np.shape(eventsForUser)[1]
                    userFriends[i, j] += score
                    userFriends[j, i] += score
        ln += 1
    fin.close()

    # 归一化矩阵
    sumNumFriends = numFriends.sum(axis=0)
    numFriends = numFriends / sumNumFriends
    sio.mmwrite("UF_numFriends", np.matrix(numFriends))
    userFriends = normalize(userFriends, norm="l1", axis=0)
    sio.mmwrite("UF_userFriends", userFriends)

# 构造event和event相似度数据
def Events():
    cleaner = DataCleaner()
    pr = ProgramEntities()
    psim = ssd.correlation
    csim = ssd.cosine

    fin = open(r"D:\kaggle_data\event_recommendation\events.csv", 'r')
    nevents = len(pr.eventIndex)
    eventPropMatrix = sparse.dok_matrix((nevents, 7))
    eventContMatrix = sparse.dok_matrix((nevents, 100))
    ln = 0
    for line in fin.readlines()[1:10]:
        cols = line.strip().split(",")
        eventId = cols[0]
        if eventId in pr.eventIndex.keys():
            i = pr.eventIndex[eventId]
            eventPropMatrix[i, 0] = cleaner.getJoinedYearMonth(cols[2]) # start_time
            eventPropMatrix[i, 1] = cleaner.getFeatureHash(cols[3]) # city
            eventPropMatrix[i, 2] = cleaner.getFeatureHash(cols[4]) # state
            eventPropMatrix[i, 3] = cleaner.getFeatureHash(cols[5]) # zip
            eventPropMatrix[i, 4] = cleaner.getFeatureHash(cols[6]) # country
            eventPropMatrix[i, 5] = cleaner.getFloatValue(cols[7]) # lat
            eventPropMatrix[i, 6] = cleaner.getFloatValue(cols[8]) # lon
            for j in range(9, 109):
                eventContMatrix[i, j-9] = cols[j]
            ln += 1
    fin.close()

    # 归一化
    eventPropMatrix = normalize(eventPropMatrix, norm="l1", axis=0)
    # sio.mmwrite("EV_eventPropMatrix", eventPropMatrix)
    eventContMatrix = normalize(eventContMatrix, norm="l1", axis=0)
    # sio.mmwrite("EV_eventContMatrix", eventContMatrix)

    # 计算event pairs相关性
    eventPropSim = sparse.dok_matrix((nevents, nevents))
    eventContSim = sparse.dok_matrix((nevents, nevents))
    for e1,e2 in pr.uniqueEventPairs:
        i = pr.eventIndex[e1]
        j = pr.eventIndex[e2]
        if (i not in eventPropSim.keys() and j not in eventPropSim.keys()):
            epsim = psim(eventPropMatrix.getrow(i).todense(), eventPropMatrix.getrow(j).todense())
            eventPropSim[i, j] = epsim
            eventPropSim[j, i] = epsim
        if (i not in eventContSim.keys() and j not in eventContSim.keys()):
            ecsim = csim(eventContMatrix.getrow(i).todense(), eventContMatrix.getrow(j).todense())
            eventContSim[i, j] = ecsim
            eventContSim[j, i] = ecsim
    sio.mmwrite("EV_eventPropSim", eventPropSim)
    sio.mmwrite("EV_eventContSim", eventContSim)

# 活跃度/event热度数据
def EventAttendees():
    # 统计某个活动，参加和不参加的人数，从而为活动活跃度做准备
    pr = ProgramEntities()
    nevents = len(pr.eventIndex)
    eventPopularity = sparse.dok_matrix((nevents,1))

    f = open(r"D:\kaggle_data\event_recommendation\event_attendees.csv", "r")
    for line in f.readlines()[1:]:
        cols = line.strip().split(",")
        eventId = cols[0]
        if eventId in pr.eventIndex.keys():
            i = pr.eventIndex[eventId]
            eventPopularity[i, 0] = len(cols[1].split(" ")) - len(cols[4].split(" "))
    f.close()
    eventPopularity = normalize(eventPopularity, norm="l1", axis=0)
    sio.mmwrite("EA_eventPopularity", eventPopularity)

def data_prepare():
    ProgramEntities()
    # Users()
    # UserFriends()
    # Events()
    # EventAttendees()


if __name__ == "__main__":
    # data_prepare()
    pass