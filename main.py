import re
import requests
from bs4 import BeautifulSoup # pip3 install bs4

def main():
    # Inputs >>>
    InputPath = "./urls" # FilePath for Input
    OutputPath = "./output.txt" # FilePath for Output
    # <<< Inputs
    with open(InputPath, "r") as f:
        urls = re.split("\n", str(f.read()))
    # if there is an empty line
    if urls[-1] == "":
        del urls[-1]
    for url in urls:
        try:
            res = requests.get(url)
            print("[ info ] Response:", res.status_code)
            soup = BeautifulSoup(res.content, "html.parser")
            inputs = soup.find_all("input") # Collect all inputs in html
            # save input {name}, {value} in json inside array
            target = []
            print("[ OK ] Url vaild")
            for input in inputs:
                try:
                    params = "?" + input["name"] + "=" + input["value"] + "&"
                    target.append(params)
                except: pass
            target = res.url + "".join(target)[:-1] # Put all params together and ( [:-1] is for delete & from the end of url)
            print("[ OK ]", len(inputs), "Inputs detected")
            # Print to Output File
            try:
                with open(OutputPath, "a"):
                    f.writelines(target)
                print(f"[ OK ] Wrote to {OutputPath}")
            except: print(f"[ ! ] Can`t write to {OutputPath}")
        except Exception as e: print(f"[ ! ]", e)
        print("#"*20)
main()
