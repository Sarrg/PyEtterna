from ._types import NoteColor, NoteSnap

def is_color(measure, color):
    submeasure = measure - int(measure)
    if col is NoteColor.GREY:
        is_grey = True
        for diff_col in NoteColor:
            if diff_col != col:
                is_grey = not is_color(measure, diff_col)
        return is_grey
    return submeasure in color.value

def get_color(measure):
    for col in NoteColor:
        if is_color(measure, col):
            return col
    tb = sys.exc_info()[2]
    raise ValueError(f"Not a valid measure: {measure}").with_traceback(tb)

def get_next_measure(measure, col: NoteColor = NoteColor.GREY):
    submeasure = measure - int(measure)
    measure_col = get_color(measure)
    if col is NoteColor.GREY:
        return measure + 1/192
    for m in col.value:
        if m > submeasure:
            return int(measure) + m
    return measure + 1/192

def get_next_measure(measure, snap: NoteSnap = NoteSnap._192THS):
    submeasure = measure - int(measure)
    snap_step = 1 / snap.value
    return (int(measure/snap_step) + 1) * snap_step


def get_nearest_measure(time: float, bpms, with_notes=False):
    measure = 0

    p_beat, p_time, p_bpm = None, 0, None
    for beat, (beat_time, bpm) in bpms.items():
        if beat_time > time:
            break
        p_beat, p_time, p_bpm = beat, beat_time, bpm

    if p_bpm != None:
        diff = time - p_time
        measure = (p_beat / 4) + (diff * p_bpm / (60.0 * 4))
    return (measure // (1/192)) / 192

def get_time(measure: float, bpms):
    p_beat, p_time, p_bpm = None, 0, None
    for beat, (time, bpm) in bpms.items():
        if beat > measure*4:
            break
        p_beat, p_time, p_bpm = beat, time, bpm
        
    if p_bpm != None:
        diff = measure*4 - p_beat
        return p_time + diff * 60.0 / p_bpm
    return 0