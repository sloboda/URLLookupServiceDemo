"""URL lookup service demo"""
from flask import Flask, jsonify, request

app = Flask(__name__)

malware_sites = [
    u'badsite.invalid',
    u'malware.site',
    u'malware.site:80',
    u'malware.site:443',
    u'querystring.badsite.invalid',
]

malware_sites_and_paths = {
    'badsite.invalid': [u'badpath.html'],
    'malware.site': [u'nasty.html',
                     u'get/cheat/codes/here/'],
    'malware.site:80': [u'nasty.html',
                     u'get/cheat/codes/here/'],
    'malware.site:443': [u'secret_to_eternal_youth.html',
                         u'I/do/not/know/a/lot/of/malware/urls/'],
    'querystring.badsite.invalid': [u'virus?want=yes'],
}

### Tests
#   Testing where we expect malware
# curl -i "http://localhost:5000/urlinfo/1/badsite.invalid/badpath.html"
# curl -i "http://localhost:5000/urlinfo/1/malware.site/nasty.html"
# curl -i "http://localhost:5000/urlinfo/1/malware.site/get/cheat/codes/here/"
# curl -i "http://localhost:5000/urlinfo/1/malware.site:80/virus/url/"
#   Testing where we expect no malware
# curl -i "http://localhost:5000/urlinfo/1/en.wikipedia.org:443/wiki/The_Order_of_the_Stick"
# curl -i "http://localhost:5000/urlinfo/1/www.google.com:443/search?q=kermit+the+frog&tbm=isch"

response_codes = {
    '2000': "NO_MALWARE_AT_THAT_HOST",
    '3000': "HOST_HAS_HAD_MALWARE_BUT_NOT_AT_THAT_URL",
    '4000': "MALWARE_AT_THAT_HOST_AND_URL",
    '9999': "INTERNAL_ERROR",
}

# Get hostname_and_port, original_path as one path
# and split on first /
# NOTE: request.query_string is something distinct.
@app.route('/urlinfo/1/<path:fullpath>', methods=['GET'])
def adhoc_test(fullpath):
    """demo test function"""
    result = "4000" # start off assuming the worst
    # Sending a hostname with no querystring
    #    throws an error on the `split` command below.
    # The following code appends a path separator '/' if there is not one present.
    if not '/' in fullpath:
        fullpath = fullpath + '/'
    hostname_and_port = '/'.join(fullpath.split("/",1)[:1])
    original_path = fullpath.split("/",1)[1:][0]
    query_string = request.query_string.decode() # because Flask serves that separately.
    if hostname_and_port in malware_sites:
        result = "3000" # Warn the caller that this host has served malware in the past.
        result = look_up_path(hostname_and_port, original_path, query_string)
    else:
        result = "2000" # Anything not in our list of malware sites is okay.
    response = build_response(result, hostname_and_port, original_path, query_string)
    return jsonify({'urlinfo_response': response})

def look_up_path(hostname, original_path, query_string):
    """look up the path from a database of known bad paths on known malware sites.

    If there are no matches in our database of known bad paths for that host,
    the URL does not serve malware.
    """
    result = "3000" # Warn the caller that this host has served malware in the past.
    paths = malware_sites_and_paths[hostname]
    if query_string:
        value_under_test = original_path + "?" + query_string
    else:
        value_under_test = original_path
    for path in paths:
        if path == value_under_test:
            result = "4000"
            break
    return result

def build_response(result, hostname, original_path, query_string):
    """Send JSON data about result to caller. Use codes from a set."""
    response = {}
    if query_string:
        url_investigated = hostname + "/" + original_path + "?" + query_string
    else:
        url_investigated = hostname + "/" + original_path
    if result not in response_codes.keys():
        result = "9999" # set a default for errors
    response["code_text"] = response_codes[result]
    response["code"] = result
    response["url_investigated"] = url_investigated
    return response

if __name__ == '__main__':
    app.run(debug=True)
