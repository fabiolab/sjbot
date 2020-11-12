{% for activity in activities %}
	**{{activity['athlete']['firstname']}} {{activity['athlete']['lastname']}}** vient d'enregistrer une nouvelle sortie : {{activity['name']}} !
	**{{round(activity['distance'] / 1000)}}km** en **{{round(activity['moving_time'] / 60)}}'**

{% endfor %}