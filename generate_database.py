import numpy as np
from datetime import date
import time

num_student = 1000
num_profile = 20
interval_time = 1
time_statis = np.fromfile(r'resource\time_statis.bin', dtype=np.float32).reshape(num_student, -1)
with open(r'resource\nickname_2300.txt') as file:
    content = file.read()

nicknames = np.array(content.split('\n'))
# nicknames = content.split('\n')
student_names = nicknames[np.random.choice(len(nicknames), num_student, replace=False)]

start_data = date(2022, 7, 14)
timeArray = time.strptime(str(start_data), "%Y-%m-%d")
ret = int(time.mktime(timeArray))

with open(r'resource\database.txt', "w") as file:
    for i, student_name in enumerate(student_names):
        for j in range(time_statis.shape[-1]):
            timeArray = time.localtime(ret + 60 * j)
            str_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            accum_time = str(int(time_statis[i, j]))
            line = '(\'' + student_name + '\',' + str(1 + np.random.randint(num_profile)) + ',\'' + str_time + '\',' + accum_time + '),\n'
            file.writelines(line)
