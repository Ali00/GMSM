#-----------------------------------------#
#          Created By Ali Malik           #
#-----------------------------------------#
import os
import threading
import thread
import multiprocessing
import subprocess
import sched
#from threading import Timer
import sys
import json
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
import time
import datetime
from itertools import tee, izip
import networkx as gx
from collections import defaultdict
import collections
import ast
import copy
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
import pox.openflow.nicira as nx
from matplotlib import pylab
import matplotlib.pyplot as plt    
from pylab import *
#-----------------------------------------
scheduler = sched.scheduler(time.time, time.sleep)
now = datetime.datetime.now()

# ------------ Clearing the experimental files -------------- 
with open('/home/mininet/pox/test.json', 'r+') as v:
	v.truncate(0)
with open('/home/mininet/pox/monitor_rtp.pcapng', 'r+') as m:
	m.truncate(0)
#------------------------------------------------------------
log = core.getLogger()
mac_map = {}
switches = {}
myswitches=[]
List_of_Sources = []
adjacency = defaultdict(lambda:defaultdict(lambda:None))
#current_p=[]
G = gx.Graph()  #initiate the graph G to maintain the network topology
G1 = gx.Graph()  #initiate the graph G1 to maintain the network flow and to be used as a monitoring
counter = 1
C = 0
Flow_global_view  = defaultdict(list)

Switch_Dictionary = { (1): 's1', (2): 's2', (3): 's3',(4): 's4', (5): 's5', (6): 's6', 
(7): 's7', (8): 's8', (9): 's9', (10): 's10', (11): 's11', (12): 's12', (13): 's13', (14): 's14',
(15): 's15', (16): 's16', (17): 's17', (18): 's18', (18): 's18', (19): 's19', (20): 's20', (21): 's21',
(22): 's22', (23): 's23', (24): 's24', (25): 's25', (26): 's26', (27): 's27', (28): 's28', (29): 's29',
(30): 's30', (31): 's31' , (32): 's32', (33): 's33', (34): 's34', (35): 's35', (36): 's36', (37): 's37',
(38): 's38', (39): 's39', (40): 's40', (41): 's41', (42): 's42', (43): 's43', (44): 's44', (45): 's45',
(46): 's46', (47): 's47', (48): 's48', (49): 's49', (50): 's50', (51): 's51',
(52): 's52', (53): 's53', (54): 's54', (55): 's55', (56): 's56', (57): 's57', (58): 's58',(59): 's59',
(60): 's60' , (61): 's61' , (62): 's62' , (63): 's63' , (64): 's64' , (65): 's65', (66): 's66',
(67): 's67', (68): 's68', (69): 's69', (70): 's70'}
#--------------------------------------------------------
Host_Dictionary = { (1): 'h1', (2): 'h2', (3): 'h3',(4): 'h4', (5): 'h5', (6): 'h6', (7): 'h7', (8): 'h8', (9): 'h9', (10): 'h10'}
Port_Dictionary = { (1): 'eth1', (2): 'eth2', (3): 'eth3',(4): 'eth4', (5): 'eth5', (6): 'eth6', (7): 'eth7', (8): 'eth8', (9): 'eth9', (10): 'eth10'}
#--------------------------------------------------------
Links_weight_Dictionary = { (1, 27) : 0, (1, 2) : 0 , (1, 3) : 0 , (2, 20) : 0 ,(2, 21) : 0 , (2, 23) : 0 , (3, 23) : 0 , (3, 12) : 0 , (3, 13) : 0 , (3, 17) :
 0 , (4, 16) : 0 , (4, 36) : 0 , (5, 8) : 0 ,  (5, 30) : 0 , (5, 14) : 0 , (6, 33) : 0 , (6, 18) : 0 , (6, 35) : 0 , (7, 8) : 0 , (7, 9) : 0 , (7, 29) : 0 , (8,
 26) : 0 , (8, 21) : 0 , (9, 24) : 0 , (9, 32) : 0 , (9, 10) : 0 , (10, 11) : 0, (10, 36) : 0 , (10, 29) : 0 , (10, 37) : 0 , (11, 24) : 0 , (11, 35) : 0 , (12
, 33) : 0 , (12, 34) : 0 , (12, 18) : 0 , (12, 35) : 0 , (13, 19) : 0 , (13, 35) : 0 , (14, 21) : 0 , (15, 25) : 0 , (15, 26) : 0 , (15, 29) : 0 , (16, 37) : 0
, (16, 22) : 0 , (17, 24) : 0 , (17, 27) : 0 , (19, 24) : 0 , (20, 28) : 0 , (20, 31) : 0 , (21, 32) : 0 , (22, 36) : 0 , (23, 28) : 0 , (25, 37) : 0 , (26, 30)
 : 0 , (27, 32) : 0 , (28, 34) : 0 , (31, 34) : 0}
#-------------------------------------------------------------------------------
def _get_raw_path (src,dst):
  global G
  global G1
  #Dijkstra algorithm using NetworkX
  print "src=",src," dst=", dst
  p = []   # To store the shortest path
  p = gx.shortest_path(G, source=src, target=dst)#, weight='weight')
  print " The path found : ", p
  return p
#------------------------------------------------------
# handler for timer function that sends the FLOW-STATE requests to some
# switches based on Flow_Graph.
def _timer_func ():
  global G1
  print "Polling function is called..."
  print ("G1 nodes are . . . ", G1.nodes())
  for connection in core.openflow._connections.values():
    print ("connection is", connection.dpid)
    if G1.has_node(Switch_Dictionary[connection.dpid]):  #Condition for active flows only
		print ("The graph G1 has the node", connection.dpid)
		connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
		#print ("connection.dpid == ", connection.dpid)
		#connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
  log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))
#------------------------------------------------------
# handler to display port statistics received in JSON format
def _handle_portstats_received (event):
  #global Links_ports
  #stats = flow_stats_to_list(event.stats)
  received_packets = 0 
  received_bytes = 0 
  for f in event.stats:
	  #if f.dl_type != pkt.ethernet.LLDP_TYPE:
	  #prev_duration_sec = prev_stats[match][event.connection.dpid]
	  if f.port_no != 65534:
		  print ('switch number =', (event.dpid),'port number =',f.port_no , "Received_packets =", f.rx_packets, "Sent_packets =", f.tx_packets)
		  #print ('switch number =', (event.dpid),'port number =',f.port_no, "Link", Links_ports [event.dpid, f.port_no]  , "Received_packets =", f.rx_packets, "Sent_packets =", f.tx_packets)
	  #print ('switch number =', dpidToStr(event.connection.dpid),'port number =',f.port_no, "Sent_packets =", f.tx_packets)
	  #print ('switch number =', dpidToStr(event.connection.dpid),'port number =',f.port_no, "Port alive =", f.duration_sec, "seconds")
  #log.debug("PortStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)
#------------------------------------------------------------------------------------------------
class Switch (EventMixin):
  global G
  
  def __init__ (self):
    self.connection = None
    self.ports = None
    self.dpid = None
    self._listeners = None
    self._connected_at = None
    #self.scheduler = sched.scheduler(time.time, time.sleep)
    #-------------------------------------------------------------------------
    # For the Abilene Topo
    mac_map[str("00:00:00:00:00:01")]=(1,1)   # host 1
    mac_map[str("00:00:00:00:00:02")]=(9,1)   # host 2
    
    #For Abilene
    mac_map[str("00:00:00:00:00:03")]=(3,1)   # host 3
    mac_map[str("00:00:00:00:00:04")]=(7,1)   # host 4
    
    #For Abilene
    mac_map[str("00:00:00:00:00:05")]=(2,1)   # host 5
    mac_map[str("00:00:00:00:00:06")]=(10,1)   # host 6
    
    # For the Us_Nobel Topo
    #mac_map[str("00:00:00:00:00:01")]=(5,1)   # host 1
    #mac_map[str("00:00:00:00:00:02")]=(10,1)   # host 2
    
    # For the Us_Nobel Topo
    #mac_map[str("00:00:00:00:00:03")]=(5,2)   # host 3
    #mac_map[str("00:00:00:00:00:04")]=(10,2)   # host 4
    
    # For the Us_Nobel Topo
    #mac_map[str("00:00:00:00:00:05")]=(5,3)   # host 5
    #mac_map[str("00:00:00:00:00:06")]=(10,3)   # host 6
    
  #-------------------------------------------------------------------------
  def __repr__ (self):
    return dpid_to_str(self.dpid)

  def _install (self, in_port, out_port, match, buf = None):
    msg = of.ofp_flow_mod()
    msg.flags = of.OFPFF_SEND_FLOW_REM
    msg.match = match
    msg.match.in_port = in_port
    msg.idle_timeout = 20
    msg.hard_timeout = 0
    msg.actions.append(of.ofp_action_output(port = out_port))
    #msg.buffer_id = buf
    self.connection.send(msg)
  #-------------------------------------------
  def pairwise(self,iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
  #-----------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------
  def check(self, port, host_s, host_d, src_switch, packet, path):
      global List_of_Sources
      global G1
      global Switch_Dictionary
      global Host_Dictionary
      global Port_Dictionary
      global Flow_global_view
      L =[]
      SW = []
      Temp_link_to_G1 = []
      Traffic = []   # The list represents the type of traffic on each link whether ICMP, UDP or TCP, it can can multiple ones.
      MM = True
      prt = Port_Dictionary[port]
      pair = [host_s, host_d]
      print "the pair is", pair 
      for x in Flow_global_view.keys():
		  if set(x) == set(pair):
			  #print "the path already exists, probably the reversed path..."
			  MM = False
      if os.stat('/home/mininet/pox/monitor_rtp.pcapng').st_size == 0: 
		  #print "************************ Sorry, The Monitor File is Empty now ************************"
		  return
      else:
		  f= open('/home/mininet/pox/test.json')
		  print "$$$$$$$$$$$$$ ... We are inside Check () function ... $$$$$$$$$$$$$"
		  cmd2 = ('tshark -r monitor_rtp.pcapng -T json > test.json') #conver the pcapng to json
		  os.system(cmd2)
		  #print "%%%%%%%%%%%%%%%%%%%%%%%%%% Pcapng is converted to Json now %%%%%%%%%%%%%%%%%%%%%%%%%%" 
		  data = json.load(f)
		  #print "%%%%%%%%%%%%%%%%%%%%%%%%%% Json is loaded now %%%%%%%%%%%%%%%%%%%%%%%%%%" 
		  data1= json.dumps(data)
		  #print "%%%%%%%%%%%%%%%%%%%%%%%%%% Json is dumped now %%%%%%%%%%%%%%%%%%%%%%%%%%"
		  data2= json.loads(data1)
		  f.close()
		  if "sip" in data1:
			  print "############## ... We found SIP ... ##################"
			  pkt_type = 'SIP'
		  if "rtp" in data1:
			  print "############## ... We found RTP ... ##################"
			  pkt_type = 'RTP'
		  if "icmp" in data1:
			  print "############## ... We found ICMP ... ##################"
			  pkt_type = 'icmp'
		  with open('/home/mininet/pox/test.json', 'r+') as v:
			  v.truncate(0)
		  with open('/home/mininet/pox/monitor_rtp.pcapng', 'r+') as m:
			  m.truncate(0)
      print " We are done ..."
      Marker = False
      if bool (Flow_global_view) == True:
		print "The dict is not empty..."
		Traffic.append(pkt_type)
		for x in Flow_global_view.keys():
			print 'x', x
			print 'pair', pair
			if set(x) == set(pair):
				print "the path already exists, probably the reversed path..."
				Marker = True
		if Marker == False:
			print "We have got a new path to add ..."
			for i in range (len(path)):
				SW.append(Switch_Dictionary[path[i]])
				#print "The path as switches is: ", SW
			L = SW #path
			L.insert(0,pair[0])
			L.insert(len(L),pair[1])
			Flow_global_view [tuple(pair)] = L #SW #path
			print (Flow_global_view)
			#print "#2 The whole path from host to host is", L
			for pair in self.pairwise(L):
				Temp_link_to_G1.append(pair)
			print Temp_link_to_G1
			#for i in range (len(Temp_link_to_G1)):
			for i in Temp_link_to_G1:
				if G1.has_edge(i[0], i[1]) == True:
					xxx = []
					#yyy = []
					print "The link", i, "is already exist in G1"
					G1[i[0]][i[1]]['weight'] = G1[i[0]][i[1]]['weight'] + 1
					xxx.append(pkt_type)
					G1[i[0]][i[1]]['Traffic'] = G1[i[0]][i[1]]['Traffic'] + xxx
				if G1.has_edge(i[0], i[1]) == False:
					G1.add_edge(i[0],i[1], weight = 1, Traffic = Traffic)  #weight =1 for the new links 
      if bool (Flow_global_view) == False:
		  #print "The dict is empty now ..."
		  Traffic.append(pkt_type)
		  for i in range (len(path)):
			  SW.append(Switch_Dictionary[path[i]])
			  #print "The path as switches is: ", SW
		  L = SW #path
		  L.insert(0,pair[0])
		  L.insert(len(L),pair[1])
		  Flow_global_view [tuple(pair)] = L #SW #path
		  print (Flow_global_view)
		  #print "#1 The whole path from host to host is", L
		  for pair in self.pairwise(L):
			  Temp_link_to_G1.append(pair)
		  print Temp_link_to_G1
		  G1.add_edges_from(Temp_link_to_G1, weight=1, Traffic = Traffic) # add the links of the computed path to G1 with Weight = 1 (initial case)
		  #fig = plt.figure()
		  #fig.canvas.set_window_title("The Current View of Abilene Flow")
		  #pos = nx.spring_layout(G1, scale=2)
		  #edge_labels = gx.get_edge_attributes(G1, 'Traffic')
		  #gx.draw_networkx_edge_labels(G1, pos, edge_labels)
		  #gx.draw_networkx(G1, with_labels = True, nodecolor='r', edge_color='b')
		  #gx.draw_networkx(G1)
		  #plt.savefig("Graph.png", format="PNG")
      print "Graph-Flow at the moment --> ", G1.edges(data=True)
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
  def _handle_PacketIn (self, event):
    global List_of_Sources
    packet = event.parsed
    port = event.port     #To pass
    S = str(packet.src)
    h_s = S[16]
    host_s = Host_Dictionary [int(h_s)]
    #print "Source host", host_s
    if host_s in List_of_Sources:
		return
    D = str(packet.dst)
    h_d = D[16]
    host_d = Host_Dictionary [int(h_d)]
    print "host_d = Host_Dictionary [int(h_d)] is --> ", host_d
    src_switch = mac_map[str(packet.src)][0]
    if host_s not in List_of_Sources:
		List_of_Sources.append(host_s)
		l2_multi().proactive1_install(mac_map[str(packet.src)], mac_map[str(packet.dst)], port, host_s, host_d, src_switch, packet)
		return
  #--------------------------------------------------------------------------------------
  def flow_G (self, port, host_s, host_d, src_switch, packet, path):
    #global current_p
    global List_of_Sources
    global G1
    global Switch_Dictionary
    global Host_Dictionary
    global Port_Dictionary
    global Flow_global_view
    L =[]
    SW = []
    Temp_link_to_G1 = []
    Traffic = []   # The list represents the type of traffic on each link whether ICMP, UDP or TCP, it can can multiple ones.
    MM = True
    #packet = event.parsed
    #por = event.port #this is the event port
    #print "packet.src=", str(packet.src), " packet.dst=", packet.dst
    #S = str(packet.src)
    #print "Source ", S
    #print "Port", por
    #print "Port_Dictionary", Port_Dictionary[por]
    prt = Port_Dictionary[port]
    #src_switch = mac_map[str(packet.src)][0]
    #print "initial source switch", Switch_Dictionary[src_switch]
    #current_switch = Switch_Dictionary[self.dpid]
    #print "current_switch", current_switch
    #print "Port_Dictionary", prt
    #h_s = S[16]
    #print h_s
    #host_s = Host_Dictionary [int(h_s)]
    #print "Source host", host_s
    #D = str(packet.dst)
    #print "Destination ", D
    #h_d = D[16]
    #host_d = Host_Dictionary [int(h_d)]
    #print "Destination host", host_d
    #Make  host_s and  host_d as tuple, ex: -->  ('h1','h2')
    '''
    pair = [host_s, host_d]
    print "the pair is", pair 
    
    for x in Flow_global_view.keys():
		if set(x) == set(pair):
			#print "the path already exists, probably the reversed path..."
			MM = False
    '''
    #---------------------------------------------------------------------------------------
    #The following procedure is to capture the first k-packets of the new arrival flow
    #if current_switch == Switch_Dictionary[src_switch] and bool (Flow_global_view) == False:
		#print "We are registering the initial packets of first flow only..."
		#x= "s1"
		#y = "eth1"
		#print "################## CREATING A PCAPNG FILE ##################"
		#print "####################################################################"
    print "the switch is", Switch_Dictionary[src_switch], "the port is", prt
    cmd =('tshark -c 2 -w monitor_rtp.pcapng -i'+Switch_Dictionary[src_switch]+ '-' +prt)
    t = threading.Thread(target=os.system, args=(cmd,))
    t.start()
    if os.stat('/home/mininet/pox/monitor_rtp.pcapng').st_size != 0:
		 print "*************** Monitoring File is not Empty ***************"
		 print "####################################################################"
    core.callDelayed(20, self.check, port, host_s, host_d, src_switch, packet, path)
    '''
    if packet.find("icmp") != None:
		print "The IP Protocol of the arrival packet is ICMP"
		pkt_type = 'ICMP'
    #if packet.find("udp") != None:
		#print "The IP Protocol of the arrival packet is UDP"
		#pkt_type = 'UDP'
    #-------------------------------------------------------------------------------
    # Add the computed path to the Flow_Graph (monitoring)
    #if not tuple(pair) in Flow_global_view:
    Marker = False
    if bool (Flow_global_view) == True:
		print "The dict is not empty..."
		Traffic.append(pkt_type)
		for x in Flow_global_view.keys():
			print 'x', x
			print 'pair', pair
			if set(x) == set(pair):
				print "the path already exists, probably the reversed path..."
				Marker = True
		if Marker == False:
			print "We have got a new path to add ..."
			for i in range (len(path)):
				SW.append(Switch_Dictionary[path[i]])
				#print "The path as switches is: ", SW
			L = SW #path
			L.insert(0,pair[0])
			L.insert(len(L),pair[1])
			Flow_global_view [tuple(pair)] = L #SW #path
			print (Flow_global_view)
			#print "#2 The whole path from host to host is", L
			for pair in self.pairwise(L):
				Temp_link_to_G1.append(pair)
			print Temp_link_to_G1
			#for i in range (len(Temp_link_to_G1)):
			for i in Temp_link_to_G1:
				if G1.has_edge(i[0], i[1]) == True:
					xxx = []
					#yyy = []
					print "The link", i, "is already exist in G1"
					G1[i[0]][i[1]]['weight'] = G1[i[0]][i[1]]['weight'] + 1
					xxx.append(pkt_type)
					G1[i[0]][i[1]]['Traffic'] = G1[i[0]][i[1]]['Traffic'] + xxx
				if G1.has_edge(i[0], i[1]) == False:
					G1.add_edge(i[0],i[1], weight = 1, Traffic = Traffic)  #weight =1 for the new links 
			#G1.add_edges_from(Temp_link_to_G1)
			#fig = plt.figure()
			#fig.canvas.set_window_title("The Current View of Abilene Flow")
			#pos = nx.spring_layout(G1, scale=2)
			#edge_labels = gx.get_edge_attributes(G1, 'Traffic')
			#gx.draw_networkx_edge_labels(G1, pos, edge_labels)
			#gx.draw_networkx(G1, with_labels = True, nodecolor='r', edge_color='b')
			#plt.show()
			#plt.savefig("Graph.png", format="PNG")
    if bool (Flow_global_view) == False:
		#print "The dict is empty now ..."
		Traffic.append(pkt_type)
		for i in range (len(path)):
			SW.append(Switch_Dictionary[path[i]])
			#print "The path as switches is: ", SW
		L = SW #path
		L.insert(0,pair[0])
		L.insert(len(L),pair[1])
		Flow_global_view [tuple(pair)] = L #SW #path
		print (Flow_global_view)
		#print "#1 The whole path from host to host is", L
		for pair in self.pairwise(L):
			Temp_link_to_G1.append(pair)
		print Temp_link_to_G1
		G1.add_edges_from(Temp_link_to_G1, weight=1, Traffic = Traffic) # add the links of the computed path to G1 with Weight = 1 (initial case)
		#fig = plt.figure()
		#fig.canvas.set_window_title("The Current View of Abilene Flow")
		#pos = nx.spring_layout(G1, scale=2)
		#edge_labels = gx.get_edge_attributes(G1, 'Traffic')
		#gx.draw_networkx_edge_labels(G1, pos, edge_labels)
		#gx.draw_networkx(G1, with_labels = True, nodecolor='r', edge_color='b')
		#gx.draw_networkx(G1)
		#plt.savefig("Graph.png", format="PNG")
    print "Graph-Flow at the moment --> ", G1.edges(data=True)	
	#if not tuple(pair) in Flow_global_view :
		#Flow_global_view [tuple(pair)] = path
		#print (Flow_global_view)
    #for j in Flow_global_view.keys():
			#print 'x', x
			#print 'pair', pair
			#if set(j) == set(pair):
				#if  j[1] == pair[0] and current_switch == Switch_Dictionary[path[-1]]:
					#print "*********************Meet the condition***********************"
    #core.callDelayed(20, self.check, pair) # You can just tack on args and kwargs
					#if os.stat('/home/mininet/pox/monitor_rtp.pcapng').st_size != 0: 
						#print "********************* The monitor_rtp.pcapng file is not empty *********************"
						#core.callDelayed(10, self.check, pair) # You can just tack on args and kwargs.
						#scheduler.enter(10, 1, self.check, (pair,))
						#scheduler.run()
						# Re-Activate ------------------------------------
						#t2 = threading.Thread(target=self.check, args=(pair,))
						#t2.start()
						#-------------------------------------------------
						#if t.is_alive() == False:
						    #print "&&&&&&&& Thread1 is not alive now &&&&&&&& "
						
						
		#t2 = threading.Thread(target=self.check, args=(pair,))
		#t2.start()
    #thread.start_new_thread(self.check(pair), ())
   '''
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
  def disconnect (self):
    if self.connection is not None:
      log.debug("Disconnect %s" % (self.connection,))
      self.connection.removeListeners(self._listeners)
      self.connection = None
      self._listeners = None

  def connect (self, connection):
    #print "type(conection.dpid)=", type(connection.dpid)
    if self.dpid is None:
      self.dpid = connection.dpid
    assert self.dpid == connection.dpid
    if self.ports is None:
      self.ports = connection.features.ports
    self.disconnect()
    log.debug("Connect %s" % (connection,))
    self.connection = connection
    self._listeners = self.listenTo(connection)
    self._connected_at = time.time()

  def _handle_ConnectionDown (self, event):
    self.disconnect()
    
  def _handle_FlowRemoved (self, event):
	  global Flow_global_view
	  global Host_Dictionary
	  global G1
	  pair = []
	  Indicator = False
	  print "Flow is removed ... "
	  #print ("Flow removed on switch", (event.dpid))
	  #print (event.ofp.match.dl_src, event.ofp.match.dl_dst)
	  s = str(event.ofp.match.dl_src)
	  d = str(event.ofp.match.dl_dst)
	  h_s = s[16]
	  h_d = d[16]
	  host_s = Host_Dictionary [int(h_s)]
	  host_d = Host_Dictionary [int(h_d)]
	  #print "host source is", host_s
	  #print "host destination is", host_d
	  pair.append(host_s)
	  pair.append(host_d)
	  pair = tuple (pair)
	  print "the pair is ", pair
	  print "the dictionary of Flow_global_view is: ", Flow_global_view
	  if bool (Flow_global_view) == True:
		  for x in Flow_global_view.keys():
			  if set(x) == set(pair):
				  print x, "equals", pair
				  print "G1.edges()", G1.edges()
				  Len_pairs = self.pairwise(Flow_global_view.get(pair))
				  print "the lenght of pairs is ", len(Len_pairs)
				  j =1
				  for i in self.pairwise(Flow_global_view.get(pair)):
					  print i
					  print "weight before update", G1[i[0]][i[1]]['weight']
					  print "traffic before update", G1[i[0]][i[1]]['Traffic']
					  G1[i[0]][i[1]]['weight'] = G1[i[0]][i[1]]['weight'] - 1
					  print "weight after update", G1[i[0]][i[1]]['weight']
					  if G1[i[0]][i[1]]['weight'] == 0:
						  Indicator = True
						  print "The link ", i, "is removed from the FLow Graph G1"
						  G1.remove_edge(i[0], i[1])
						  if j < 7:
							  G1.remove_node(i[0])
						  if j ==7:
							  G1.remove_node(i[0])
							  G1.remove_node(i[1])
						  #G1.remove_node(i[1])
						  print "The node of G1 are ...", G1.nodes()
						  j+=1
					  if j == 7 and Indicator == True:
						  print ("Removing from Flow_global_view")
						  del Flow_global_view [x] 
	  '''				  
	  if Indicator == True:
		  #print "the dictionary of Flow_global_view is: ", Flow_global_view
		  del Flow_global_view [x] # This means that the edges of this end-points were removed in the previous step
	  '''
	  #print "Graph Edges", G1.edges()
	  
	  #if x not in Flow_global_view:
		  #fig = plt.figure()
		  #fig.canvas.set_window_title("The Current View of Abilene Flow")
		  #gx.draw_networkx(G1)
		  #plt.savefig("Graph.png", format="PNG")	  
		  
  '''
  def _handle_FlowRemoved (self, event):
    #log.debug("Flow removed on switch %s", dpidToStr(event.dpid))
    print "Flow entry has been removed ... "
    #flow = event.ofp
    #log.info("flow: src %s dst %s",flow.match.nw_src, flow.match.nw_dst)
    #print event.__dict__() # to get available info
  '''    
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class l2_multi (EventMixin):
  global Links_weight_Dictionary
  global mac_map
  global counter
  global G

  def __init__ (self):
     #context = zmq.Context.instance()
     #self.socket = context.socket(zmq.PUB)  # Set up the ZMQ publisher "socket"
     #self.socket.bind(PUB_URL)
     #self.scheduler = sched.scheduler(time.time, time.sleep)
     # Listen to dependencies
     def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
      #core.openflow.addListeners('FlowRemoved', 'handle_flow_removal')
     core.call_when_ready(startup, ('openflow','openflow_discovery'))
     print "init completed"
  #-------------------------------------------
  def _handle_ConnectionUp (self, event):
      sw = switches.get(event.dpid)
      if sw is None:
        # New switch
        sw = Switch()
        switches[event.dpid] = sw
        sw.connect(event.connection)
        myswitches.append(event.dpid)
      else:
        sw.connect(event.connection)
    #------------------------------------------- 
  def pairwise(self,iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
    #------------------------------------------- 
  def proactive1_install(self, sorc, dest, port, host_s, host_d, src_switch, packet):
	  print "I'm the proactive function"
	  eth_sr = ""
	  eth_ds = ""
	  p = _get_raw_path (sorc[0], dest[0])
	  #p = [1,2,6,8,7,9]
	  rev_p = p[::-1]
	  #print "The path is", p
	  print "The reversed path is", rev_p
	  for key, value in mac_map.items():
		  #print "The key is", key
		  if dest[0] == value[0]:
			  eth_ds = key
			  print "The eth_ds is", eth_ds
		  if sorc[0] == value[0]:
			  eth_sr = key
			  print "The eth_sr is", eth_sr
	  in_ports = []
	  out_ports = []
	  src = p[0]
	  dst = p[-1]
	  print "dest_mac is", dest
	  dst_mac = "00:00:00:00:00:02"
	  print "Source node is", src
	  print "Destination node is", dst
	  for pair in self.pairwise(p):
		  print (pair)
		  out_ports.append(adjacency[pair[0]][pair[1]])
	  out_ports.insert(len(out_ports),1)
	  for pair in self.pairwise(rev_p):
		  in_ports.append(adjacency[pair[0]][pair[1]])
	  in_ports.insert(len(in_ports),1)
	  for i in range (len(p)):
		  msg = nx.nx_flow_mod()
		  msg.priority = 10
		  msg.idle_timeout = 100
		  #msg.hard_timeout = 0
		  msg.match.of_eth_src = EthAddr(eth_sr) #("00:00:00:00:00:01")
		  msg.match.of_eth_dst = EthAddr(eth_ds) #("00:00:00:00:00:02")
		  msg.actions.append(nx.nx_action_dec_ttl())
		  msg.actions.append(of.ofp_action_output(port = out_ports[i]))
		  core.openflow.sendToDPID(switches[p[i]].dpid, msg)
		  print "-------Path Has Been Installed-------"
		  #-------------------------------------------------------------
	  for i in range (len(p)):
		  msg = nx.nx_flow_mod()
		  msg.priority = 10
		  msg.idle_timeout = 100
		  #msg.hard_timeout = 10000
		  msg.match.of_eth_src = EthAddr(eth_ds) #("00:00:00:00:00:02")
		  msg.match.of_eth_dst = EthAddr(eth_sr) #("00:00:00:00:00:01")
		  msg.actions.append(nx.nx_action_dec_ttl())
		  msg.actions.append(of.ofp_action_output(port = in_ports[i]))
		  core.openflow.sendToDPID(switches[rev_p[i]].dpid, msg)
		  print "-------Reversed Path Has Been Installed-------"
	  Switch().flow_G(port, host_s, host_d, src_switch, packet, p)
  #--------------------------------------------  
  #def _handle_FlowRemoved (self, event):
	  #print "Flow is removed ... "
	  #log.debug ("Flow removed on switch %s", dpidToStr(event.dpid))
      #log.debug("Got FlowRemoved: %s", event.connection)
  #---------------------------------------------------------------------  
  def _handle_LinkEvent(self, event):
        #global current_p
        global C
        #csv1 = open(Failure_events, "a")
        l = event.link
        sw1 = l.dpid1
        sw2 = l.dpid2
        pt1 = l.port1
        pt2 = l.port2
        G.add_node( sw1 )
        G.add_node( sw2 )
        print "switch--", sw1, "port: ", pt1, "port:", pt2, "--switch", sw2

        no_edges=0
        for p in myswitches:
          for q in myswitches:
             if adjacency[p][q]!=None:
               no_edges+=1
        print "number of edges=", (no_edges*0.5)
        #print "current_p=", current_p

        #if len(myswitches)==37 and (no_edges*0.5) ==56:
           #if event.removed:
              #print sw1, "----", sw2, " is removed"
           #clear = of.ofp_flow_mod(command=of.OFPFC_DELETE)
           #for dpid in current_p:
             #if switches[dpid].connection is None: continue
             #switches[dpid].connection.send(clear)

        if event.added:
            #print "link is added"
            if adjacency[sw1][sw2] is None:
              adjacency[sw1][sw2] = l.port1
              adjacency[sw2][sw1] = l.port2
              G.add_edge(sw1,sw2)

        if event.removed:
            #print "link is removed"
            try:
                if sw2 in adjacency[sw1]: del adjacency[sw1][sw2]
                if sw1 in adjacency[sw2]: del adjacency[sw2][sw1]
                G.remove_edge(sw1,sw2)

                #record the failed links
                #KK = []
                #KK.append(sw1)
                #KK.append(sw2)
                #ZZ3 = tuple(KK)
                #row1 =  str(ZZ3) + " && " + str(datetime.datetime.now()) + "\n"
                #csv1.write(row1)
            except:
                print "remove edge error"
        try:
            #print nx.shortest_path(self.G,2,33)

             N= gx.number_of_nodes(G)
             print "Number of nodes in the current graph is: ", N
             E= gx.number_of_edges(G)
             print "Number of Edges in the current graph is: ", E

             #if (N == 14) and (E == 21) and (C == 0):    #Janos-US
                 #C+=1
                 #self.proactive1_install()
                 
             ''' 
                 print "Graph is ready now :-) "
                 print "Graph nodes are: ",G.nodes()
                 print "Graph edges are:", G.edges()
                 #------------------------------------
                 # Now we will assign the links weight to every edge in G
                 Edges = G.edges()
                 # Now we will assign the links weight to every edge in G
                 #if counter ==1:
                 for i in range (nx.number_of_edges(G)):
                         #print Links_weight_Dictionary[Edges[i]]
                         G[Edges[i][0]][Edges[i][1]]['weight'] = Links_weight_Dictionary[Edges[i]]
             ''' 
                 #for i in range (nx.number_of_edges(G)):
                        #print G.get_edge_data(Edges[i][0],Edges[i][1])
                        #print
                 #   counter+=1
                 #------------------------------------

                 #nx.draw(self.G, with_labels=True)
                 #plt.show()

        except:
            print "no such complete Graph yet..."
    #-------------------------------------------
    
def launch ():
    core.registerNew(l2_multi)
    #core.openflow.addListenerByName("FlowRemoved", _handle_FlowRemoved)
    core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received)
    # timer set to execute every five seconds
    Timer(10, _timer_func, recurring=True)
