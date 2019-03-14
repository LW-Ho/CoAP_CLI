import logging
log = logging.getLogger("moteData")

import upload_data_requests

import struct
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class MoteData(Base):
    __tablename__ = 'mote_data'

    id = Column(Integer, primary_key=True)
    mote = Column(String(200))
    packet_tcflow = Column(Integer)
    start_asn = Column(Integer)
    end_asn = Column(Integer)
    event_counter = Column(Integer)
    event_threshold = Column(Integer)
    event_threshold_last_change = Column(Integer)
    packet_counter = Column(Integer)
    parent_address = Column(String(10))
    rank = Column(Integer)
    parent_link_etx = Column(Integer)
    parent_link_rssi = Column(Integer)
    gasValue = Column(Integer) # Gas Value 16bit.
    gasAlarm = Column(Integer) # Gas Alarm 8bit
    temperature = Column(Integer) # temp 16bit
    humidity = Column(Integer) # humi 16bit
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __str__(self):
        output = []
        output += ['mote    : {0}'.format(self.mote)]
        output += ['priority: {0}'.format(self.packet_tcflow)]
        output += ['startAsn: {0}'.format(self.start_asn)]
        output += ['endAsn  : {0}'.format(self.end_asn)]
        output += ['ec      : {0}'.format(self.event_counter)]
        output += ['et      : {0}'.format(self.event_threshold)]
        output += ['etlc    : {0}'.format(self.event_threshold_last_change)]
        output += ['pc      : {0}'.format(self.packet_counter)]
        output += ['parent  : {0}'.format(self.parent_address)]
        output += ['rank    : {0}'.format(self.rank)]
        output += ['p_etx   : {0}'.format(self.parent_link_etx)]
        output += ['p_rssi  : {0}'.format(self.parent_link_rssi)]
        output += ['s_Temp  : {0}'.format(self.temperature)]
        output += ['s_Humi  : {0}'.format(self.humidity)]
        output += ['s_GV  : {0}'.format(self.gasValue)]
        output += ['s_GA  : {0}'.format(self.gasAlarm)]

        return '\n'.join(output)

    @classmethod
    def make_from_bytes(cls, mote, data):
        packet_format = [
            "<xx",  # start_flag
            "B",    # packet_priority uiny8 ; 0
            "b",    # gas_Alarm int8 ; 1
            #"x",    # alignment_padding[1]
            "I",    # start_asn ; 2
            "I",    # end_asn ; 3
            "I",    # event_counter ; 4
            "B",    # event_threshold ; 5
            "xxx",  # alignment_padding[3]
            "I",    # event_threshold_last_change ; 6
            "I",    # packet_counter ; 7
            "cc",   # parent_address ; 8 9
            "H",    # rank ; 10
            "H",    # parent_link_etx ; 11
            "h",    # parent_link_rssi ; 12
            "h",    # gasValue  int16 ; 13
            "h",    # temperature int16 ; 14
            "h",    # humidity int16 ; 15
            "xx",   # end_flag[2] 
            #"xx",   # end_alignment_padding[2]
        ]
        packet_format_str = ''.join(packet_format)
        packet_item = struct.unpack(packet_format_str, data)
        mote_data = MoteData(
            mote=mote,
            packet_tcflow=packet_item[0],
            start_asn=packet_item[2],
            end_asn=packet_item[3],
            event_counter=packet_item[4],
            event_threshold=packet_item[5],
            event_threshold_last_change=packet_item[6],
            packet_counter=packet_item[7],
            parent_address="".join("{:02x}".format(ord(c)) for c in packet_item[8:10]),
            rank=packet_item[10],
            parent_link_etx=packet_item[11],
            parent_link_rssi=packet_item[12],
            temperature=packet_item[14],
            humidity=packet_item[15],
            gasValue=packet_item[13],
            gasAlarm=packet_item[1],
        )
        upload_data_requests.send(mote,packet_item[0],packet_item[14],packet_item[15],packet_item[13],packet_item[1])
        return mote_data
    
