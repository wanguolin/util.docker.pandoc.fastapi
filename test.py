import requests
import base64
import webbrowser
from pathlib import Path
import tempfile

markdown_content = """
# Test Document
## Section 1
This is a test.
"""

base64_content = base64.b64encode(markdown_content.encode()).decode()

response = requests.post(
    "http://localhost:8080/convert", json={"content": base64_content}
)

if response.status_code == 200:
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = Path(tmp.name)

    # 用默认浏览器打开 PDF
    webbrowser.open(f"file://{tmp_path.absolute()}")
    print(f"Opening PDF in browser. Temporary file: {tmp_path}")
else:
    print(f"Error: {response.status_code}")
