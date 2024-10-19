
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from typing import List, AsyncGenerator
from string import ascii_lowercase
from itertools import count
import random
import asyncio

app = FastAPI()


# Message type
@strawberry.type
class Message:
    node_id: int
    message: str


@strawberry.type
class Query:
    @strawberry.field
    def messages(self, node_ids: List[int]) -> List[Message]:
        mock_messages = [ Message(node_id=_id, message=ascii_lowercase[random.randint(0, 25)]) for _id in range(26)]
        return [
            message
            for message in mock_messages
            if message.node_id in node_ids
        ]


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def produce_message(self) -> AsyncGenerator[Message, None]:
        # Subscription that keeps sending a Message
        for _ in count():
            asyncio.sleep(5)
            yield Message(node_id=random.randint(0, 26), message=ascii_lowercase[random.randint(0, 25)])

schema = strawberry.Schema(query=Query, subscription=Subscription)

# Create the FastAPI app
app = FastAPI()

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Mount the GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")