from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_risk_commentary(
    commodity,
    risk_increase,
    shock_multiplier
):
    """
    Generate AI-powered financial commentary.
    """

    prompt = f"""
    You are a financial risk analyst AI.

    Analyze the following scenario:

    Commodity: {commodity}

    Risk Increase:
    {risk_increase:.2f}

    Shock Multiplier:
    {shock_multiplier}

    Explain:
    - market impact,
    - financial implications,
    - possible causes,
    - investor risk concerns.

    Keep response concise and professional.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content