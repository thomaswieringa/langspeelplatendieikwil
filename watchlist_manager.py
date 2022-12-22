import discogs_client


class WatchlistManager:
    def __init__(self, key, versions):
        self.d = discogs_client.Client('ExampleApplication/0.1', user_token=key)
        self.versions = versions
        print("Welcome!")

    def run(self):
        print('options:')
        print('1. show masters in watchlist')
        print('2. search for another records to add to the watchlist')
        print('3. upload all versions of masters to discog')
        print('4. erase watchlist')
        choice = int(input())
        if choice == 1:
            self.show_masters()
        if choice == 2:
            self.search()
        if choice == 3:
            self.upload()
        if choice == 4:
            print('sure? y or n')
            sure = input()
            if sure == 'y':
                self.versions.delete_all()
            self.run()

    def show_masters(self):
        print("current master wantlist:")
        # Using readlines()
        file1 = open('masters.txt', 'r')
        for line in file1.readlines():
            print(self.d.master(line).title)
        self.run()

    def search(self):
        print("enter search...")
        search = input()
        results = self.d.search(search, type='master')
        print("found {} results:".format(len(results)))
        for i, result in enumerate(results):
            print("{}. {}".format(i+1, result))
        print('enter number of record you want to add:')
        number = int(input())
        print("you chose {}!".format(results[number-1]))
        self.append_new_line('masters.txt', str(results[number-1].id))
        self.run()

    def append_new_line(self, file_name, text_to_append):
        """Append given text as a new line at the end of file"""
        # Open the file in append & read mode ('a+')
        with open(file_name, "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(text_to_append)

    def upload(self):
        file1 = open('masters.txt', 'r')
        for master_id in file1.readlines():
            print('adding for id = {}'.format(master_id))
            self.versions.add_all_versions(master_id)

