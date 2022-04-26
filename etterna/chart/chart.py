import numpy as np

def zeropad_chart(c, snap):
    snap = snap.value
    snap_step = 1 / snap
    
    padded= {}
    
    measure = 0
    for k, v in c.items():
        cur_measure = np.floor(k)
        if measure != cur_measure:
            measure = cur_measure
            for i in range(snap):
                padded[measure + snap_step*i] = '0000'
        padded[k] = v
    return padded

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


class Chart:
    data = None
    
    def __init__(self, data):
        self.data = data
        pass
    
    def zeropad(self, snap):
        return Chart(zeropad_chart(self.data, snap))
    
    def numpy(self):
        chart = list(self.data.items())
        chart = np.array(chart)
        measures = np.expand_dims(list(chart[:, 0]), axis=1).astype(np.float32)
        chart = np.char.replace(chart[:, 1], 'F', '0')
        chart = np.char.replace(chart, 'M', '0')
        chart = np.array(list(map(list, chart)), dtype=np.float32)
        return np.concatenate((measures, chart), axis=1)

    def get_nearest_measure(time: float, with_notes=False):
        return 0.0
    
    def get_time(measure: float):
        return 0.0