import chromadb
from chromadb.config import Settings
import ollama
from pyzotero import zotero
from tqdm import tqdm
import os
import subprocess

QUERY = "Auscultation is not reliable"
N_CONTEXT = 5
LOADING_ZOTERO = False
LLM_QUERY = True
RESET = False
MODEL = "phi3:mini"

process = subprocess.Popen(["ollama", "run", MODEL])
process.terminate()

# setup Chroma in-memory, for easy prototyping. Can add persistence easily!
client = chromadb.PersistentClient(settings=Settings(allow_reset=True))
if RESET:
    client.reset()

# Create collection. get_collection, get_or_create_collection, delete_collection also available!
collection = client.get_or_create_collection("all-my-documents")

if LOADING_ZOTERO:
    print("\nFetching data...")

    # Initialize Zotero client for user (use group id and "group" for group libraries)
    zot = zotero.Zotero(
        library_id=os.environ.get("ZOTERO_USER_ID"),
        library_type="user",
        api_key=os.environ.get("ZOTERO_API_KEY"),
        local=False
    )

    annotations = zot.everything(zot.items(itemType="annotation"))

    for annotation in tqdm(annotations):
        annot = annotation['data']
        if 'annotationText' in annot:
            content = annot['annotationText']
            #annotationComment = annot['annotationComment']
            #annotationTags = annot['annotationTags']
            collection.add(
                documents=[content],
                # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
                metadatas=[{"parent": annot['parentItem']}],
                ids=[annot["key"]],
            )

print("\nRetrieving context...")

# Query/search most similar results. You can also .get by id
results = collection.query(
    query_texts=[QUERY],
    n_results=N_CONTEXT,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)

for i, key in enumerate(results['ids'][0]):
    parent = results['metadatas'][0][i]['parent']
    text = results['documents'][0][i]
    print(f"\nzotero://open-pdf/library/items/{parent}?annotation={key.ljust(40)}: {results['distances'][0][i]}")
    print(text)

context = "\n".join(results['documents'][0])

if LLM_QUERY:
    print("\nLLM query...")

    response = ollama.chat(model=MODEL, messages=[
        {"role": "system",
         "content": "You are a helpful scientific assistant. Use exclusively the provided context to answer the user's question."},
        {"role": "user", "content": f"Context:\n{context}\nUser query: Write a short paragraph on this topic: {QUERY}"}
    ])

    if response['done']:
        print(response['message']['content'])
    else:
        print("Something went wrong...")