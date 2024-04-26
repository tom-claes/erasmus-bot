from langchain.docstore.document import Document
from langchain_community.document_transformers import BeautifulSoupTransformer


bs_transformer = BeautifulSoupTransformer()


with open('erasmus-site-parsed/opleidingen_toegepaste-informatica.html', 'r') as file:
    html_content = file.read()

document = [Document(page_content = html_content)]

doc_transformed = bs_transformer.transform_documents(document, tags_to_extract=["span", "table", "li", "d", "h1", "h2", "h3", "h4", "h5", "p"], unwanted_tags=["a"])[0]
print(doc_transformed.page_content)