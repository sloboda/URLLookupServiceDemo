import requests
import pytest

def test_get_response_code_200():
    # Does the web service return 200 for a URL it has?
    response = requests.get("http://localhost:5000/urlinfo/1/badsite.invalid")
    assert response.status_code == 200

def test_get_response_code_404():
    # Does the web service return 404 for a URL it does not have?
    response = requests.get("http://localhost:5000/urlinfo/1")
    assert response.status_code == 404

def test_get_response_in_json_format():
    # Does the web service return JSON content?
    response = requests.get("http://localhost:5000/urlinfo/1/badsite.invalid")
    assert response.headers["Content-Type"] == "application/json"

def test_get_response_body_element_code_on_malware():
    # A known bad URL should return a code defined in `response_codes`
    response = requests.get("http://localhost:5000/urlinfo/1/badsite.invalid/badpath.html")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "4000"

def test_get_response_body_element_code_on_nonmalware():
    # A URL not in the malware database is assumed to be good.
    # This URL should return a code defined in `response_codes`
    response = requests.get("http://localhost:5000/urlinfo/1/en.wikipedia.org:443/wiki/The_Order_of_the_Stick")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "2000"

def test_get_response_body_element_code_on_malware_with_querystring():
    response = requests.get("http://localhost:5000/urlinfo/1/querystring.badsite.invalid/virus?want=yes")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "4000"

def test_get_response_body_element_code_on_nonmalware_with_querystring():
    # May I see a picture of Kermit The Frog?
    response = requests.get("http://localhost:5000/urlinfo/1/www.google.com:443/search?q=kermit+the+frog&tbm=isch")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "2000"

def test_get_code_on_malware_with_hostname_and_port_and_file():
    response = requests.get("http://localhost:5000/urlinfo/1/malware.site:443/secret_to_eternal_youth.html")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "4000"

def test_get_code_on_malware_with_hostname_and_port_and_path_with_separators():
    response = requests.get("http://localhost:5000/urlinfo/1/malware.site:443/I/do/not/know/a/lot/of/malware/urls/")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "4000"


