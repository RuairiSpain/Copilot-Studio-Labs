"""Dataverse Web API helpers for Part 2 (notebooks 26, 31).

Part 1 treated `crd_supplierspend` / `crd_supplierperformance` as if they
already existed (workflows and MCP tools query them from `09` onward).
Notebook `26` is where they're actually modeled — this module is the
thin, idempotent (get-or-create) wrapper around the Web API calls that
takes, so the notebook cell reads as intent, not raw HTTP.
"""
from __future__ import annotations

import requests

from csx.config import Settings

API_VERSION = "v9.2"


def _base_url(settings: Settings) -> str:
    settings.require("DATAVERSE_ENV_URL")
    return f"{settings.get('DATAVERSE_ENV_URL').rstrip('/')}/api/data/{API_VERSION}"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
    }


def get_or_create_table(settings: Settings, token: str, logical_name: str, display_name: str,
                          primary_column_display_name: str = "Name") -> dict:
    """EntityMetadata get-or-create. Re-running notebook 26 must not error
    on a table that already exists — that's the whole point of this
    wrapper over a raw POST."""
    base = _base_url(settings)
    existing = requests.get(
        f"{base}/EntityDefinitions(LogicalName='{logical_name}')",
        headers=_headers(token),
    )
    if existing.status_code == 200:
        print(f"[dataverse] table '{logical_name}' already exists — reusing")
        return existing.json()

    body = {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
        "SchemaName": logical_name,
        "DisplayName": {"@odata.type": "Microsoft.Dynamics.CRM.Label",
                          "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                                 "Label": display_name, "LanguageCode": 1033}]},
        "DisplayCollectionName": {"@odata.type": "Microsoft.Dynamics.CRM.Label",
                                    "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                                           "Label": f"{display_name}s", "LanguageCode": 1033}]},
        "OwnershipType": "UserOwned",
        "IsActivity": False,
        "PrimaryNameAttribute": f"{logical_name}_name",
        "Attributes": [{
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": f"{logical_name}_name",
            "MaxLength": 200,
            "DisplayName": {"@odata.type": "Microsoft.Dynamics.CRM.Label",
                              "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                                     "Label": primary_column_display_name, "LanguageCode": 1033}]},
        }],
    }
    response = requests.post(f"{base}/EntityDefinitions", headers=_headers(token), json=body)
    response.raise_for_status()
    print(f"[dataverse] created table '{logical_name}'")
    return {"LogicalName": logical_name}


def get_or_create_column(settings: Settings, token: str, table_logical_name: str,
                           column_logical_name: str, attribute_type: str, display_name: str,
                           extra: dict | None = None) -> None:
    base = _base_url(settings)
    existing = requests.get(
        f"{base}/EntityDefinitions(LogicalName='{table_logical_name}')/Attributes(LogicalName='{column_logical_name}')",
        headers=_headers(token),
    )
    if existing.status_code == 200:
        print(f"[dataverse] column '{table_logical_name}.{column_logical_name}' already exists — reusing")
        return

    body = {
        "@odata.type": attribute_type,
        "SchemaName": column_logical_name,
        "DisplayName": {"@odata.type": "Microsoft.Dynamics.CRM.Label",
                          "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                                 "Label": display_name, "LanguageCode": 1033}]},
        **(extra or {}),
    }
    response = requests.post(
        f"{base}/EntityDefinitions(LogicalName='{table_logical_name}')/Attributes",
        headers=_headers(token), json=body,
    )
    response.raise_for_status()
    print(f"[dataverse] created column '{table_logical_name}.{column_logical_name}'")


def upsert_row(settings: Settings, token: str, table_set_name: str, alternate_key: dict, fields: dict) -> str:
    """Upsert by alternate key — the get-or-create pattern for row data,
    used by 26's seed data and 31's write-back verification."""
    base = _base_url(settings)
    key = ",".join(f"{k}='{v}'" for k, v in alternate_key.items())
    headers = {**_headers(token), "Prefer": "return=representation"}
    response = requests.patch(f"{base}/{table_set_name}({key})", headers=headers, json=fields)
    response.raise_for_status()
    return response.headers.get("OData-EntityId", "")


def get_row(settings: Settings, token: str, table_set_name: str, row_id: str, select: list[str] | None = None) -> dict:
    base = _base_url(settings)
    params = {"$select": ",".join(select)} if select else {}
    response = requests.get(f"{base}/{table_set_name}({row_id})", headers=_headers(token), params=params)
    response.raise_for_status()
    return response.json()


def assert_security_role_scoped(settings: Settings, token_as_restricted_user: str,
                                  table_set_name: str, row_id: str) -> bool:
    """Returns True if the restricted-user token is correctly denied read
    access — the app-side equivalent of 05's SharePoint trimming pair.
    A 403/404 here is success, not failure."""
    base = _base_url(settings)
    response = requests.get(f"{base}/{table_set_name}({row_id})", headers=_headers(token_as_restricted_user))
    return response.status_code in (403, 404)
