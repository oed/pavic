#!/usr/bin

import subprocess
import re

def run_pactl_command(args):
    args.insert(0, "pactl")
    return subprocess.check_output(args)

class PulseController():
    def __init__(self):
        self.sinks = []
        self.sink_inputs = []
        self.update()

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
            description = re.search('Description: (.*?)\\\\', sink_data).group(1)
            sinks.append([sink_data[0], name, description, muted, vol])

        return sinks

    def _get_sink_input_data(self):
        data = run_pactl_command(["list", "sink-inputs"])
        data = str(data)
        inputs_data = data.split("Sink Input #")[1:]

        inputs = []
        for input_data in inputs_data:
            sink = re.search('Sink: (.*?)\\\\', input_data).group(1)
            mute = re.search('Mute: (.*?)\\\\', input_data).group(1)
            if mute == 'no':
                muted = False
            else:
                muted = True

            vols = re.search('Volume: 0: (.*?)% 1: (.*?)%', input_data)
            vol = int((int(vols.group(2)) + int(vols.group(1)))/2)

            name = re.search('application.name = "(.*?)"\\\\', input_data).group(1)
            icon = re.search('application.icon_name = "(.*?)"\\\\', input_data).group(1)
            inputs.append([input_data[0], sink, muted, vol, name, icon]) 

        return inputs

    def _update_unit(self, unit, data, modify, create):
        for d in data:
            for u in unit:
                if u.index == d[0]:
                    modify(u, d) 
                    break
            else:       
                unit.append(create(d))
                   
    def _modify_sink(self, sink, data):
        sink.name = data[1]
        sink.description = data[2]
        sink.muted = data[3]
        sink.vol = data[4]

    def _create_sink(self, data):
        return PulseSink(data[0], data[1],
                            data[2], data[3],
                            data[4])

    def _modify_sink_input(self, s_inp, data):
        s_inp.sink = data[1]
        s_inp.muted = data[2]
        s_inp.vol = data[3]
        s_inp.app_name = data[4]
        s_inp.icon_name = data[5]

    def _create_sink_input(self, data):
        return PulseSinkInput(data[0], data[1],
                                data[2], data[3],
                                data[4], data[5])

    def update(self):
        # update sinks
        self._update_unit(self.sinks, self._get_sinks_data(),
                self._modify_sink, self._create_sink)
        # update sink-inputs
        self._update_unit(self.sink_inputs, self._get_sink_input_data(),
                self._modify_sink_input, self._create_sink_input)

class PulseSink():
    def __init__(self, index, name, description, muted, vol):
        self.index = index
        self.name = name
        self.description = description
        self.muted = muted
        self.vol = vol

    def toggle_mute(self):
        run_pactl_command(["set-sink-mute", self.index, "toggle"])
        self.muted = not self.muted

    def change_vol(self, percentage_point):
        self.vol += percentage_point
        run_pactl_command(["set-sink-volume", self.index, self.vol+"%%"])

class PulseSinkInput():
    def __init__(self, index, sink, muted, vol, app_name, icon_name):
        self.index = index
        self.sink = sink
        self.muted = muted
        self.vol = vol
        self.app_name = app_name
        self.icon_name = icon_name

    def toggle_mute(self):
        run_pactl_command(["set-sink-input-mute", self.index, "toggle"])
        self.muted = not self.muted

    def change_vol(self, percentage_point):
        self.vol += percentage_point
        run_pactl_command(["set-sink-input-volume", self.index, self.vol+"%%"])

    def change_sink(self, sink_index):
        run_pactl_command(["move-sink-input", self.index, sink_index])
