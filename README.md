# README response

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
   going to use *MALWARE_AT_THAT_HOST_AND_URL* and *NO_MALWARE_AT_THAT_HOST* as
   response values. These values are set in the dictionary `response_codes`.
   They may be tuned in consultation with the HTTP proxy service owners.
2. Nothing on this exercise says "Use this set of criteria to determine SAFE
   from MALWARE." I assume some other "URL qualification service" exists. When
   my "URL lookup service" encounters `$COMPLETELY_NEW_HOSTNAME_AND_PORT` with
   `$COMPLETELY_NEW_PATH_AND_QUERY_STRING`, the agreed action is my service
   defines these values as *NO_MALWARE_AT_THAT_HOST*.  My service does not
   initiate any sort of qualification to start checking that new URL for malware.
   I created test URLs (malware and non-malware) to prove this service would
   work. All of them are examples. Identifying malware is beyond the scope of
   this exercise.
3. I can prove the requested resource does not match any entry in the database
   of malware URLs. I cannot prove that the URL is safe from all threats; the
   URL may still lead to some other threat that my service has not identified:
   [XSS attacks](https://en.wikipedia.org/wiki/Cross-site_scripting),
   [CSRF attacks](https://en.wikipedia.org/wiki/Cross-site_request_forgery), a
   website vulnerable to [SQL injection](https://en.wikipedia.org/wiki/SQL_injection), or something else.
   So while I can prove a malware URL is not in the database, I cannot prove the URL
   is "safe from any threat ever."
4. I assume I can claim the '1' in `GET /urlinfo/1/` as my version number one for
   this web service.
5. Storing a colon in hostname:port as a key instead of `%3A` is probably okay.
   See https://stackoverflow.com/q/2053132/5978252
6. To avoid building a database of the entire Internet web space
   (Good, Bad, and Unknown_so_in_evaluation_state), I am revising the scope so
   that there's two types of URLs:
   1. `$KNOWN_MALWARE_HOSTNAME_AND_PORT`/`$KNOWN_MALWARE_ORIGINAL_PATH_AND_QUERY_STRING`
   2. Anything else.
   As in: if it's not pulled from the database as a match, this service lets it
   pass. We only track URLs identified as malware and everything else is okay. I
   have outlined some of the risks I see with this approach in Assumption (3).

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

This web service "URLLookupServiceDemo" was developed on a
[Ubuntu](https://en.wikipedia.org/wiki/Ubuntu)
20.04 LTS system and tested on a second Ubuntu 20.04 LTS system.

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
    * pylint - for static code analysis
    * pytest - for testing
    * requests - issue requests to the web framework.

### Installation

1. Clone this git repository to `URLLookupServiceDemo/`
2. `cd` to the directory `URLLookupServiceDemo/`
3. Create a virtual environment

    `$ virtualenv URLLookupServiceDemo`

4. Install modules as specified in file `requirements.txt`

    `$ URLLookupServiceDemo/bin/pip3 install -U -r requirements.txt`


### How to start the service

From the directory, with the virtual environment started,
call `$YOUR_VIRTUAL_ENV/bin/python3 ./urlinfo.py`

See Examples below.

In the examples below, my virtual environment is named
`URLLookupServiceDemo` and I start the service as follows:
```
URLLookupServiceDemo/bin/python3 ./urlinfo.py
```


## How to test

Multiple test tools make for well-tested code. For testing:

* [pylint](https://pypi.org/project/pylint/) - provides static code analysis and syntax error checking.
* [pytest](https://docs.pytest.org/en/stable/) - provides automated testing
* [curl](https://curl.se/) - request URLs at the command line. And more!
* [Postman](https://www.postman.com/) - I have used Postman for REST api
  testing. Use of Postman is not covered in this document.

### Static analysis with pylint

See Examples below

### Testing with pytest

See Examples below

### Testing with curl

I also tested from the command line with [curl](https://curl.se/)

See Examples below

# Future Considerations

A non-exclusive list of items to address in the future.

0. Bugs and Additional Features
    * Add more testing.
    * I'm missing a test to force an internal error on the result. I would
      revise this to either test for the "9999" code, or refactor that code out.
    * Flask can be configured to run on different IP address and port.
      `localhost:5000` is what I have configured for testing and demonstration
      purposes only.
1. Logging
    * Logging has to be added for multiple reasons.
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
    * When deploying to production, arguably the tests and pylint should be
      removed. These files increase disk usage. Debugging and testing should not
      be done on a production system.
3. Monitoring
    * [Runscope](https://www.runscope.com/)
      or some other sort of API web service monitoring would provide
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
    * Tracking IP addresses would help correct the known issue that the service
      does not check for equivalent URLs. e.g. `bad.com/nasty.html` is distinct
      in the database from `bad.com:80/nasty.html` right now.
      Both could be stored under a single IP.
6. Database improvements
    * Replace hash table with sqlite3 database.
    * Replace sqlite3 with redis key-value stores
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
8. [Sharding](https://en.wikipedia.org/wiki/Shard_%28database_architecture%29)
    * With this demo, all values are stored in one database.
    * Some hostnames (google.com) will be requested more than others. Monitoring
      will demonstrate which 10% of hostnames make up 90% of the requests.
    * If the service is refactored to store IP addresses, the databases could be
      sharded by IP octets. The top 10% hosts, the hosts that our proxy
      service queries for the most often with the most reads,
      they get their own dedicated shard. Logging and monitoring will tell us
      which hosts these are.
    * Logging and evaluation will allow us to estimate if the overhead required
      for this is worth the effort.
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
10. Performance
    * This web service maintains two data structures: a table of
    hostnames_and_ports and a second table of hostnames_and_ports plus
    original_path_and_query_string. My decision here is to add a performance
    cost at time of insertion into the database to gain a faster lookup. If the
    hostname has no entry in the first table, the service can respond faster and
    never have to look at the second, larger, presumably slower table.


# Part 2

As a thought exercise, please describe how you would accomplish the following:

* The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system?
    * sqlite3 database
    * redis
    * Sharding the database. Split the terms read most often to their own dedicated node.
    * Timestamp the database entries and review/move to cold storage/remove the
      oldest. Do bad URLs stay alive forever? Do they stay bad forever?
* Assume that the number of requests will exceed the capacity of a single
  system, describe how might you solve this, and how might this change if you have
  to distribute this workload to an additional region, such as Europe.
    * Put the service behind a load balancer
    * Work with a cloud provider for global replication across regions
    * Rework the service for a docker container and use kubernetes to scale response
      to demand.
* What are some strategies you might use to update the service with new URLs?
  Updates may be as much as 5 thousand URLs a day with updates arriving every 10
  minutes.
    * Scale out the read databases and have them fed from a master which takes writes.
* You’re woken up at 3am, what are some of the things you’ll look for?
    * The ticket that covers what woke me up at 03:00. If there is no ticket
      already created, I create one. If it is worth waking me up, it is worth
      tracking in our ticketing system.
    * Scope of the issue. Is everything down? Is one person reporting one part
      of one aspect is slow? These details go in the ticket.
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
    requested from this version for some agreed upon limit of days past the
    deadline, we can edit the code to respond with 308 Permanent Redirect to
    force clients to move to version 2. Alternatively the version 1 could be
    removed which would cause clients to get a hard fail.
* You need to deploy a new version of this application. What would you do?
    * The `/1/` in the URL is already a version indicator. Rolling out version two
    involves creating `/urlinfo/2/` This allows new clients to use the new version
    and old clients to continue using version 1.

# Examples

Setting up the first virtual environment.
```
david@mal:~/projects$ cd URLLookupServiceDemo/
david@mal:~/projects/URLLookupServiceDemo$ virtualenv URLLookupServiceDemo
created virtual environment CPython3.8.5.final.0-64 in 161ms
  creator CPython3Posix(dest=/home/david/projects/URLLookupServiceDemo/URLLookupServiceDemo, clear=False, global=False)
  seeder FromAppData(download=False, pkg_resources=latest, wheel=latest, urllib3=latest, distlib=latest, colorama=latest, msgpack=latest, pep517=latest, html5lib=latest, contextlib2=latest, packaging=latest, pytoml=latest, appdirs=latest, lockfile=latest, setuptools=latest, progress=latest, ipaddr=latest, chardet=latest, pyparsing=latest, retrying=latest, six=latest, requests=latest, CacheControl=latest, pip=latest, webencodings=latest, distro=latest, certifi=latest, idna=latest, via=copy, app_data_dir=/home/david/.local/share/virtualenv/seed-app-data/v1.0.1.debian)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
david@mal:~/projects/URLLookupServiceDemo$ URLLookupServiceDemo/bin/pip3 install -U -r  requirements.txt
Collecting Flask
  Using cached Flask-1.1.2-py2.py3-none-any.whl (94 kB)
Collecting pylint
  Using cached pylint-2.7.4-py3-none-any.whl (346 kB)
Collecting pytest
  Using cached pytest-6.2.3-py3-none-any.whl (280 kB)
Collecting requests
  Downloading requests-2.25.1-py2.py3-none-any.whl (61 kB)
     |████████████████████████████████| 61 kB 665 kB/s
Collecting itsdangerous>=0.24
  Using cached itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting click>=5.1
  Using cached click-7.1.2-py2.py3-none-any.whl (82 kB)
Collecting Jinja2>=2.10.1
  Using cached Jinja2-2.11.3-py2.py3-none-any.whl (125 kB)
Collecting Werkzeug>=0.15
  Using cached Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
Collecting isort<6,>=4.2.5
  Using cached isort-5.8.0-py3-none-any.whl (103 kB)
Collecting mccabe<0.7,>=0.6
  Using cached mccabe-0.6.1-py2.py3-none-any.whl (8.6 kB)
Collecting toml>=0.7.1
  Using cached toml-0.10.2-py2.py3-none-any.whl (16 kB)
Collecting astroid<2.7,>=2.5.2
  Using cached astroid-2.5.2-py3-none-any.whl (222 kB)
Requirement already satisfied, skipping upgrade: packaging in ./URLLookupServiceDemo/lib/python3.8/site-packages (from pytest->-r requirements.txt (line 3)) (20.3)
Collecting iniconfig
  Using cached iniconfig-1.1.1-py2.py3-none-any.whl (5.0 kB)
Collecting pluggy<1.0.0a1,>=0.12
  Using cached pluggy-0.13.1-py2.py3-none-any.whl (18 kB)
Collecting attrs>=19.2.0
  Using cached attrs-20.3.0-py2.py3-none-any.whl (49 kB)
Collecting py>=1.8.2
  Using cached py-1.10.0-py2.py3-none-any.whl (97 kB)
Requirement already satisfied, skipping upgrade: urllib3<1.27,>=1.21.1 in ./URLLookupServiceDemo/lib/python3.8/site-packages (from requests->-r requirements.txt (line 4)) (1.25.8)
Requirement already satisfied, skipping upgrade: chardet<5,>=3.0.2 in ./URLLookupServiceDemo/lib/python3.8/site-packages (from requests->-r requirements.txt (line 4)) (3.0.4)
Requirement already satisfied, skipping upgrade: idna<3,>=2.5 in ./URLLookupServiceDemo/lib/python3.8/site-packages (from requests->-r requirements.txt (line 4)) (2.8)
Requirement already satisfied, skipping upgrade: certifi>=2017.4.17 in ./URLLookupServiceDemo/lib/python3.8/site-packages (from requests->-r requirements.txt (line 4)) (2019.11.28)
Collecting MarkupSafe>=0.23
  Using cached MarkupSafe-1.1.1-cp38-cp38-manylinux2010_x86_64.whl (32 kB)
Collecting lazy-object-proxy>=1.4.0
  Using cached lazy_object_proxy-1.6.0-cp38-cp38-manylinux1_x86_64.whl (58 kB)
Processing /home/david/.cache/pip/wheels/5f/fd/9e/b6cf5890494cb8ef0b5eaff72e5d55a70fb56316007d6dfe73/wrapt-1.12.1-py3-none-any.whl
Installing collected packages: itsdangerous, click, MarkupSafe, Jinja2, Werkzeug, Flask, isort, mccabe, toml, lazy-object-proxy, wrapt, astroid, pylint, iniconfig, pluggy, attrs, py, pytest, requests
  Attempting uninstall: requests
    Found existing installation: requests 2.22.0
    Uninstalling requests-2.22.0:
      Successfully uninstalled requests-2.22.0
Successfully installed Flask-1.1.2 Jinja2-2.11.3 MarkupSafe-1.1.1 Werkzeug-1.0.1 astroid-2.5.2 attrs-20.3.0 click-7.1.2 iniconfig-1.1.1 isort-5.8.0 itsdangerous-1.1.0 lazy-object-proxy-1.6.0 mccabe-0.6.1 pluggy-0.13.1 py-1.10.0 pylint-2.7.4 pytest-6.2.3 requests-2.25.1 toml-0.10.2 wrapt-1.12.1
david@mal:~/projects/URLLookupServiceDemo$
```



Running pylint
```
david@mal:~/projects/URLLookupServiceDemo$ URLLookupServiceDemo/bin/pylint ./urlinfo.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

david@mal:~/projects/URLLookupServiceDemo$
```


Starting the service:
```
david@mal:~/projects/URLLookupServiceDemo$ URLLookupServiceDemo/bin/python3 ./urlinfo.py
 * Serving Flask app "urlinfo" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 110-425-814

```

Running pytest

1. In one terminal, start the service as described in *Starting the service*
2. In a second terminal, start the same virtualenv with the same modules and run the tests:

```
david@mal:~$ cd projects/URLLookupServiceDemo/
david@mal:~/projects/URLLookupServiceDemo$ source URLLookupServiceDemo/bin/activate
(URLLookupServiceDemo) david@mal:~/projects/URLLookupServiceDemo$ URLLookupServiceDemo/bin/pytest tests/all_tests.py
============================================================ test session starts =============================================================
platform linux -- Python 3.8.5, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/david/projects/URLLookupServiceDemo
collected 9 items

tests/all_tests.py .........                                                                                                           [100%]

============================================================= 9 passed in 0.10s ==============================================================
(URLLookupServiceDemo) david@mal:~/projects/URLLookupServiceDemo$ URLLookupServiceDemo/bin/pytest -v  tests/all_tests.py
============================================================ test session starts =============================================================
platform linux -- Python 3.8.5, pytest-6.2.3, py-1.10.0, pluggy-0.13.1 -- /home/david/projects/URLLookupServiceDemo/URLLookupServiceDemo/bin/python
cachedir: .pytest_cache
rootdir: /home/david/projects/URLLookupServiceDemo
collected 9 items

tests/all_tests.py::test_get_response_code_200 PASSED                                                                                  [ 11%]
tests/all_tests.py::test_get_response_code_404 PASSED                                                                                  [ 22%]
tests/all_tests.py::test_get_response_in_json_format PASSED                                                                            [ 33%]
tests/all_tests.py::test_get_response_body_element_code_on_malware PASSED                                                              [ 44%]
tests/all_tests.py::test_get_response_body_element_code_on_nonmalware PASSED                                                           [ 55%]
tests/all_tests.py::test_get_response_body_element_code_on_malware_with_querystring PASSED                                             [ 66%]
tests/all_tests.py::test_get_response_body_element_code_on_nonmalware_with_querystring PASSED                                          [ 77%]
tests/all_tests.py::test_get_code_on_malware_with_hostname_and_port_and_file PASSED                                                    [ 88%]
tests/all_tests.py::test_get_code_on_malware_with_hostname_and_port_and_path_with_separators PASSED                                    [100%]

============================================================= 9 passed in 0.10s ==============================================================
(URLLookupServiceDemo) david@mal:~/projects/URLLookupServiceDemo$
```


curl

The python virtualenv is not required, so I deactivated it before calling curl.

This example shows using curl to make a request to the service and look at the
response. In the example, the "hostname_and_port" is `en.wikipedia.org:443/` and
the "original_path_and_query_string" is `wiki/The_Order_of_the_Stick`
```
(URLLookupServiceDemo) david@mal:~/projects/URLLookupServiceDemo$ deactivate
david@mal:~/projects/URLLookupServiceDemo$ curl -i "http://localhost:5000/urlinfo/1/en.wikipedia.org:443/wiki/The_Order_of_the_Stick"
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 173
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Sun, 04 Apr 2021 22:55:27 GMT

{
  "urlinfo_response": {
    "code": "2000",
    "code_text": "NO_MALWARE_AT_THAT_HOST",
    "url_investigated": "en.wikipedia.org:443/wiki/The_Order_of_the_Stick"
  }
}
david@mal:~/projects/URLLookupServiceDemo$
```
