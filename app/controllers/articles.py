from marshmallow import ValidationError
from starlette.responses import JSONResponse
from app.services import ArticlesService
from logging import Logger
from starlette.exceptions import HTTPException
from app.responses import response, server_error_response


class ArticlesController:
    def __init__(self, logger: Logger, dbManager, openai_service):
        self.article_service = ArticlesService(
            logger, dbManager, openai_service)
        self.logger = logger

    def init_routes(self):
        path = "/articles"
        return [
            (path, "POST", self.articles_create),
            (path + "/{id}", "GET", self.articles_get),
            (path + "/{id}/summarize", "POST", self.articles_summarize)
        ]

    async def articles_create(self, request):
        """
        tags: ['Articles']
        description: Create new article data.
        requestBody:
          required: true
          description: Article data to be added.
          content:
            application/json:
              schema:
                type: object
                properties:
                  title:
                    type: string
                    example: The Lost Treasure of Atlantis
                  content:
                    type: string
                    example: "Beneath the waves, Atlantis hides its treasures, a mystery beckoning daring souls. 
                      Riches and relics lure adventurers on a perilous quest, braving the unknown depths. 
                      Their journey promises both danger and discovery."
        responses:
          200:
            description: Success creating new article data.
            content:
              application/json:
                schema:
                  allOf:
                    - $ref: '#/components/schemas/ResponseDetails'
                    - type: object
                      properties:
                        result:
                          $ref: '#/components/schemas/Article'
          400:
            description: Bad Request Error
          404:
            description: Not Found Error
          500:
            description: Internal Server Error
        """
        result = None
        try:
            data = await request.json()
            result = await self.article_service.create_article(data)
            return response(status=200, message="Successfully created article", result=result)
        except ValidationError as err:
            raise HTTPException(status_code=400, detail=err.messages)
        except Exception as e:
            self.logger.error(str(e))
            return server_error_response()

    async def articles_get(self, request):
        """
        description: Retrieve article by id.
        tags: ['Articles']
        parameters:
          - name: id
            required: true
            in: path
            description: id of article
            example: 1
            schema:
              type: string
        responses:
          200:
            description: Success retrieving article data.
            content:
              application/json:
                schema:
                  allOf:
                    - $ref: '#/components/schemas/ResponseDetails'
                    - type: object
                      properties:
                        result:
                          $ref: '#/components/schemas/Article'
          404:
            description: Not Found Error
          500:
            description: Internal Server Error
        """
        result = None
        try:
            result = await self.article_service.get_by_id(request.path_params["id"])
        except Exception as e:
            self.logger.error(str(e))
            return server_error_response()

        if result == None:
            raise HTTPException(status_code=404)

        return response(status=200, message="Successfully retrieved article", result=result)

    async def articles_summarize(self, request):
        """
        tags: ['Articles']
        description: Generates a summary of the article content and updates the summary
        parameters:
          - name: id
            required: true
            in: path
            description: id of article
            example: 1
            schema:
              type: string
        responses:
          200:
            description: Success creating new article data.
            content:
              application/json:
                schema:
                  allOf:
                    - $ref: '#/components/schemas/ResponseDetails'
                    - type: object
                      properties:
                        result:
                          $ref: '#/components/schemas/Article'
          404:
            description: Not Found Error
          500:
            description: Internal Server Error
        """
        result = None
        try:
            result = await self.article_service.summarize(request.path_params["id"])
        except Exception as e:
            self.logger.error(str(e))
            return server_error_response()

        if result == None:
            raise HTTPException(status_code=404)

        return response(status=200, message="Successfully summarized article", result=result)
