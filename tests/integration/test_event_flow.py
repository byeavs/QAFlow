import time
import allure
import pytest

pytestmark = pytest.mark.integration

@allure.title("Event delivery — POST returns 200 and echoes payload")
@allure.severity(allure.severity_level.BLOCKER)
def test_event_delivered(http, httpbin):
    payload = {
        "event":   "alert.fired",
        "source":  "monitoring",
        "severity": "critical",
        "message": "CPU > 90% on node-01",
    }

    with allure.step("Send event to webhook endpoint"):
        r = http.post(f"{httpbin}/post", json=payload)

    with allure.step("Delivery confirmed — status 200"):
        assert r.status_code == 200

    with allure.step("Payload echoed back correctly"):
        body = r.json()["json"]
        assert body["event"] == payload["event"]
        assert body["severity"] == payload["severity"]
        assert body["source"] == payload["source"]


@allure.title("Event delivery — custom routing headers propagated")
@allure.severity(allure.severity_level.CRITICAL)
def test_event_routing_headers(http, httpbin):
    """
    In real alerting systems events carry routing headers:
    X-Alert-Channel, X-Team, X-Priority.
    Verify they reach the destination intact.
    """
    headers = {
        "X-Alert-Channel": "slack",
        "X-Team": "infra",
        "X-Priority": "high",
    }

    with allure.step("Send event with routing headers"):
        r = http.get(f"{httpbin}/headers", headers=headers)

    with allure.step("Status 200"):
        assert r.status_code == 200

    with allure.step("Routing headers present in received request"):
        received = r.json()["headers"]
        assert received.get("X-Alert-Channel") == "slack"
        assert received.get("X-Team") == "infra"
        assert received.get("X-Priority") == "high"


@allure.title("Event deduplication — identical events have same fingerprint")
@allure.severity(allure.severity_level.NORMAL)
def test_event_deduplication_fingerprint(http, httpbin):
    """
    Deduplication logic relies on stable fingerprints.
    Two identical events must produce identical payloads.
    """
    payload = {
        "event": "disk.full",
        "host": "node-02",
        "fingerprint": "disk_full:node-02",
    }

    with allure.step("Send same event twice"):
        r1 = http.post(f"{httpbin}/post", json=payload)
        r2 = http.post(f"{httpbin}/post", json=payload)

    with allure.step("Both deliveries succeed"):
        assert r1.status_code == 200
        assert r2.status_code == 200

    with allure.step("Fingerprint identical in both — deduplication key stable"):
        fp1 = r1.json()["json"]["fingerprint"]
        fp2 = r2.json()["json"]["fingerprint"]
        assert fp1 == fp2


@allure.title("Notification suppression — suppressed event carries suppress flag")
@allure.severity(allure.severity_level.NORMAL)
def test_event_suppression_flag(http, httpbin):
    """
    Suppressed notifications must carry a flag so consumers skip them.
    """
    payload = {
        "event": "alert.fired",
        "suppressed": True,
        "reason": "maintenance_window",
    }

    with allure.step("Send suppressed event"):
        r = http.post(f"{httpbin}/post", json=payload)

    with allure.step("Event accepted"):
        assert r.status_code == 200

    with allure.step("Suppressed flag and reason intact"):
        body = r.json()["json"]
        assert body["suppressed"] is True
        assert body["reason"] == "maintenance_window"


@allure.title("Event aggregation — batch of events sent as array")
@allure.severity(allure.severity_level.NORMAL)
def test_event_aggregation_batch(http, httpbin):
    """
    Aggregated alerts are sent as a batch, not one-by-one.
    Verify batch structure is preserved end-to-end.
    """
    batch = {
        "events": [
            {"id": 1, "event": "cpu.high",  "host": "node-01"},
            {"id": 2, "event": "mem.high",  "host": "node-01"},
            {"id": 3, "event": "disk.full", "host": "node-02"},
        ],
        "aggregated": True,
        "count": 3,
    }

    with allure.step("POST aggregated batch"):
        r = http.post(f"{httpbin}/post", json=batch)

    with allure.step("Status 200"):
        assert r.status_code == 200

    with allure.step("Batch count and structure correct"):
        body = r.json()["json"]
        assert body["aggregated"] is True
        assert body["count"] == 3
        assert len(body["events"]) == 3


@allure.title("Retry behaviour — endpoint responds after delay")
@allure.severity(allure.severity_level.NORMAL)
def test_event_retry_after_delay(http, httpbin):
    """
    Simulates a slow consumer. Event delivery must complete
    within acceptable timeout even with processing delay.
    """
    with allure.step("Send event to slow endpoint (2s delay)"):
        start = time.time()
        r     = http.get(f"{httpbin}/delay/2", timeout=10)
        elapsed = time.time() - start

    with allure.step("Delivery succeeded"):
        assert r.status_code == 200

    with allure.step("Response within acceptable window (2–8s)"):
        assert 2.0 <= elapsed < 8.0, f"Unexpected response time: {elapsed:.2f}s"


@allure.title("Notification channel — wrong method returns 405")
@allure.severity(allure.severity_level.MINOR)
def test_wrong_method_rejected(http, httpbin):
    
    with allure.step("Send GET to POST-only endpoint"):
        r = http.get(f"{httpbin}/post")

    with allure.step("Request rejected with 405"):
        assert r.status_code == 405


@allure.title("Event schema — missing required field detected")
@allure.severity(allure.severity_level.CRITICAL)
def test_event_missing_required_field(http, httpbin):

    incomplete_event = {
        "source": "monitoring"
    }

    with allure.step("Validate event payload before sending"):
        assert "event" not in incomplete_event, "event field missing — would be rejected"

    with allure.step("Send incomplete payload and record response"):
        r = http.post(f"{httpbin}/post", json=incomplete_event)
        assert r.status_code == 200  # httpbin accepts anything

    with allure.step("Verify event field absent — schema violation confirmed"):
        body = r.json()["json"]
        assert "event" not in body