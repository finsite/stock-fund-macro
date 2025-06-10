"""Processor module for macroeconomic data analysis.

This module processes incoming macroeconomic data messages and prepares
them for publishing or storage. It includes basic validation and transformation
logic that can be extended with more sophisticated analysis.
"""

from typing import Any

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def process_macro_data(data: dict[str, Any]) -> dict[str, Any]:
    """Process a macroeconomic data payload.

    This function validates and enriches incoming macro data.
    Expected keys may include 'indicator', 'value', 'unit', 'date', etc.

    Args:
        data (dict[str, Any]): The raw macroeconomic data message.

    Returns:
        dict[str, Any]: The validated and enriched message ready for output.
    """
    if "indicator" not in data or "value" not in data:
        logger.warning("📉 Invalid macro data: missing required fields.")
        data["valid"] = False
        return data

    # Example enrichment: normalize units or categorize indicators
    indicator = data["indicator"].lower()
    data["category"] = _categorize_indicator(indicator)
    data["valid"] = True

    logger.debug("✅ Processed macro data: %s", data)
    return data


def _categorize_indicator(indicator: str) -> str:
    """Assign a category based on the macroeconomic indicator name."""
    if any(keyword in indicator for keyword in ["gdp", "growth", "output"]):
        return "economic_growth"
    if any(keyword in indicator for keyword in ["inflation", "cpi", "ppi"]):
        return "price_stability"
    if any(keyword in indicator for keyword in ["unemployment", "jobs", "labor"]):
        return "employment"
    if any(keyword in indicator for keyword in ["rate", "interest", "fed"]):
        return "monetary_policy"
    return "other"
