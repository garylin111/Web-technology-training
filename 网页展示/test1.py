import matplotlib as mpl
import random
mpl.use('Agg')
import matplotlib.pyplot as plt

a=sorted(random.sample(list(range(1,100)),3))
b=sorted(random.sample(list(range(1,100)),3))
print(a,b)
plt.plot(a,b)
# plt.show()
plt.savefig('picture.jpg')