from jinja2 import Environment, FileSystemLoader
from loguru import logger
import random
import emojis

TEMPLATES_DIR = ["../templates", "templates"]
RANKS_EMOJII = {
    "R6": "<:R6:710586107560984680>",
    "R5": "<:R5:710586107737276537>",
    "R4": "<:R4:710586107426766889>",
    "P12": "<:P12:710583882776576161>",
    "P11": "<:P11:710586107397406720>",
    "P10": "<:P10:710586107124908043>",
    "NC": "<:NC:710586107724824617>",
    "N3": "<:N3:710586107477098587>",
    "N2": "<:N2:710586107703853087>",
    "N1": "<:N1:710586107653259324>",
    "D9": "<:D9:710586107561115669>",
    "D8": "<:D8:710586107712241765>",
    "D7": "<:D7:710586107389018195>",
}

STRAVA_TITLES = ["Well done !", "Bravo ! ", "Bien joué !", "Forza !", "Youhou !"]
BRAVO_EMOJIS = [":smile:", ":snake:", ":smiley:", ":astonished:", ":+1:", ":smirk:", ":running:", ":dash:", ":ok_hand:",
                ":muscle:", ":clap:", ":punch:", ":tada:", ":trophy:", ":alien:"]


def transform_rank(rank: str) -> str:
    return RANKS_EMOJII.get(rank.upper(), rank)


class BotMessages:

    def __init__(self):
        file_loader = FileSystemLoader(TEMPLATES_DIR)
        self.env = Environment(loader=file_loader)

    def help(self, bot_prefix: str) -> str:
        template = self.env.get_template('help.tpl')
        return template.render(bot_prefix=bot_prefix)

    def hello(self) -> str:
        template = self.env.get_template('hello.tpl')
        return template.render()

    def top(self, discipline: str, players: list) -> str:
        template = self.env.get_template('top.tpl')
        return template.render(discipline=discipline, players=players)

    def info_player(self, licence, first_name, last_name, category, player_rank) -> str:
        template = self.env.get_template('info_player.tpl')
        ranks = {
            'simple_sublevel': transform_rank(player_rank.get('simpleSubLevel')),
            'simple_best_sublevel': transform_rank(player_rank.get('bestSimpleSubLevel')),
            'simple_rate': player_rank.get('simpleRate'),
            'double_sublevel': transform_rank(player_rank.get('doubleSubLevel')),
            'double_best_sublevel': transform_rank(player_rank.get('bestDoubleSubLevel')),
            'double_rate': player_rank.get('doubleRate'),
            'mixte_sublevel': transform_rank(player_rank.get('mixteSubLevel')),
            'mixte_best_sublevel': transform_rank(player_rank.get('bestMixteSubLevel')),
            'mixte_rate': player_rank.get('mixteRate')
        }
        return template.render(licence=licence, first_name=first_name, last_name=last_name, category=category,
                               ranks=ranks)

    def new_strava_activities(self, activities: list) -> str:
        template = self.env.get_template('strava_activities.tpl')
        return template.render(activities=activities, round=round)

    @staticmethod
    def new_strava_activities_title() -> str:
        return f"{random.choice(STRAVA_TITLES)} {emojis.encode(random.choice(BRAVO_EMOJIS))}"
