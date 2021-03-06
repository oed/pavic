#!/usr/bin/python

import argparse
import pulsecontroller
import subprocess
import sys

version = 0.1

class pavic():
    def __init__(self, program, sink, step):
        self.program = program
        self.sink = sink
        self.step = step
        self.pc = pulsecontroller.PulseController()

        self.clients = self.get_clients()

    def get_clients(self):
        client_list = []
        if not self.sink == None:
            for s in self.pc.sinks:
                if int(s.index) == self.sink:
                    client_list.append(s)
        if self.program == 'CURRENT':
            self.program = self._get_current_program()
        for s in self.pc.sink_inputs:
            if self.program in s.app_name:
                client_list.append(s)

        return client_list

    def _get_current_program(self):
        active = subprocess.check_output("xprop -root _NET_ACTIVE_WINDOW".split()).decode("utf-8")
        active = active[active.find('0'):-1]
        text = subprocess.check_output(["xprop", "-id", active, "WM_CLASS"]).decode("utf-8")
        return text[text.find('"')+1:text.find('",')]

    def do_action(self, action):
        if action == 'toggle_mute':
            for client in self.clients:
                client.toggle_mute()
        elif action == 'vol_up':
            for client in self.clients:
                client.change_vol(self.step)
        elif action == 'vol_down':
            for client in self.clients:
                client.change_vol(self.step*-1)
        if not self.sink == None:
            print("Error: Can't change sink on a sink.")
            sys.exit(1)
        elif action == 'sink_next':
            for client in self.clients:
                client.change_sink(self.pc.sinks[self._get_sink_index(client) + 1 % len(self.pc.sinks)].index)
        elif action == 'sink_prev':
            for client in self.clients:
                client.change_sink(self.pc.sinks[self._get_sink_index(client) - 1 % len(self.pc.sinks)].index)

    def _get_sink_index(self, client):
        for sink in self.pc.sinks:
            if sink.index == client.sink:
                return int(sink.index)
        return 0



def main():
    parser = argparse.ArgumentParser(prog="pavic")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1' )
    parser.add_argument('action',
            choices=['vol_up', 'vol_down', 'toggle_mute', 'sink_next', 'sink_prev'])
    parser.add_argument('-s', '--step', type=int, default=10,
            help="step in which volume is changed")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--program', default='CURRENT',
            help="which program(s) to change volume on")
    group.add_argument('-z', '--sink', type=int,
            help="which sink(s) to change volume on")

    args = parser.parse_args()

    p = pavic(args.program, args.sink, args.step)
    p.do_action(args.action)

if __name__ == '__main__':
    main()
