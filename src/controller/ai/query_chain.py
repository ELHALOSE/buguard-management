from .llm import llm
from .parser import query_parser
from .prompt import SQL_PROMPT_TEMPLATE
from langchain_core.prompts import PromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy import text

sql_prompt = PromptTemplate.from_template(SQL_PROMPT_TEMPLATE)

# دمج الـ Prompt مع نموذج Gemini
sql_generation_chain = sql_prompt | llm 


async def process_natural_language_query(db: AsyncSession, user_question: str) -> dict:
    # 1. توليد الاستعلام من النموذج
    raw_response = await sql_generation_chain.ainvoke({"question": user_question})
    sql_query = raw_response.content.strip().replace("```sql", "").replace("```", "").strip()
    
    # 2. الحماية (Guardrails): التأكد من أن السؤال في النطاق وأن الاستعلام آمن
    if sql_query == "OUT_OF_SCOPE":
        return {"error": "The question is out of scope. Please ask about assets, certificates, domains, etc."}
    
    if not sql_query.lower().startswith("select"):
        return {"error": "Invalid operation. Only SELECT queries are allowed."}

    # 3. تنفيذ الاستعلام على قاعدة البيانات بأمان
    try:
        result = await db.execute(text(sql_query))
        rows = result.mappings().all() # يحول النتائج إلى قواميس (Dictionaries)
        
        return {
            "query_used": sql_query,
            "results_count": len(rows),
            "data": [dict(row) for row in rows]
        }
    except Exception as e:
        logging.error(f"DB Execution Error: {str(e)}")
        return {"error": "Could not execute the query. Please rephrase your question."}