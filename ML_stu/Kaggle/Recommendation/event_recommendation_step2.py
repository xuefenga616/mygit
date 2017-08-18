#coding:utf-8
import pickle
import numpy as np
import scipy.io as sio
from matplotlib import pyplot
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

class DataRewrite(object):
    def __init__(self):
        # 读入数据做初始化
        self.userIndex = pickle.load(open("PE_userIndex.pkl", "rb"))
        self.eventIndex = pickle.load(open("PE_eventIndex.pkl", "rb"))
        self.userEventScores = sio.mmread("PE_userEventScores").todense()
        self.userSimMatrix = sio.mmread("US_userSimMatrix").todense()
        self.eventPropSim = sio.mmread("EV_eventPropSim").todense()
        # self.eventContSim = sio.mmread("EV_eventContSim").todense()
        self.numFriends = sio.mmread("UF_numFriends")
        self.userFriends = sio.mmread("UF_userFriends").todense()
        self.eventPopularity = sio.mmread("EA_eventPopularity").todense()

    def plotCurve(self):
        fig = pyplot.figure()
        ax1 = fig.add_subplot(121)
        cmap = mpl.cm.cool
        pyplot.title("User-based")
        pyplot.xlabel("user")
        # pyplot.ylabel("user")
        ax1.imshow(self.userSimMatrix, cmap=cmap)

        ax2 = fig.add_subplot(122)
        cmap = mpl.cm.cool
        pyplot.title("Item-based")
        pyplot.xlabel("event")
        # pyplot.ylabel("event")
        ax2.imshow(self.eventPropSim[:1000,:1000], cmap=cmap)

        pyplot.show()

    def userReco(self, userId, eventId):
        # 根据User-based协同过滤，得到event的推荐度
        i = self.userIndex[userId]
        j = self.eventIndex[eventId]
        vs = self.userEventScores[:, j]
        sims = self.userSimMatrix[i, :] # 用户间相似度
        prod = sims * vs
        try:
            return prod[0, 0] - self.userEventScores[i, j]
        except:
            return 0

    def eventReco(self, userId, eventId):
        # 基于item-based协同过滤，得到Event的推荐度
        i = self.userIndex[userId]
        j = self.eventIndex[eventId]
        js = self.userEventScores[i, :]
        psim = self.eventPropSim[:, j]  # event相似度
        pprod = js * psim

        pscore = 0
        try:
            pscore = pprod[0, 0] - self.userEventScores[i, j]
        except:
            pass
        return pscore

    def userPop(self, userId):
        # 基于用户的朋友个数来推断用户的社交程度
        if userId in self.userIndex.keys():
            i = self.userIndex[userId]
            try:
                return self.numFriends[0, i]
            except:
                return 0
        else:
            return 0

    def friendInfluence(self, userId):
        # 朋友对用户的影响，主要考虑用户所有的朋友中有多少是非常喜欢参加各种event的
        nusers = np.shape(self.userFriends)[1]
        i = self.userIndex[userId]
        return (self.userFriends[i, :].sum(axis=0) / nusers)[0, 0]

    def eventPop(self, eventId):
        # 活动本身的热度，主要是通过参与的人数来界定
        i = self.eventIndex[eventId]
        return self.eventPopularity[i, 0]

    def rewriteData(self, start=1, train=True, header=True):
        # 把前面user-based和item-based协同过滤，以及各种影响度作为特征组合在一起
        fn = r"D:\kaggle_data\event_recommendation\train.csv" if train else r"D:\kaggle_data\event_recommendation\test.csv"
        fin = open(fn, "r")

        fn1 = "train.csv" if train else "test.csv"
        fout = open("data_"+fn1, "w")
        # 写入表头
        if header:
            ocolNames = ["invited", "user_reco", "evt_p_reco", "user_pop", "frnd_inf1", "evt_pop"]
            if train:
                ocolNames.append("interested")
                ocolNames.append("not_interested")
            fout.write(",".join(ocolNames) + "\n")

        ln = 0
        for line in fin:
            ln += 1
            if ln < start:
                continue
            cols = line.strip().split(",")
            userId = cols[0]
            eventId = cols[1]
            invited = cols[2]
            if ln % 500 == 0:
                print('%s:%d (userId, eventId)=(%s, %s)' %(fn, ln, userId, eventId))
            user_reco = self.userReco(userId, eventId)
            evt_p_reco = self.eventReco(userId, eventId)
            user_pop = self.userPop(userId)
            frnd_inf1 = self.friendInfluence(userId)
            evt_pop = self.eventPop(eventId)
            ocols = [invited, user_reco, evt_p_reco, user_pop, frnd_inf1, evt_pop]
            if train:
                ocols.append(cols[4])   # interested
                ocols.append(cols[5])   # not_interested
            fout.write(",".join(map(lambda x:str(x), ocols)) + "\n")
        fin.close()
        fout.close()

    def rewriteTrainingSet(self):
        self.rewriteData(True)

    def rewriteTestSet(self):
        self.rewriteData(False)

if __name__ == "__main__":
    dr = DataRewrite()
    dr.plotCurve()
    # dr.rewriteData(train=True, start=2, header=True)
    # dr.rewriteData(train=False, start=2, header=True)

