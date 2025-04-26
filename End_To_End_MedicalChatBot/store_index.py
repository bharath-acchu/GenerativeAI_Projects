from src.helper import load_pdf,text_split,getGoogleEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
load_dotenv()
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

extracted_data = load_pdf(data='Data/')
text_chunks = text_split(extracted_data)
embeddings = getGoogleEmbeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"

pc.create_index(
    name=index_name,
    dimension=768, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)


def batch(iterable, batch_size=500):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

for chunk_batch in batch(text_chunks, batch_size=500):
    PineconeVectorStore.from_documents(
        documents=chunk_batch,
        index_name=index_name,
        embedding=embeddings
    )

print("✅ Uploaded safely in manual batches!")
