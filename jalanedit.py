#!/usr/bin/python

"""This example is based on this video: https://www.youtube.com/watch?v=_C4H2gBdyQY"""

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import os

def topology():
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    sta1 = net.addStation( 'sta1', wlans=2, ip='10.0.0.2/8', max_x=120, max_y=50, min_v=1.4, max_v=1.6 )
	sta2 = net.addStation( 'sta2', ip='10.0.0.3/8', position='40,35,0')
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    ap1 = net.addAccessPoint( 'ap1', ssid='ssid_ap1', mode= 'g', channel=6, position='70,25,0' )
    ap2 = net.addAccessPoint( 'ap2', ssid='ssid_ap2', mode= 'g', channel=1, position='30,25,0' )
    ap3 = net.addAccessPoint( 'ap3', ssid='ssid_ap3', mode= 'g', channel=11, position='110,25,0' )
    s4 = net.addSwitch( 's4', mac='00:00:00:00:00:10' )
    c1 = net.addController( 'c1', controller=Controller )

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(ap1, s4)
    net.addLink(ap2, s4)
    net.addLink(ap3, s4)
    net.addLink(s4, h1)

    sta1.cmd('modprobe bonding mode=3')
    sta1.cmd('ip link add bond0 type bond')
    sta1.cmd('ip link set bond0 address 02:01:02:03:04:08')
    sta1.cmd('ip link set sta1-wlan0 down')
    sta1.cmd('ip link set sta1-wlan0 address 00:00:00:00:00:11')
    sta1.cmd('ip link set sta1-wlan0 master bond0')
    sta1.cmd('ip link set sta1-wlan1 down')
    sta1.cmd('ip link set sta1-wlan1 address 00:00:00:00:00:12')
    sta1.cmd('ip link set sta1-wlan1 master bond0')
    sta1.cmd('ip addr add 10.0.0.10/8 dev bond0')
    sta1.cmd('ip link set bond0 up')

    print "*** Starting network"
    net.build()
    c1.start()
    s4.start( [c1] )
    ap1.start( [c1] )
    ap2.start( [c1] )
    ap3.start( [c1] )

    sta1.cmd('ip addr del 10.0.0.2/8 dev sta1-wlan0')
	sta2.start()
    os.system('ovs-ofctl add-flow s4 actions=normal')

    """seed"""
    net.seed(12)

    """uncomment to plot graph"""
    net.plotGraph(max_x=140, max_y=140)
    
    "*** Available models: RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWaypoint, GaussMarkov ***"
    net.associationControl( 'ssf' )
	net.startMobility(startTime=0, model='RandomDirection')

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()