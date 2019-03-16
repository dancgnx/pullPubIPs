#!/usr/bin/env python
# Import CloudGenix SDK
import cgxinit
import cloudgenix
import sys
import os
import json


# create CGX SDK opbject
cgx = cgxinit.go()

# authenticate to CGX


jd=cgx.interactive.jd
jd_detailed=cloudgenix.jd_detailed

#print header
print("{site},{element},{ipaddress},{nat},{itype}".format(site="Site Name",element="Device Name",ipaddress="IP address",nat="NAT IP address",itype="Type of address"))
# get sites table
res = cgx.get.sites()
if not res:
    jd_detailed(res)
    sys.exit()

# create a site dictionary to translate a site ID to a site name
# the object returned from the cgx.get.sites() function contain cgx_content item.
# cgx_content contains a disctinary that contains the sites object. Inside that dictionary,
# there an list called "itmes". That list contain all the sites
sites={}
for site in res.cgx_content["items"]:
    sites[site["id"]] = site["name"]

# iterate on all elements (CGX devices are called elements in the API)
for element in cgx.get.elements().cgx_content["items"]:
    if element["site_id"] in ["0","1"]:
        #the element is unassigned to a site we should skipp it
        continue
    element_name = element["name"]
    site_id = element["site_id"]
    element_siteName = sites[site_id]
    element_id = element["id"]
    #iterate on all interfaces
    # check if element is valid and has interfaces
    interfaces = cgx.get.interfaces(site_id,element_id)
    if interfaces:
        for interface in interfaces.cgx_content["items"]:
            # check if the interface is a Internet interface
            if interface["used_for"] == "public":
                # check if pppoe
                if interface["type"] == "pppoe":
                    interface_type="dynamic"
                elif not interface["ipv4_config"]:
                    # the interface isn't configured we shell skip it
                    continue
                # check if we have a static ip address
                elif interface["ipv4_config"]["type"] == "static":
                    #its a static address
                    interface_ip = interface["ipv4_config"]["static_config"]["address"]
                    interface_type="static"
                else:
                    # its a DHCP address
                    interface_type="dynamic"

                # resolve dynamic address
                if interface_type == "dynamic":
                    # get interface status
                    interface_status = cgx.get.interfaces_status(site_id,element_id,interface["id"]).cgx_content
                    if interface_status["operational_state"] == "down":
                        interface_ip = "NA"
                    else:
                        #check for ipv4 address
                        if interface_status["ipv4_addresses"]:
                            interface_ip = interface_status["ipv4_addresses"][0]
                        elif interface_status["ipv6_addresses"]:
                            interface_ip = interface_status["ipv6_addresses"][0]

                #check if NAT is configured
                if interface["nat_address"]:
                    NAT = interface["nat_address"]
                else:
                    NAT= "NA"
                print("{site},{element},{ipaddress},{nat},{itype}".format(site=element_siteName,element=element_name,ipaddress=interface_ip,nat=NAT,itype=interface_type))


