import aiohttp
import asyncio
import os, sys
from dotenv import load_dotenv
from datetime import datetime
import aiomysql

API_URL = "https://www.federalregister.gov/api/v1/documents.json"
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
}

async def fetch_data():
    today = datetime.today().strftime("%Y-%m-%d")
    params = {
        "per_page": 10,
        "order": "newest",
        "conditions[publication_date][gte]": "2025-06-01",
        "conditions[publication_date][lte]": today
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching data: {response.status}")
                return {}

async def save_to_db(data):
    conn = await aiomysql.connect(
        host=DB_CONFIG["host"],
        port=3306,
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["db"],
        autocommit=True
    )
    def clean_text(value):
        if not value:
            return ""
        return str(value).replace("\n", " ").replace('"', "'").strip()
    async with conn.cursor() as cur:
        for doc in data.get("results", []):
            title = (doc.get("title") or "").replace('\n', ' ').replace('"', "'")
            publication_date = doc.get("publication_date")
            agency_names = ", ".join(doc.get("agency_names", []))
            abstract = (doc.get("abstract") or "").replace('\n', ' ').replace('"', "'")

            await cur.execute("""
                INSERT INTO documents (document_number, title, publication_date, agency_names, summary)
                VALUES (%s, %s, %s, %s, %s) AS new
                ON DUPLICATE KEY UPDATE
                    title = new.title,
                    publication_date = new.publication_date,
                    agency_names = new.agency_names,
                    summary = new.summary
            """, (
                doc.get("document_number"),
                title,
                publication_date,
                agency_names,
                abstract
            ))
    conn.close()

async def main():
    print(" Fetching documents...")
    data = await fetch_data()
    if data:
        print(f" Fetched {len(data.get('results', []))} documents. Saving...")
        await save_to_db(data)
        print("Saved successfully.")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
