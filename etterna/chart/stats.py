import numpy as np
from .chart import Chart

def summary(c: Chart):
    c = c.numpy()
    column_note_count = np.count_nonzero(c[:, 2:],axis=0)
    print(f'Notes: {np.sum(column_note_count)}')
    print(f'Per Column: {column_note_count}')