import xml.etree.ElementTree as ET
import numpy as np
from .chart import Song
from .chart import Chart
from .chart import timing

def load_profile(path):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(path, parser)
    return tree.getroot()


def load_data(profile, path):
    data = []
    scores = profile.find('./PlayerScores')
    now = datetime.now()
    for chart in scores.findall('Chart'):
        curchart = {}
        curchart['name'] = chart.attrib['Song']
        curchart['step'] = chart.attrib['Steps']
        for scoresat in chart.findall('ScoresAt'):
            curchart['rate'] = scoresat.attrib['Rate']
            for score in scoresat.findall('Score'):
                if score.find('SkillsetSSRs') != None:
                    msd = (float(score.find('SkillsetSSRs').find('Overall').text))
                    df = open(path + score.attrib['Key'])
                    diffs = [float(line.split(' ')[1]) for line in df.readlines()]
                    diffs = [1000.0*d for d in diffs if d < 1.0]
                    wife = (float(score.find('SSRNormPercent').text)*100.0)
                    date = datetime.strptime(score.find('DateTime').text[0:10], '%Y-%m-%d')
                    days = ((now - date).days)
                    sd = (np.std(diffs))
                    modsplit = score.find('Modifiers').text.split(", ")
                    mods = {}
                    if (modsplit[0][0] == 'C'):
                        mods['cmod'] = int(modsplit[0][1:])
                    mods['skin'] = modsplit[3]
                    #wifedata.append(wife)
                    arr = {
                        'chart': curchart,
                        'msd': msd,
                        'wife': wife,
                        'sd': sd,
                        'inputs': diffs,
                        'days': days,
                        'mods': mods
                    }
                    data.append(arr)
    return data

def load_song(path):
    song = Song()
    instep = False
    measure = 0
    notes = []
    
    with open(path) as f:
        line = f.readline()
        while line:
            if instep:
                if line[0] in [',', ';']:
                    for i in range(len(notes)):
                        if notes[i] != '0000':
                            note_measure = (measure + (i / len(notes)))
                            time = timing.get_time(note_measure, song.bpms)
                            step[note_measure] = [time, notes[i]]
                    notes = []
                    measure = measure + 1
                    if line[0] == ';':
                        song.charts.append(Chart(step, song.bpms))
                        notes.clear()
                        instep = False
                else:
                    notes.append(line[:-1])
            else:
                if line[0] == '#':
                    s = line.split(':', 1)
                    if len(s) == 2:
                        propName = s[0][1:].lower()
                        if propName == "notes":
                            instep = True
                            measure = 0                        
                            step = {}
                            f.readline()
                            f.readline()
                            f.readline()
                            f.readline()
                            f.readline()
                            
                        if len(s[1]) > 2:
                            prop = s[1].rstrip('\n\r')
                            try:
                                prop = float(prop.rstrip(';'))
                            except ValueError:
                                pass
                            
                            if propName == "bpms":
                                p_beat = 0
                                time = -song.offset
                                bpm = 1
                                while len(line) != 0:

                                    bpmsig = prop.split('=')
                                    if len(bpmsig) == 2:
                                        beat = float(bpmsig[0].replace(',', ''))
                                        diff = beat - p_beat
                                        time += diff * 60.0 / bpm
                                        p_beat = beat
                                        bpm = float(bpmsig[1])
                                        song.bpms[beat] = (time, bpm)
                                    
                                    if ';' in line:
                                        break;
                                    line = f.readline()
                                    prop = line.rstrip('\n\r')
                            else:
                                song.__setattr__(propName, prop)
                                
            line = f.readline()
        
    return song
