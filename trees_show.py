import trees
import treeplotter
#mydat,labels = trees.create_dataset()

#print(mydat)
#rint(labels)
#香农熵的计算
#a = trees.shannon_entropy(mydat)
#print(a)
#分离数据集
#b = trees.split_dataset(mydat,0,1)
#print(b)

#信息增益
#c = trees.best_way(mydat)
#print(c)
#myTree = trees.create_tree(mydat,labels)
#print(myTree)
#d = treeplotter.createplot()
#print(d)

#myTree = treeplotter.retrive_tree(0)
#print(myTree)

#print(treeplotter.getnumleaf(myTree))
#print(treeplotter.get_treedepth(myTree))
#print(treeplotter.createplot(myTree))

#print(trees.classify(myTree,labels,[1,1]))

#trees.store_tree(myTree,'classify_storage.txt')
#print(trees.grab_tree('classify_storage.txt'))

#隐形眼镜类型预测

fr = open('lenses.txt')
#将lenses里的字符去掉空格，并以tab分隔开
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
#对应的标签
lenses_labels = ['age','prescript','astigmatic','tearrate']
lenses_tree = trees.create_tree(lenses, lenses_labels)
print(lenses_tree)
print(treeplotter.createplot(lenses_tree))