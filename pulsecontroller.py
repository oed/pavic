#!/usr/bin

class PulseController:

    def __init__(self):
        self.update_state();

    def update_state(self):
        pass


class PulseState:
    pass

import subprocess

class PulseSinkInput:
    def __init__(self, index, sink, muted, vol, app_name, icon_name):
        self.index = index
        self.sink = sink
        self.muted = muted
        self.vol = vol
        self.app_name = app_name
        self.icon_name = icon_name

    def toggle_mute(self):
        subprocess.Popen(["pactl set-sink-input-mute %s toggle" %self.index], stdout=subprocess.PIPE, shell=True) 

    def change_vol(percentage_point):
        self.vol += percentage_point
        subprocess.Popen(["pactl set-sink-input-volume %s %s" %(self.index, self.vol)], stdout=subprocess.PIPE, shell=True)

    def change_sink(sink_index):
        subprocess.Popen(["pactl move-sink-input %s %s" %(self.index, sink_index)], stdout=subprocess.PIPE, shell=True)
