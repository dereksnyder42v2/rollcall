# rollcall
Attempt to simplify management of IoT devices in a home network.  
(do I have to say it?...plz don't use this in professional settings...haha)  
  
Essentially, this kit maintains a table of IP addresses and hostnames. The table is updated by requesting the endpoint and specifying the hostname in the query string, e.g.:  
<b>$ curl (address:port)/cgi-bin/rollcall.py?hostname=hal</b>    
...would update the table entry for the hostname 'hal', and as a response, you would get a .json something like:  
  
<b>
{<br />
    "table": {<br />
        "hal": "{\"IP\": \"10.0.0.201\", \"TIME\": \"2020-03-15 23:54\"}"<br />
    },<br />
    "errMsgs": [<br />
        "HOSTNAME invalid or not found"<br />
    ]<br />
}<br />
</b>  
<br /><br />  
Why is my Redis server not running in docker??  
Comment out the 'bind' statement in /etc/redis/redis.conf

How do I flush my Redis DB?  
$ redis-cli flushall
