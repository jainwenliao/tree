from math import log
import operator


def create_dataset():
    dataset = ([[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']])
    #混合数据越多，熵越大
    #dataset = ([[1,1,'maybe'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']])
    labels = ['no surfacing','flippers']
    return dataset, labels


#计算给定数据的香农熵
def shannon_entropy(dataset):
    #熵的长度
    num_entries = len(dataset)
    #初始化标签数
    label_counts = {}

    for feature_vector in dataset:
        #创建一个数据字典，键值等于最后一列的数值
        current_lable = feature_vector[-1]
        #遍历labels_counts字典中所有的键,如果不是字典里的标记为0次
        if current_lable not in label_counts.keys():
            label_counts[current_lable] = 0
        #记录当前类别出现的次数
        label_counts[current_lable] += 1
    #初始化香农熵
    shan_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key])/num_entries
        shan_ent -= prob * log(prob,2)

    return shan_ent


#分离数据集
def split_dataset(dataset,axis,value):
    #创建一个新的数据集
    new_dataset =[]
    #抽取数据
    for feature_vector in dataset:
        if feature_vector[axis] == value:
            #将符合axis==value的行中除了axis列的其他数据加到new_dataset中
            #例如axis=0,value=1例子中的，第一列中为1的行除去第一列后加到new_dataset里。
            reduced_vector = feature_vector[:axis]
            reduced_vector.extend(feature_vector[axis+1:])
            new_dataset.append(reduced_vector)
    return new_dataset
   

#找出最好的数据划分方式
def best_way(dataset):
    num_features = len(dataset[0])-1#获取数据的长度，最后一列是label所有-1
    #计算分类前的香农熵
    base_entropy = shannon_entropy(dataset)

    best_info_gain = 0.0#要选择最高的信息增益
    best_feature = -1#最好特征的索引，-1表示不存在还没开始

    for i in range(num_features):
        feature_list = [example[i] for example in dataset]#将数据库中所有的值都提取出来
        unique_vals = set(feature_list) #第i列属性的取值数集合
        new_entropy = 0.0
        for value in unique_vals:#求第i列属性每个不同值的熵
            sub_dataset = split_dataset(dataset,i,value)#按第i列来划分子数据集
            prob = len(sub_dataset)/float(len(dataset)) #子数据集的概率
            new_entropy += prob*shannon_entropy(sub_dataset)#所有子数据集的香农熵和

        info_gain = base_entropy-new_entropy#信息增益，分类前-分类后

        if(info_gain > best_info_gain):#保存信息增益最大的值以及所在的列值
            best_info_gain = info_gain
            best_feature += 1
    return best_feature#选择信息增益最大的作为最好的划分选择

#找出出现次数出现最多的分类标签
def majority_count(self,class_list):
    class_count = {}

    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0

    class_count[vote] += 1
    #将字典迭代化，按照迭代化后的每个数据项的第二列为排序依据，逆序（从大到小）
    sorted_class_count = sorted(class_count.interitems(), key = operator.itemgetter(1),reverse=True)
    return sorted_class_count[0][0]#返回最大值


#创建数的函数代码
def create_tree(dataset,labels):
    class_list = [example[-1] for example in dataset]#获取最后一列，即label列表
    #如果class_list中的label都一样，则返回class_list[0]
    #就是说class_list里面第一个label出现的次数等于class_list的长度
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    #如果只出现一次，返回出现次数最多的lable
    if len(class_list[0]) == 1:
        return majority_count(class_list)
        
    bestfeat = best_way(dataset)#最好的数据划分
    bestfeatlabel = labels[bestfeat]#根据下标找属性名称，作为树的根节点
    #以bestfeatlabel为根节点创建一个空树
    my_tree = {bestfeatlabel:{}}
    #删掉已经选择的label
    del(labels[bestfeat])
    #将bestfeat对应的数据从dataset中提取出来，并创建一个无重复值的列表
    feat_values = [example[bestfeat] for example in dataset]
    unique_vals = set(feat_values)

    for value in feat_values:
        sublabels = labels[:]
        my_tree[bestfeatlabel][value] =create_tree(split_dataset(dataset,bestfeat,value),sublabels)

    return my_tree

#使用决策树的分类函数
def classify(input_tree,feature_labels,test_vector):
    #找到树的第一个分类特征
    first_str = list(input_tree.keys())[0]
    #从树中得到该特征的分支
    second_dict = input_tree[first_str]
    feature_index = feature_labels.index(first_str)
    #遍历分类特征的所有取值
    for key in second_dict.keys():
        if test_vector[feature_index] == key:
            if type(second_dict[key]).__name__ == "dict":
                class_label = classify(second_dict[key],feature_labels,test_vector)
            else:
                class_label = second_dict[key]
    return class_label
            

#使用pickle模块存储决策树
#将数序列化为二进制
def store_tree(input_tree,filename):
    import pickle
    fw = open(filename,'wb')
    #序列化
    pickle.dump(input_tree,fw)
    fw.close()
#获取树，反序列化
def grab_tree(filename):
    import pickle
    fr = open(filename,"rb+")
    return pickle.load(fr)