"""init

Revision ID: f5da7bf41365
Revises: 
Create Date: 2023-08-13 13:23:37.050415

"""
from typing import Sequence, Union

import pgvector
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f5da7bf41365"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    ## Add vector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organisation",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("pictureUrl", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "database",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("engine", sa.String(), nullable=False),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("organisationId", sa.String(), nullable=True),
        sa.Column("ownerId", sa.String(), nullable=True),
        sa.Column("public", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisationId"],
            ["organisation.id"],
        ),
        sa.ForeignKeyConstraint(
            ["ownerId"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_organisation",
        sa.Column("userId", sa.String(), nullable=False),
        sa.Column("organisationId", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisationId"],
            ["organisation.id"],
        ),
        sa.ForeignKeyConstraint(
            ["userId"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("userId", "organisationId"),
    )
    op.create_table(
        "conversation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("ownerId", sa.String(), nullable=True),
        sa.Column("databaseId", sa.Integer(), nullable=False),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ["databaseId"],
            ["database.id"],
        ),
        sa.ForeignKeyConstraint(
            ["ownerId"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "query",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("query", sa.String(), nullable=False),
        sa.Column("databaseId", sa.Integer(), nullable=False),
        sa.Column("validatedSQL", sa.String(), nullable=True),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("creatorId", sa.String(), nullable=True),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False),
        sa.Column("tag", sa.String(), nullable=True),
        sa.Column("tables", sa.String(), nullable=True),
        sa.Column("wheres", sa.String(), nullable=True),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.Column(
            "visualisationParams",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["creatorId"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["databaseId"],
            ["database.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "table",
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("databaseId", sa.Integer(), nullable=False),
        sa.Column("schemaName", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.ForeignKeyConstraint(
            ["databaseId"],
            ["database.id"],
        ),
        sa.PrimaryKeyConstraint("databaseId", "schemaName", "name"),
    )
    op.create_table(
        "conversation_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversationId", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("display", sa.Boolean(), nullable=False),
        sa.Column("done", sa.Boolean(), nullable=False),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False),
        sa.Column(
            "functionCall", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("queryId", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversationId"],
            ["conversation.id"],
        ),
        sa.ForeignKeyConstraint(
            ["queryId"],
            ["query.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "prediction",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("queryId", sa.Integer(), nullable=True),
        sa.Column("modelName", sa.String(), nullable=False),
        sa.Column("prompt", sa.String(), nullable=True),
        sa.Column("output", sa.String(), nullable=True),
        sa.Column("params", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("response", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("params_hash", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["queryId"],
            ["query.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "table_column",
        sa.Column("columnName", sa.String(), nullable=False),
        sa.Column("dataType", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("tableDatabaseId", sa.Integer(), nullable=False),
        sa.Column("tableSchemaName", sa.String(), nullable=False),
        sa.Column("tableName", sa.String(), nullable=False),
        sa.Column("isIdentity", sa.Boolean(), nullable=False),
        sa.Column("foreignTableSchema", sa.String(), nullable=True),
        sa.Column("foreignTable", sa.String(), nullable=True),
        sa.Column("foreignColumn", sa.String(), nullable=True),
        sa.Column("examples", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.ForeignKeyConstraint(
            ["tableDatabaseId", "tableSchemaName", "tableName"],
            ["table.databaseId", "table.schemaName", "table.name"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "columnName", "tableDatabaseId", "tableSchemaName", "tableName"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("table_column")
    op.drop_table("prediction")
    op.drop_table("conversation_message")
    op.drop_table("table")
    op.drop_table("query")
    op.drop_table("conversation")
    op.drop_table("user_organisation")
    op.drop_table("database")
    op.drop_table("user")
    op.drop_table("organisation")
    # ### end Alembic commands ###
