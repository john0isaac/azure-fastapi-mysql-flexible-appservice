# ruff: noqa: UP007
# ruff: noqa: UP006
import os
import typing

from sqlmodel import Field, Relationship, SQLModel, create_engine

MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)
MYSQL_SSL = os.environ.get("MYSQL_SSL")

sql_url = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
if MYSQL_SSL:
    sql_url = f"{sql_url}?ssl_mode={MYSQL_SSL}"

engine = create_engine(sql_url)


def create_db_and_tables():
    return SQLModel.metadata.create_all(engine)


class CruiseDestinationLink(SQLModel, table=True):
    destination_id: typing.Optional[int] = Field(
        default=None,
        foreign_key="destination.id",
        primary_key=True,
    )
    cruise_id: typing.Optional[int] = Field(
        default=None,
        foreign_key="cruise.id",
        primary_key=True,
    )


class Destination(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    subtitle: typing.Optional[str]
    description: typing.Optional[str]
    cruises: typing.List["Cruise"] = Relationship(
        back_populates="destinations",
        link_model=CruiseDestinationLink,
    )

    def __str__(self):
        return f"{self.name}"


class Cruise(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: typing.Optional[str]
    subtitle: typing.Optional[str]
    destinations: typing.List["Destination"] = Relationship(
        back_populates="cruises",
        link_model=CruiseDestinationLink,
    )

    def __str__(self):
        return f"{self.name}"


class InfoRequest(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str
    notes: str
    cruise_id: int = Field(default=None, foreign_key="cruise.id")
