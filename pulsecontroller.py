#!/usr/bin

class PulseController:

    def __init__(self):
        self.update_state();

    def update_state(self):
        pass


import subprocess
import re

def run_pactl_command(args):
    args.insert(0, "pactl")
    return subprocess.check_output(args)

class PulseState:
    def __init__(self):
        self._init_sinks()
        self._init_sink_inputs()

    def _init_sinks(self):
        data = run_pactl_command(["list", "sinks"])
        data = str(data)
        sinks_data = data.split("Sink #")[1:]

        self.sinks = []
        for sink_data in sinks_data:
            
            mute = re.search('Mute: (.*?)\\\\', sink_data).group(1)
            if mute == 'no':
                muted = False
            else:
                muted = True

            vols = re.search('Volume: 0: (.*?)% 1: (.*?)%', sink_data)
            vol = int((int(vols.group(2)) + int(vols.group(1)))/2)

            sink = PulseSink(sink_data[0],
                   re.search('Name: (.*?)\\\\', sink_data).group(1),
                   re.search('Description: (.*?)\\\\', sink_data).group(1),
                   muted,
                   vol)
            self.sinks.append(sink)
                   

    def _init_sink_inputs(self):
        data = run_pactl_command(["list", "sink-inputs"])
        # TODO - create sink-inputs from data

    def get_data_points(data, main_point, data_points):
        main_points = data.split(main_point)



class PulseSink(object):
    def __init__(self, index, name, description, muted, vol):
        self.index = index
        self.name = name
        self.description = description
        self.muted = muted
        self.vol = vol

    def toggle_mute(self):
        subprocess.Popen(["pactl set-sink-mute %s toggle" %self.index], stdout=subprocess.PIPE, shell=True)
        self.muted = not self.muted

    def change_vol(self, percentage_point):
        self.vol += percentage_point
        subprocess.Popen(["pactl set-sink-volume %s %s%%" %(self.index, self.vol)], stdout=subprocess.PIPE, shell=True)

class PulseSinkInput(object):
    def __init__(self, index, sink, muted, vol, app_name, icon_name):
        self.index = index
        self.sink = sink
        self.muted = muted
        self.vol = vol
        self.app_name = app_name
        self.icon_name = icon_name

    def toggle_mute(self):
        subprocess.Popen(["pactl set-sink-input-mute %s toggle" %self.index], stdout=subprocess.PIPE, shell=True) 
        self.muted = not self.muted

    def change_vol(self, percentage_point):
        self.vol += percentage_point
        subprocess.Popen(["pactl set-sink-input-volume %s %s%%" %(self.index, self.vol)], stdout=subprocess.PIPE, shell=True)

    def change_sink(self, sink_index):
        subprocess.Popen(["pactl move-sink-input %s %s" %(self.index, sink_index)], stdout=subprocess.PIPE, shell=True)
