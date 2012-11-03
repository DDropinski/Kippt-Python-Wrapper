import json
import ast
import requests
import sys

# python 2/3 mismatch, no workaround
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

class User:
    # Example:
    # client = kippt_wrapper.User('myUsername','kjsdfklj2lhg323423klj42')
    def __init__(self, Username, apitoken):
        self.Username = Username
        self.apitoken = apitoken
        self.header = {'X-Kippt-Username': Username,
                       'X-Kippt-API-Token': apitoken,
                       'X-Kippt-Client': 'Kippt-Python-Wrapper,me@ThomasBiddle.com,https://github.com/thomasbiddle/Kippt-Projects',
                       'content-type': 'application/vnd.kippt.20120609+json'}

    # Check if our credentials are valid.
    # Example:
    # User.check_auth()
    #
    # Return True on success and False on failure.
    def check_auth(self):
        r = requests.get('https://kippt.com/api/account/', headers=self.header)
        if r.status_code is 200:
            return True
        else:
            return False

    # Get our lists.
    # Example:
    # meta, lists = User.get_lists(offset = 5)
    # meta, lists = User.get_lists(50, 5) # (limit, offset)
    # meta, lists = User.get_lists()
    # x = meta['total_count']
    # for i in lists: print i['title'] ( Returns Python list of Kippt Lists )
    #
    # Available values in meta:
    # total_count, limit, offset
    # Available values in each list:
    # rss_url, updated, title, created, slug, id, resource_uri
    #
    # Returns data on success, and false on failure.
    def get_lists(self, limit = 0, offset = 0):
        url = 'https://kippt.com/api/lists?limit=' + str(limit) + '&offset=' + str(offset)
        r = requests.get(url, headers=self.header)
        if r.status_code is 200:
            return r.json['meta'], r.json['objects']
        else:
            return False, False

    # Get a list.
    # Example:
    # myList = User.get_list(54433)
    # x = myList['title']
    #
    # Available values in list:
    # rss_url, updated, title, created, slug, id, resource_uri
    #
    # Returns data on success, and false on failure.
    def get_list(self, id):
        r = requests.get('https://kippt.com/api/lists/' + str(id), headers=self.header)
        if r.status_code is 200:
            return r.json
        else:
            return False

    # Get list collaborators
    # Example:
    # myCollabs = User.get_list_collab(54433)
    # for i in myCollabs: print i['Username']
    #
    # Available values in list:
    # Username, avatar_url, id, resource_uri
    #
    # Returns data on success, and false on failure.
    def get_list_collab(self, id):
        r = requests.get('https://kippt.com/api/lists/' + str(id) + '/collaborators', headers=self.header)
        if r.status_code is 200:
            return r.json
        else:
            return False

    # Get our clips.
    # Example:
    # myClips = User.get_clips()
    # myClips = User.get_clips(54332, 20, 5) # (listID, limit, offset)
    # myClips = User.get_clips(limit = 20)
    #
    # Available values in meta:
    # total_count, limit, offset
    # Available values in clip:
    # id, url, title, list, notes, is_starred, url_domain, created, updated, resource_uri
    #
    # Returns data on success, and false on failure.
    def get_clips(self, listID = None, limit = 0, offset = 0):
        params = { "limit": str(limit),
                   "offset": str(offset) }
        url = 'https://kippt.com/api/clips?limit={limit}&offset={offset}'.format(**params)
        if not listID is None:
            url = url + '&list=' + str(listID)
        r = requests.get(url, headers=self.header)
        if r.status_code is 200:
            return r.json['meta'], r.json['objects']
        else:
            return False, False

    # Get a clip.
    # Example:
    # myClip = User.get_clip(2027593)
    # x = myClip['title']
    #
    # Available values in clip:
    # id, url, title, list, notes, is_starred, url_domain, created, updated, resource_uri
    #
    # Returns data on success, and false on failure.
    def get_clip(self, id):
        r = requests.get('https://kippt.com/api/clips/' + str(id), headers=self.header)
        if r.status_code is 200:
            return r.json
        else:
            return False

    # Search for a query.
    # Example:
    # mySearch = User.search("Programming")
    #
    # Available values in meta:
    # total_count, limit, offset
    # Available values in clip:
    # id, url, title, list, notes, is_starred, url_domain, created, updated, resource_uri
    #
    # Returns data on success, and false on failure.
    def search(self, query, limit = 0, offset = 0):
        query = quote_plus(query)
        params = { "query": query,
                    "limit": str(limit),
                    "offset": str(offset)
        }
        r = requests.get('https://kippt.com/api/search/clips/?q={query}&limit={limit}&offset={offset}'.format(**params),
                        headers=self.header)
        if r.status_code is 200:
            return r.json['meta'], r.json['objects']
        else:
            return False, False

    # Create a list.
    # Examples:
    # User.create_list('My New List!')
    #
    # Will return data on success and False on failure.
    def create_list(self, name):
        clipdata = {'title': name}
        r = requests.post('https://kippt.com/api/lists/', data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 201:
            return r.json
        else:
            return False

    # Add a clip.
    # Examples:
    # User.add_clip('www.kippt.com')
    # User.add_clip('www.kippt.com',title="My Title!")
    # User.add_clip('www.kippt.com',1234,starred="true",notes='My Notes!')
    #
    # Will return data on success and False on failure.
    def add_clip(self, url, listID=0, title = None, starred = None, notes = None, ):
        clipdata = {'url': url, 'list': '/api/lists/' + str(listID)}
        if not title is None:
            clipdata['title'] = title
        if not starred is None:
            clipdata['is_starred'] = starred
        if not notes is None:
            clipdata['notes'] = notes
        r = requests.post('https://kippt.com/api/clips/', data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 201:
            return r.json
        else:
            return False

    # Create a list.
    # Examples:
    # newList = User.create_list('Programming')
    # print newList
    def create_list(self, name):
        clipdata = {'title': name}
        r = requests.post('https://kippt.com/api/lists/', data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 201:
            return r.json
        else:
            return False

    # Delete a clip ( Only clip owners can modify or delete clips, not collaborators! )
    # Examples:
    # User.delete_clip(2028643)
    #
    # Will return True on success, and False on failure
    def delete_clip(self, id):
        r = requests.delete('https://kippt.com/api/clips/' + str(id), headers=self.header)
        if r.status_code is 204:
            return True
        else:
            return False

    # Delete a List
    # Examples:
    # User.delete_list(54433)
    #
    # Will return True on success, and False on failure
    def delete_list(self, id):
        r = requests.delete('https://kippt.com/api/lists/' + str(id), headers=self.header)
        if r.status_code is 204:
            return True
        else:
            return False

    # Update a Clip ( Only clip owners can modify or delete clips, not collaborators! )
    # Example:
    # pyRespUpdate_clip(id=2027593, list_uri='/api/lists/55284/')
    #
    # Returns True on success, False on failure.
    def update_clip(self, id, title = None, notes = None, listID = None, starred = None):
        clipdata = {}
        if not title is None:
            clipdata['title'] = title
        if not notes is None:
            clipdata['notes'] = notes
        if not starred is None:
            clipdata['is_starred'] = starred
        if not listID is None:
            clipdata['list'] = '/api/lists/55284/' + listID
        r = requests.put('https://kippt.com/api/clips/' + str(id), data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 200:
            return True
        else:
            return False

    # Updating List ( With Python Requests )
    # Example:
    # client.update_list(55284, title="New Title!")
    #
    # Returns True on success, False on failure.
    def update_list(self, id, title = None):
        clipdata = {}
        if not title is None:
            clipdata['title'] = title
        r = requests.put('https://kippt.com/api/lists/' + str(id), data=json.dumps(clipdata), headers=self.header)
        if r.status_code is 200:
            return True
        else:
            return False

