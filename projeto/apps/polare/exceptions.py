class CredencialPGDInvalida(Exception):
    """Ocorre quando a api PGD não retorna o token bearer de authorização."""


class EntidadeNaoProcessada(Exception):
    """Ocorre quando o formato json dos dados enviados é inválido."""
