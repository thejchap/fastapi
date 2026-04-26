from fastapi.openapi.docs import get_swagger_ui_html
from tryke import expect, test


@test
def init_oauth_html_chars_are_escaped():
    xss_payload = "Evil</script><script>alert(1)</script>"
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"appName": xss_payload},
    )
    body = html.body.decode()

    expect("</script><script>" in body).to_be_falsy()
    expect(body).to_contain("\\u003c/script\\u003e\\u003cscript\\u003e")


@test
def swagger_ui_parameters_html_chars_are_escaped():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        swagger_ui_parameters={"customKey": "<img src=x onerror=alert(1)>"},
    )
    body = html.body.decode()
    expect("<img src=x onerror=alert(1)>" in body).to_be_falsy()
    expect(body).to_contain("\\u003cimg")


@test
def normal_init_oauth_still_works():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"clientId": "my-client", "appName": "My App"},
    )
    body = html.body.decode()
    expect(body).to_contain('"clientId": "my-client"')
    expect(body).to_contain('"appName": "My App"')
    expect(body).to_contain("ui.initOAuth")
