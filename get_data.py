import requests, lxml, os, sys, json, time
from bs4 import BeautifulSoup

url_home = 'https://www.skidrow-games.com/page/'

url_games_list = 'https://www.skidrow-games.com/pc-games/?lcp_page2=1#lcp_instance_2'

url_repacks = 'https://www.skidrowreloaded.com/category/pc-repack/page/1/'

base_url = 'https://www.skidrow-games.com/'

def get_new_games(page):
    games_list = []
    res = requests.get(url_home + str(page) + "/")
    soup = BeautifulSoup(res.content, 'lxml')
    for post in soup.find_all('div', {'class': 'post'}):
        # title, link, uid, tag, thumb_url, description = ''
        title = post.find('h2').find('a').text
        link = post.find('h2').find('a').get('href')
        uid = link.replace(base_url, '').replace('/', '')
        tag = post.find('div', {'class':'meta'}).find('a').text
        img_tag = post.find('div', {'class' : 'post-excerpt'}).find('center').find('img', {'class' : {'aligncenter'}})
        thumb_url = img_tag.get('data-lazy-src')
        description = img_tag.parent.findNext('p').findNext('p').text
        game_info = {
            'uid': uid,
            'title': title,
            'link': link,
            'tag': tag,
            'thumb_url': thumb_url,
            'description': description,
            'meta_details': get_game_details(link)
        }
        games_list.append(game_info)
    print(games_list)
    print(len(games_list))
    data = {'games_list' : games_list}
    write_data(data)

def write_data(data):
    os.chdir(os.getcwd())
    with open('game_info.json','w') as f:
        json.dump(data, f, indent=4)

def get_game_details(link):
    time.sleep(2)
    game_info = {}
    skip_index = [1,2,8,9]
    i = 0
    response = requests.get(link)
    info_soup = BeautifulSoup(response.content, 'lxml')
    for tabs in info_soup.find_all('div', {'class':'wordpress-post-tabs'})[0].find('div'):
        i += 1
        if i in skip_index:
            continue
        # print('\nTabs:\n')
        # print(tabs)
        # continue

        # For getting game info
        if i == 3:
            tab_1 = tabs

            # For getting description of the game
            desc = tab_1.find('h5').findNext('p')
            description = desc.text
            desc_f = desc.parent.findNext('p').findNext('p')
            description = description + desc_f.text
            game_info['description'] = description

            # For getting more info of the game
            img_pr = desc_f.findNext('p')
            # thumbURL = img_pr.find('img').get('src')
            more_tags = img_pr.findNext('p')
            try:
                for tags in more_tags.text.split('\n'):
                    pair = tags.split(':')
                    # tag_info = 
                    game_info[pair[0].lower().replace(' ','_')] = pair[1].strip()
                    # game_info.append(tag_info)
                release_tag = more_tags.findNext('p')
                for tags in release_tag.text.split('\n'):
                    pair = tags.split(':')
                    game_info[pair[0].strip().lower().replace(' ','_')] = pair[1].strip()
                    # game_info.append(tag_info)
            except:
                pass

            # For getting the download urls
                # For getting all urls
            liner = tab_1.find('p',text='____________________')
            isNotSteam = True
            steam_text = 'Support the developers. buy this game if you like it. BUY IT!'
            p_tag = liner.findNext('p')
            oth = []
            while(isNotSteam):
                if(p_tag is None):
                    isNotSteam = False
                    break
                if(str(p_tag.text) == steam_text):
                    break

                # For getting just the torrent urls
                try:
                    # other_link = {p_tag.text.lower().strip().replace(' ','_'), p_tag.find('a').get('href')}
                    oth.append(p_tag.find('a').get('href'))
                except:
                    pass
                if(p_tag.text.lower().strip() == 'torrent magnet download'):
                    torrent_url = p_tag.find('a')
                    game_info['magnetURL']=torrent_url.get('href')
                    # game_info.append(torrent_info)

                if(p_tag.text.lower().strip() == 'torrent download'):
                    torrent_url = p_tag.find('a')
                    game_info['torrentURL'] = torrent_url.get('href')
                    # game_info.append(torrent_info)
                p_tag = p_tag.findNext('p')
            game_info['other_links']=oth

        # For getting system requirements
        if i == 4:
            # print(tabs)
            requirements = {'minimum':[],'recommended':[]}
            j = 0
            for head in tabs.find_all('p'):
                j += 1
                for li in head.findNext('ul').find_all('li'):
                    try:
                        parts = li.text.split(':')
                        min_info = (parts[0].strip(), parts[1].strip().replace('\u00ae',''))
                        if(j == 1):
                            requirements['minimum'].append(min_info)
                        else:
                            requirements['recommended'].append(min_info)
                    except:
                        pass
            game_info['system_requirements'] = requirements

        # For getting screenshots
        if i == 5:
            scs = []
            for p in tabs.find_all('p'):
                parts = p.find('img').get('src')
                if parts.find('https') == -1:
                    continue
                scs.append(parts)
            game_info['screenshots']=scs
        
        # For getting gameplay or trailer
        if i == 6:
            game_info['gameplayURL']=tabs.find('iframe').get('src')
    print(game_info)
    return game_info
    # write_data({'game_info': game_info}) 


        

if __name__ == '__main__':
    get_new_games(1)
    # get_game_details('https://www.skidrow-games.com/mafia-iii-stones-unturned-dlc-crack-cdx/')