import numpy as np
from ._types import NoteSnap
from . import timing



class Chart(object):
    # TODO add max snap
    def __init__(self, data, bpms = None):
        self.data = data
        self.bpms = bpms
        pass
    
    def zeropad(self, snap: NoteSnap):
        snap = snap.value
        snap_step = 1 / snap
        padded= {}
    
        measure = -1
        for k, v in self.data.items():
            cur_measure = np.floor(k)
            if measure != cur_measure:
                measure = cur_measure
                for i in range(snap):
                    note_measure = measure + snap_step*i
                    note_time = self.get_time(note_measure)
                    padded[note_measure] = [note_time, '0000']
            padded[k] = v
        self.data = padded
    
    def unzeropad(self):
        unpadded = {}
        for k, v in c.items():
            if v != '0000':
                unpadded[k] = v
        self.data = unpadded
    
    def numpy(self):
        chart = np.asarray(list(self.data.keys()))
        measures = np.expand_dims(chart, axis=1)
        chart = np.asarray(list(self.data.values()))
        timings = np.expand_dims(chart[:, 0], axis=1).astype(np.float64)
        chart = np.char.replace(chart[:, 1], 'F', '8')
        chart = np.char.replace(chart, 'M', '9')
        chart = np.array(list(map(list, chart)), dtype=np.float64)
        return np.concatenate((measures, timings, chart), axis=1)



    def get_nearest_measure(self, time: float, with_notes=False):
        if with_notes:
            measure = 0
            prev = None
            for k, v in self.data.items():
                if v[0] > time:
                    diff = v[0]-time
                    p_diff = time - prev[1]
                    if prev is None or (p_diff > diff):
                        measure = k
                        prev = None
                    break
                prev = (k, v[0], v[1])

            if prev is not None:
                measure = prev[0]
            return (measure // (1/192)) / 192
        return timing.get_nearest_measure(time, self.bpms)
    
    def get_time(self, measure: float):
        return timing.get_time(measure, self.bpms)

def from_numpy(data, bpms):
    chart_data = {}
    timing_slice = 2 if len(data.shape) else 1
    for t, col in zip(data[:, 0:timing_slice], data[:, timing_slice:]):
        col_str = ''.join(str(int(x)) if x < 8 else 'F' if x == 8 else 'M' for x in col)
        chart_data[t[0]] = (t[1], col_str) if timing_slice == 2 else col_str
    return Chart(chart_data, bpms)

def zeropad(c: Chart, snap: NoteSnap):
    snap = snap.value
    snap_step = 1 / snap
    padded= {}
    
    measure = -1
    for k, v in c.data.items():
        cur_measure = np.floor(k)
        if measure != cur_measure:
            measure = cur_measure
            for i in range(snap):
                note_measure = measure + snap_step*i
                note_time = c.get_time(note_measure)
                padded[note_measure] = [note_time, '0000']
        padded[k] = v
    return Chart(padded, c.bpms.copy())

def unzeropad(c: Chart):
    unpadded = {}
    for k, v in c.items():
        if v != '0000':
            unpadded[k] = v
    return Chart(unpadded, c.bpms.copy())
