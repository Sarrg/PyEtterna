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


class Chart(object):
    def __init__(self, data, bpms = None):
        self.data = data
        self.bpms = bpms
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

    def from_numpy(data, bpms):
        pass

    def get_nearest_measure(self, time: float, with_notes=False):
        # TODO if before 0 measure return 0
        
        prev = None
        for k, v in self.data.items():
            if v[0] > time:
                if with_notes:
                    diff = v[0]-time
                    p_diff = time - prev[1]
                    return k if prev is None or (p_diff > diff) else prev[0]
                break
            prev = (k, v[0], v[1])
        
        if with_notes and prev[1] < time:
            return prev[0]
        
        measure = 0.0
        if not prev is None:
            prev_time = prev[1]
            measure = prev[0]
            prev_bpm = 0
            for i, (timing, (change_time, bpm)) in enumerate(self.bpms.items()):
                change_measure = timing / 4              
                
                if (measure < change_measure or np.isclose(measure, change_measure)):                        
                    if change_time > time:
                        break
                    prev_time = change_time
                    measure = change_measure
                prev_bpm = bpm
            measure += (time - prev_time) / (4 * 60 / prev_bpm)

        return (measure // (1/192)) / 192
    
    def get_time(self, measure: float):
        measure = (measure // (1/192)) / 192
        if measure in self.data:
            return self.data[measure][0]
        
        prev = None
        for k, v in self.data.items():
            if k > measure:
                break
            prev = (k, v[0], v[1])
        
        time = 0.0
        if not prev is None:
            time = prev[1]
            prev_measure = prev[0]
            prev_bpm = 0
            for i, (timing, (change_time, bpm)) in enumerate(self.bpms.items()):
                change_measure = timing / 4
                if (measure < change_measure or np.isclose(measure, change_measure)):                        
                    if change_time > time:
                        break
                    time = change_time
                    prev_measure = change_measure
                prev_bpm = bpm
            measure_diff = measure - prev_measure
            if not np.isclose(measure_diff, 0):
                time_step = 4.0 * 60.0 / prev_bpm
                time += time_step * measure_diff
        return time
