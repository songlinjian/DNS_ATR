#!/usr/bin/env python
# coding: utf-8

import ConfigParser
from gevent import monkey
from gevent.server import StreamServer
import dns.resolver
import dns.message
import dns.rrset
import dns.query
import struct
import socket
monkey.patch_all()
#import socket


# try dnspython module here
def dns_forward(dns_message, port=5353):
    ans = dns.query.tcp(dns_message, dns_default, port=port)
    # return a dns.message.Message object to wire format data

    print ans.question[0].name

    for i in ans.answer:
        print i.to_text()

    return ans


# read the DNS wireformat data and reply
def forward(data, addr, sock):
    dns_message = dns.message.from_wire(data)
    qname = dns_message.question[0].name
    qtype = dns_message.question[0].rdtype
    qclass = dns_message.question[0].rdclass
    # note: the id of the query(qid) should be record in case the query is hit
    # the cache. The id of the cached answer will be replace by this new qid
    qid = dns_message.id
    # check the cache
    #ans = DNSServer.cache.get((qname, qtype, qclass))
    # if cache miss
    #if ans is None:
    #    print 'Cache miss! Forward the query to ', dns_default
    dns_ans = dns_forward(dns_message)
    #ans = dns.resolver.Answer(qname, qtype, qclass, dns_ans)

    #    DNSServer.cache.put((qname, qtype, qclass), ans)
    #    print 'Cache max_size is :', DNSServer.cache.max_size
    #    print 'Cache len is :', len(DNSServer.cache.data)

    # if cache hit
    #else:
    #    print 'Cache hit! Good!!!'
    #    ans.response.id = qid

    dns_ans_wire = dns_ans.to_wire()
    s_len = len(dns_ans_wire)
    print s_len
    # 由主机字节序改成网络字节序
    # 用二进制数字构造2字节字符串
    two_byte = struct.pack("H", socket.htons(s_len))
    # print socket.ntohs(struct.unpack("h", two_byte)[0]) #反向操作等于s_len
    TCP_DNS_wire = '%s%s' % (two_byte, dns_ans_wire)

    #answers, soa = query(str(qname).rstrip('.'))
    #answer_dns = pack_dns(dns, answers, soa)

    # 将查询到的应答包放入LRUCache以后使用
    #DNSServer.dns_cache[qname] = dns_response_wire
    # 返回
    #sock.sendto(dns_response_wire, addr)

    sock.sendall(TCP_DNS_wire)


# def _init_cache_queue():
#     while True:
#         data, addr, sock = DNSServer.deq_cache.get()
#         print data
#         gevent.spawn(handler, data, addr, sock)


def handle(socket, address):
    # 接受数据
    print "receive a query from :", address
    wire_data = socket.recv(4096)
    # from RFC1035: The message is prefixed with a two byte length
    # field which gives the message length, excluding the two byte
    # length field.

    # ntohs 网络字节序转到主机字节序，16位
    # struct.unpack("H",  wire_data[:2]) 读取二进制字节 转变为short int
    # print socket.ntohs(struct.unpack("h", wire_data[:2])[0])
    wire_message = wire_data[2:]
    #print len(wire_message)
    # 缓存队列保存元组：(请求包，请求地址，sock)
    #DNSServer.deq_cache.put((wire_message, self.client_address[0], self.request))
    forward(wire_message, address, socket)


class DNSServer(object):
    @staticmethod
    def start():
        # 缓存队列，收到的请求都先放在这里，然后从这里拿数据处理

        #DNSServer.cache = dns.resolver.LRUCache(lru_size)

        # 启动DNS服务器，用gevent.server
        print 'Start DNS server at %s:%d\n' % (ip, port)
        dns_server = StreamServer((ip, port), handle)
        dns_server.serve_forever()


def load_config(filename):
    with open(filename, 'r') as fc:
        cfg = ConfigParser.ConfigParser()
        cfg.readfp(fc)

    return dict(cfg.items('DEFAULT'))


if __name__ == '__main__':
    # read the config file
    #config_file = os.path.basename(__file__).split('.')[0] + '.ini'
    config_file = 'config.ini'
    config_dict = load_config(config_file)

    ip, port = config_dict['ip'], int(config_dict['port'])
    deq_size, lru_size = int(
        config_dict['deq_size']), int(
        config_dict['lru_size'])
    db = config_dict['db']
    dns_default = config_dict['dns']

    # 启动服务器
    DNSServer.start()
