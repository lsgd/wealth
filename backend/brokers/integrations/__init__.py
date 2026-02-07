"""
Broker integration factory.
"""
from typing import Any, Dict

from brokers.models import Broker

from .base import BrokerIntegrationBase


def get_broker_integration(
    broker: Broker,
    credentials: Dict[str, Any]
) -> BrokerIntegrationBase:
    """
    Factory function to get the appropriate broker integration.

    Args:
        broker: The Broker model instance
        credentials: Decrypted credentials dictionary

    Returns:
        BrokerIntegrationBase: The appropriate integration instance

    Raises:
        ValueError: If the broker is not supported
    """
    if broker.integration_type == 'fints':
        from .fints_integration import FinTSIntegration
        return FinTSIntegration(
            credentials=credentials,
            bank_identifier=broker.bank_identifier,
            fints_server=broker.fints_server
        )

    if broker.code == 'ibkr':
        # Check if using Flex Web Service (token-based) or Gateway
        if credentials.get('flex_token') and credentials.get('query_id'):
            from .ibkr_flex import IBKRFlexIntegration
            return IBKRFlexIntegration(credentials=credentials)
        else:
            from .ibkr import IBKRIntegration
            return IBKRIntegration(
                credentials=credentials,
                gateway_url=broker.api_base_url or 'https://localhost:5000'
            )

    if broker.code == 'truewealth':
        from .truewealth import TrueWealthIntegration
        return TrueWealthIntegration(credentials=credentials)

    if broker.code == 'viac':
        from .viac import VIACIntegration
        return VIACIntegration(credentials=credentials)

    if broker.code == 'morganstanley':
        from .morganstanley import MorganStanleyIntegration
        return MorganStanleyIntegration(credentials=credentials)

    if broker.code == 'ibkr_flex':
        from .ibkr_flex import IBKRFlexIntegration
        return IBKRFlexIntegration(credentials=credentials)

    raise ValueError(f"Broker '{broker.code}' is not yet supported for automated sync.")
