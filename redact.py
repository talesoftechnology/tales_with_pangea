

from pangea.services import Redact

# include your API token here
redact = Redact(token="pts_6cbbz3ikyknt4ei7zkbp7nrq26hrg7x4")

info = {"Company Name" : "Tales of technology", 
        "Status" : "Active",
        "WAN IP Address" : "12.90.21.8",
        "Vendor" : "Cisco",
        "Customer Name" : "Christy H",
        "Phone Number" : "+1 (555)123-4567",
        "Email ID" : "christy02@mail.com",
        "Address" : "144 Main St. Lotus pond",
        "City" : "San Francisco",
        "State" : "California"}

config = {
"users"  : """
Users

{
    'mircea': {
        'level': 15,
        'password': '$1$0P70xKPa$z46fewjo/10cBTckk6I/w/',
        'sshkeys': [
            'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4pFn+shPwTb2yELO4L7NtQrKOJXNeCl1je
        ]
    }
}
""",
"routes" : """
Routes

{
    "1.0.0.0/24": [
        {
            "protocol"          : u"BGP",
            "inactive_reason"   : u"Local Preference",
            "last_active"       : False,
            "age"               : 105219,
            "next_hop"          : u"172.17.17.17",
            "selected_next_hop" : True,
            "preference"        : 170,
            "current_active"    : False,
            "outgoing_interface": u"ae9.0",
            "routing_table"     : "inet.0",
            "protocol_attributes": {
                "local_as"          : 13335,
                "as_path"           : u"2914 8403 54113 I",
                "communities"       : [
                    u"2914:1234",
                    u"2914:5678",
                    u"8403:1717",
                    u"54113:9999"
                ],
                "preference2"       : -101,
                "remote_as"         : 2914,
                "local_preference"  : 100
            }
        }
    ]
}
""",

"interfaces_info" : """
Interfaces information 

{
    u'FastEthernet8': {
        u'ipv4': {
            u'10.66.43.169': {
                'prefix_length': 22
            }
        }
    },
    u'Loopback555': {
        u'ipv4': {
            u'192.168.1.1': {
                'prefix_length': 24
            }
        },
        u'ipv6': {
            u'1::1': {
                'prefix_length': 64
            },
            u'2001:DB8:1::1': {
                'prefix_length': 64
            },
            u'2::': {
                'prefix_length': 64
            },
            u'FE80::3': {
                'prefix_length': u'N/A'
            }
        }
    },
    u'Tunnel0': {
        u'ipv4': {
            u'10.63.100.9': {
                'prefix_length': 24
            }
        }
    }
}
""",

"arp_table" : """
ARP Table

[
    {
        'interface' : 'MgmtEth0/RSP0/CPU0/0',
        'mac'       : '5C:5E:AB:DA:3C:F0',
        'ip'        : '172.17.17.1',
        'age'       : 1454496274.84
    },
    {
        'interface' : 'MgmtEth0/RSP0/CPU0/0',
        'mac'       : '5C:5E:AB:DA:3C:FF',
        'ip'        : '172.17.17.2',
        'age'       : 1435641582.49
    }
]
""",

"uptime": """
Uptime

"151005.57332897186"
"""
}
           


check_res = redact.redact_structured(config, debug=True)

print(check_res.raw_result["redacted_data"]["routes"])

