import json

def create():
    data: None
    with open("services.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    service_id = input("service_id: ")
    platform = input("platform: ")
    name = input("name: ")
    min = int(input("min: "))
    max = int(input("max: "))
    price = int(input("price (1000): "))
    data[service_id] = {"platform": platform, "name": name, "min": min, "max": max, "price": price}
    with open("services.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, separators=(",", ": "))
        file.close()



if __name__ == '__main__':
    create()