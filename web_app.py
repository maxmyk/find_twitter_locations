"""

3. Розробити web-додаток за допомогою якого можна
буде зображати на карті дані (поле "location") про
товаришів (людей, на яких ви підписані) вказаного
облікового запису в Twitter. Значення поля
"location", яке вказав товариш повинно зображатися
на карті довільним типом маркера, але повинно
містити також й ім'я цього товариша  (значення
поля "screen_name"). Web-додаток повинен бути
розгорнутий на сервісі https://www.pythonanywhere.com

"""

import argparse
import requests
import json


"""
Importing necessary libraries
"""


def args_parser():
    """
    args_parser()
    Parses positional arguments
    """
    parser = argparse.ArgumentParser(description='main.py parser')
    parser.add_argument("nick", type=str, help="Your NICKNAME")
    return parser.parse_args()


def locations_parser(data: dict):
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
    Returns file name in the folowing format:
    map_d_m_Y-H:M:S.html
    """
    import folium
    from folium.plugins import HeatMap
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
    # HeatMap(locations, name='All films locations HeatMap',
    #         control=True, show=False).add_to(map_1)
    folium.LayerControl().add_to(map_1)
    from datetime import datetime
    now = datetime.now()
    # new_label = f'map_{"".join(now.strftime(f"%d_%m_%Y-%H:%M:%S"))}.html'
    import os
    print(os.path.abspath(os.getcwd()))
    new_label='templates/map.html'
    map_1.save(new_label)
    return f'Map file is {new_label}'


def main(nick_name: str):
    """
    Main function
    """
    import time
    now = time.time()
    usr_id = requests.get("https://api.twitter.com/2/users/by/username/"+nick_name, headers={
                          'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMwMZQEAAAAAS5Xs%2FWlF2rG5r%2Fn%2B4BO1g%2BpO1mQ%3DnGZr3bljfOxImVkKCKG3J8BNjGkER13lZ2SxXv6jvxYEJrRKg8'})


    usr_id = usr_id.json()
    ans = json.dumps(usr_id, indent=4, ensure_ascii=False)
    usr_locations = requests.get("https://api.twitter.com/2/users/"+usr_id["data"]["id"]+"/following?user.fields=location", headers={
                                 'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMwMZQEAAAAAS5Xs%2FWlF2rG5r%2Fn%2B4BO1g%2BpO1mQ%3DnGZr3bljfOxImVkKCKG3J8BNjGkER13lZ2SxXv6jvxYEJrRKg8'})
    usr_locations = usr_locations.json()
    ans1 = json.dumps(usr_locations, indent=4, ensure_ascii=False)
    locations = locations_parser(usr_locations)
    create_map(locations)
    print(f' # Time: {time.time() - now} sec.')
    print('\n # Success!')


def pre_main():
    args = args_parser()
    nick_name = args.nick
    main(nick_name)



if __name__ == '__main__':
    pre_main()
