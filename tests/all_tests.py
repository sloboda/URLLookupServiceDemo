import requests
import pytest

def test_get_response_code_200():
    response = requests.get("http://localhost:5000/urlinfo/1/badsite.invalid")
    assert response.status_code == 200

def test_get_response_code_404():
    response = requests.get("http://localhost:5000/urlinfo/1")
    assert response.status_code == 404

def test_get_response_in_json_format():
    response = requests.get("http://localhost:5000/urlinfo/1/badsite.invalid")
    assert response.headers["Content-Type"] == "application/json"

def test_get_response_body_element_code_on_malware():
    response = requests.get("http://localhost:5000/urlinfo/1/badsite.invalid/badpath.html")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "4000"

def test_get_response_body_element_code_on_nonmalware():
    response = requests.get("http://localhost:5000/urlinfo/1/en.wikipedia.org:443/wiki/The_Order_of_the_Stick")
    response_body = response.json()
    assert response_body["urlinfo_response"]["code"] == "2000"

