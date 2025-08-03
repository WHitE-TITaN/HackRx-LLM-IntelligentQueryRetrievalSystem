import pdfplumber as pdfReader
import requests
from io import BytesIO

class TextPullOut:
  def extractText(self, linkFile: str) -> str:
    file = requests.get(linkFile)
    with pdfReader.open(BytesIO(file.content)) as pdf:
      text = ""
      for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
          text += page_text + "\n"

    return text
