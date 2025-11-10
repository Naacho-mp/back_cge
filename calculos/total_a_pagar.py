from decimal import Decimal

tarifaFija = Decimal('1033.19')
valorKwh = Decimal('160.55')
cargoAdicional = Decimal('450.00')
valorIva = Decimal('0.19')

def calcular_montos(kwh_total: Decimal):
    tarifa_base = tarifaFija + (valorKwh * kwh_total)
    cargos = cargoAdicional
    subtotal = tarifa_base + cargos
    iva = (subtotal * valorIva).quantize(Decimal('1.00'))
    total_boleta = (subtotal + iva).quantize(Decimal('1.00'))
    return {
        "tarifa_base": tarifa_base.quantize(Decimal('1.00')),
        "cargos": cargos.quantize(Decimal('1.00')),
        "iva": iva,
        "total": total_boleta
    }
