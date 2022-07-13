import numpy as np
from datetime import date
import time
import yaml

num_student = 720
num_profile = 20
interval_time = 1
time_statis = np.fromfile(r'resource\time_statis.bin', dtype=np.float32).reshape(num_student, -1)
with open(r'resource\nickname_2300.txt') as file:
    content = file.read()

nicknames = np.array(content.split('\n'))
student_names = nicknames[np.random.choice(len(nicknames), num_student, replace=False)]

colleges = yaml.safe_load(open(r'resource\colleges.yaml', 'r', encoding='utf-8'))["colleges"]
num_college = len(colleges)

start_data = date(2022, 7, 14)
timeArray = time.strptime(str(start_data), "%Y-%m-%d")
ret = int(time.mktime(timeArray))
student_shuffle = np.arange(num_student)
np.random.shuffle(student_shuffle)
with open(r'resource\database.txt', "w") as file:
    for i, student_name in enumerate(student_names):
        profile = np.random.randint(num_profile)
        college = colleges[student_shuffle[i]//5]
        for j in range(time_statis.shape[-1]):
            timeArray = time.localtime(ret + 60 * j)
            str_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            accum_time = str(int(time_statis[i, j]))
            line = '(\'' + student_name + '\',' + str(profile) + ',' + college + ',\'' + str_time + '\',' + accum_time + '),\n'
            file.writelines(line)
