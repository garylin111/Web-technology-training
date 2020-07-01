import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
# 设置matplotlib正常显示中文和负号
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False     

# 生成画布
plt.figure(figsize=(20, 8), dpi=80)
# 横坐标电影名字
movie_name = ['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴','降魔传','追捕','七十七天','密战','狂兽','其它']
# 纵坐标票房
y=[73853,57767,22354,15969,14839,8725,8716,8318,7916,6764,52222]
x=range(len(movie_name))

plt.bar(x,y,width=0.5, color=['b','r','g','y','c','m','y','k','c','g','g'])
plt.xticks(x, movie_name)

plt.savefig('./123.jpg')
plt.show()

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

plt.plot([1,2,3],[5,7,4])
# plt.show()
plt.savefig('picture.jpg')