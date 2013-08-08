#!/usr/bin/python

import argparse

version = 0.1

def main():
    parser = argparse.ArgumentParser(prog="pavic")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1' )
    parser.add_argument('action', 
            choices=['vol_up', 'vol_down', 'toggle_mute', 'sink_next', 'sink_prev'])
    parser.add_argument('-s', '--step', type=int, 
            help="step in which volume is changed")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--program', default='current', 
            help="which program(s) to change volume on")
    group.add_argument('-z', '--sink', type=int, 
            help="which sink(s) to change volume on")
    
    args = parser.parse_args()

    print(args.program)
    print(args.sink)
    print(args.step)

if __name__ == '__main__':
    main()
