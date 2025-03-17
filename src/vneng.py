#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from typing import ClassVar, NoReturn, List, Dict, Any

# Related third-party module imports
import requests


class VNEngine:
    """
    Virtual Number Engine
    """
    def __init__(self, use_mock: bool = False) -> NoReturn:
        """
        Initialize variables for the engine

        Parameters:
            use_mock (bool): Whether to use the mock API
        """
        # Set the API base URL
        self.lang: str = "?lang=en"
        self.base: str = "https://mock.temp-number.org/v1" if use_mock else "https://tn-api.com/api/v1"
        self.endpoint: str = "free_numbers_content/"
        self.country_url: str = f"{self.base}/{self.endpoint}countries"

    def get_online_countries(self) -> List[Dict[str, str]]:
        """
        Get details about available countries

        Returns:
            list: Online countries
        """
        response: ClassVar[Any] = requests.get(url=self.country_url).json()
        
        if response.get("response") == "1":
            all_countries: List[Dict[str, str]] = response.get("countries", [])
            return [country for country in all_countries if country.get("online")]
        return []

    def get_country_numbers(self, country: str) -> List[Dict[str, str]]:
        """
        Get specific country numbers

        Parameters:
            country (str): Country name (e.g., Russia, Spain)

        Returns:
            list: Available numbers for that country
        """
        numbers_url: str = f"{self.country_url}/{country}{self.lang}"
        response: ClassVar[Any] = requests.get(url=numbers_url).json()
        
        if response.get("response") == "1":
            return [{"human_readable": num["data_humans"], "full_number": num["full_number"]} for num in response.get("numbers", [])]
        return []

    def get_number_inbox(self, country: str, number: str) -> List[Dict[str, str]]:
        """
        Get inbox messages of a specific number

        Parameters:
            country (str): Country name (e.g., Russia, Spain)
            number (str): Number code for the country

        Returns:
            list: Messages in the number's inbox
        """
        number_detail_url: str = f"{self.country_url}/{country}/{number}{self.lang}"
        response: ClassVar[Any] = requests.get(url=number_detail_url).json()
        
        if response.get("response") == "1" and response.get("online"):
            return [{msg["data_humans"]: msg["text"]} for msg in response.get("messages", {}).get("data", [])]
        return []
