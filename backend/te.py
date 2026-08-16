from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


pdf_path = "data/uploads/Machine_Learning.pdf"
path = Path(pdf_path)
loader = PyPDFLoader(str(path))

documents = loader.load()
print("Hello\n")
print(len(documents))
