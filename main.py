import requests
import json
import sys

app_id = '35c52a29'
app_key = 'f6468381dcae571d482e848ce2230562'


p = input("Enter your sentence: ")
words = p.split(" ")
wordCount = len(words)
print ("The word count is:", wordCount)




def create_sentence():
    for s in words:
        if s == 'the' or s == 'is':
            sys.stdout.write(s + " ")
        else:
            language = 'en'
            word_id = s
            url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/synonyms;antonyms'
            r = requests.get(url, headers ={'app_id': app_id, 'app_key': app_key})
            if "code {}\n".format(r.status_code) == "404":
                sys.stdout.write(s + " ")
            else:
                r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key}).json()
                json_syn = r['results']
                print("code {}\n".format(r.status_code))
                print("text \n" + r.text)
                print("json \n" + json.dumps(r.json()))
                json_syn1 = json_syn[0]
                json_syn2 = json_syn1["lexicalEntries"]
                json_syn3 = json_syn2[0]
                json_syn4 = json_syn3['entries']
                json_syn5 = json_syn4[0]
                json_syn6 = json_syn5['senses']
                json_syn7 = json_syn6[0]
                json_syn8 = json_syn7['synonyms']
                json_syn9 = json_syn8[0]
                sys.stdout.write(json_syn9['id'] + " ")


create_sentence()

