# importing graphene and defining our GraphQL data
import graphene
from fastapi import FastAPI
# importing Starlette's `GraphQLApp`
from starlette.graphql import GraphQLApp


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


app = FastAPI()
# adding Starlette's `GraphQLApp`
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))
