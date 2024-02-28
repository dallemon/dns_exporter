"""Certificate related tests."""
import logging

import pytest
import requests


### certificate verify fail with default system ca
def test_cert_verify_fail_doh(dns_exporter_example_config, caplog):
    """Test cert verify functionality with protocol doh when there is a hostname mismatch."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "doh",
            "family": "ipv4",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="certificate_error"} 1.0' in r.text


def test_cert_verify_fail_dot(dns_exporter_example_config, caplog):
    """Test cert verify functionality with protocol dot when there is a hostname mismatch."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "dot",
            "family": "ipv4",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="certificate_error"} 1.0' in r.text


# this fails because the adguard servers have IP:.... SAN entries in the certificates
# to be fixed when a doq server with no ip SAN exists
@pytest.mark.xfail()
def test_cert_verify_fail_doq(dns_exporter_example_config, caplog):
    """Test cert verify functionality with protocol doq when there is a hostname mismatch."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "94.140.14.140",  # dns-unfiltered.adguard.com
            "query_name": "example.com",
            "protocol": "doq",
            "family": "ipv4",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="certificate_error"} 1.0' in r.text


###################################################################################
### certificate verify fail with custom ca


def test_cert_verify_fail_custom_ca_doh(dns_exporter_example_config, caplog):
    """Test cert verify functionality with protocol doh and a selfsigned cert as CA."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "doh",
            "family": "ipv4",
            "verify_certificate_path": "tests/certificates/test.crt",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="certificate_error"} 1.0' in r.text


def test_cert_verify_fail_custom_ca_dot(dns_exporter_example_config, caplog):
    """Test cert verify functionality with protocol dot and a selfsigned cert as CA."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "dot",
            "family": "ipv4",
            "verify_certificate_path": "tests/certificates/test.crt",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="certificate_error"} 1.0' in r.text
    assert "Protocol dot raised ssl.SSLCertVerificationError, returning certificate_error" in caplog.text


# this fails because the adguard servers have IP:.... SAN entries in the certificates
@pytest.mark.xfail()
def test_cert_verify_fail_custom_ca_doq(dns_exporter_example_config, caplog):
    """Test cert verify functionality with protocol doq and a selfsigned cert as CA."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "94.140.14.140",  # dns-unfiltered.adguard.com
            "query_name": "example.com",
            "protocol": "doq",
            "family": "ipv4",
            "verify_certificate_path": "tests/certificates/test.crt",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="certificate_error"} 1.0' in r.text


###################################################################################
### test certificate verification disabled


def test_cert_verify_false_doh(dns_exporter_example_config, caplog):
    """Test cert verify functionality disabled allows lookups with bad certs for doh."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "doh",
            "family": "ipv4",
            "verify_certificate": False,
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert "dnsexp_dns_query_success 1.0" in r.text


def test_cert_verify_false_dot(dns_exporter_example_config, caplog):
    """Test cert verify functionality disabled allows lookups with bad certs for dot."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "dot",
            "family": "ipv4",
            "verify_certificate": False,
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert "dnsexp_dns_query_success 1.0" in r.text


def test_cert_verify_false_doq(dns_exporter_example_config, caplog):
    """Test cert verify functionality disabled allows lookups with bad certs for doq."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "94.140.14.140",  # dns-unfiltered.adguard.com
            "query_name": "example.com",
            "protocol": "doq",
            "family": "ipv4",
            "verify_certificate": False,
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert "dnsexp_dns_query_success 1.0" in r.text


###################################################################################
# test certificate verification with an invalid ca path


def test_cert_verify_invalid_path_doh(dns_exporter_example_config, caplog):
    """Test cert verify functionality when an invalid CA path is provided for doh."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "doh",
            "family": "ipv4",
            "verify_certificate_path": "/nonexistant",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="invalid_request_config"} 1.0' in r.text
    assert "Protocol doh raised OSError, returning invalid_request_config" in caplog.text


def test_cert_verify_invalid_path_dot(dns_exporter_example_config, caplog):
    """Test cert verify functionality when an invalid CA path is provided for dot."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "91.239.100.100",
            "query_name": "example.com",
            "protocol": "dot",
            "family": "ipv4",
            "verify_certificate_path": "/nonexistant",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="invalid_request_config"} 1.0' in r.text
    assert "Protocol dot raised ValueError, is verify_certificate_path wrong" in caplog.text


@pytest.mark.filterwarnings("ignore:.*:pytest.PytestUnhandledThreadExceptionWarning")
def test_cert_verify_invalid_path_doq(dns_exporter_example_config, caplog):
    """Test cert verify functionality when an invalid CA path is provided for doq."""
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    r = requests.get(
        "http://127.0.0.1:25353/query",
        params={
            "server": "94.140.14.140",  # dns-unfiltered.adguard.com
            "query_name": "example.com",
            "protocol": "doq",
            "family": "ipv4",
            "verify_certificate_path": "/nonexistant",
        },
    )
    assert r.status_code == 200, "non-200 returncode"
    assert 'dnsexp_failures_total{reason="invalid_request_config"} 1.0' in r.text
    assert "Protocol doq raised dns.quic._common.UnexpectedEOF - is verify_certificate_path wrong?" in caplog.text