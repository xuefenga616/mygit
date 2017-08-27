import random

file = open("/tmp/datas", "w")

for index in xrange(0, 10000):
    file.write("col1_" + str(random.randint(1, 100)) + "\tcol1_" +
               str(random.randint(1, 100)) + "\tcol1_" + str(random.randint(1, 100)) + "\n")

file.close()
