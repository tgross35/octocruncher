from os import getenv
import pdb
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.dsl import DSLQuery, DSLSchema, dsl_gql

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url="https://octopart.com/api/v4/endpoint", headers={'token': ''})

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Using `async with` on the client will start a connection on the transport
# and provide a `session` variable to execute queries on this connection.
# Because we requested to fetch the schema from the transport,
# GQL will fetch the schema just after the establishment of the first session
async with client as session:

    ds = DSLSchema(client.schema)

    ds.Query.search

    q1 = ds.Query.search(q='GRM155R71C104KA88D')
    q1.select(ds.part.mpn)
    q1.select(ds.part.manufacturer)

    print(dsl_gql(DSLQuery(q1)))

# Provide a GraphQL query
# query = gql(
#     """
# query {
#   # The playground will complain about missing required search arguments,
#   # however, these are given default values in the schema.
#   # Look at the "DOCS" tab on the right side of the screen for more details.
#   search(q: "GRM155R71C104KA88D", limit: 3) {
#     results {
#       part {
#         mpn
#         manufacturer {
#           name
#         }
#         # Brokers are non-authorized dealers. See: https://octopart.com/authorized
#         # sellers(include_brokers: false) {
#         #   company {
#         #     name
#         #   }
#         #   # offers {
#         #   #   click_url
#         #   #   inventory_level
#         #   #   prices {
#         #   #     price
#         #   #     currency
#         #   #     quantity
#         #   #   }
#         #   # }
#         # }
#       }
#     }
#   }
# }
# """
# )

# # Execute the query on the transport
# result = client.execute(query)
# print(client.schema)
# print(result)

# print(client.schema._implementations_map)
# print(client.schema.type_map)
