from langchain_core.output_parsers import JsonOutputParser

from .schema import AssetQuery

query_parser = JsonOutputParser(
    pydantic_object=AssetQuery
)
