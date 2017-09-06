# DNS_ATR
As the increasing use of DNSSEC and IPv6, there are more public evidence and concerns on IPv6 fragmentation issues due to larger DNS payloads over IPv6. This memo introduces an simple improvement on authoritative server by replying additional truncated response just after the normal large response.

This repo contains the draft and test script of DNS ATR (Additional Truncated Response). Note the script directory contains two python scripts listening on UDP and TCP respectively. They work as a proxy demo of ATR which sit between resolver and authoritative servers. The ATR function is implemented in DNS UDP forwarder which sends additional truncated response with atr_size: 1220 octets. The DNS TCP forwarder can receive the query after the resolver fall back to TCP.
