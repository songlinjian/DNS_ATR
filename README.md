# DNS_ATR
Draft and test script of DNS ATR(Additional Truncated Response )

Note the script directory contains two python scripts listening on both TCP and UDP. They can work as a proxy demo of ATR which sits between resolver and authoritative servers. The ATR function is implemented in DNS UDP forwarder which send additional truncated response according to a fixed size 1220 octets. The DNS TCP forwarder can receive the query after the resolver fall back to TCP.
