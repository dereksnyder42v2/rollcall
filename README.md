# rollcall
Attempt to simplify management of IoT devices in a home network.  
(do I have to say it?...plz don't use this in professional settings...haha)  
  
Essentially, this kit maintains a table of IP addresses and hostnames. The table is updated by requesting the endpoint and specifying the ip and hostname in the query string, e.g.:  
<b>$ curl (address:port)/cgi-bin/rollcall.py?hostname=hal&ip=192.168.0.1</b>    
...would update the table entry for the hostname 'hal', and as a response, you would get a plaintext web page something like:  
  
<i>
OK<br />
(key),(val)<br />
hal,192.168.0.1<br />
</i>  
  
Why is my Redis server not running in docker??  
Comment out the 'bind' statement in /etc/redis/redis.conf

How do I flush my Redis DB?  
$ redis-cli flushall
