import pdfplumber as pdfReader
import requests
from io import BytesIO
from typing import List

class TextPullOut:
  def chunking (self, text : str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

  def extractText(self, linkFile: str) -> str:
    file = requests.get(linkFile)
    with pdfReader.open(BytesIO(file.content)) as pdf:
      text = ""
      for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
          text += page_text + "\n"

    return text
  
  def chunkedText(self, linkFile:str) -> list[str]:
    text = self.extractText(linkFile)
    return self.chunking(text)

