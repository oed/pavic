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

        self.sinks = []
        self.sink_inputs = []
        self.update_sinks()
        self.update_sink_inputs()

    def _get_sinks_data(self):
        data = run_pactl_command(["list", "sinks"])
        data = str(data)
        sinks_data = data.split("Sink #")[1:]

        sinks = []
        for sink_data in sinks_data:
            
            mute = re.search('Mute: (.*?)\\\\', sink_data).group(1)
            if mute == 'no':
                muted = False
            else:
                muted = True

            vols = re.search('Volume: 0: (.*?)% 1: (.*?)%', sink_data)
            vol = int((int(vols.group(2)) + int(vols.group(1)))/2)

            name = re.search('Name: (.*?)\\\\', sink_data).group(1),
            description = re.search('Description: (.*?)\\\\', sink_data).group(1),
            sinks.append([sink_data[0], name, description, muted, vol])

        return sinks

    def _get_sink_input_data(self):
        data = run_patctl_command(["list", "sink-inputs"])
        data = str(data)
        inputs_data = data.split("Sink Input #")[1:]

        inputs = []
        # TODO - parse the data 

        return inputs

    def update_sinks(self):
        sinks_data = _get_sinks_data()

        for sink_data in sinks_data:
            # TODO - only add sink if it's different from existing sinks
            sink = PulseSink(sink_data[0], sink_data[1],
                                sink_data[2], sink_data[3],
                                sink_data[4])

            self.sinks.append(sink)
                   

    def update_sink_inputs(self):
        data = run_pactl_command(["list", "sink-inputs"])
        # TODO - create sink-inputs from data


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
