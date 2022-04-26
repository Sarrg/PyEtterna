from ..types import NoteColor, NoteSnap

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