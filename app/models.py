from datetime import datetime
import uuid
from enum import Enum as PyEnum
from sqlalchemy import Integer, String, DateTime, CHAR, func, ForeignKey, UniqueConstraint, \
    CheckConstraint, Text, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

#SE ESTABLECEN LOS MODELOS NECESARIOS PARA LA CREACION DE TABLAS POSTERIORMENTE

class Cliente(Base):
    __tablename__ = 'cliente'
    id_cliente: Mapped[str] = mapped_column(CHAR(36),primary_key=True, default=lambda: str(uuid.uuid4()))
    rut: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    nombre_razon: Mapped[str] = mapped_column(String(100), nullable=False)
    email_contacto: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    direccion_facturacion: Mapped[str] = mapped_column(String(200), nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    medidores: Mapped[list["Medidor"]] = relationship("Medidor", back_populates="cliente", cascade="all, delete-orphan")
    boletas: Mapped[list["Boleta"]] = relationship("Boleta", back_populates="cliente",cascade="all, delete-orphan"
    )



class Medidor(Base):
    __tablename__ = 'medidor'
    id_medidor: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_medidor: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False)
    id_cliente: Mapped[str] = mapped_column(ForeignKey("cliente.id_cliente", ondelete="CASCADE"))
    direccion_suministro: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="medidores")
    lecturas: Mapped[list["LecturaConsumo"]] = relationship("LecturaConsumo",back_populates="medidor", cascade="all, delete-orphan"
    )


class LecturaConsumo(Base):
    __tablename__ = 'lectura_consumo'
    id_lectura: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_medidor: Mapped[int] = mapped_column(ForeignKey("medidor.id_medidor"))
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    lectura_kwh: Mapped[int] = mapped_column(Integer, nullable=False)
    observacion: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("id_medidor", "anio", "mes", name="lectura_unica_anio_mes"),
        CheckConstraint("lectura_kwh >= 0", name="verifica_lectura_no_negativa")
    )
    medidor: Mapped["Medidor"] = relationship("Medidor", back_populates="lecturas")


class Boleta(Base):
    __tablename__ = 'boleta'
    id_boleta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[str] = mapped_column(ForeignKey("cliente.id_cliente"))
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    kwh_total: Mapped[float] = mapped_column(Float, nullable=False)
    tarifa_base: Mapped[float] = mapped_column(Float, nullable=False)
    cargos: Mapped[float] = mapped_column(Float, nullable=False)
    iva: Mapped[float] = mapped_column(Float, nullable=False)
    total_pagar: Mapped[float] = mapped_column(Float, nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("id_cliente", "anio", "mes", name="boleta_unica_cliente_anio_mes"),
    )

    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="boletas")