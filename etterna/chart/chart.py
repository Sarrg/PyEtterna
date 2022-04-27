import numpy as np
from ._types import NoteSnap
from . import timing

def unpad_chart(c):
    unpadded = {}
    for k, v in c.items():
        if v != '0000':
            unpadded[k] = v
    return unpadded

def chart2numpy(chart):
    chart = list(chart.items())
    chart = np.array(chart)
    measures = np.expand_dims(list(chart[:, 0]), axis=1).astype(np.float32)
    chart = np.char.replace(chart[:, 1], 'F', '0')
    chart = np.char.replace(chart, 'M', '0')
    chart = np.array(list(map(list, chart)), dtype=np.float32)
    return np.concatenate((measures, chart), axis=1)


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
        return Chart(padded, self.bpms)
    
    def numpy(self):
        chart = np.asarray(list(self.data.keys()))
        measures = np.expand_dims(chart, axis=1)
        chart = np.asarray(list(self.data.values()))
        timings = np.expand_dims(chart[:, 0], axis=1).astype(np.float64)
        chart = np.char.replace(chart[:, 1], 'F', '0')
        chart = np.char.replace(chart, 'M', '0')
        chart = np.array(list(map(list, chart)), dtype=np.float64)
        return np.concatenate((measures, timings, chart), axis=1)

    def from_numpy(data, bpms):
        pass

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
