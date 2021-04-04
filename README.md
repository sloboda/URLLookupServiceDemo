# README Draft response

Web Service Demo

*NOTE*: This is demonstration software. Do not use this in any production
service.

## Assignment

We have an HTTP proxy that is scanning traffic looking for malware URLs. Before allowing HTTP connections to be made, this proxy asks a service that maintains several databases of malware URLs if the resource being requested is known to contain malware.

Part 1: Write a small web service that responds to GET requests where the caller passes in a URL and the service responds with some information about that URL. The GET requests would look like this:

```
  GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}
```

The caller wants to know if it is safe to access that URL or not. As the implementer you get to choose the response format and structure. These lookups are blocking users from accessing the URL until the caller receives a response from your service.

Part 2: As a thought exercise, please describe how you would accomplish the following:

* The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system?
* Assume that the number of requests will exceed the capacity of a single system, describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe.
* What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes.
* You’re woken up at 3am, what are some of the things you’ll look for?
* Does that change anything you've done in the app?
* What are some considerations for the lifecycle of the app?
* You need to deploy a new version of this application. What would you do?


# Part 1

## Assumptions

1. The caller wants to know if there is malware at that URL or not. So, I'm
   going to use *MALWARE_AT_THAT_HOST_AND_URL* and *NO_MALWARE_AT_THAT_HOST* as response values.
2. I'm not sure I can trust a `$KNOWN_SAFE_ORIGINAL_PATH_AND_QUERY_STRING`
   on a `$KNOWN_MALWARE_HOSTNAME_AND_PORT`. Can any path be designated safe from
   malware if the host providing that path has been known to hand out malware?
   I assume no.
3. Nothing on this exercise says "Use this set of criteria to determine SAFE
   from MALWARE." I assume some other "URL qualification service" exists. When
   my "URL lookup service" encounters `$COMPLETELY_NEW_HOSTNAME_AND_PORT` with
   `$COMPLETELY_NEW_PATH_AND_QUERY_STRING`, the agreed action is my service
   defines these values as *NO_MALWARE_AT_THAT_HOST*.  My service does not
   initiate any sort of qualification to start checking that new URL for malware.
4. I assume I can claim the '1' in `GET /urlinfo/1/` as my version number one for
   this web service.
5. Storing a colon in hostname:port as a key instead of `%3A` is probably okay.
   See https://stackoverflow.com/q/2053132/5978252
6. REVISION. To avoid building a database of the entire Internet web space
   (Good, Bad, and Unknown_so_in_evaluation_state), I am revising the scope so
   that there's two types of URLs:
   1. `$KNOWN_MALWARE_HOSTNAME_AND_PORT`/`$KNOWN_MALWARE_ORIGINAL_PATH_AND_QUERY_STRING`
   2. Anything else.
   As in, if it's not pulled from the database as a match, this service lets it
   pass. We only track bad URLs and everything else is okay.

## Tests

What am I testing?

Test for the following:

1. `$KNOWN_MALWARE_HOSTNAME_AND_PORT`/`$KNOWN_MALWARE_ORIGINAL_PATH_AND_QUERY_STRING` returns
   *MALWARE_AT_THAT_HOST_AND_URL*.
2. Anything else returns 200 OK. I did not find it in my database of malware, so
   it must be safe. Go ahead. (Note the dangers with this approach!) Verify this
   with two different non-malware URLs.

## Set up

### Prerequisites

This web service demonstration assumes the following prerequisites are
installed:

* Python 3
* virtualenv (called *venv* in Python 3).
    * A virtual environment ensures the Python interpreter, libraries and
    scripts installed into it are isolated from those installed in other
    virtual environments. This allows staff to work on multiple projects with
    divergent dependencies.
* python modules defined in `requirements.txt`
    * Flask - python web framework
    * requests - issue requests to the web framework.

### Installation

1. Clone this git repository to `URLLookupServiceDemo/`
2. `cd` to the directory `URLLookupServiceDemo/`
3. Create a virtual environment


For testing:

* pylint - provides static code analysis and syntax error checking.
* pytest - provides automated testing
* [curl](https://curl.se/)
* [Postman](https://www.postman.com/) - I have used Postman for REST api testing.

## How to test

Details here on how to perform all the tests identified above.

Test non-malware URLs:
```
curl -i "http://localhost:5000/urlinfo/1/en.wikipedia.org:443/wiki/The_Order_of_the_Stick"
curl -i "http://localhost:5000/urlinfo/1/www.google.com:443/search?q=kermit+the+frog&tbm=isch"
```


# Future Considerations

A non-exclusive list of items to address in the future.

1. Logging
    * Log for performance improvements. Log when a request is received, when a
      response is set, which parts take the longest time.
    * Log for caching. Are some hostnames requested more often (google.com) and
      others rarely requested?
    * Log for globalization and internationalization. Client IPs hitting this
      service are most likely only the HTTP proxy. Logging time stamps will help
      globalization efforts in at least two ways:
      1. Correlating requests from upstream clients. The proxy may have
         geolocation details that will indicate where most clients are. This
         suggests where to expand first: Australia, Europe, North America, et cetera.
      2. Time of day. If 90% of requests are coming during North America
         business hours, that implies North America business traffic.
2. Security
    * There's no authentication on this app. Any client that can access this web
      service can feed it requests and skim off the databases of malware URLs,
      initiate a Denial Of Service attack, or other attacks. Some sort of token
      or authentication would be required for a production service.
    * There's no encryption on the content. Set up TLS to prevent packets from
      being read between client and this service.
3. Monitoring
    * Runscope or some other sort of API web service monitoring would provide
      metrics. This would help improve performance and guarantee achievement of
      SLAs. Uptime and performance data would help sales.
    * Runscope would also be able to detect if the performance degraded or
      failed, and send an alert to a team member on call.
    * Assuming this web service is wildly successful and scaled out globally,
      some sort of monitoring would help not only for service degradation but to
      estimate failover performance. E.g. Monitoring Europe, Asia and North
      America from North America will let staff get a sense of service response
      times from Europe to North America if the NA services all failed.
    * This API might not be able to be monitored by a Software As A Service
      vendor. I would not go into production without some form of monitoring. If
      you cannot monitor it, you cannot measure it, you cannot manage it.
4. Caching
    * Performance both at the proxy server making requests to this URL lookup
      service and the URL lookup service will improve if the proxy may cache
      responses.
    * A duration for the cache should be established and evaluated.
    * I'd expect to run this for a period of time and gather real world evidence
      about how many responses should be cached, and for how long.
5. Replace FQDN hostnames with IP addresses
    * It's common for companies to have multiple hostnames point to a single IP
      address. When I worked as a web site manager there were over fifty
      variants of the company name assigned to the same load balancer IP
      address.
    * Hostnames are able to be changed faster than IP addresses. Hostname edits
      require a change to DNS. IP address ownership changes require registrars
      and money.
    * Attaching malware URLs to IP addresses will result in less churn within
      the databases of malware URLs.
    * There's a performance hit to doing a DNS lookup on a hostname. The time
      spent looking up and storing an IP is going to pay off later in reducing
      the size of the hostname database.
6. Replace hash table with sqlite3. Replace sqlite3 with redis key-value stores
      when things are very large scale.
7. Replicate for high volume reads and fewer writes
    * This service is lopsided in that the unnamed service providing new URL
      updates (what I'm calling the "URL qualification service") might provide
      five thousand URLs a day with updates arriving every ten minutes. That is
      minuscule compared with millions of reads every second from global HTTP
      proxies.
    * Writes would go to a master at the top of the tree, and be pushed
      down to numerous replicas the URL lookup service treats as read-only. I
      know LDAP services support this kind of "optimized for massive reads"
      configuration. I believe redis does, but I'd want to confirm.
8. Sharding
    * With this demo, all values are stored in one database.
    * Some hostnames (google.com) will be requested more than others. Monitoring
      will demonstrate which 10% of hostnames make up 90% of the requests.
    * If the service is refactored to store IP addresses, the databases could be
      sharded by IP octets. The top 10% hosts, the hosts that our proxy
      service queries for the most often with the most reads,
      they get their own dedicated shard. Logging and monitoring will tell us
      which hosts these are.
9. Many additional questions about the "URL qualification service" that fills
   the databases used by my "URL lookup service"
    * How long does it take for a new URL to be designated as KNOWN_MALWARE?
    * Once designated as SAFE, how long until the URL is checked again?
    * Once designated as KNOWN_MALWARE, how long until the URL is checked again?
    * Is it possible for a URL once designated KNOWN_MALWARE to clean up and be
      designated SAFE?
    * Potentially if this time interval between checks is short, I would need
      another state `FLAPPING` as the URL switches from KNOWN_MALWARE to SAFE and
      back again.
    * If the URL is never checked again once it is designated SAFE or
      KNOWN_MALWARE, how do customers know this database of malware URLs is
      current and correct?




# Part 2

As a thought exercise, please describe how you would accomplish the following:

* The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system?
    * sqlite3 database
    * redis
    * Sharding the database. Split the terms read most often to their own dedicated node.
    * Timestamp the database entries and review/move to cold storage/remove the
      oldest. Do bad URLs stay alive forever? Do they stay bad forever?
* Assume that the number of requests will exceed the capacity of a single system, describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe.
    * Put the service behind a load balancer
    * Work with a cloud provider for global replication across regions
    * Rework the service for a docker container and use kubernetes to scale response
      to demand.
* What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes.
    * Scale out the read databases and have them fed from a master which takes writes.
* You’re woken up at 3am, what are some of the things you’ll look for?
    * Details from whatever woke me up. This will steer further investigation.
    * Logs produced by urlinfo service
    * Logs produced by the http proxy calling urlinfo service
    * Runscope API reports
* Does that change anything you've done in the app?
    * Logging is missing and needs to be added
* What are some considerations for the lifecycle of the app?
    * The `/1/` in the URL is already a version indicator. Rolling out version two
    involves creating `/urlinfo/2/` This allows new clients to use the new version
    and old clients to continue using version 1.
    * When it comes to decommissioning version 1, my team can announce to our
    customers a decommission deadline. Once logs show absolutely no one has
    requested from this version for NNN days past the deadline, we can edit the
    code to respond with 308 Permanent Redirect to force clients to move to
    version 2. Alternatively the version 1 could be removed which would cause
    clients to get a hard fail.
* You need to deploy a new version of this application. What would you do?
    * The `/1/` in the URL is already a version indicator. Rolling out version two
    involves creating `/urlinfo/2/` This allows new clients to use the new version
    and old clients to continue using version 1.

