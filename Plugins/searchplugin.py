from Plugins.search import SearchNews
from typing import Optional, List
from semantic_kernel.kernel_pydantic import KernelBaseModel
from utils import *
from typing import TYPE_CHECKING, Annotated
from utils import *
from semantic_kernel.functions import KernelArguments, kernel_function
import logging,re



### Defining Pydantic model for the plugin
class News(KernelBaseModel):
    title: str 
    content: str 

class Code(KernelBaseModel):
    company_code: str


class SearchPlugin:

    def __init__(self):
        self.searchengine = SearchNews(csv_path="Resources/newsdata.csv")

    @kernel_function(name="SearchNews", description="fetch stock market related news for a particular timeframe.")
    async def search_news(
        self,
        from_date: Annotated[str, "starting date for which news is to be fetched.Expects in YYYY-MM-DD format.eg:2024-05-01"],
        company_code: Optional[Annotated[str, f"code of the company obtained from SearchCode function"]] = None,
        to_date: Optional[Annotated[str, "end date for for which news is fetched.Expects in YYYY-MM-DD format.eg:2024-05-08"]] = None,
    ) -> Annotated[list[dict], "list of dict containing title and content of news"]:
        
        """Search for news artciles based on keyword"""
        logging.info(f"CALLING SearchNews Function: {str(company_code),from_date,to_date}")


   
        news_list = self.searchengine.get_news(company_code=company_code,from_date=from_date,to_date=to_date)
        

        logging.info(f"OUTPUT SearchNews Function:{news_list}")
        news_list = [News(title=item['title'], content=item['content']) for item in news_list]
        
        return news_list
    

    @kernel_function(name="SearchCode",description="Extrats company name from user query and returns corresponding code")
    async def search_code(
        self,
        company_name: Annotated[str, "name of the company"]
    )-> Annotated[str, "code of company in stockmarket"]:
        
        
        company_code = None
        if 'facebook' in company_name.lower() or 'meta' in company_name.lower():
            company_code =  "META"
        if 'amazon' in company_name.lower():
            company_code =  "AMZN"
        if 'google' in company_name.lower():
            company_code =  "GOOG"
        if 'netflix' in company_name.lower():
            company_code =   "NFLX"
        
        logging.info(f"COMPANY NAME: {company_name} and COMPANY CODE: {company_code}")
        return Code(company_code=company_code)



