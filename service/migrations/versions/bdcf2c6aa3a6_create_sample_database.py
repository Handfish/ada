"""create sample database

Revision ID: bdcf2c6aa3a6
Revises: 4b610242919c
Create Date: 2023-08-15 10:52:00.920707

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from back.models import Database
from data.sample.create import create_sample_database, delete_sample_database

# revision identifiers, used by Alembic.
revision: str = "bdcf2c6aa3a6"
down_revision: Union[str, None] = "4b610242919c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tables with clients,products and orders tables
    sqlite_path = create_sample_database()

    op.execute(
        sa.insert(Database).values(
            name="sample",
            description="Sample database with clients, products and orders tables",
            details={"filename": sqlite_path},
            _engine="sqlite",
            public=True,
            ownerId="admin",
            metadata=[
                {
                    "name": "clients",
                    "schema": "main",
                    "columns": [
                        {
                            "name": "id",
                            "type": "NUMERIC",
                            "Noneable": True,
                            "description": None,
                        },
                        {
                            "name": "name",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "email",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "phone",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "address",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                    ],
                    "is_view": False,
                    "description": None,
                },
                {
                    "name": "orders",
                    "schema": "main",
                    "columns": [
                        {
                            "name": "id",
                            "type": "NUMERIC",
                            "Noneable": True,
                            "description": None,
                        },
                        {
                            "name": "client_id",
                            "type": "INTEGER",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "product_id",
                            "type": "INTEGER",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "quantity",
                            "type": "INTEGER",
                            "Noneable": False,
                            "description": None,
                        },
                    ],
                    "is_view": False,
                    "description": None,
                },
                {
                    "name": "products",
                    "schema": "main",
                    "columns": [
                        {
                            "name": "id",
                            "type": "NUMERIC",
                            "Noneable": True,
                            "description": None,
                        },
                        {
                            "name": "name",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "price",
                            "type": "DECIMAL(10, 2)",
                            "Noneable": False,
                            "description": None,
                        },
                    ],
                    "is_view": False,
                    "description": None,
                },
                {
                    "name": "clients",
                    "schema": "main",
                    "columns": [
                        {
                            "name": "id",
                            "type": "NUMERIC",
                            "Noneable": True,
                            "description": None,
                        },
                        {
                            "name": "name",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "email",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "phone",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "address",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                    ],
                    "is_view": False,
                    "description": None,
                },
                {
                    "name": "orders",
                    "schema": "main",
                    "columns": [
                        {
                            "name": "id",
                            "type": "NUMERIC",
                            "Noneable": True,
                            "description": None,
                        },
                        {
                            "name": "client_id",
                            "type": "INTEGER",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "product_id",
                            "type": "INTEGER",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "quantity",
                            "type": "INTEGER",
                            "Noneable": False,
                            "description": None,
                        },
                    ],
                    "is_view": False,
                    "description": None,
                },
                {
                    "name": "products",
                    "schema": "main",
                    "columns": [
                        {
                            "name": "id",
                            "type": "NUMERIC",
                            "Noneable": True,
                            "description": None,
                        },
                        {
                            "name": "name",
                            "type": "VARCHAR(255)",
                            "Noneable": False,
                            "description": None,
                        },
                        {
                            "name": "price",
                            "type": "DECIMAL(10, 2)",
                            "Noneable": False,
                            "description": None,
                        },
                    ],
                    "is_view": False,
                    "description": None,
                },
            ],
        )
    )


def downgrade() -> None:
    # Delete file from disk
    delete_sample_database()
