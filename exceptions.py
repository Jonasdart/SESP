class ComputerNameOutOfDefaults(Exception):
    def __init__(self):
        self.message = 'O nome do computador está fora dos padrões. Comunique à T.I.'
    def __str__(self):
        return self.message

class VersionError(Exception):
    def __init__(self):
        self.message = 'A versão do software está desatualizada'
    def __str__(self):
        return self.message

class InstalationError(Exception):
    def __init__(self):
        self.message = 'O executável não foi instalado'
    def __str__(self):
        return self.message
