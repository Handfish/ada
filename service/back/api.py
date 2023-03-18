from back.models import Database, Table, TableColumn, User
from back.session import session
from flask import Blueprint, g, jsonify, request
from middleware import database_middleware, user_middleware
from sqlalchemy import or_

api = Blueprint("back_api", __name__)


@api.route("/databases", methods=["GET"])
@user_middleware
def get_databases():
    user = getattr(g, "user", None)
    organisationId = g.organisationId
    # Filter databases based on ownerId (userId) OR organisationId
    databases = (
        session.query(Database)
        .filter(
            or_(Database.ownerId == user.id, Database.organisationId == organisationId)
        )
        .all()
    )
    return jsonify(databases)


@api.route("/tables", methods=["GET"])
def get_tables():
    tables = [{"schema": t._schema, "table": t._table} for t in g.datalake.tables]
    return jsonify(tables)


@api.route("/databases/<int:database_id>/schema", methods=["GET"])
def get_schema(database_id):
    # Get the user ID from request headers or other means (e.g. JWT)
    user_id = request.headers.get("user_id")

    # Filter databases based on user ID and specific database ID
    database = session.query(Database).filter_by(id=database_id).first()

    if not database:
        return jsonify({"error": "Database not found"}), 404

    # Query the Table and TableColumn models to get the schema data
    tables = session.query(Table).filter_by(databaseId=database_id).all()
    columns = session.query(TableColumn).filter_by(tableDatabaseId=database_id).all()

    # Convert the result into the desired JSON format
    result = []
    for table in tables:
        schema_data = {
            "schemaName": table.schemaName,
            "name": table.name,
            "columns": [],
        }

        for column in columns:
            if (
                column.tableName == table.name
                and column.tableSchemaName == table.schemaName
            ):
                schema_data["columns"].append(
                    {
                        "name": column.columnName,
                        "dataType": column.dataType,
                        "isIdentity": column.isIdentity,
                        "examples": column.examples,
                    }
                )

        result.append(schema_data)

    return jsonify(result)
