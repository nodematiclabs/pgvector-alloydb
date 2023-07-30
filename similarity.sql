SELECT id
FROM embeddings
ORDER BY embedding <-> (SELECT embedding FROM embeddings ORDER BY id DESC LIMIT 1)
LIMIT 2;