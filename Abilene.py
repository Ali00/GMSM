#-----------------------------------------#
#          Created By Ali Malik           #
#-----------------------------------------#
#import zmq
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
#from mininet.link import Link, TCLink
from mininet.link import TCLink
from mininet.node import CPULimitedHost
#----
#import sys
#import fnss
#import random
#import sched
#import time
#from threading import Thread
#import math
#import numpy as np
#from threading import Timer
#from collections import defaultdict
#import datetime
#from random import randint
#import networkx as nx, igraph as ig
#import pylab as plt
#from collections import Counter
#from itertools import tee, izip
#import string
#import heapq

#-------------------------------------------------------------------------------
#context = zmq.Context()
#socket = context.socket(zmq.REQ)
#socket.connect("tcp://localhost:5556")

net = Mininet( controller=RemoteController, host = CPULimitedHost, link=TCLink, switch=OVSKernelSwitch,xterms = False )
cls = TCLink
#G = nx.Graph()
#Global_Failure_Counter=0  # Global counter to keep the number of all links failure
#X_param = 1 # Global counter to avoid the first false failure (division by zero)

def topology():

        global net
        global cls
        # Add hosts and switches
        h1 = net.addHost( 'h1', mac= "00:00:00:00:00:01", cpu=.9)
        h2 = net.addHost( 'h2', mac= "00:00:00:00:00:02", cpu=.9)
        h3 = net.addHost( 'h3', mac= "00:00:00:00:00:03", cpu=.9)
        h4 = net.addHost( 'h4', mac= "00:00:00:00:00:04", cpu=.9)
        
        h5 = net.addHost( 'h5', mac= "00:00:00:00:00:05", cpu=.9)
        h6 = net.addHost( 'h6', mac= "00:00:00:00:00:06", cpu=.9)
        #--------------------------------------------------
        S1 = net.addSwitch( 's1')
        S2 = net.addSwitch( 's2')
        S3 = net.addSwitch( 's3')
        S4 = net.addSwitch( 's4')
        S5 = net.addSwitch( 's5')
        S6 = net.addSwitch( 's6')
        S7 = net.addSwitch( 's7')
        S8 = net.addSwitch( 's8')
        S9 = net.addSwitch( 's9')
        S10 = net.addSwitch( 's10')
        S11 = net.addSwitch( 's11')
        S12 = net.addSwitch( 's12')
        c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

        # Adding links
        net.addLink(h1, S1, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, delay='10ms')#, loss=10)#, use_htb=True)  
        net.addLink(h2, S9, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)  
        #net.addLink(h3, S1, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)  
        #net.addLink(h4, S9, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True) 
        
        net.addLink(h3, S3, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)  
        net.addLink(h4, S7, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True) 
        
        net.addLink(h5, S2, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink(h6, S10, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        #----------------------------------------------------------
        net.addLink( S1 , S2, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S1 , S3, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S3 , S4, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S2 , S3, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S2 , S6, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S4 , S5, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S5 , S6, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S6 , S8, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S8 , S7, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S8 , S11, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S7 , S9, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S9 , S10, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S10 , S11, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S11 , S12, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        net.addLink( S5 , S11, cls=TCLink,bw=8)#, max_queue_size= 1000, use_htb=True)#, jitter=3000)#, delay='10ms')#, loss=10)#, use_htb=True)
        #----------------------------------------------------------
        # Build The Network
        net.build()
        c0.start()
        S1.start(  [c0] )
        S2.start(  [c0] )
        S3.start(  [c0] )
        S4.start(  [c0] )
        S5.start(  [c0] )
        S6.start(  [c0] )
        S7.start(  [c0] )
        S8.start(  [c0] )
        S9.start(  [c0] )
        S10.start(  [c0] )
        S11.start(  [c0] )
        S12.start(  [c0] )
       
        ############################################
        h1.cmd("arp -s 10.0.0.2 00:00:00:00:00:02")
        h2.cmd("arp -s 10.0.0.1 00:00:00:00:00:01")
        h3.cmd("arp -s 10.0.0.4 00:00:00:00:00:04")
        h4.cmd("arp -s 10.0.0.3 00:00:00:00:00:03")
        h5.cmd("arp -s 10.0.0.6 00:00:00:00:00:06")
        h6.cmd("arp -s 10.0.0.5 00:00:00:00:00:05")
        #h7.cmd("arp -s 10.0.0.8 00:00:00:00:00:08")
        #h8.cmd("arp -s 10.0.0.7 00:00:00:00:00:07")
        #h9.cmd("arp -s 10.0.0.10 00:00:00:00:00:10")
        #h10.cmd("arp -s 10.0.0.9 00:00:00:00:00:09")
        #h11.cmd("arp -s 10.0.0.12 00:00:00:00:00:12")
        #h12.cmd("arp -s 10.0.0.11 00:00:00:00:00:11")
        #net.cmd("xterm h1")
        #############################################
        print "*** Running CLI"
        CLI( net )

        #print "*** Stopping network"
        #net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
