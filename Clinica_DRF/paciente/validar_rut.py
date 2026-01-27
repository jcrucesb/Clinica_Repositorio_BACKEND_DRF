def validar_rut(rut):
    # Limpiar el RUT (quitar puntos, guión y convertir a mayúscula)
    rut = rut.strip().replace(".", "").replace("-", "").upper()
    
    # Debemos realizar un conteo de los carácteres en el rut ingresado.
    # Validar longitud mínima y máxima
    if len(rut) < 8 or len(rut) > 9:
        return False 
    
    # Separar números y dígito verificador
    rut_sin_dv = rut[:-1]
    dv_ingresado = rut[-1]
    
    # Validar que solo sean números y K
    if not rut_sin_dv.isdigit() or (dv_ingresado not in "0123456789K"):
        return False
    
    # Calcular dígito verificador esperado
    suma = 0
    multiplicador = 2
    
    for d in reversed(rut_sin_dv):
        suma += int(d) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    
    resto = suma % 11
    dv_esperado = 11 - resto if resto != 0 else 0
    
    # Manejar caso especial para K (10)
    if dv_esperado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_esperado)
    
    return dv_ingresado == dv_esperado