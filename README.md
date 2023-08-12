# GMSM-Graph-Modeling-for-SDN-Monitoring

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://github.com/Ali00/GMSM/assets/12594727/b626bb0d-4e6e-4c4b-a32a-6ae00684c222" width="750" height="400"/>
      <figcaption><p align="center">Fig.1: GMSM Prototype</figcaption>
    </figure>
  </div>
</div>

 ### Network Framework:
The framework has been evaluated by the SDN emulator "Mininet": http://mininet.org/ with POX as a network operating system
(controller): https://github.com/noxrepo/pox/ 

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/170259341-ca574068-90b1-4b2b-967a-2401b4fc3257.png" width="300" height="300"/>
      <figcaption><p align="center">Fig.2: GMSM Framework</figcaption>
    </figure>
  </div>
</div>


### Network Topology: 
The network is modelled as an undirected graph G(V,E) by using the NetworkX tool, https://networkx.github.io/. To represent the data plane topology, Abilene network topology has been adopted from http://sndlib.zib.de/home.action. 6 clients are added to generate traffic and represent different class of services.

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/170260825-11c04c02-0f44-48b2-b4d2-5e04460dd57e.png" width="500" height="300"/>
      <figcaption><p align="center">Fig.3: Abilene Topology</figcaption>
    </figure>
  </div>
</div>


### Experimental Results: 

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/183019823-c55f98c8-29d6-4311-a864-c91af3eb4db1.png" width="500" height="300"/>
      <figcaption><p align="center">Fig.4: Evaluation of two different CoS flows: video and ICMP.
Information is captured from the {s 2 , s 6 } link of the Abilene topology. The channel capacity is 8Mbps. The video and ICMP flows traverse a common path (s 1 , s 2 , s 6 , s 8 , s 7 , s 9 ).</figcaption>
    </figure>
  </div>
</div>


<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/183020486-2997b944-d934-4ae2-abd6-ba8c20a8627b.png" width="500" height="250"/>
      <figcaption><p align="center">Fig.5: Network overhead measurement: the total number of
invoked OpenFlow messages are: 2578, 2735 and 2764 messages for
GMSM, active-flow and periodic monitoring respectively.</figcaption>
    </figure>
  </div>
</div>


<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/183020796-b388605c-2394-4639-ad0a-3682ff4f5e2e.png" width="500" height="300"/>
      <figcaption><p align="center">Fig.6: The count of OpenFlow stats request/reply packets per 1ms
versus time are illustrated when the monitoring function is set at 10s
intervals for GMSM, Active Flow and Periodic Monitoring. The □
represents the stats request and ♢ represents stats reply.</figcaption>
    </figure>
  </div>
</div>


<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/183021021-2c7d993f-b972-48c6-a82f-9e33cc96a6ca.png" width="350" height="150"/>
      <figcaption><p align="center">Fig.7: Number of switches used in monitoring: GMSM queries
the smallest number of switches vs periodic and active monitoring.</figcaption>
    </figure>
  </div>
</div>


```diff
- `If you use this framework or any of its code in your work then, please cite our IEEE Access publication:
+ "Graph Modeling for Openflow Switch Monitoring"`
 ```

 https://ieeexplore.ieee.org/abstract/document/10213403
