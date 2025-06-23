import aiomysql
from fetch import DB_CONFIG  
async def query_federal_documents(query:str):
   
    try:
        if not query.strip().lower().startswith("select"):
            return "Only SELECT queries are allowed."

        conn = await aiomysql.connect(**DB_CONFIG)
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query)
            result = await cursor.fetchall()
        conn.close()
        if not result:
            return "No documents found for your query."

        return "\n\n".join(
            f" Title: {row['title']}\n Date: {row['publication_date']}\nAgency: {row['agency_names']}\n Summary: {row['summary']}"
            for row in result
        )
 
    except Exception as e:
        return f"Database query failed with error: {e}"
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_federal_documents",
            "description": "Queries the federal documents database with a raw SQL SELECT statement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A valid SQL SELECT query to run against the documents table.",
                    },
                },
                "required": ["query"],
            },
        },
    }
]

available_tools = {
    "query_federal_documents": query_federal_documents,
}