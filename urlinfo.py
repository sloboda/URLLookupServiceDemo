"""URL lookup service demo"""
from flask import Flask, jsonify

app = Flask(__name__)

malware_sites = [
    u'badsite.invalid',
    u'malware.site',
    u'malware.site:80',
    u'malware.site:443',
]

malware_sites_and_paths = {
    'badsite.invalid': [u'badpath.html'],
    'malware.site': [u'nasty.html','get/cheat/codes/here/'],
    'malware.site:80': [u'virus/url/'],
    'malware.site:443': [u'secret_to_eternal_youth.html',
                          'I/do/not/know/a/lot/of/malware/urls/'],
}

response_codes = {
    '2000': "NO_MALWARE_AT_THAT_HOST",
    '3000': "HOST_HAS_HAD_MALWARE_BUT_NOT_THAT_URL",
    '4000': "MALWARE_AT_THAT_HOST_AND_URL",
    '9999': "INTERNAL_ERROR",
}

# Get hostname_and_port, original_path_and_query_string as one path
# and split on first /
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
    original_path_and_query_string = fullpath.split("/",1)[1:][0]
    if hostname_and_port in malware_sites:
        result = "3000" # Warn the caller that this host has served malware in the past.
        result = look_up_path(hostname_and_port, original_path_and_query_string)
    else:
        result = "2000" # Anything not in our list of malware sites is okay.
    response = build_response(result, hostname_and_port, original_path_and_query_string)
    return jsonify({'urlinfo_response': response})

def look_up_path(hostname, original_path):
    """look up the path from a database of known bad paths on known malware sites.

    If there are no matches in our database of known bad paths for that host,
    the URL does not serve malware.
    """
    result = "3000" # Anything not in our list of malware sites is okay.
    paths = malware_sites_and_paths[hostname]
    for path in paths:
        if path == original_path:
            result = "4000"
            break
    return result

def build_response(result, hostname, original_path):
    """Send JSON data about result to caller. Use codes from a set"""
    response = {}
    if result not in response_codes.keys():
        result = "9999" # set a default for errors
    response["code_text"] = response_codes[result]
    response["code"] = result
    response["url_investigated"] = hostname + "/" + original_path
    return response

if __name__ == '__main__':
    app.run(debug=True)
