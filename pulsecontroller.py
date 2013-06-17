#!/usr/bin

class PulseController:

    def __init__(self):
        self.update_state();

    def update_state(self):
        pass


import subprocess

def run_pactl_command(args):
    return subprocess.check_output(args.insert(0, "pactl"))

class PulseState:
    def __init__(self):
        self._init_sinks()
        self._init_sink_inputs()

    def _init_sinks(self):
        data = run_pactl_command(["list", "sinks"])
        # TODO - create sinks from data

    def _init_sink_inputs(self):
        data = run_pactl_command(["list", "sink-inputs"])
        # TODO - create sink-inputs from data

class PulseSink:
    def __init__(self, index, name, description, muted, vol):
        self.index = index
        self.name = name
        self.description = description
        self.muted = muted
        self.vol = vol

    def toggle_mute(self):
        subprocess.Popen(["pactl set-sink-mute %s toggle" %self.index], stdout=subprocess.PIPE, shell=True)

    def change_vol(self, percentage_point):
        self.vol += percentage_point
        subprocess.Popen(["pactl set-sink-volume %s %s%%" %(self.index, self.vol)], stdout=subprocess.PIPE, shell=True)

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
        muted = not muted

    def change_vol(self, percentage_point):
        self.vol += percentage_point
        subprocess.Popen(["pactl set-sink-input-volume %s %s%%" %(self.index, self.vol)], stdout=subprocess.PIPE, shell=True)

    def change_sink(self, sink_index):
        subprocess.Popen(["pactl move-sink-input %s %s" %(self.index, sink_index)], stdout=subprocess.PIPE, shell=True)
