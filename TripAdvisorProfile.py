def extract_profile(soup):

    def get_travel_style(soup):
        travel_style_list = []
        travel_style = soup.find_all('div', {'class': 'tagBubble unclickable'})
        for ts in travel_style:
            travel_style_list.append(ts.get_text().strip())
        return travel_style_list

    username = soup.find('span', {'class': 'nameText'}).get_text().strip()
    hometown = soup.find('div', {'class': 'hometown'}).get_text().strip()
    age_since = soup.select_one('.ageSince .since').get_text().strip()
    short_desc = soup.select('.ageSince p')[1].get_text().strip()
    no_reviews = int(soup.find('a', {'name': 'reviews'}).get_text().replace('Reviews', ''))
    travel_style = get_travel_style(soup)
    user_contribution = int(soup.find('div',{'class':'level tripcollectiveinfo'}).find('span').get_text())
    
    return {
        "username": username,
        "hometown": hometown,
        "age_since": age_since,
        "short_desc": short_desc,
        "no_reviews": no_reviews, 
        "travel_style": travel_style,
        "user_contribution": user_contribution
    }