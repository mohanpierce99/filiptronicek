import requests
from os import getenv
import datetime
from dotenv import load_dotenv

from modify import write

load_dotenv()

user = "filiptronicek"
repo = "filiptronicek.github.io"

url = "https://api.github.com/repos/{}/{}/git/trees/master?recursive=1".format(user, repo)
headers = {'Authorization': getenv("TOKEN")}
r = requests.get(url, headers=headers)
res = r.json()

posts = []

for file in res["tree"]:
    if "_posts/" in file["path"]:
        fileNm = file["path"].split("/")[-1]
        dateStr = fileNm[:10]
        date_time_obj = datetime.datetime.strptime(dateStr, "%Y-%M-%d")
        fmtTime = date_time_obj.strftime("%B %d, %Y")
        flUrl = f"https://raw.githubusercontent.com/filiptronicek/filiptronicek.github.io/master/_posts/{fileNm}"
        flReq = requests.get(flUrl).text
        if "title" in flReq.strip().split("\n")[1]:
            title = flReq.strip().split("\n")[1]
        elif "title" in flReq.strip().split("\n")[2]:
            title = flReq.strip().split("\n")[2]
        else:
            title = fileNm
        blogUrl = f"https://blog.trnck.dev/{fileNm[11:].replace('.md','/')}"
        posts.append({"time": fmtTime, "title": title, "url": blogUrl})
write(posts[-1]["title"],posts[-1]["url"], posts[-1]["time"])