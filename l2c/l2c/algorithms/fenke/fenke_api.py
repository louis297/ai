# -*- coding:utf-8 -*-
from gensim.models import word2vec
from gensim import models
import gensim
import logging
import jieba
import re

# 导入自定义词典
jieba.load_userdict("algorithms/fenke/dict.txt")
# read original file to analysis
# 不处理的词
fr = open('algorithms/fenke/stopwords.txt', 'r')
tmpstr = ""
for ln in fr:
    if tmpstr == "":
        tmpstr = ln.strip("\n")
    else:
        tmpstr = tmpstr + "," + ln.strip("\n")
stopwords = tmpstr.split(sep=",")
# stopwords = {}.fromkeys(['哪些','怎么','多少','呢','的', '包括', '医生', '是', '等', '了', '也', '啊', '！', '吗', '，', '。', '：', '、', '？', ':'])
# 表示单位的词
unitwords = {}.fromkeys(['岁', '年', '月', '日', '号', '周', '星期', '天', '度', '米', '分', '次', '个', 'mg', 'mm'])

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# model_skin = models.Word2Vec.load_word2vec_format('med20170208.model_skin.txt',binary=False)
# model_other = models.Word2Vec.load_word2vec_format('med20170208.model_other.txt',binary=False)
# model_other = models.Word2Vec.load_word2vec_format('med20170316_shilu.model',binary=True)
model_other = gensim.models.KeyedVectors.load_word2vec_format('algorithms/fenke/med20170407_shilu.model', binary=True)

# 分类名称
fr = open('algorithms/fenke/keshi_cate.txt', 'r')
tmpstr = ""
for ln in fr:
    if tmpstr == "":
        tmpstr = ln.strip("\n")
    else:
        tmpstr = tmpstr + "|" + ln.strip("\n")
catename = tmpstr.split(
    sep="|")  # {}.fromkeys(["外科","骨科","精神科","皮肤科","耳鼻喉科","外科","风湿科","儿科","内科","神经内科","泌尿科","风湿科","肿瘤科","胰腺炎"])
dic = dict.fromkeys(catename, 0)


# api version interface
def fenke_api(input_words):
    try:
        for x in dic.keys():
            dic[x] = 0

        query = re.sub("\d", "", input_words)
        thecatename = ""
        theval = 0
        words1 = jieba.cut(query, cut_all=False)
        tmpi = 0

        tmpstr = ''.rjust(15, ' ')
        for lst in words1:
            if ((lst not in stopwords) and (lst.strip() != "")):
                tmpstr = tmpstr + "  " + lst  # [0:3]
            else:
                tmpstr = tmpstr
        # tmpstr=tmpstr+"\t合计"
        # print(tmpstr)

        for cate in catename:
            catelist = cate.split(sep=",")
            words = jieba.cut(query, cut_all=False)
            tmpval = 0
            tmpstr = cate.rjust(15, "　")
            res = 0
            for word in words:
                if ((word not in stopwords) and (word.strip() != "")):
                    # 不在停用词中，且不为空，则计算与该类的相似度
                    try:
                        res = abs(model_other.similarity(catelist[2], word))
                        dic[cate] = dic[cate] + res
                        tmpval = tmpval + res
                        tmpstr = tmpstr + "\t" + str(round(res, 2)) + "　"
                    except Exception as err:
                        tmpval = tmpval + 0

            mstr = str(round(tmpval, 3))
            # print(tmpstr+"\t"+mstr)
            # 判断科室
            if abs(theval) < abs(tmpval):
                theval = tmpval
                thecatename = cate
            # 显示科室的相关性
            # print("科室："+cate+"，相关性："+str(tmpval))
        # 显示最可能的科室
        icnt = 0
        mylist = sorted(dic.items(), reverse=True, key=lambda d: d[1])
        for x in mylist:  # dict.keys():
            mycatelist = x[0].split(sep=",")
            icnt = icnt + 1
            if icnt > 10:
                break
            # else:
            # print(mycatelist[0].rjust(4,"　"),"-->",mycatelist[1].rjust(6,"　"),"-->",mycatelist[2].rjust(7,"　"),"：",x[1])
            # print(x.rjust(10,"　"),"：",dict[x])
        # return "分诊科室：" + thecatename + str(theval)
        return "分诊科室：" + thecatename
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    while True:
        print('请输入症状：')
        input_words = input().strip()
        if not input_words:
            break
        ret = fenke_api(input_words=input_words)
        print(ret, '\n')
