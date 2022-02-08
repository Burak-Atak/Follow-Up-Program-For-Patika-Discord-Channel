import requests
import json

# Channels ID
LINKEDIN_ID = "897117940304994393"
GITHUB_ID = "897117940493729802"


# This class gets links from channels.
class GetLinks:

    parameters = {
        "limit": 100
    }

    def __init__(self):
        self.text_name = ""
        self.linkedin = False
        self.data_list = []
        self.added = []
        self.authorization = ""

    # This function reads entered text after update self.added and runs the retrieve_messages() function.
    def read_file(self, authorization, linkedin=False,):
        self.linkedin = True if linkedin else False
        self.text_name = "linkedin_links.txt" if linkedin else "github_links.txt"
        self.added.clear()
        self.data_list.clear()
        self.authorization = authorization

        try:
            with open(self.text_name, "r", encoding="utf-8") as text_file:
                self.added = text_file.readlines()
        except FileNotFoundError:
            pass

        self.retrieve_messages()

    # This function get data from Discord API and runs write_to_file() function.
    def retrieve_messages(self):
        channel_id = LINKEDIN_ID if self.linkedin else GITHUB_ID

        headers = {
            "authorization": self.authorization
        }

        r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers,
                         params=self.parameters)

        self.write_to_file(json.loads(r.text))

    # This function takes data argument and adds new links to txt file.
    def write_to_file(self, data):
        last_message_year = int(data[-1]["timestamp"].split("T")[0].split("-")[0])
        self.data_list.extend(data)

        if last_message_year == 2022:
            last_message_id = data[-1]["id"]
            self.parameters["before"] = last_message_id
            self.retrieve_messages()
        else:
            with open(self.text_name, "a", encoding="utf-8") as text_file:
                for i in self.data_list:
                    message_year = int(i["timestamp"].split("T")[0].split("-")[0])
                    content = i["content"]
                    if (message_year == 2022) and (" " not in content) and (".com" in content) and (content + "\n") not in self.added:
                        text_file.writelines(content + "\n")
                        self.added.append(content)

            self.added.clear()

        self.parameters.pop('before', None)

