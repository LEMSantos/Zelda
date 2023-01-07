from abc import ABCMeta, abstractmethod

from pygame import Surface


class AbstractLevel(metaclass=ABCMeta):
    """Classe abstrata que define o básico de um nível.

    Args:
        metaclass (ABCMeta, optional): define a classe como abstrata
    """

    def __init__(self, screen: Surface) -> None:
        """Setup básico para um nível do jogo.

        A superfície passada por parâmetro permite que o nível seja
        desenhado em diferentes superfícies dependendo da necessidade,
        além de habilitar features como zoom.

        Args:
            screen (Surface): superfíce em que o nível será desenhado
        """
        self.display_surface = screen

    @abstractmethod
    def run(self) -> None:
        """Atualiza e desenha os elementos presentes no nível
        """
        pass
