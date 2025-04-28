from database.database import Base
from sqlalchemy import (
    Column,
    Integer,
    Float,
    Enum,
    UniqueConstraint,
    String,
    ForeignKey,
    Date,
)
from sqlalchemy.sql import func
import enum


class HistoryDataType(enum.Enum):
    TRADINGVIEW = 0
    BLOOMBERG = 1


class HistoryData(Base):
    __tablename__ = "HistoryData"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(Enum(HistoryDataType), nullable=False)
    timestamp = Column(Date, nullable=False)
    close = Column(Float, nullable=False)
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    symbolId = Column(Integer, ForeignKey("Symbol.id"), nullable=False)

    __table_args__ = (UniqueConstraint("type", "timestamp", "symbolId"),)


class ForecastData(Base):
    __tablename__ = "ForecastData"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    type = Column(Enum(HistoryDataType), nullable=False)
    timestamp = Column(Date, nullable=False)
    symbolSubModelId = Column(Integer, ForeignKey("SymbolSubModel.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("date", "type", "timestamp", "symbolSubModelId"),
    )


class Symbol(Base):
    __tablename__ = "Symbol"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)


class Model(Base):
    __tablename__ = "Model"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)


class SubModel(Base):
    __tablename__ = "SubModel"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    modelId = Column(Integer, ForeignKey("Model.id"), nullable=False)

    __table_args__ = (UniqueConstraint("name", "modelId"),)


class SymbolSubModel(Base):
    __tablename__ = "SymbolSubModel"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    symbolId = Column(Integer, ForeignKey("Symbol.id"), nullable=False)
    subModelId = Column(Integer, ForeignKey("SubModel.id"), nullable=False)

    __table_args__ = (UniqueConstraint("symbolId", "subModelId"),)
