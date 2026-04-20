from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma(collection_name="bot_personas", embedding_function=embedding)

personas = {
    "bot_a": "I believe AI and crypto will solve all human problems.",
    "bot_b": "I believe tech monopolies are destroying society.",
    "bot_c": "I care about markets, ROI, trading."
}

for bot_id, text in personas.items():
    db.add_texts([text], metadatas=[{"bot_id": bot_id}])

def route_post_to_bots(post_content, threshold=0.5):
    results = db.similarity_search_with_score(post_content, k=3)

    matched = []
    for doc, score in results:
        similarity = 1 - score
        if similarity > threshold:
            matched.append(doc.metadata["bot_id"])

    return matched


if __name__ == "__main__":
    print(route_post_to_bots("New AI model released"))