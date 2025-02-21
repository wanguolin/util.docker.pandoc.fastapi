from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import base64
import tempfile
import subprocess
import os

app = FastAPI()


@app.post("/convert")
async def convert_markdown(request: Request):
    data = await request.json()
    markdown_content = base64.b64decode(data["content"]).decode("utf-8")

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_md:
        temp_md.write(markdown_content.encode("utf-8"))
        temp_md.flush()
        pdf_path = temp_md.name.replace(".md", ".pdf")

        subprocess.run(
            ["pandoc", temp_md.name, "-o", pdf_path, "--pdf-engine=wkhtmltopdf"]
        )

        def iterfile():
            with open(pdf_path, "rb") as f:
                yield from f
            os.unlink(temp_md.name)
            os.unlink(pdf_path)

        return StreamingResponse(
            iterfile(),
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=converted.pdf"},
        )
