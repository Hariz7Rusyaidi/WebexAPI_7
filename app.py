import requests
import json
from datetime import datetime

# handle all the interractions of the program
class WebexAPI:
    def __init__(self):
        self.base_url = "https://webexapis.com/v1"
        self.token = ""
        self.headers = {}

    def set_token(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def test_connection(self):
        url = f"{self.base_url}/people/me"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return True
        return False

    def get_user_info(self):
        url = f"{self.base_url}/people/me"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return 
            {
                "Displayed Name": data.get("displayName"),
                "Nickname": data.get("nickName"),
                "Emails": data.get("emails")
            }
        return None

    def list_rooms(self, max_rooms=5):
        url = f"{self.base_url}/rooms"
        params = {"max": max_rooms}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            rooms = response.json().get("items", [])
            return [
            {
                "Room ID": room.get("id"),
                "Room Title": room.get("title"),
                "Date Created": room.get("created"),
                "Last Activity": room.get("lastActivity")
            } for room in rooms]
        return []

    def create_room(self, title):
        url = f"{self.base_url}/rooms"
        data = {"title": title}
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return True
        return False

    def send_message(self, room_id, message):
        url = f"{self.base_url}/messages"
        data = {
            "roomId": room_id,
            "text": message
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return True
        return False

# main functions and main menu interface of program
def main():
    webex = WebexAPI()

    # Get user's Webex token
    token = input("Enter your Webex token: ")
    webex.set_token(token)

    while True:
        print("\nMenu:")
        print("0. Test connection")
        print("1. Display user information")
        print("2. List rooms")
        print("3. Create a room")
        print("4. Send message to a room")
        print("5. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == "0":
            if webex.test_connection():
                print("Connection successful!")
            else:
                print("Connection failed. Please check your token.")

        elif choice == "1":
            user_info = webex.get_user_info()
            if user_info:
                for key, value in user_info.items():
                    print(f"{key}: {value}")
            else:
                print("Failed to retrieve user information.")

        elif choice == "2":
            rooms = webex.list_rooms()
            if rooms:
                for i, room in enumerate(rooms, 1):
                    print(f"\nRoom {i}:")
                    for key, value in room.items():
                        print(f"{key}: {value}")
            else:
                print("No rooms found or failed to retrieve rooms.")

        elif choice == "3":
            title = input("Enter the title for the new room: ")
            if webex.create_room(title):
                print(f"Room '{title}' created successfully!")
            else:
                print("Failed to create the room.")

        elif choice == "4":
            rooms = webex.list_rooms()
            if rooms:
                print("Available rooms:")
                for i, room in enumerate(rooms, 1):
                    print(f"{i}. {room['Room Title']}")
                room_choice = int(input("Choose a room number: ")) - 1
                if 0 <= room_choice < len(rooms):
                    message = input("Enter your message: ")
                    if webex.send_message(rooms[room_choice]['Room ID'], message):
                        print("Message sent successfully!")
                    else:
                        print("Failed to send the message.")
                else:
                    print("Invalid room number.")
            else:
                print("No rooms available.")

        elif choice == "5":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()