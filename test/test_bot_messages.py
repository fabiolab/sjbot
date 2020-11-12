from sjbot.bot_messages import BotMessages

bm = BotMessages()


def test_message_hello():
    assert 'hello' in bm.hello().lower()


def test_message_top_noplayer():
    players = []
    discipline = 'sh'
    rendered = bm.top(discipline, players)
    assert 'TOP 20 Sjb en' in rendered
    assert discipline.upper() in rendered


def test_message_top():
    players = [{
        "rank": "1",
        "name": "John Woo",
        "subLevel": "N2",
        "frenchRank": "12"
    }, {
        "rank": "2",
        "name": "Arnold S.",
        "subLevel": "N3",
        "frenchRank": "4567"
    }]
    discipline = 'sh'
    rendered = bm.top(discipline, players)
    assert 'TOP 20 Sjb en' in rendered
    assert discipline.upper() in rendered
    for player in players:
        assert player['name'] in rendered
        assert player['rank'] in rendered
        assert player['frenchRank'] in rendered


def test_help():
    bot_prefix = '$'
    rendered = bm.help(bot_prefix)
    assert bot_prefix in rendered
    assert 'SJBot' in rendered


def test_info_player():
    player = {
        'licence': '123456',
        'first_name': 'John',
        'last_name': 'Woo',
        'category': 'Senior',
        'player_rank': {
            'simpleSubLevel': 'N3',
            'bestSimpleSubLevel': 'N2',
            'simpleRate': '12345',
            'doubleSubLevel': 'D8',
            'bestDoubleSubLevel': 'N2',
            'doubleRate': '456789',
            'mixteSubLevel': 'P12',
            'bestMixteSubLevel': 'P10',
            'mixteRate': '12'
        }
    }
    rendered = bm.info_player(**player)
    assert 'N3' in rendered
    assert '12345' in rendered
