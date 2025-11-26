import json, operator

ranks = ["Что-то слышал", "Новичок в Ярче", "Изучающий Ассортимент", "Эксперт Выгоды 🌈",
         "Искорка Ярче 🔥", "Постоянный покупатель ☀️", "Живущий Ярко ✨✨", "Перееханная бабушка"]
rank_count = [0, 3, 7, 14, 20, 27, 35, 100]
award = "[✨Самый яркий✨]"

class yarchePerson:
    def __init__(self, name: str, username: str):
        self.name = name
        self.username = username
        self.rank = 0
        self.count = 1

    def __repr__(self):
        return f"YarcheRank(name='{self.name}', rank={self.rank}, count={self.count})"

def handle_yarche_mention(name: str, username: str):
    # Открываем файл для чтения
    with open("yarche.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    message = ""

    flag = False
    for object in data:
        if object['username'] == username:
            flag = True
            object['count'] += 1
            for i in range(len(rank_count)):
                if object['count'] == rank_count[i]:
                    object['rank'] += 1
                    message = handle_rank_up(object['name'], object['rank'])

    if flag == False:
        person = yarchePerson(name, username)
        newPersonDict = person.__dict__
        data.append(newPersonDict)

    # Открываем файл для записи
    with open("yarche.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Write:", data)

    return message

def handle_rating():
    message: str = "Рейтинг всех фанатов сети магазинов Ярче! ✨\n"
    # Открываем файл для чтения
    with open("yarche.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data = sorted(data, key=operator.itemgetter('count'), reverse=True)

    for index, object in enumerate(data):
        message += (f"\n{object['name']} (@{object['username']}) "
                    f"[{ranks[object['rank']]}] - {object['count']} упоминаний! ")
        if index == 0: message += "\n" + award + "\n"

    return message

def handle_rank_up(name: str, rank: int):
    message = f"✨✨ {name} получил новый ранг {ranks[rank]} !"
    return message

