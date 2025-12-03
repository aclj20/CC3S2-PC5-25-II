"""Excepciones personalizadas para la aplicación."""


class FlagException(Exception):
    """Excepción base para errores relacionados con banderas."""
    pass


class FlagNotFoundException(FlagException):
    """Excepción lanzada cuando no se encuentra una bandera."""
    
    def __init__(self, flag_name: str):
        self.flag_name = flag_name
        self.message = f"No se encontró la bandera: '{flag_name}'"
        super().__init__(self.message)


class DuplicateFlagException(FlagException):
    """Excepción lanzada al intentar crear una bandera con un nombre duplicado."""
    
    def __init__(self, flag_name: str):
        self.flag_name = flag_name
        self.message = f"Ya existe una bandera con el nombre: '{flag_name}'"
        super().__init__(self.message)


class InvalidRolloutPercentageException(FlagException):
    """Excepción lanzada cuando el porcentaje de despliegue no es válido."""
    
    def __init__(self, value: int):
        self.value = value
        self.message = f"Porcentaje de despliegue inválido: {value}. Debe estar entre 0 y 100"
        super().__init__(self.message)


class InvalidFlagNameException(FlagException):
    """Excepción lanzada cuando el formato del nombre de la bandera no es válido."""
    
    def __init__(self, name: str):
        self.name = name
        self.message = f"Nombre de bandera inválido: '{name}'. Use solo caracteres alfanuméricos, guiones y guiones bajos. No se permiten espacios."
        super().__init__(self.message)