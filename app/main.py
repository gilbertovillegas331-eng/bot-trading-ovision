"""Punto de entrada de OVISION Alpha 0.1.0."""

from core.core import OviCore


def main() -> int:
    """Inicia OVISION y devuelve un código de salida."""
    print("=" * 44)
    print("          OVISION Alpha 0.1.0")
    print("=" * 44)

    core = OviCore()
    return 0 if core.start() else 1


if __name__ == "__main__":
    raise SystemExit(main())
