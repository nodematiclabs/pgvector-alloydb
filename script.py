import psycopg2

from vertexai.language_models import TextEmbeddingModel

model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

embeddings = model.get_embeddings([
    "A candlelit dinner in New York City",
    "A sunset Paella dinner on the beach",
    "An Argentinian steakhouse dinner"
])
for i, embedding in enumerate(embeddings):
    vector = embedding.values

    try:
        # Connect to the postgres DB
        conn = psycopg2.connect(
            dbname="demonstration",
            user="postgres",
            password="CHANGEME",
            host="CHANGEME",
            port="5432"
        )
        cur = conn.cursor()

        # SQL query to insert the vector
        query = f"""
        INSERT INTO embeddings
        VALUES ({i}, '[{','.join(map(str, vector))}]')
        """
        cur.execute(query, (list(vector),))
        conn.commit()

        print("Successfully saved the vector to the database")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()