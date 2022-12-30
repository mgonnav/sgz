from django.core.validators import RegexValidator

alphabetic_validator = RegexValidator(
    r"^[a-zA-Z ]*$", "Solo se permiten letras y espacios."
)

ruc_validator = RegexValidator(
    r"^(10|20|15|16|17)[0-9]{9}$",
    "RUC inválido. Debe estar conformado por números y empezar por 10, 20, 15, 16 o 17.",
)

numeric_validator = RegexValidator(r"^[0-9]*$", "Solo se permiten números.")

hex_code_validator = RegexValidator(
    r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    "Código de color inválido. Por favor use un código hexadecimal en formato de 6 dígitos.",
)
