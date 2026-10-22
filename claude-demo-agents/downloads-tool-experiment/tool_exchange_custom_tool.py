def get_topic(path = 'topics.txt') ->str:
    with open(path,"r") as file :
        return file.readline()

if __name__ == "__main__":
    print(get_topic())
