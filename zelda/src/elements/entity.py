from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Tuple, Union, Sequence
from math import sin

from pygame import Rect, Surface
from pygame.time import get_ticks as get_time_ticks
from pygame.sprite import AbstractGroup, Sprite
from pygame.math import Vector2

from zelda.src.core.timer import Timer


class Entity(ABC, Sprite):
    """Classe que representa uma entidade no jogo.

    Entidades podem ser tanto players quando inimigos. Essa classe abarca
    funcionalidades comuns de ambos.
    """

    hitbox: Rect
    status: str
    speed: int
    animation_speed: float
    _animations: Dict[str, Sequence[Surface]]

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup],
                 handle_collisions: Callable[["Entity", str], None],) -> None:
        """Inicializa a entidade com a posição, os grupos e a colisão

        Args:
            position (Tuple[float, float]):
                posição da entidade na tela, em pixels
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos que a entidade deve pertencer quando for
                utilizada no jogo
            handle_collisions (Callable[[str], None]):
                função para lidar com as colisões horizontais e
                verticais
        """
        super().__init__(groups)

        # Setup
        self._import_assets()
        self._handle_collisions = handle_collisions

        # Movimento
        self.direction = Vector2()

        # Cooldowns
        self._cooldowns = {
            "invincibility": Timer(300),
            **self._create_cooldowns()
        }

        # Ações
        self._get_status()
        self._frame_index = 0

        # Gráfico
        self.image = self._animations[self.status][self._frame_index]
        self.rect = self.image.get_rect(topleft=position)

    @abstractmethod
    def _import_assets(self) -> None:
        pass

    @abstractmethod
    def _get_status(self) -> None:
        pass

    @abstractmethod
    def _create_cooldowns(self) -> Dict[str, Timer]:
        pass

    def _update_cooldowns(self):
        """Atualiza todos os timers utilizados.
        """
        for cooldown in self._cooldowns.values():
            cooldown.update()

    def _move(self, speed: int) -> None:
        """Método para movimentar a entidade na tela.
        """
        _direction = self.direction

        # Garante que a velocidade é constante em qualquer direção
        if self.direction.magnitude() > 0:
            _direction = self.direction.normalize()

        # Movimenta horizontalmente
        self.hitbox.centerx += round(_direction.x * speed)
        self.rect.centerx = self.hitbox.centerx
        self._handle_collisions(self, "horizontal")

        # Movimenta verticalmente
        self.hitbox.centery += round(_direction.y * speed)
        self.rect.centery = self.hitbox.centery
        self._handle_collisions(self, "vertical")

    @staticmethod
    def _weave_value() -> int:
        """Método estático para gerar a oscilação utilizada no flicker.
        """
        value = sin(get_time_ticks())
        return 255 if value >= 0 else 0

    def _animate(self, animation_speed: float) -> None:
        """Executa a animação da entidade de acordo com o status atual.
        """
        self._frame_index += animation_speed
        self._frame_index %= len(self._animations[self.status])

        self.image = self._animations[self.status][int(self._frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        self._flicker()

    def _flicker(self) -> None:
        """Gera o efeito de piscar o sprite enquanto a invencibilidade
        está ativada.
        """
        if self._cooldowns["invincibility"].active:
            alpha = self._weave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self) -> None:
        self._get_status()
        self._update_cooldowns()
        self._move(self.speed)
        self._animate(self.animation_speed)
