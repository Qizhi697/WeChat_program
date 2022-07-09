import numpy as np
import plotly.graph_objects as go

num_student = 1000
N = 30
time_statis = np.fromfile('time_statis.bin', dtype=np.float32).reshape(num_student, -1)
student_selected = np.random.choice(num_student, N, replace=False)
random_x = np.linspace(0, 14400 * 6, 14400 * 6 + 1)/360

fig = go.Figure()
# Add traces
for i in range(N):
    fig.add_trace(go.Scatter(x=random_x, y=time_statis[student_selected[i], 1440 * 6:]))
fig.show()
