import recording
import models
import random
import re

from models import Terrain, HexNumber, Port


def get_players():
    players = list()
    players.append(models.Player(seat=0, name='yurick', color='green'))
    players.append(models.Player(seat=1, name='ross', color='red'))
    players.append(models.Player(seat=2, name='josh', color='blue'))
    players.append(models.Player(seat=3, name='zach', color='orange'))
    return players

def get_record_with_random_board():
    record = recording.GameRecord()

    players = get_players()
    terrain = ([Terrain.wood]*4 + [Terrain.wheat]*4 + [Terrain.sheep]*4 +
               [Terrain.ore]*3 + [Terrain.brick]*3)
    numbers = ([HexNumber.two] +
               [HexNumber.three]*2 + [HexNumber.four]*2 +
               [HexNumber.five]*2 + [HexNumber.six]*2 + [HexNumber.eight]*2 +
               [HexNumber.nine]*2 + [HexNumber.ten]*2 + [HexNumber.eleven]*2 +
               [HexNumber.twelve])
    ports = [Port.any, Port.ore, Port.any, Port.sheep, Port.any, Port.wood, Port.brick, Port.any, Port.wheat]

    random.shuffle(terrain)
    random.shuffle(numbers)
    random.shuffle(ports)

    desert = random.randint(0, models.NUM_TILES-1)
    terrain.insert(desert, Terrain.desert)
    numbers.insert(desert, HexNumber.none)

    record.record_pregame(players, terrain, numbers, ports)
    return record


def test_record_pregame():
    record = get_record_with_random_board()
    print(record.dump())
    lines = record.dump().split('\n')
    i = 0

    if not re.match('\w+ v[\d\.]+', lines[i]):
        print('Line {0} must contain the version number.\n{1}'.format(i, lines[i]))
        return False
    i += 1

    if not re.match('timestamp: ', lines[i]):
        print('Line {0} must contain the timestamp.\n{1}'.format(i, lines[i]))
        return False
    i += 1

    if not re.match('players: \d', lines[i]):
        print('Line {0} must contain the number of players.\n{1}'.format(i, lines[i]))
        return False
    num_players = int(lines[i][len('players: '):])
    i += 1

    for _ in range(num_players):
        if not re.match('name: \w+, color: \w+, seat: \d', lines[i]):
            print ('Player line must contain name, color, and seat.\n{0}'.format(
                lines[i]
            ))
            return False
        i += 1

    if not re.match('terrain: ((wood|brick|wheat|sheep|ore|desert) ?){19}', lines[i]):
        print('Terrain line must contain 19 space-separated identifiers (wood|brick|wheat|sheep|ore|desert).\n{0}'.format(
            lines[i]
        ))
        return False
    i += 1

    if not re.match('numbers: ((None|2|3|4|5|6|8|9|10|11|12) ?){19}', lines[i]):
        print('Numbers line must contain 19 space-separated integers on [2,6]U[8,12].\n{0}'.format(
            lines[i]
        ))
        return False
    i += 1

    if not re.match('ports: ((\w+2:1|3:1) ?){9}', lines[i]):
        print('Ports line must contain 9 space-separated port identifiers.\n{0}'.format(
            lines[i]
        ))
        return False
    i += 1

    if not re.match('...CATAN!', lines[i]):
        print('Second-last line must be "...CATAN!".\n{0}'.format(lines[i]))
        return False
    i += 1

    if not re.match('', lines[i]):
        print('Last line must be terminating newline.\n')
        return False
    i += 1

    if len(lines) > i:
        print('Must not contain trailing lines afer "...CATAN!\\n". Found {0} lines, should have been {1}.\n{2}'.format(
            len(lines),
            i,
            lines[i]
        ))
        return False

    return True


def test_turn():
    player = models.Player(0, 'ross', 'red')
    record = recording.GameRecord()

    record.record_player_roll(player, 2)
    record.record_player_ends_turn(player)

    lines = record.dump().split('\n')
    assert lines[0] == 'red rolls 2'
    assert lines[0] == 'red ends turn'

    print(record.dump())
