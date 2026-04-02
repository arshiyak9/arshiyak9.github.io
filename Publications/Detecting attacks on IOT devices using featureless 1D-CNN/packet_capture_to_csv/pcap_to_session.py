#This script takes a pcap file and converts it into separate sessions (pcap format) and stores them in a destination folder.
from pathlib import Path
import subprocess as sp
import os
from pcap_splitter.splitter import PcapSplitter

#Basic query
#ps = PcapSplitter("network_traffic.pcap")
#print(ps.split_by_session("dest_pcaps_folder"))

for each in pcaplist:
    ps = PcapSplitter(each)
    folder="session/session_"+os.path.splitext(each)[0].split("/")[-2]
    print(folder)
    #folder=Path("session_"+os.path.splitext(each)[0].split("/")[-2]).mkdir(parents=True, exist_ok=True)
    print(ps.split_by_session(folder))