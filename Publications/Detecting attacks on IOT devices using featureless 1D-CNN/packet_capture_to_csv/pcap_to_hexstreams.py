#This file captures pcap files to hexstreams using tshark. Tshark is a CLI of Wireshark.
import binascii
from csv import writer
import subprocess as sp
import os, json
import numpy as np
import pandas as pd

# Convert each packet into hexstream
def get_tshark_hexstreams(capture_path: str) -> list:
    """Get the frames in a capture as a list of hex strings."""
    cmds = ["tshark", "-x", "-r", capture_path, "-c", "14000", "-T", "json"]
    frames_text = sp.check_output(cmds, text=True)
    frames_json = json.loads(frames_text)
    hexstreams = [frame["_source"]["layers"]["frame_raw"][0] for frame in frames_json]
    return hexstreams


if __name__=="__main__":
    thisdir=os.getcwd()
    ''' The variable 'pcaplist' stores the names of all files with .pcap extension'''
    pcaplist = [f for f in os.listdir(thisdir) if f.endswith('.pcap')]
    for pcap in pcaplist:
    '''showAllHeaders function saves pcap into a csv. All headers are included. For a packet view, each row in csv is a packet, so on.'''
        get_tshark_hexstreams(apcap)
