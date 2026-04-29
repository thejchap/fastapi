from fastapi.openapi.docs import get_swagger_ui_html
from tryke import expect, test


@test("init_oauth values are HTML-escaped to prevent XSS")
def init_oauth_html_chars_are_escaped():
    xss_payload = "Evil</script><script>alert(1)</script>"
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"appName": xss_payload},
    )
    body = html.body.decode()

    expect("</script><script>" in body, "raw script tags absent").to_be_falsy()
    expect(body, "Swagger UI body").to_contain("\\u003c/script\\u003e\\u003cscript\\u003e")


@test("swagger_ui_parameters values are HTML-escaped to prevent XSS")
def swagger_ui_parameters_html_chars_are_escaped():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        swagger_ui_parameters={"customKey": "<img src=x onerror=alert(1)>"},
    )
    body = html.body.decode()
    expect(
        "<img src=x onerror=alert(1)>" in body,
        "raw img tag absent",
    ).to_be_falsy()
    expect(body, "Swagger UI body").to_contain("\\u003cimg")


@test("Normal init_oauth values are emitted unchanged")
def normal_init_oauth_still_works():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"clientId": "my-client", "appName": "My App"},
    )
    body = html.body.decode()
    expect(body, "Swagger UI body").to_contain('"clientId": "my-client"')
    expect(body, "Swagger UI body").to_contain('"appName": "My App"')
    expect(body, "Swagger UI body").to_contain("ui.initOAuth")
