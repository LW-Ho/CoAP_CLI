import logging
log = logging.getLogger("Node Information")

import struct

def make_from_bytes(cls, mote, data):
    packet_format = [
        "<xx",  # start_flag
        "B",    # packet_tcflow
        "x",   # alignment_padding[1]
        "I",    # start_asn
        "I",    # end_asn
        "I",    # event_counter
        "B",    # event_threshold
        "xxx",  # alignment_padding[3]
        "I",    # event_threshold_last_change
        "I",    # packet_counter
        "cc",   # parent_address
        "H",    # rank
        "H",    # parent_link_etx
        "h",    # parent_link_rssi
        "xx",   # end_flag[2]
        "xx",   # end_alignment_padding[2]
    ]
    packet_format_str = ''.join(packet_format)
    packet_item = struct.unpack(packet_format_str, data)
    mote_data = MoteData(
        mote=mote,
        packet_tcflow=packet_item[0],
        start_asn=packet_item[1],
        end_asn=packet_item[2],
        event_counter=packet_item[3],
        event_threshold=packet_item[4],
        event_threshold_last_change=packet_item[5],
        packet_counter=packet_item[6],
        parent_address="".join("{:02x}".format(ord(c)) for c in packet_item[7:9]),
        rank=packet_item[9],
        parent_link_etx=packet_item[10],
        parent_link_rssi=packet_item[11],
    )
    
    return mote_data
