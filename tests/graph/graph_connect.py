from caladrius.graph.client.gremlin.client import GremlinClient

CONFIG = {"gremlin.server.url" : "localhost:8182"}

gremlin_client = GremlinClient(CONFIG)

print("Graph client available as: gremlin_client")
