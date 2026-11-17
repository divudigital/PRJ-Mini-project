from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

embeddings = FakeEmbeddings(
    size=1536
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)

def get_context(query):

    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context