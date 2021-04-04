#!flask/bin/python
"""URL lookup service demo"""
from flask import Flask

app = Flask(__name__)

malware_sites = [
    {
        'hostname': u'badsite.invalid',
    },
    {
        'hostname': u'malware.site',
    }
]

@app.route('/urlinfo/1/<hostname_and_port>/<original_path_and_query_string>', methods=['GET'])
def adhoc_test(hostname_and_port, original_path_and_query_string):
    """demo test function"""
    return hostname_and_port

if __name__ == '__main__':
    app.run(debug=True)
