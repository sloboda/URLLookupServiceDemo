#!flask/bin/python
"""URL lookup service demo"""
from flask import Flask

app = Flask(__name__)

malware_sites = [
    u'badsite.invalid',
    u'malware.site',
    u'malware.site:443',
    u'malware.site:80',
]

# Get hostname_and_port, original_path_and_query_string as one path
# and split on first /
@app.route('/urlinfo/1/<path:fullpath>', methods=['GET'])
def adhoc_test(fullpath):
    """demo test function"""
    # In testing, sending a hostname with no querystring
    #    throws an error on the `split` command below.
    # The following code appends a path separator '/' if there is not one present.
    if not '/' in fullpath:
        fullpath = fullpath + '/'
    hostname_and_port = '/'.join(fullpath.split("/",1)[:1])
    original_path_and_query_string = fullpath.split("/",1)[1:][0]
    if hostname_and_port in malware_sites:
        result = "4000_MALWARE_DETECTED"
        result_path = look_up_path(original_path_and_query_string)
        result_path = result_path + "foo"
    else:
        result = "3000_YOUR_HOSTNAME_IS_OK" # Anything not in our list of malware sites is okay.
#       result = "[" + hostname_and_port + "]" # debugging
    return result

def look_up_path(path):
    """look up the path from a database of known bad paths on known malware sites.
    """
    return path

if __name__ == '__main__':
    app.run(debug=True)
