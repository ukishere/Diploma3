import classes
import json

def new_start():
    client = classes.User()
    client.check_user()
    client.create_database()

    offset = 0
    new_victims = []

    while len(new_victims) < 10:
        victims = client.get_victims(offset)
        new_victims.extend(client.check_victims(victims))
        offset += 10
        if offset == 1000:
            print('Больше никого не осталось.')
            exit()

    new_victims = new_victims[0:10]
    client.add_victims_photo(new_victims)

    with open('vkinder_results.json', 'w') as file:
        json.dump(new_victims, file, indent=2, ensure_ascii=False)

    client.remember_victims(new_victims)
    print('Поиск завершен. Список кандидатов сформирован.')

if __name__ == '__main__':
    new_start()
