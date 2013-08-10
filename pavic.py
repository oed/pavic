#!/usr/bin/python

import argparse
import pulsecontroller
import subprocess

version = 0.1

class pavic():
    def __init__(self, program, sink, step):
        self.program = program
        self.sink = sink
        self.step = step
        self.pc = pulsecontroller.PulseController()

        self.clients = self.get_clients()

    def get_clients(self):
        if not self.sink == None:
            for s in self.pc.sinks:
                if int(s.index) == self.sink:
                    return [s]
        if self.program == 'CURRENT':
            name = self._get_current_program()
            print (name)
            for s in self.pc.sink_inputs:
                if s.name == self.app_name:
                    return [s]

        return []

    def _get_current_program(self):
        text = subprocess.check_output("xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) WM_CLASS")
        
        return text[text.find('"'):text.find('",')]

    def do_action(self, action):
        if action == 'toggle_mute':
            for client in self.clients:
                client.toggle_mute()



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

    print(args.program)
    print(args.sink)
    print(args.step)

    p = pavic(args.program, args.sink, args.step)
    p.do_action(args.action)
    
if __name__ == '__main__':
    main()
