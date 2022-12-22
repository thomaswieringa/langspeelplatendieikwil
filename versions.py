import requests
import json


class Versions:

    def __init__(self, key, user):
        self.key = key
        self.user = user
        self.headers = {"Authorization": "Discogs token={}".format(self.key)}

    def all_versions(self, master_id):
        """
        Returns all vinyl versions of a master
        :param master_id: id of the master we want the versions for
        :return: list of the releases
        """
        url = "https://api.discogs.com/masters/{}/versions".format(int(master_id))
        versions = []
        page = 1
        while True:
            response = json.loads(requests.get(url=url,
                                               headers=self.headers,
                                               params={'page': page, 'per_page': 100}).text)
            if len(response['versions']) == 0:
                # filter the versions
                versions_filtered = list(filter(lambda x: 'Vinyl' in x['major_formats'], versions))
                print("found {} versions".format(len(versions_filtered)))
                return versions_filtered
            versions.extend(response['versions'])
            page += 1

    def add_all_versions(self, master_id):
        """
        Adds all versions of a master to the wantlist in discogs
        :param master_id:
        :return:
        """
        all_versions = self.all_versions(master_id)
        for version in all_versions:
            self.add(version['id'])
        print("added all versions to want list")

    def add(self, release_id):
        """
        Adds a release to the wantlist in discogs
        :param release_id:
        :return:
        """
        url = 'https://api.discogs.com/users/{}/wants/{}'.format(self.user, release_id)
        requests.put(url=url, headers=self.headers)
        print("added release")

    def delete_all(self):
        url = 'https://api.discogs.com/users/{}/wants'.format(self.user)
        response = json.loads(requests.get(url=url, headers=self.headers).text)
        for item in response['wants']:
            self.delete(item['id'])
        print("deleted all releases from watchlist")

    def delete(self, release_id):
        url = 'https://api.discogs.com/users/{}/wants/{}'.format(self.user, release_id)
        requests.delete(url=url, headers=self.headers)
