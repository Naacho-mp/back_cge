def validar_rut(rut: str) -> bool:
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 2:
        return False

    cuerpo, dv = rut[:-1], rut[-1]
    acum = 0
    multiplicador = 2

    for c in reversed(cuerpo):
        acum += int(c) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    digito_calculado = 11 - (acum % 11)
    if digito_calculado == 10:
        digito_calculado = "K"
    elif digito_calculado == 11:
        digito_calculado = "0"
    else:
        digito_calculado = str(digito_calculado)

    return dv == digito_calculado