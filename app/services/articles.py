import uuid
from logging import Logger
from sqlalchemy.exc import DatabaseError
from app.database.tables import ArticlesDatabase
from app.tools.openai_service import OpenAIService
from app.schemas.articles import ArticleCreateSchema


class ArticlesService:
    def __init__(self, logger: Logger, dbManager, openai_service: OpenAIService):
        self.articles_db = ArticlesDatabase(dbManager)
        self.logger = logger
        self.openai_service = openai_service

    async def create_article(self, data):
        # validate schema
        ArticleCreateSchema().load(data)
        try:
            data["id"] = uuid.uuid4()
            await self.articles_db.create_article(data)
            return {
                "id": str(data["id"]),
                "title": data["title"],
                "content": data["content"],
                "summary": None
            }
        except DatabaseError as e:
            self.logger.error("Error creating article")
            raise Exception(e)
        except Exception as e:
            self.logger.error(f"ERROR: {str(e)}")
            raise Exception(e)

    async def get_by_id(self, id):
        try:
            result = await self.articles_db.get_one_by_id(id)
            return result
        except DatabaseError as e:
            self.logger.error("Error retrieving article")
            raise Exception(e)
        except Exception as e:
            self.logger.error(f"ERROR: {str(e)}")

    async def summarize(self, id):
        article = None
        result = None
        try:
            article = await self.articles_db.get_one_by_id(id)
        except DatabaseError as e:
            self.logger.error("Error retrieving article")
            raise Exception(e)
            
        if (article):
            summary = None
            try:
                summary_result = await self.openai_service.summarize_text(article["content"])
                summary = summary_result.content
            except Exception as e:
                raise Exception(e)

            if (summary):
                try:
                    await self.articles_db.update_by_id(id, summary)
                    result = {
                        **article,
                        "summary": summary
                    }
                except DatabaseError as e:
                    self.logger.error("Error updating article")
                    raise Exception(e)
        return result
