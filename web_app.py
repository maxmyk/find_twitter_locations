"""
Web app parser and map creator
"""

# Importing necessary libraries
import requests


def locations_parser(data: dict):
    """
    Parses locations
    """
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    locations = set()
    geolocator = Nominatim(user_agent='lab_request_new')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    counter = 0
    for element in data["data"]:
        try:
            print(f' $ parser.py => Processed: {counter}/{len(data["data"])} locations;\n' +
                  f' $           => Physical address: {element["location"]}')
            counter += 1
            location = geocode(element['location'])
            if location != None:
                locations.add(
                    (element["name"], location.latitude, location.longitude))
            else:
                location = geocode(
                    ''.join(element['location'].split(' ')[-3:]))
                if location != None:
                    locations.add(
                        (element["name"], location.latitude, location.longitude))
                else:
                    location = geocode(
                        ''.join(element['location'].split(' ')[-2:]))
                    if location != None:
                        locations.add(
                            (element["name"], location.latitude, location.longitude))
                    else:
                        location = geocode(
                            ''.join(element['location'].split(' ')[-1]))
                        if location != None:
                            locations.add(
                                (element["name"], location.latitude, location.longitude))
                        else:
                            locations.add((element["name"], 44.9332, 7.5401))
        except KeyError:
            locations.add(
                (element["name"], 44.9332, 7.5401))
    return list(locations)


def create_map(data: dict) -> str:
    """
    Creates map using Folium.
    """
    import folium
    from random import uniform
    cur_pos = (49.81763, 24.02295)
    # cur_pos = (44.9332, 7.5401)
    map_1 = folium.Map(location=cur_pos, zoom_start=10, control_scale=True)
    folium.Marker(
        location=cur_pos,
        popup='My location',
        icon=folium.Icon(color='green', icon='home'),
    ).add_to(map_1)
    locs = []
    for element in data:
        loc = (element[1], element[2])
        if loc == cur_pos:
            loc = [loc[0]+uniform(-0.002, 0.002), loc[1] +
                   uniform(-0.002, 0.002)]
        while loc in locs:
            loc = [loc[0]+uniform(-0.002, 0.002), loc[1] +
                   uniform(-0.002, 0.002)]
        locs.append(loc)
    for num, element in enumerate(data):
        folium.Marker(
            location=locs[num],
            popup=element[0],
            icon=folium.Icon(color='green', icon='ok-sign'),
        ).add_to(map_1)
    folium.LayerControl().add_to(map_1)
    return map_1


def main(nick_name: str):
    """
    Main function
    """
    from secret_key import s_key
    print(s_key())
    usr_id = requests.get("https://api.twitter.com/2/users/by/username/"+nick_name, headers={
                          'Authorization': 'Bearer '+s_key()})
    usr_id = usr_id.json()
    usr_locations = requests.get("https://api.twitter.com/2/users/"+usr_id["data"]["id"] +
                                 "/following?user.fields=location", headers={
                                 'Authorization': 'Bearer '+s_key()})
    usr_locations = usr_locations.json()
    locations = locations_parser(usr_locations)
    return create_map(locations)


def pre_main():
    """
    Pre main function
    """
    nick_name = input()
    main(nick_name)


if __name__ == '__main__':
    pre_main()
