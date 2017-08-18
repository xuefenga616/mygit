import tensorflow as tf
import numpy as np

# a = tf.random_normal((100, 100))
# b = tf.random_normal((100, 500))
# c = tf.matmul(a, b)
# sess = tf.InteractiveSession()
# print(sess.run(c))

import matplotlib.pyplot as plt

x = np.arange(0., np.e, 0.01)
y1 = np.exp(-x)
y2 = np.log(x)

fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.plot(x, y1, "b", label="Training score")
ax1.set_ylabel('Score')
ax1.set_title("Learning Curves (Tensorflow )")

ax2 = ax1.twinx()  # this is the important function
ax2.plot(x, y2, 'r', label="Cross-validation score")
ax2.set_xlim([0, np.e])

plt.legend(loc="best")
plt.show()