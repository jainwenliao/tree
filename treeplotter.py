import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']#中文显示

#使用matplotlib绘制树形图
#定义决策点、叶节点、和箭头的属性
decision_node = dict(boxstyle = 'sawtooth',fc='0.8')#锯齿形
leaf_node = dict(boxstyle = 'round4',fc = "0.8")#圆形
arrow_args = dict(arrowstyle = '<-')

def plot_node(nodetxt, centerpt,parentpt,nodetype):
    createplot.ax1.annotate(nodetxt,xy=parentpt,xycoords='axes fraction',xytext=centerpt,textcoords='axes fraction',\
        va="center",ha='center',bbox=nodetype,arrowprops=arrow_args)

def createplot(intree):
    fig = plt.figure(1,facecolor = "white")
    fig.clf()#清除图像
    ax_props = dict(xticks=[],yticks=[])
    createplot.ax1 = plt.subplot(111,frameon=False,**ax_props) #frameon是否覆盖下面的层
    #树的叶节点个数，总宽度
    plot_tree.totalW = float(getnumleaf(intree))
    #树的深度，总高度
    plot_tree.totalD = float(get_treedepth(intree))
    #有效范围都是0.0到1.0,plot_tree.totalW是叶子节点的总数，所以1/plot_tree.totalW是相邻两个叶子节点的距离
    plot_tree.xoff = -0.5/plot_tree.totalW#起始根节点的左侧，叶子节点距离一半处的位置
    plot_tree.yoff = 1.0#纵坐标在最上面
    #树根节点位置固定放在（0.5,1.0）位置
    plot_tree(intree,(0.5,1.0),'')
    plt.show()
    
#预先储存树的信息
def retrive_tree(i):
    list_trees = [{'no surfacing':{0: 'no', 1:{'flippers':{0:'no',1:'yes'}}}},
    {'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}
    ]

    return list_trees[i]

#通过计算叶节点的数量确定x的长度，计算树的层数确定y的高度
#定义获取叶节点函数
def getnumleaf(mytree):
    #初始化numleaf
    num_leaf = 0
    first_str =list(mytree.keys())[0]#返回以列表的形式mytree里面所有的键,并取第一个值
    second_dict = mytree[first_str]#获取属性
    for key in second_dict.keys():
        if type(second_dict[key]).__name__=='dict':#判断second_dict是否是字典
            num_leaf += getnumleaf(second_dict[key])#如果是字典类型，递归调用函数
        else:
            num_leaf += 1#如果不是字典类型，叶子节点加1

    return num_leaf

def get_treedepth(mytree):
    max_depth = 0#初始化
    first_str = list(mytree.keys())[0]
    second_dict = mytree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__=='dict':
            this_depth = 1 + get_treedepth(second_dict[key])#如果是字典类型，就继续调用函数，并且深度加1
        else:
            this_depth = 1#如果不是字典类型即最后一层了，深度为1
        #获取树的最大高度
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def plot_midtext(child_point,parent_point,txt_str):
    #在父子节点之间填充文本信息
    x_mid = (parent_point[0] - child_point[0])/2.0 + child_point[0]
    y_mid = (parent_point[1] - child_point[1])/2.0 + child_point[1]
    createplot.ax1.text(x_mid,y_mid,txt_str)

def plot_tree(mytree,parent_point,nodetxt):
    #计算树的宽度
    num_leaf = getnumleaf(mytree)
    #计算树的高度
    depth = get_treedepth(mytree)

    first_str = list(mytree.keys())[0]
    #计算子节点的坐标，取中间值（0.5,1）
    child_point = (plot_tree.xoff + (1.0 + float(num_leaf))/2.0/plot_tree.totalW,plot_tree.yoff)

    plot_midtext(child_point,parent_point,nodetxt)
    plot_node(first_str,child_point,parent_point,decision_node)
    second_dict = mytree[first_str]
    #向下一层，y的值
    plot_tree.yoff = plot_tree.yoff - 1.0/plot_tree.totalD

    for key in second_dict.keys():
        #如果是字典即非叶子节点，则递归调用plot_tree画出叶子节点
        if type(second_dict[key]).__name__=='dict':
            plot_tree(second_dict[key],child_point,str(key))
        #如果是叶子节点，更新x_off,
        else:
            plot_tree.xoff = plot_tree.xoff + 1.0/plot_tree.totalW
            plot_node(second_dict[key],(plot_tree.xoff,plot_tree.yoff),child_point,leaf_node)
            plot_midtext((plot_tree.xoff,plot_tree.yoff),child_point,str(key))

    plot_tree.yoff = plot_tree.yoff + 1.0/plot_tree.totalD    