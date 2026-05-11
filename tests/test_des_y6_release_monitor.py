from tools.check_des_y6_release_monitor import discover


def test_des_y6_release_monitor_detects_candidate_links(monkeypatch):
    html = """
    <html>
      <body>
        <a href="/releases/y6a2/DESY6_3x2pt_covariance.fits.gz">covariance</a>
        <a href="/releases/y6a2/DESY6_3x2pt_data_vector.txt">data vector</a>
      </body>
    </html>
    """

    def fake_fetch(url: str) -> str:
        return html

    monkeypatch.setattr("tools.check_des_y6_release_monitor.fetch", fake_fetch)

    result = discover(["https://des.ncsa.illinois.edu/releases/y6a2/"])

    assert result["status"] == "CANDIDATE_RELEASE_LINKS_FOUND"
    assert len(result["candidate_links"]) == 2
    assert any("covariance" in item["url"].lower() for item in result["candidate_links"])
    assert any("data_vector" in item["url"].lower() for item in result["candidate_links"])


def test_des_y6_release_monitor_preserves_pending_status(monkeypatch):
    def fake_fetch(url: str) -> str:
        return "<html><body><a href='/static/manifest.json'>manifest</a></body></html>"

    monkeypatch.setattr("tools.check_des_y6_release_monitor.fetch", fake_fetch)

    result = discover(["https://des.ncsa.illinois.edu/releases/y6a2/"])

    assert result["status"] == "PENDING_RELEASE"
    assert result["candidate_links"] == []
