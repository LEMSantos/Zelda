Zelda
=====

Implementação de uma versão simplificada do jogo [Zelda](https://www.nintendo.pt/Jogos/Portal-Nintendo/Portal-The-Legend-of-Zelda/Portal-The-Legend-of-Zelda-627606.html) utilizando a biblioteca [Pygame](http://www.pygame.org). O jogo abarca alguns do elementos principais como:

- Uso de ferramentas
- Interação do player com elementos do jogo como árvores e plantas
- Compra e venda de itens
- Passagem de tempo e mudanças no clima
- Inventório
- Mecânica de cultivo

dentre outos elementos interessantes.

A versão codificada no vídeo de passo a passo foi modificada visando uma melhor organização de pastas, mudanças na implementação para facilitar a manutenção futura, além de documentação das classes e funções.

Setup (testado no linux Ubuntu 20.04)
-------------------------------------

1. Instale o Python 3.x (recomendada a versão 3.8)
2. Instale o [Pipenv](https://pipenv.pypa.io/en/latest/)
3. Clone o repositório:

    ```bash
    $ git clone https://github.com/LEMSantos/Zelda.git
    ```
    ou faça o download do zip e extraia.

4. No diretório principal rode:

    ```bash
    $ pipenv install
    $ pipenv run python -m zelda
    ```

5. Aproveite o jogo.


Material
--------

Assets e passo a passo - [Creating a Zelda style game in Python [with some Dark Souls elements]](https://youtu.be/QU1pPzEGrqw)

Demonstração
------------

[pygame]: http://www.pygame.org
[pipenv]: https://pipenv.readthedocs.io/en/latest/
