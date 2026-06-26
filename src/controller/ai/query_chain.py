from .llm import llm
from .parser import query_parser
from .prompt import SQL_PROMPT_TEMPLATE, RISK_PROMPT_TEMPLATE
from langchain_core.prompts import PromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy import text
from langchain_core.output_parsers import PydanticOutputParser
from src.controller.ai.schema import RiskAssessment

parser = PydanticOutputParser(pydantic_object=RiskAssessment)

sql_prompt = PromptTemplate.from_template(SQL_PROMPT_TEMPLATE)
risk_prompt = PromptTemplate(
    template=RISK_PROMPT_TEMPLATE,
    input_variables=["asset_data"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

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
    


async def analyze_asset_risk(asset_data: dict) -> RiskAssessment:
    # 1. إنشاء الـ Chain
    chain = risk_prompt | llm | parser
    
    # 2. الاستدعاء
    result = await chain.ainvoke({"asset_data": str(asset_data)})
    return result