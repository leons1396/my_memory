import sys
import tkinter as tk

sys.path.append("C:/Users/Leon/Documents/programming/MY-MEMORY")
from src.view import game_window


class Controller:
    def __init__(self, model, main_window):
        print("new controller")
        self.model = model
        self.main_window = main_window
        self.game_start = True

    def start(self):
        self.main_window.create_start_window()

    def create_game_window(self):
        # make sure only one game window is open
        if not self.model.game_window_is_open:
            # check the entered values
            if not self.main_window.check_inputs():
                print("There are some invalid inputs")
                return

            print("Create game window")
            # hide the start/root window
            self.main_window.withdraw()
            # self = controller itself
            self.game_window = game_window.GameWindow(self, self.main_window)
            self.model.set_player_names(self.main_window.get_player_names_from_user())
            print("++++ game setting model", self.model.get_game_setting())
            self.game_window.create_game_window(**self.model.get_game_setting())
            self.model.game_window_is_open = True
            # set the randomly assigned card values to the model
            self.model.set_card_values(self.game_window.get_card_values())
            self.model.init_scores()
            player_name, player_idx = self.model.get_player()
            self.game_window.show_player(player_name=player_name, player_idx=player_idx)

        else:
            print("Game window already exists")

    def delete_game_window(self):
        # show the start/root window
        self.main_window.deiconify()
        self.game_window.destroy()
        self.model.game_window_is_open = False
        self.model.clean_round()
        self.model.set_default()

    def set_difficulty_lvl(self, lvl):
        self.model.set_difficulty_level(lvl)
        self.main_window.set_difficulty_level(lvl)

    def play_round(self, card_idx):
        print("Click on Card")
        # view players turn
        # check if a card is already open
        if card_idx not in self.model.get_temp_card_idx():
            print("Set temp card idx")
            self.model.set_temp_card_idx(card_idx)
        else:
            # continue
            # TODO some kind of message to the user???
            print("Card already open")
            return

        if self.model.are_two_cards_open():
            self.game_window.show_card(self.model.get_temp_card_idx())
            self.game_window.update()
            if self.model.check_pair():
                # pair found
                player_name, player_idx = self.model.get_player()
                self.update_scores(player_name=player_name, player_idx=player_idx)
                self.game_window.deactivate_cards(self.model.get_temp_card_idx())
                change_player = False
            else:
                # no pair found
                change_player = True
                self.game_window.after(
                    1000, self.game_window.close_cards(self.model.get_temp_card_idx())
                )

            self.model.clean_round()
            self.model.next_player(change_player)

            if change_player and self.model.get_game_setting()["num_players"] > 1:
                # shows the next player wo is in turn for the next round
                player_name, player_idx = self.model.get_player()
                self.game_window.show_player(
                    player_name=player_name, player_idx=player_idx
                )

        else:
            # only one card is open, continue
            self.game_window.show_card(self.model.get_temp_card_idx())
            return

    def update_scores(self, player_name, player_idx):
        score = self.model.get_and_update_score(name=player_name)
        self.game_window.update_player_score(player_idx=player_idx, score=score)
        self.game_window.update_remaining_score()
