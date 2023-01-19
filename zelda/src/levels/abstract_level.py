from abc import ABCMeta, abstractmethod

from pygame import Surface


class AbstractLevel(metaclass=ABCMeta):
    """Classe abstrata que define o básico de um nível.

    Essa classe gerencia os diferentes elementos que são visíveis ou
    invisiveis na tela. Os elementos invisíveis funcionam como
    obstáculos para o player.

    A classe também lida com inputs específicos do nível, como menus e
    interações do player com o mapa.
    """

    def __init__(self, screen: Surface) -> None:
        """Setup básico para um nível do jogo.

        A superfície passada por parâmetro permite que o nível seja
        desenhado em diferentes superfícies dependendo da necessidade,
        além de habilitar features como zoom.

        Args:
            screen (Surface): superfície em que o nível será desenhado
        """
        self.display_surface = screen

    @abstractmethod
    def run(self) -> None:
        """Atualiza e desenha os elementos presentes no nível
        """
        pass
