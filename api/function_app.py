import json
import os

import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
from azure.data.tables import TableClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

PARTITION = "counter"
ROW = "visits"


def increment(table):
    """Read the visit count, add one, save it, and return the new value."""
    try:
        entity = table.get_entity(PARTITION, ROW)
    except ResourceNotFoundError:
        entity = {"PartitionKey": PARTITION, "RowKey": ROW, "count": 0}
    entity["count"] = int(entity.get("count", 0)) + 1
    table.upsert_entity(entity)
    return entity["count"]


@app.route(route="counter", methods=["GET"])
def counter(req: func.HttpRequest) -> func.HttpResponse:
    table = TableClient.from_connection_string(
        os.environ["TABLE_CONNECTION"], table_name="visitorcounter"
    )
    count = increment(table)
    return func.HttpResponse(
        json.dumps({"count": count}), mimetype="application/json"
    )
