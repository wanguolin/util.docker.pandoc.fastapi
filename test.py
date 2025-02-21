import requests
import base64
import webbrowser
from pathlib import Path
import tempfile

import dotenv
import os

dotenv.load_dotenv()

GATEWAY_URL = os.getenv("GATEWAY_URL")
API_KEY = os.getenv("API_KEY")


def main():
    gateway_url = GATEWAY_URL
    api_key = API_KEY

    # Test markdown content
    markdown_content = """# Test Document
## Section 1
This is a test."""

    print(f"\nUsing test content:\n{markdown_content}")

    try:
        # Convert content to base64
        base64_content = base64.b64encode(markdown_content.encode()).decode()
        print("\nConverted content to base64")

        print(f"\nSending request to: {gateway_url}")
        response = requests.post(
            gateway_url,
            json={"content": base64_content},
            headers={
                "Content-Type": "application/json",
                "Accept": "application/pdf",
                "x-api-key": api_key,
            },
        )

        print(f"\nResponse status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")

        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(response.content)
                tmp_path = Path(tmp.name)

            print(f"\nSuccess! Opening PDF in browser...")
            print(f"Temporary file location: {tmp_path}")
            webbrowser.open(f"file://{tmp_path.absolute()}")
        else:
            print(f"\nError: Status code {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"\nError occurred: {str(e)}")


if __name__ == "__main__":
    main()
