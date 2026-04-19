import allure
import pytest

pytestmark = pytest.mark.integration

@allure.title("Event flow — source fires, router receives, channel confirmed")
@allure.severity(allure.severity_level.BLOCKER)
def test_full_event_chain(http, httpbin):

    with allure.step("Stage 1: source emits raw event"):
        raw = {"event": "alert.fired", "host": "node-01", "severity": "warning"}
        r1  = http.post(f"{httpbin}/post", json=raw)
        assert r1.status_code == 200
        received_raw = r1.json()["json"]

    with allure.step("Stage 2: router enriches event"):
        enriched = {
            **received_raw,
            "channel":     "slack",
            "team":        "infra",
            "routed":      True,
        }
        assert enriched["routed"] is True
        assert "channel" in enriched

    with allure.step("Stage 3: channel receives enriched event"):
        r3 = http.post(f"{httpbin}/post", json=enriched)
        assert r3.status_code == 200
        delivered = r3.json()["json"]

    with allure.step("Enriched fields intact at destination"):
        assert delivered["channel"] == "slack"
        assert delivered["team"] == "infra"
        assert delivered["host"] == "node-01"
        assert delivered["routed"] is True


@allure.title("Routing — critical events go to PagerDuty channel")
@allure.severity(allure.severity_level.CRITICAL)
def test_routing_critical_to_pagerduty(http, httpbin):

    event = {"event": "db.down", "severity": "critical", "host": "db-primary"}

    with allure.step("Determine channel by severity"):
        channel = "pagerduty" if event["severity"] == "critical" else "slack"
        assert channel == "pagerduty"

    with allure.step("Route event to pagerduty channel"):
        routed = {**event, "channel": channel}
        r = http.post(f"{httpbin}/post", json=routed)
        assert r.status_code == 200

    with allure.step("Channel tag correct in delivered payload"):
        assert r.json()["json"]["channel"] == "pagerduty"


@allure.title("Routing — warning events go to Slack channel")
@allure.severity(allure.severity_level.NORMAL)
def test_routing_warning_to_slack(http, httpbin):
    event = {"event": "cpu.high", "severity": "warning", "host": "node-03"}

    with allure.step("Determine channel by severity"):
        channel = "pagerduty" if event["severity"] == "critical" else "slack"
        assert channel == "slack"

    with allure.step("Route event to slack channel"):
        routed = {**event, "channel": channel}
        r = http.post(f"{httpbin}/post", json=routed)
        assert r.status_code == 200

    with allure.step("Slack channel confirmed"):
        assert r.json()["json"]["channel"] == "slack"


@allure.title("Event state — fired → resolved transition")
@allure.severity(allure.severity_level.CRITICAL)
def test_alert_fired_then_resolved(http, httpbin):
    """
    Alert lifecycle: fired → acknowledged → resolved.
    Each state change must be delivered.
    """
    base = {"alert_id": "cpu-001", "host": "node-01"}

    with allure.step("Fire alert"):
        r1 = http.post(f"{httpbin}/post", json={**base, "state": "fired"})
        assert r1.status_code == 200
        assert r1.json()["json"]["state"] == "fired"

    with allure.step("Acknowledge alert"):
        r2 = http.post(f"{httpbin}/post", json={**base, "state": "acknowledged"})
        assert r2.status_code == 200
        assert r2.json()["json"]["state"] == "acknowledged"

    with allure.step("Resolve alert"):
        r3 = http.post(f"{httpbin}/post", json={**base, "state": "resolved"})
        assert r3.status_code == 200
        assert r3.json()["json"]["state"] == "resolved"

    with allure.step("All three state transitions delivered"):
        states = [
            r1.json()["json"]["state"],
            r2.json()["json"]["state"],
            r3.json()["json"]["state"],
        ]
        assert states == ["fired", "acknowledged", "resolved"]


@allure.title("Multi-channel — same event delivered to two channels")
@allure.severity(allure.severity_level.NORMAL)
def test_multi_channel_delivery(http, httpbin):
    """
    Critical events are fanned out to multiple channels simultaneously.
    """
    event = {"event": "site.down", "severity": "critical", "alert_id": "site-001"}

    with allure.step("Deliver to Slack"):
        r_slack = http.post(f"{httpbin}/post", json={**event, "channel": "slack"})
        assert r_slack.status_code == 200

    with allure.step("Deliver to PagerDuty"):
        r_pd = http.post(f"{httpbin}/post", json={**event, "channel": "pagerduty"})
        assert r_pd.status_code == 200

    with allure.step("Both channels received the same alert_id"):
        assert r_slack.json()["json"]["alert_id"] == "site-001"
        assert r_pd.json()["json"]["alert_id"] == "site-001"