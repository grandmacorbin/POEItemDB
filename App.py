import mysql.connector
from dotenv import load_dotenv
import os

    
def get_item_by_type(conn):
    get_item = "SELECT itemName, rarity, levelReq FROM item WHERE itemType = %s"
    itemType = input("Input item type your looking for: ")
    try:
        cursor = conn.cursor()
        cursor.execute(get_item, (itemType,))
        
        results = cursor.fetchall()
        if results:
            print(f"\n{'Name':<15} {'Rarity':<15} {'level Requirment'}")
            print("-" * 60)
            for item in results:
                print(f"{item[0]:<15} {item[1]:<15} {item[2]}")
        else:
            print("No items found with that item type")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def get_currency_list(conn):
    get_description = "SELECT * from currency"
    
    try:
        cursor = conn.cursor()
        cursor.execute(get_description)
        results = cursor.fetchall()
        print(f"\n{'Currency':<25} {'Value':<10} {'Description'}")
        print("-" * 60)
        for item in results:
            print(f"{item[0]:<25} {int(item[2]):<10} {item[1]}")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def insert_gem_into_socket(conn):
    query = "INSERT INTO itemsocket (itemName, socketPosition, socketColor, socketedGem) VALUES (%s, %s, %s, %s)"
    name = input("name of item: ")
    socket_Position = input("position of socket (1,2,3,4): ")
    socket_Color = input("Color of Socket (Red, Green, Blue): ")
    skillGem = input("SkillGem being socketed: ")
    select_query = "SELECT itemName, socketedGem FROM itemSocket WHERE itemName = %s and socketedGem = %s"
    insert_Skillgem = "INSERT INTO skillgems (gemName, gemColor) VALUES (%s, %s)"
    
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (name, socket_Position, socket_Color, skillGem))
        conn.commit()
        cursor.execute(select_query, (name, skillGem))
        result = cursor.fetchall()
        cursor.execute(insert_Skillgem, (skillGem, socket_Color))
        conn.commit()
        for item in result:
            print(f"\nSkillgem: {item[1]} socketed into {item[0]}")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def if_npc_sells(conn):
    Query = "SELECT itemName, price FROM sells WHERE npcName = %s"
    npc_Name = input("Enter NPC's name: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute(Query, (npc_Name,))
        result = cursor.fetchall()
        print(f"\n{'Item':<15} {'price'}")
        print("_"*60)
        for item in result:
            print(f"{item[0]:<15} {item[1]}")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    

def main():
    load_dotenv()

    try:
        cnx = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME', 'POEDB')
            )
        print("Connection successful", cnx.is_connected)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    while True:
        print("\nMenu:")
        print("1. Find item by item type")
        print("2. Get list of currency with description")
        print("3. insert skilgem into item socket")
        print("4. See the items an NPC sells")
        print("5. Exit")
        ans = input("Enter your choice: ")
        
        if ans == "1":
            get_item_by_type(cnx)
        elif ans == "2":
            get_currency_list(cnx)
        elif ans == "3":
            insert_gem_into_socket(cnx)
        elif ans == "4":
            if_npc_sells(cnx)
        elif ans == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()