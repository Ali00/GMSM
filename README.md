# GMSM-Graph-Modeling-for-SDN-Monitoring

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/170258380-fcb0a9ad-43ce-4458-bb1a-4cec222107ed.png" width="400" height="400"/>
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

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `If you use this framework or any of its code in your work then, please cite the following publication: "Smart routing: Towards proactive fault handling of software-defined
