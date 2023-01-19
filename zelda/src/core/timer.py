from typing import Callable

from pygame.time import get_ticks


class Timer:
    """Classe de suporte para representar um timer do jogo.

    A classe Timer funciona como um contador que controla o tempo entre
    a ativação e desativação. Ela serve, por exemplo, para controlar os
    cooldowns de ataque e de magia do player.
    """

    def __init__(self, duration: float, func: Callable = None) -> None:
        """Inicializa a classe timer.

        A inicialização é feita zerando o tempo inicial e colocando o
        timer como inativo inicialmente.

        Args:
            duration (float):
                tempo de duração do timer em milissegundos
            func (Callable, optional):
                função que será chamada automaticamente após o timer ser
                concluído. None por padrão.
        """
        self.duration = duration
        self.__extended_duration = duration
        self.func = func

        self.start_time = 0
        self.active = False

    def activate(self) -> None:
        """Ativa o timer.
        """
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self) -> None:
        """Desativa o timer
        """
        self.active = False
        self.start_time = 0
        self.__extended_duration = self.duration

    def extend_duration(self, extend_time: int) -> None:
        """Aumenta a duração do timer já definido

        Args:
            extend_time (int):
                tempo para extender a duração do timer
        """
        self.__extended_duration = self.duration + extend_time

    def update(self) -> None:
        """Atualiza o timer.

        O método de atualizar o timer sempre verifica se o tempo
        determinado já foi concluído desde a ativação, e desativa o
        timer automaticamente após a conclusão. Além disso, ao finalizar
        chama a função, caso ela tenha sido passada na inicialização.
        """
        current_time = get_ticks()

        if (current_time - self.start_time) >= self.__extended_duration:
            if self.func and self.start_time != 0:
                self.func()

            self.deactivate()
