from otree.api import *

import random

cu = Currency


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'lottery_simple'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    payoff_hi = cu(4.00)
    payoff_lo = cu(0)
    payoff_hi2 = cu(30.00)
    payoff_mid = cu(0.5)
    payoff_lo2 = cu(0)
    payoff_2_hi = cu(5.00)
    payoff_2_lo = cu(1.4)
    probability_hi = 80
    probability_lo = 20
    sure_payoff = cu(3.2)
    payoff_hi3 = cu(7.20)
    payoff_mid3 = cu(0.45)
    payoff_lo3 = cu(0)
    payoff_3_hi = cu(4.00)
    payoff_3_mid3 = cu(3.4)
    payoff_3_lo = cu(2)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        round_numbers = list(range(1, C.NUM_ROUNDS + 1))
        random.shuffle(round_numbers)
        selected_round = random.randint(1, C.NUM_ROUNDS)
        p.participant.selected_round = selected_round


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Question = models.StringField(
        choices=[
            [1, "Lottery 1: You have 80% chance to win 4 and 0 otherwise"],
            [2, "Lottery 2: You have 100% chance to win 3.2"]
        ],
        doc='Players decision', widget=widgets.RadioSelect
    )
    Question2 = models.StringField(
        choices=[
            [1, "Lottery 1: You have 10% chance to win £30, 40% chance to win £0.5 and 50% chance to win 0"],
            [2, "Lottery 2: You have 50% chance to win £5 and 50% chance to win £1.4"]
        ],
        doc='Players decision', widget=widgets.RadioSelect
    )
    Question3 = models.StringField(
        choices=[
            [1, 'Lottery 1: You have 42% chance to win 7.2; 40% chance to win 0.45 and 18% to win 0'],
            [2, 'Lottery 2: You have 40% chance to win 4; 40% chance to win 3.4 and 20% chance to win 2']
            ],
        doc='Players decision', widget=widgets.RadioSelect,
    )
    selected_round = models.IntegerField()
    choice = models.IntegerField()
    choice_in_round = models.StringField()
    payment = models.FloatField()
    final_pay = models.CurrencyField()


# PAGES
class Question(Page):
    form_model = 'player'
    form_fields = ['Question']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(choice_in_round=player.in_rounds(1, C.NUM_ROUNDS))

# create dict for payoff for each question
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.session.rewards = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4"}

        if player.in_rounds(1, C.NUM_ROUNDS):

            if int(player.Question) == 1:
                random_number = random.randint(1, 100)
                if random_number <= C.probability_hi:
                    payoff = C.payoff_hi
                else:
                    payoff = C.payoff_lo
            else:
                payoff = C.sure_payoff
            player.payoff = payoff
        player.session.rewards[1] = player.payoff

    # @staticmethod
    # def vars_for_template(player:Player):
    #     return {
    #         "payoff": player.in_rounds(1, C.NUM_ROUNDS),
    #     }

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.payoff = player.in_rounds(1, C.NUM_ROUNDS) == player.payoff
    #     payment = {}
    #     payment[player.payoff] = player.in_rounds(1, C.NUM_ROUNDS)
    #     print(payment)
    #     player.session.rewards[1] = player.payoff


class Question2(Page):
    form_model = 'player'
    form_fields = ['Question2']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(choice_in_round=player.in_rounds(1, C.NUM_ROUNDS))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # if participant.selected_round == round(2):
        if player.in_rounds(1, C.NUM_ROUNDS):
            if int(player.Question2) == 1:
                random_number = random.randint(1, 100)
                if random_number <= 10:
                    payoff2 = C.payoff_hi2
                elif 11 <= random_number <= 50:
                    payoff2 = C.payoff_mid
                else:
                    payoff2 = C.payoff_lo2
            else:
                random_number = random.randint(1, 100)
                if random_number <= 50:
                    payoff2 = C.payoff_2_hi
                else:
                    payoff2 = C.payoff_2_lo
            player.payoff = payoff2
        player.session.rewards[2] = player.payoff
        #
        # @staticmethod
        # def vars_for_template(player: Player):
        #     return {
        #         "payoff": player.in_rounds(1, C.NUM_ROUNDS),
        #     }


class Question3(Page):
    form_model = 'player'
    form_fields = ['Question3']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(choice_in_round=player.in_rounds(1, C.NUM_ROUNDS))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # if participant.selected_round == round(3):
        if player.in_rounds(1, C.NUM_ROUNDS):
            if int(player.Question3) == 1:
                random_number = random.randint(1, 100)
                if random_number <= 42:
                    payoff3 = 7.2
                elif 43 <= random_number <= 82:
                    payoff3 = 0.45
                else:
                    payoff3 = 0
            else:
                random_number = random.randint(1, 100)
                if random_number <= 40:
                    payoff3 = 4
                elif 41 <= random_number <= 80:
                    payoff3 = 3.4
                else:
                    payoff3 = 2
            player.payoff = payoff3
        player.session.rewards[3] = player.payoff
        return player.payoff

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
    #def before_next_page(player: Player, timeout_happened):
        import random
        participant = player.participant
        if player.round_number == C.NUM_ROUNDS:
            random_round = random.randint(1, 3)
            participant.selected_round = random_round
            player.selected_round = random_round

        if participant.selected_round == 1:
            player.choice_in_round = player.Question
        elif participant.selected_round == 2:
            player.choice_in_round = player.Question2
        else:
            player.choice_in_round = player.Question3


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        reward = player.session.rewards[player.participant.selected_round]
        return {
            #  reward = player.session.rewards[player.participant.selected_round
            "reward": reward,
        }


page_sequence = [Question, Question2, Question3, Results]
