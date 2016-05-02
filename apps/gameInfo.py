# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# Input your game's name
# <GAME NAME> : <SOURCE FILE NAME>
GAME_LIST = {
    '숫자야구': 'bullsAndCows',
    '마피아': 'mafia',
    '총잡이이론': 'gunner'
}

GAME_INFO = {
    '숫자야구': {
        'MIN_NEED_PERSON': 1,
        'ALLOW_EXIT': 1
    }
}

# Input your game's mode name (OPTIONAL)
# <GAME NAME> : {<MODE NAME> : [<VARIABLE NAME>, MIN, DEFAULT, MAX]}
MODE_LIST = {
    '숫자야구': {
        '자릿수': [
            'digit',
            1,
            4,
            9
        ],
        '16진수': [
            'hexMode',
            0,
            0,
            1
        ]
    }
}
