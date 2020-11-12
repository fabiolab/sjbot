**TOP 20 Sjb en {{discipline.upper()}} !**
{% for player in players[:20] %}
{{player.get("rank")}}. {{player.get("name")}} ({{player.get("subLevel")}} - nat : {{player.get("frenchRank")}}){% endfor %}
