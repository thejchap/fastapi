from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.openapi_callbacks import tutorial001_py310 as mod


@fixture
def client() -> TestClient:
    client = TestClient(mod.app)
    client.headers.clear()
    return client


@test("POST /invoices/ accepts an invoice")
def get(client: TestClient = Depends(client)):
    response = client.post(
        "/invoices/", json={"id": "fooinvoice", "customer": "John", "total": 5.3}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"msg": "Invoice received"})


@test("invoice_notification callback can be invoked directly")
def dummy_callback():
    # Just for coverage.
    mod.invoice_notification({})


@test("OpenAPI schema includes the registered callbacks")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/invoices/": {
                        "post": {
                            "summary": "Create Invoice",
                            "description": 'Create an invoice.\n\nThis will (let\'s imagine) let the API user (some external developer) create an\ninvoice.\n\nAnd this path operation will:\n\n* Send the invoice to the client.\n* Collect the money from the client.\n* Send a notification back to the API user (the external developer), as a callback.\n    * At this point is that the API will somehow send a POST request to the\n        external API with the notification of the invoice event\n        (e.g. "payment successful").',
                            "operationId": "create_invoice_invoices__post",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [
                                            {
                                                "type": "string",
                                                "format": "uri",
                                                "minLength": 1,
                                                "maxLength": 2083,
                                            },
                                            {"type": "null"},
                                        ],
                                        "title": "Callback Url",
                                    },
                                    "name": "callback_url",
                                    "in": "query",
                                }
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Invoice"
                                        }
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "422": {
                                    "description": "Validation Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError"
                                            }
                                        }
                                    },
                                },
                            },
                            "callbacks": {
                                "invoice_notification": {
                                    "{$callback_url}/invoices/{$request.body.id}": {
                                        "post": {
                                            "summary": "Invoice Notification",
                                            "operationId": "invoice_notification__callback_url__invoices___request_body_id__post",
                                            "requestBody": {
                                                "required": True,
                                                "content": {
                                                    "application/json": {
                                                        "schema": {
                                                            "$ref": "#/components/schemas/InvoiceEvent"
                                                        }
                                                    }
                                                },
                                            },
                                            "responses": {
                                                "200": {
                                                    "description": "Successful Response",
                                                    "content": {
                                                        "application/json": {
                                                            "schema": {
                                                                "$ref": "#/components/schemas/InvoiceEventReceived"
                                                            }
                                                        }
                                                    },
                                                },
                                                "422": {
                                                    "description": "Validation Error",
                                                    "content": {
                                                        "application/json": {
                                                            "schema": {
                                                                "$ref": "#/components/schemas/HTTPValidationError"
                                                            }
                                                        }
                                                    },
                                                },
                                            },
                                        }
                                    }
                                }
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "HTTPValidationError": {
                            "title": "HTTPValidationError",
                            "type": "object",
                            "properties": {
                                "detail": {
                                    "title": "Detail",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                }
                            },
                        },
                        "Invoice": {
                            "title": "Invoice",
                            "required": ["id", "customer", "total"],
                            "type": "object",
                            "properties": {
                                "id": {"title": "Id", "type": "string"},
                                "title": {
                                    "title": "Title",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "customer": {"title": "Customer", "type": "string"},
                                "total": {"title": "Total", "type": "number"},
                            },
                        },
                        "InvoiceEvent": {
                            "title": "InvoiceEvent",
                            "required": ["description", "paid"],
                            "type": "object",
                            "properties": {
                                "description": {
                                    "title": "Description",
                                    "type": "string",
                                },
                                "paid": {"title": "Paid", "type": "boolean"},
                            },
                        },
                        "InvoiceEventReceived": {
                            "title": "InvoiceEventReceived",
                            "required": ["ok"],
                            "type": "object",
                            "properties": {"ok": {"title": "Ok", "type": "boolean"}},
                        },
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "title": "Location",
                                    "type": "array",
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                },
                                "msg": {"title": "Message", "type": "string"},
                                "type": {"title": "Error Type", "type": "string"},
                                "input": {"title": "Input"},
                                "ctx": {"title": "Context", "type": "object"},
                            },
                        },
                    }
                },
            }
        )
    )
