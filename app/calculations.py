import numpy as np
import pandas as pd

# returns numpy array of beam lengths
def beam_np(beam_type:str, length:int):
    if beam_type in ("D78", "LV78"):
        beam = np.zeros(6)
        if length <= 2:
            beam[length - 1] = 1
        else:
            beam[5] = length // 6
            if length % 6 != 0:
                beam[length % 6 - 1] = 1
    elif beam_type in ("AHD", "LX133"):
        beam = np.zeros(4)
        if length == 1:
            beam[0] = 1
        else: 
            beam[3] = length // 4
            if length % 4 != 0:
                beam[length % 4 - 1] = 1
    return beam

# returns associated beam, spigot and pin codes
def beam_code(beam_type):
    if beam_type == 'D78':
        beam = 'BA'
        spigot = "BS0001"
        pin = "AF0001"
    elif beam_type == 'LV78':
        beam = 'LVB'
        spigot = "LVS0001"
        pin = "LFX0001"
    elif beam_type == 'AHD':
        beam = 'BD'
        spigot = "BS0006"
        pin = "AF0001"
    elif beam_type == 'LX133':
        beam = 'LXA'
        spigot = "LXS0001"
        pin = "LFX0001"
    else: ValueError
    return {'beam':beam, 'spigot':spigot, 'pin':pin}

# returns pandas dataframe of beam codes and lengths
def beam_pd(beam_type:str, length:int):
    beam = beam_np(beam_type, length)
    joints = np.sum(beam) - 1
    spigots = joints * 2
    codes = beam_code(beam_type)
    if beam_type in ('D78', 'LV78'):
        pins = spigots * 6
        beam_lengths = np.arange(1000, 6001, 1000)
    elif beam_type in ('AHD', 'LX133'):
        pins = spigots * 8
        beam_lengths = np.arange(1000, 4001, 1000)
    beam_codes = np.empty((len(beam_lengths), 1), dtype=object)
    for i, l in enumerate(beam_lengths):
        beam_codes[i] = codes['beam'] + str(l)
    beams = np.column_stack((beam_codes, beam))
    joints = np.array([[codes['pin'], pins], [codes['spigot'], spigots]], dtype=object)
    parts = np.vstack((joints, beams))
    parts = parts[parts[:, 1] != 0]
    parts = pd.DataFrame(parts, columns=['Code', 'Qty'])
    return parts

parts = beam_pd('D78', 20)
print(parts.to_html())