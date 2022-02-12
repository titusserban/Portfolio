from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.views.generic import TemplateView
import requests
from humanfriendly import format_timespan


# View for routing 
class Route(TemplateView):
	
	template_name = 'googleapi/route.html'

	def get_context_data(self, **kwargs):
		context = super(Route, self).get_context_data(**kwargs)
		context["google_api_key"] = settings.GOOGLE_API_KEY
		context["base_country"] = settings.BASE_COUNTRY
		return context


def google_directions(*args, **kwargs):
    # handle the directions from Google by accessing them from the url via **kwargs
    lat_a = kwargs.get("lat_a")
    long_a = kwargs.get("long_a")
    lat_b = kwargs.get("lat_b")
    long_b = kwargs.get("long_b")
    lat_c = kwargs.get("lat_c")
    long_c = kwargs.get("long_c")
    lat_d = kwargs.get("lat_d")
    long_d = kwargs.get("long_d")

	# Construct the parameters
    origin = f"{lat_a}, {long_a}"
    destination = f"{lat_b}, {long_b}"
    waypoints = f"{lat_c}, {long_c} | {lat_d}, {long_d}"

	# The API request to Google cloud
    result = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json?",
        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints,
            "key": settings.GOOGLE_API_KEY
        }
    )

    directions = result.json()

	# Check to see if the response status is OK
    if directions["status"] == "OK":

        routes = directions["routes"][0]["legs"]

        distance = 0
        duration = 0
        route_list = []

		# Manipulate the data from the API call 
        for route in range(len(routes)):

			# Add to the total distance
            distance += int(routes[route]["distance"]["value"])
            # Add to the total duration
            duration += int(routes[route]["duration"]["value"])

            route_step = {
                'origin': routes[route]["start_address"],
                'destination': routes[route]["end_address"],
                'distance': routes[route]["distance"]["text"],
                'duration': routes[route]["duration"]["text"],
                'steps': [
                    [
                        s["distance"]["text"],
                        s["duration"]["text"],
                        s["html_instructions"],

                    ]
                    for s in routes[route]["steps"]]
                }
            
            route_list.append(route_step)
            
    return {
        "origin": origin,
        "destination": destination,
        "distance": f"{round(distance/1000, 2)} Km",
        "duration": format_timespan(duration),
        "route": route_list
        }


# View for displaying the map 
def map(request):
	lat_a = request.GET.get("lat_a", None)
	long_a = request.GET.get("long_a", None)
	lat_b = request.GET.get("lat_b", None)
	long_b = request.GET.get("long_b", None)
	lat_c = request.GET.get("lat_c", None)
	long_c = request.GET.get("long_c", None)
	lat_d = request.GET.get("lat_d", None)
	long_d = request.GET.get("long_d", None)

	# Check if all 4 addresses are added
	if lat_a and lat_b and lat_c and lat_d:
		directions = google_directions(
			lat_a= lat_a,
			long_a=long_a,
			lat_b = lat_b,
			long_b=long_b,
			lat_c= lat_c,
			long_c=long_c,
			lat_d = lat_d,
			long_d=long_d
			)

		context = {
			"google_api_key": settings.GOOGLE_API_KEY,
			"base_country": settings.BASE_COUNTRY,
			"lat_a": lat_a,
			"long_a": long_a,
			"lat_b": lat_b,
			"long_b": long_b,
			"lat_c": lat_c,
			"long_c": long_c,
			"lat_d": lat_d,
			"long_d": long_d,
			"origin": f'{lat_a}, {long_a}',
			"destination": f'{lat_b}, {long_b}',
			"directions": directions
			}

		return render(request, 'googleapi/map.html', context)
	
	return redirect(reverse('googleapi:route'))

	