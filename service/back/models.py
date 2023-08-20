import json
from dataclasses import dataclass, field
from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, session

Base = declarative_base()


def format_to_camel_case(**kwargs):
    # change lower_case keys to camelCase keys
    def camel_case(snake_str):
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    kwargs = {camel_case(k): v for k, v in kwargs.items()}
    return kwargs


def format_to_snake_case(**kwargs):
    # change camelCase keys to lower_case keys
    def snake_case(name):
        name = name[0].lower() + name[1:]
        return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip(
            "_"
        )

    kwargs = {snake_case(k): v for k, v in kwargs.items()}
    return kwargs


@dataclass
class Database(Base):
    id: int
    name: str
    description: str
    engine: str
    details: dict
    organisationId: str
    ownerId: str
    public: bool

    __tablename__ = "database"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    _engine = Column(String, nullable=False, name="engine")
    details = Column(JSONB, nullable=False)
    organisationId = Column(String, ForeignKey("organisation.id"))
    ownerId = Column(String, ForeignKey("user.id"))
    public = Column(Boolean, nullable=False, default=False)

    organisation = relationship("Organisation")
    owner = relationship("User")

    # Hotfix for engine, "postgres" should be "postgresql"
    @property
    def engine(self):
        return self._engine.replace("postgres", "postgresql")


class Organisation(Base):
    __tablename__ = "organisation"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


@dataclass
class ConversationMessage(Base):
    __tablename__ = "conversation_message"

    id: int
    conversationId: int
    role: str
    content: str
    data: dict
    display: bool
    done: bool
    functionCall: dict
    queryId: int

    id = Column(Integer, primary_key=True)
    conversationId = Column(Integer, ForeignKey("conversation.id"), nullable=False)
    role = Column(String, nullable=False)
    name = Column(String)
    content = Column(String, nullable=True)
    functionCall = Column(JSONB)
    data = Column(JSONB)
    display = Column(Boolean, nullable=False, default=True)
    done = Column(Boolean, nullable=False, default=False)
    createdAt = Column(TIMESTAMP, nullable=False, default=text("now()"))
    updatedAt = Column(TIMESTAMP, nullable=False, default=text("now()"))
    queryId = Column(Integer, ForeignKey("query.id"), nullable=True)

    conversation = relationship("Conversation", back_populates="messages")

    # format params before creating the object
    def __init__(self, **kwargs):
        kwargs = format_to_camel_case(**kwargs)
        super().__init__(**kwargs)

    def to_dict(self):
        # Export to dict, only keys declared in the dataclass
        return {
            "id": self.id,
            "conversationId": self.conversationId,
            "role": self.role,
            "name": self.name,
            "content": self.content,
            "functionCall": self.functionCall,
            "data": self.data,
            "display": self.display,
            "done": self.done,
            # "createdAt": self.createdAt,
            # "updatedAt": self.updatedAt,
            "queryId": self.queryId,
        }

    @classmethod
    def from_openai_dict(cls, **kwargs):
        if kwargs.get("function_call"):
            arguments_dumps = kwargs["function_call"].get("arguments")
            if arguments_dumps:
                kwargs["function_call"]["arguments"] = json.loads(arguments_dumps)
        return ConversationMessage(**kwargs)

    def to_openai_dict(self) -> dict:
        res = {
            "role": self.role,
            "content": self.content,
        }
        if self.name:
            res["name"] = self.name
        if self.functionCall:
            res["function_call"] = {
                "name": self.functionCall["name"],
                # if functionCall["arguments"] is a dict, we dump it to a string
                # because the OpenAI API doesn't accept nested dicts
                "arguments": json.dumps(self.functionCall["arguments"])
                if isinstance(self.functionCall["arguments"], dict)
                else self.functionCall["arguments"],
            }

        return res


@dataclass
class Conversation(Base):
    __tablename__ = "conversation"

    id: int
    name: str
    ownerId: str
    databaseId: int
    createdAt: str
    updatedAt: str
    # messages: List[ConversationMessage] = field(default_factory=list)

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ownerId = Column(String, ForeignKey("user.id"))
    databaseId = Column(Integer, ForeignKey("database.id"), nullable=False)
    createdAt = Column(TIMESTAMP, nullable=False, default=text("now()"))
    updatedAt = Column(TIMESTAMP, nullable=False, default=text("now()"))

    owner = relationship("User")
    database = relationship("Database")
    messages = relationship(
        "ConversationMessage", back_populates="conversation", lazy="joined"
    )


class Query(Base):
    __tablename__ = "query"

    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False)
    databaseId = Column(Integer, ForeignKey("database.id"), nullable=False)
    validatedSQL = Column(String)
    result = Column(JSONB)
    comment = Column(String)
    creatorId = Column(String, ForeignKey("user.id"))
    createdAt = Column(TIMESTAMP, nullable=False, default=text("now()"))
    updatedAt = Column(TIMESTAMP, nullable=False, default=text("now()"))
    tag = Column(String)
    tables = Column(String)
    wheres = Column(String)
    embedding = Column(Vector(1536))

    database = relationship("Database")
    creator = relationship("User")

    visualisationParams = Column(JSONB)


class User(Base):
    __tablename__ = "user"

    email = Column(String, nullable=False, unique=True)
    id = Column(String, primary_key=True)
    pictureUrl = Column(String)
    # organisationId = Column(String, ForeignKey("organisation.id"))
    # organisation = relationship("Organisation")


class UserOrganisation(Base):
    __tablename__ = "user_organisation"

    userId = Column(String, ForeignKey("user.id"), primary_key=True)
    organisationId = Column(String, ForeignKey("organisation.id"), primary_key=True)

    organisation = relationship("Organisation")
    user = relationship("User")


if __name__ == "__main__":
    from session import DATABASE_URL
    from sqlalchemy import create_engine

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
