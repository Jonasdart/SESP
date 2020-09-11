class ComputerNameOutOfDefaults(Exception):
    def __init__(self):
        self.message = 'O nome do computador está fora dos padrões, no GLPI. Comunique a T.I.'
    def __str__(self):
        return self.message
