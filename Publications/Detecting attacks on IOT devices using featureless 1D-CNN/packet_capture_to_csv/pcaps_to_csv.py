#This script converts all pcap files into csv for training 1D-CNN model
import binascii
from csv import writer
import subprocess as sp
import os, json
import numpy as np
import pandas as pd

def get_tshark_hexstreams(capture_path: str) -> list:
    """Get the frames in a capture as a list of hex strings."""
    cmds = ["tshark", "-x", "-r", capture_path, "-c", "14000", "-T", "json"]
    frames_text = sp.check_output(cmds, text=True)
    frames_json = json.loads(frames_text)
    hexstreams = [frame["_source"]["layers"]["frame_raw"][0] for frame in frames_json]
    return hexstreams

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def showAllHeaders(file):
#all headers are included in the pcap
    raw_row=[]
    output = get_tshark_hexstreams(file)
    for each in output:
        encoded_str=str.encode(each)
#        r=np.random.randint(0, 255, size=(20))
        for i in range(len(encoded_str)):
            raw_row.append(encoded_str[i])
    append_list_as_row("showAll_benign.csv", raw_row)

def remEthHeader(file):
#Remove Ethernet headers only from each pcap
    raw_row=[]
    output = get_tshark_hexstreams(file)
    for each in output:
        encoded_str=str.encode(each)
#            r=np.random.randint(0, 255, size=(20))
        for i in range(14,len(encoded_str)):
#                print(i)
            raw_row.append(encoded_str[i])
    append_list_as_row("remeth_benign.csv", raw_row)

def remIpHeader(file):
#Remove IP headers only from each pcap
    raw_row=[]
    output = get_tshark_hexstreams(file)
    for each in output:
        encoded_str=str.encode(each)
#            r=np.random.randint(0, 255, size=(20))
        for i in range(14):
#                print(i)
            raw_row.append(encoded_str[i])
#            print(",\n")
        for i in range(34,len(encoded_str)):
#                print(i)
            raw_row.append(encoded_str[i])
    append_list_as_row("remip_benign.csv", raw_row)

def remAllHeaders(file):
#Remove all(ethernet + IP) headers from each pcap
    raw_row=[]
    output = get_tshark_hexstreams(file)
    for each in output:
        encoded_str=str.encode(each)
#            r=np.random.randint(0, 255, size=(20))
        for i in range(34,len(encoded_str)):
#                print(i)
            raw_row.append(encoded_str[i])
    append_list_as_row("remAll_benign.csv", raw_row)


if __name__=="__main__":
    thisdir=os.getcwd()
    pcaplist = [f for f in os.listdir(thisdir) if f.endswith('.pcap')]
    #Convert all the files in the current folder to CSV (to each header category)
	for apcap in pcaplist:
    	showAllHeaders(apcap)
    	remAllHeaders(apcap)
    	remEthHeader(apcap)
    	remIpHeader(apcap)

