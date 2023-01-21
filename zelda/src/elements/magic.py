from random import randint
from typing import Union, List

from pygame.math import Vector2
from pygame.sprite import AbstractGroup
from pygame.mixer import Sound

from zelda.src.settings import TILESIZE, BASE_PATH
from zelda.src.elements.player import Player
from zelda.src.core.particle_effect import AnimationPlayer


class MagicPlayer:
    """Classe que representa um método para execução das animações
    relacionadas ao uso de magias.

    Essa classe lida tanto com as animações, quanto com a manutenção
    da vida e energia do player ao utilizar magia.
    """

    def __init__(self, animation_player: AnimationPlayer) -> None:
        """Inicializa a classe MagicPlayer.

        Args:
            animation_player (AnimationPlayer):
                player responsável por executar as animações das partículas
        """
        self.__animation_player = animation_player

        self.__heal_sound = Sound(f"{BASE_PATH}/audio/heal.wav")
        self.__flame_sound = Sound(f"{BASE_PATH}/audio/flame.wav")

        self.__heal_sound.set_volume(0.3)
        self.__flame_sound.set_volume(0.2)

    def heal(self,
             player: Player,
             strength: int,
             cost: int,
             groups: Union[List[AbstractGroup], AbstractGroup]) -> None:
        """Gerencia as animações relacionadas a magia de cura.

        Args:
            player (Player):
                instância do player no jogo
            strength (int):
                quantidade de vida que será curada
            cost (int):
                custo de energia para utilizar a magia
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos de sprites em que as animações devem estar
        """
        if player.energy >= cost:
            player.energy -= cost
            player.health += strength

            heal_offset = Vector2(0, -60)
            self.__animation_player.create_particles(
                name="heal",
                position=player.rect.center + heal_offset,
                groups=groups,
            )

            self.__animation_player.create_particles(
                name="aura",
                position=player.rect.center,
                groups=groups,
            )

            self.__heal_sound.play()

    def flame(self,
              player: Player,
              cost: int,
              groups: Union[List[AbstractGroup], AbstractGroup]) -> None:
        """Gerencia as animações relacionadas a magia de fogo.

        Args:
            player (Player):
                instância do player no jogo
            cost (int):
                custo de energia para utilizar a magia
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos de sprites em que as animações devem estar
        """
        if player.energy >= cost:
            player.energy -= cost

            status = player.status.split("_")[0]
            axis = "y" if status in ["up", "down"] else "x"
            direction = -1 if status in ["up", "left"] else 1

            for i in range(1, 6):
                flame_offset = Vector2(
                    randint(-TILESIZE // 3, TILESIZE // 3),
                    randint(-TILESIZE // 3, TILESIZE // 3))

                setattr(
                    flame_offset,
                    axis,
                    getattr(flame_offset, axis) + direction * i * TILESIZE)

                self.__animation_player.create_particles(
                    name="flame",
                    position=player.rect.center + flame_offset,
                    groups=groups,
                )

            self.__flame_sound.play()
