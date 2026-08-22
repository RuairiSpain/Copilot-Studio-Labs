"""Construct a Copilot Studio client, delegated or application (SP).

Both paths need the `CopilotStudio.Copilots.Invoke` permission — delegated
on the signed-in user, application on the service principal. Delegated is
the notebook-local variant (interactive device-code sign-in); application
is the CI-safe variant. Notebook 01 exercises both so the difference is
felt once, early, rather than discovered in a pipeline failure.
"""
from __future__ import annotations

from csx.config import Settings

SCOPE = "https://api.powerplatform.com/CopilotStudio.Copilots.Invoke"


def get_delegated_token(settings: Settings) -> str:
    """Interactive device-code flow, public client. Local/notebook use only."""
    import msal

    settings.require("TENANT_ID", "DELEGATED_CLIENT_ID")
    app = msal.PublicClientApplication(
        client_id=settings.get("DELEGATED_CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{settings.get('TENANT_ID')}",
    )
    flow = app.initiate_device_flow(scopes=[SCOPE])
    if "user_code" not in flow:
        raise RuntimeError(f"Failed to create device flow: {flow}")
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(f"Token acquisition failed: {result.get('error_description')}")
    return result["access_token"]


def get_application_token(settings: Settings) -> str:
    """Client-credentials flow, confidential client / service principal. CI-safe."""
    import msal

    settings.require("TENANT_ID", "APP_CLIENT_ID", "APP_CLIENT_SECRET")
    app = msal.ConfidentialClientApplication(
        client_id=settings.get("APP_CLIENT_ID"),
        client_credential=settings.get("APP_CLIENT_SECRET"),
        authority=f"https://login.microsoftonline.com/{settings.get('TENANT_ID')}",
    )
    result = app.acquire_token_for_client(scopes=["https://api.powerplatform.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"Token acquisition failed: {result.get('error_description')}")
    return result["access_token"]


def get_copilot_client(settings: Settings, delegated: bool = True):
    """Build a microsoft_agents.copilotstudio.client.CopilotClient.

    delegated=True  -> interactive device-code token (local notebook run)
    delegated=False -> service-principal token (CI / non-interactive run)
    """
    from microsoft_agents.copilotstudio.client import (
        ConnectionSettings,
        CopilotClient,
        PowerPlatformCloud,
        AgentType,
    )

    settings.require("DATAVERSE_ENV_ID", "AGENT_SCHEMA_NAME")
    token = get_delegated_token(settings) if delegated else get_application_token(settings)

    connection = ConnectionSettings(
        environment_id=settings.get("DATAVERSE_ENV_ID"),
        agent_identifier=settings.get("AGENT_SCHEMA_NAME"),  # publisher-prefix_sanitized-name
        cloud=PowerPlatformCloud.PROD,
        copilot_agent_type=AgentType.PUBLISHED,
        custom_power_platform_cloud=None,
    )
    return CopilotClient(connection, token)
