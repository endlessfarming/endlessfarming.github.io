import json
import os
import urllib.request

from bs4 import BeautifulSoup


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def main():
    PAGES = 21
    DIFFICULTY = "easy"
    level = 1
    ids = []
    for page in range(1, PAGES + 1):
        url = f"http://endlessfrontierdata.com/spirithighlands/{DIFFICULTY}/{page}"
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        html = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(html)
        divs = soup("a", {"style": "text-decoration:none;color:white;"})
        tuples = []
        for div in divs:
            id = (
                div.findChildren("img")[0].get("src").split("/")[-1].replace(".png", "")
            )
            if id != "honor" and id != "gem":
                lvl_id_tuple = (level, int(id))
                tuples.append(lvl_id_tuple)
            level += 1
        ids += tuples

    if DIFFICULTY == "easy":
        filename = "../app/static/json/pets.json"
    elif DIFFICULTY == "hard":
        filename = "../app/static/json/hard_sh_pets.json"
    else:
        raise ValueError("Diffculty should be in {easy, hard}.")

    with open(filename, "r") as json_file:
        data = json.load(json_file)
        for key, items in data.items():
            id = int(items["img"].split("/")[-1].replace(".png", ""))
            items["from"] = [lvl for lvl, pet in ids if pet == id]

    os.remove(filename)
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    main()
