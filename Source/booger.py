import json
import os

class ShopItem:
    def __init__(self, item_type, price, ids):
        self.item_type = item_type
        self.price = price
        self.ids = ids

    def to_dict(self):
        return {
            "itemGrants": self.ids,
            "price": self.price
        }

class CustomShop:
    def __init__(self):
        self.shop_data = {"//": "BR Item Shop Config"}
        self.item_number = 1

    def add_item(self):
        tab_choice = input("Is the item for 'featured' or 'daily'? (type 'done' to finish): ").strip().lower()
        if tab_choice == 'done':
            return False
        if tab_choice not in ['featured', 'daily']:
            print("Invalid choice.")
            return True

        price = self.get_price(tab_choice)
        id_list = self.get_ids(tab_choice)

        key_name = f"{tab_choice}{self.item_number}"
        self.shop_data[key_name] = ShopItem(tab_choice, price, id_list).to_dict()
        self.item_number += 1
        return True

    def get_price(self, tab_choice):
        while True:
            price_input = input(f"Enter the price for {tab_choice}{self.item_number}: ")
            try:
                return int(price_input)
            except ValueError:
                print("Invalid price entered.")

    def get_ids(self, tab_choice):
        print(f"Enter the IDs for {tab_choice}{self.item_number} (one per line). When done, press Enter twice:")
        id_list = []
        while True:
            id_input = input()
            if id_input == "":
                break
            prefix = self.get_prefix(id_input)
            id_list.append(prefix + id_input)
        return id_list

    def get_prefix(self, id_input):
        if "MusicPack" in id_input:
            return "AthenaMusicPack:"
        elif "Character" in id_input or "CID" in id_input:
            return "AthenaCharacter:"
        elif "EID" in id_input:
            return "AthenaDance:"
        return ""

    def save_shop(self, filename="catalog_config.json"):
        with open(filename, 'w') as f:
            json.dump(self.shop_data, f, indent=4)
        print(f"Shop created successfully and saved as '{filename}'.")

    def run(self):
        while self.add_item():
            continue
        self.save_shop()

class ConfigGenerator:
    def __init__(self, filename="IDs.txt"):
        self.filename = filename
        self.config = {}

    def load_ids(self):
        if not os.path.exists(self.filename):
            print(f"{self.filename} not found.")
            return []
        with open(self.filename, "r") as file:
            return [line.strip() for line in file if line.strip()]

    def generate_config(self):
        ids = self.load_ids()
        for i, entry in enumerate(ids, start=1):
            id, price = entry.split(":")
            price = int(price)
            self.add_entry(id, price, i)

    def add_entry(self, id, price, index):
        if id.startswith("EID_"):
            self.config[f"featured{index}"] = {"itemGrants": [f"AthenaDance:{id}"], "price": price}
        elif id.startswith("Character_") or id.startswith("CID_"):
            self.config[f"featured{index + len(self.config)}"] = {"itemGrants": [f"AthenaCharacter:{id}"], "price": price}
        elif id.startswith("MusicPack_"):
            self.config[f"featured{index + 2 * len(self.config)}"] = {"itemGrants": [f"AthenaMusicPack:{id}"], "price": price}

    def merge_configs(self, existing_file="catalog_config.json"):
        if os.path.exists(existing_file):
            with open(existing_file, "r") as infile:
                existing_data = json.load(infile)
            existing_data.update(self.config)
            with open(existing_file, "w") as outfile:
                json.dump(existing_data, outfile, indent=4)
            print("Configuration merged into 'catalog_config.json'.")

def main():
    action = input("Would you like to create a custom shop (enter 'create') or generate config from IDs.txt (enter 'generate')? ").strip().lower()
    if action == 'create':
        shop = CustomShop()
        shop.run()
    elif action == 'generate':
        generator = ConfigGenerator()
        generator.generate_config()
        generator.merge_configs()
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()
