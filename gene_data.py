import numpy as np


def sigmf(x, a, c):
    y = 1 / (1 + np.exp(a * (x - a * c)))
    return y


def forward(sleep_c, study_c, ramdom_ratio, index):
    rand = np.random.rand(num_student)
    keep_sleep_ratio = sigmf(interval_time * student_fea[:, 1, index - 1], attr, sleep_c)
    if np.random.rand() < ramdom_ratio:
        sleep_radom = np.random.choice(num_student, int(ramdom_ratio * num_student / 10), replace=False)
        keep_sleep_ratio[sleep_radom] = 0.5
    keep_study_ratio = sigmf(interval_time * student_fea[:, 1, index - 1], attr, study_c)
    if np.random.rand() < ramdom_ratio:
        study_radom = np.random.choice(num_student, int(ramdom_ratio * num_student / 10), replace=False)
        keep_study_ratio[study_radom] = 0.5
    student_fea[student_fea[:, 0, index - 1] == 0, 0, index] = (rand > keep_sleep_ratio).astype(int)[student_fea[:, 0, index - 1] == 0]
    student_fea[student_fea[:, 0, index - 1] == 1, 0, index] = (rand < keep_study_ratio).astype(int)[student_fea[:, 0, index - 1] == 1]
    student_fea[:, 1, index] = 0
    index_keep = student_fea[:, 0, index] == student_fea[:, 0, index - 1]
    student_fea[index_keep, 1, index] = student_fea[index_keep, 1, index - 1] + 1


if __name__ == '__main__':
    # initialize params
    day = 2
    num_student = 720
    interval = 1
    interval_time = 1 / interval
    length = interval * 1440 * day + 1
    day0 = 1440 * interval
    student_fea = np.zeros((num_student, 3, length + interval * 1440))
    student_fea[:, 1, day0 - 1] = 30 * interval

    # generate normal random_data until all data in range [0,1]
    attr = np.random.normal(loc=0.6, scale=0.3, size=num_student)
    range_out = num_student - ((attr > 0.1) & (attr < 1)).astype(int).sum()
    while range_out > 0:
        res = np.random.normal(loc=0.6, scale=0.3, size=range_out)
        attr = np.append(attr[(attr > 0.1) & (attr < 1)], res)
        range_out = num_student - ((attr > 0.1) & (attr < 1)).astype(int).sum()

    # set variable value for sigmf function according to different times of each day
    for i, time in enumerate(np.linspace(0, day * 1440, length)):
        index = day0 + i
        if (time % 1440) // 60 < 7:
            forward(900, 50, 0.002, index)
        elif (time % 1440) // 60 < 11:
            forward(150, 300, 0.05, index)
        elif (time % 1440) // 60 < 14:
            forward(300, 300, 0.02, index)
        elif (time % 1440) // 60 < 17:
            forward(150, 300, 0.05, index)
        elif (time % 1440) // 60 < 19:
            forward(200, 400, 0.05, index)
        elif (time % 1440) // 60 < 22:
            forward(100, 400, 0.05, index)
        elif (time % 1440) // 60 < 24:
            forward(900, 300, 0.02, index)

        # compute the total study time in each day
        if time % 1440 < 1e-5:
            student_fea[:, 2, index] = 0
        else:
            student_fea[student_fea[:, 0, index] == 0, 2, index] = student_fea[
                student_fea[:, 0, index] == 0, 2, index - 1]
            student_fea[student_fea[:, 0, index] == 1, 2, index] = student_fea[student_fea[:, 0, index] == 1, 2, index - 1] + interval_time

    # save simulation data
    # student_fea[:, :2, :].astype('int16').tofile(r'resource\student_fea.bin')
    student_fea[:, -1, interval * 1440:].astype('float32').tofile(r'resource\time_statis.bin')
