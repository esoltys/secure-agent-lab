# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from functools import cached_property
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from google.genai import Client

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"


# Define the custom Gemini model wrapper that retrieves the API key from environment variables
class KeyGemini(Gemini):
    api_key: str = ""

    @cached_property
    def api_client(self) -> Client:
        import os

        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
        key = self.api_key or os.environ.get("GEMINI_API_KEY", "")
        return Client(api_key=key)

    @cached_property
    def _live_api_client(self) -> Client:
        import os

        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
        key = self.api_key or os.environ.get("GEMINI_API_KEY", "")
        return Client(api_key=key)


# In-memory store for registered users and discount codes
REGISTERED_USERS = {"user_123", "user_456", "user_789"}
VALID_DISCOUNT_CODES = {"WELCOME50", "SUMMER20"}
REDEEMED_CODES = set()


def redeem_discount_code(user_id: str, code: str) -> str:
    """Redeems a single-use discount code for a registered user.

    Args:
        user_id: The registered user ID of the customer (e.g. user_123).
        code: The discount code to redeem (e.g. WELCOME50, SUMMER20).

    Returns:
        A message indicating whether the redemption was successful or the reason for failure.
    """
    code_upper = code.strip().upper()

    if user_id not in REGISTERED_USERS:
        return f"Error: User ID '{user_id}' is not registered."

    if code_upper not in VALID_DISCOUNT_CODES:
        return f"Error: Discount code '{code_upper}' is invalid."

    if code_upper in REDEEMED_CODES:
        return f"Error: Discount code '{code_upper}' has already been redeemed."

    REDEEMED_CODES.add(code_upper)
    return f"Success: Discount code '{code_upper}' has been successfully redeemed for user '{user_id}'!"


root_agent = Agent(
    name="root_agent",
    model=KeyGemini(
        model="gemini-2.5-flash",
        api_key=os.environ.get("GEMINI_API_KEY", ""),
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are an AI shopping assistant for a retail store. Assist customers with their shopping queries, product information, and discount code redemptions using the tools provided.",
    tools=[redeem_discount_code],
)

app = App(
    root_agent=root_agent,
    name="app",
)
