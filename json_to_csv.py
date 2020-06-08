import csv
import json
import requests

# Set your credentials here:
api_key = 'your key'
token = 'your token'


def write_data_to_csv(cards, lists, members, csv_writer):
    for index, card in enumerate(cards):
        if index == 0:
            headers = reconcile_card_data(card, lists, members)
            csv_writer.writerow(headers)

        card_data = reconcile_card_data(card, lists, members)
        try:
            csv_writer.writerow(card_data.values())
        except:
            continue


def get_list_from_id(id, lists):
    for list in lists:
        if list['id'] == id:
            if 'Done' in list['name']:
                return 'done'
            else:
                return list['name']


def get_members_from_ids(ids, members):
    members_names = []
    for id in ids:
        for member in members:
            if member['id'] == id:
                members_names.append(member['fullName'])

    return members_names


def reconcile_card_data(card, lists, members):
    card_data = {}
    reconciled_keys = ['id', 'idList', 'name', 'desc', 'idMembers', 'url']
    for key in reconciled_keys:
        try:
            if key == 'idList':
                card_data['list'] = get_list_from_id(card[key], lists)
            elif key == 'idMembers':
                card_data['members'] = get_members_from_ids(card[key], members)
            else:
                card_data[key] = card[key]
        except:
            continue

    return card_data


def get_board_by_id(id, api_key, token):
    url = "https://api.trello.com/1/boards/{}".format(id)
    querystring = {
        "actions": "all", "boardStars": "none", "cards": "all", "card_pluginData": "false",
        "checklists": "none", "customFields": "false",
        "fields": "name,desc,descData,closed,idOrganization,pinned,url,shortUrl,prefs,labelNames",
        "lists": "open", "members": "all", "memberships": "none", "membersInvited": "none",
        "membersInvited_fields": "all", "pluginData": "false", "organization": "false",
        "organization_pluginData": "false", "myPrefs": "false", "tags": "false", "key": "{}".format(api_key),
        "token": "{}".format(token)
    }

    http_res = requests.get(url, querystring)
    board_res = http_res.json()

    print(board_res)
    return board_res


def get_board_id_by_member_credentials(api_key, token):
    team_name = 'City of Cape Town Front End'
    url = 'https://api.trello.com/1/members/me/boards'
    querystring = {"key": "{}".format(api_key),
                   "token": "{}".format(token)}

    http_res = requests.get(url, querystring)
    json_res = http_res.json()

    for board_res in json_res:
        contraventions_board_id = 'CLrEPcZG'
        if board_res['shortLink'] == contraventions_board_id:
            board = board_res
            break

    print(board)
    return board['id']


def get_trello_board_data_via_api():
    # Registered with trello for developers for:


    board_id = get_board_id_by_member_credentials(api_key, token)
    board = get_board_by_id(board_id, api_key, token)

    cards = board['cards']
    lists = board['lists']
    members = board['members']

    return cards, lists, members



def get_trello_board_data_from_file():
    with open('C:\\Users\\toast\\PycharmProjects\\testing\\data.json', encoding="utf8") as json_file:
        data = json.load(json_file)
        cards = data['cards']
        lists = data['lists']
        members = data['members']

    return cards, lists, members


def main():
    # cards, lists, members = get_trello_board_data_from_file()
    cards, lists, members = get_trello_board_data_via_api()

    data_file = open('C:\\Users\\toast\\PycharmProjects\\testing\\data_file.csv', 'w', newline='')
    csv_writer = csv.writer(data_file, delimiter=';')
    write_data_to_csv(cards, lists, members, csv_writer)
    data_file.close()


if __name__ == "__main__":
    main()
