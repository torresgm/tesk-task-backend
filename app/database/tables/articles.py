import sqlalchemy
from app.database.manager import DatabaseManager


class ArticlesDatabase:
    def __init__(self, dbManager: DatabaseManager):
        self.table = sqlalchemy.Table(
            "articles",
            dbManager.metadata,
            sqlalchemy.Column("id", sqlalchemy.UUID(
                as_uuid=True), primary_key=True),
            sqlalchemy.Column("title", sqlalchemy.String(255), nullable=False),
            sqlalchemy.Column("content", sqlalchemy.Text, nullable=False),
            sqlalchemy.Column("summary", sqlalchemy.Text, nullable=True),
        )
        self.db = dbManager.database

    async def create_article(self, data):
        query = self.table.insert().values(
            id=data["id"],
            title=data["title"],
            content=data["content"]
        )
        await self.db.execute(query)

    async def get_one_by_id(self, id):
        query = self.table.select().where(self.table.c.id == id)
        result = await self.db.fetch_one(query)
        content = None
        if (result):
            content = {
                **result,
                "id": str(result["id"])
            }
        return content

    async def update_by_id(self, id, new_value):
        query = self.table.update().where(self.table.c.id == id).values(summary=new_value)
        await self.db.execute(query)
