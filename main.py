"""log a game of Settlers of Catan.

TODO: Allow ports to be selected during pregame
TODO: Control size adjustment with resizing of window
TODO: Simplify the algorithm for red placement now there is a connected path through
      the graph that visits every node.
TODO: Docstrings and unittests.
"""

import tkinter
import pprint
import logging
import argparse

import views
import models


class CatanSpectator(tkinter.Frame):

    def __init__(self, options=None, *args, **kwargs):
        super(CatanSpectator, self).__init__()
        self.options = options or dict()
        board = models.Board(terrain=self.options.get('terrain'),
                             numbers=self.options.get('numbers'),
                             ports=self.options.get('ports'),
                             pieces=self.options.get('pieces'))
        self.game = models.Game(board=board, pregame=self.options.get('pregame'))
        self.game.observers.add(self)
        self._in_game = self.game.state.is_in_game()

        self._board_frame = views.BoardFrame(self, self.game)
        self._log_frame = views.LogFrame(self, self.game)
        self._board_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        self._log_frame.grid(row=1, column=0, sticky=tkinter.W)

        self._board_frame.redraw()

        self._setup_game_toolbar_frame = views.SetupGameToolbarFrame(self, self.game)
        self._toolbar_frame = self._setup_game_toolbar_frame
        self._toolbar_frame.grid(row=0, column=1, rowspan=2, sticky=tkinter.N)

        self.lift()

    def notify(self, observable):
        was_in_game = self._in_game
        self._in_game = self.game.state.is_in_game()
        if was_in_game and not self.game.state.is_in_game():
            logging.debug('we were in game, NO WE\'RE NOT')
            self._toolbar_frame.grid_forget()
            #self._toolbar_frame = self._setup_game_toolbar_frame
            self._toolbar_frame.grid(row=0, column=1, rowspan=2, sticky=tkinter.N)
        elif not was_in_game and self.game.state.is_in_game():
            logging.debug('we were not in game, NOW WE ARE')
            self._toolbar_frame.grid_forget()
            self._toolbar_frame = views.GameToolbarFrame(self, self.game)
            self._toolbar_frame.grid(row=0, column=1, rowspan=2, sticky=tkinter.N)

    def setup_options(self):
        return self._setup_game_toolbar_frame.options.copy()

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(module)s:%(funcName)s:%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='log a game of catan')
    parser.add_argument('--terrain', help='random|preset|empty|debug, default empty')
    parser.add_argument('--numbers', help='random|preset|empty|debug, default empty')
    parser.add_argument('--ports', help='random|preset|empty|debug, default preset')
    parser.add_argument('--pieces', help='random|preset|empty|debug, default empty')
    parser.add_argument('--pregame', help='on|off, default on')

    args = parser.parse_args()
    options = {
        'terrain': args.terrain,
        'numbers': args.numbers,
        'ports': args.ports,
        'pieces': args.pieces,
        'pregame': args.pregame,
    }
    logging.info('args=\n{}'.format(pprint.pformat(options)))
    app = CatanSpectator(options=options)
    app.mainloop()


if __name__ == "__main__":
    main()
