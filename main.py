import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup # pip3 install bs4
def main():
    # Inputs >>>>>>>>>>
    InputPath = "./urls" # FilePath for Input
    OutputPath = "./output" # FilePath for Output
    Write_To_Output = False # to Write the output to a {OutputPath}
    Show_Info = False # to print Infomation about every process
    Show_Urls = True # to print params to console
    Show_Errors = False # to print errors if errors occuried (This Function won`t stop the code from continue)
    # <<<<<<<<<< Inputs
    with open(InputPath, "r") as f:
        urls = re.split("\n", str(f.read()))
    del InputPath
    for url in urls:
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, "html.parser")
            params = []
            for input in soup.findAll("input"):
                try:
                    params.append("?" + input["name"] + "=" + input["value"] + "&")
                except Exception as e:
                    if Show_Errors == True:
                        print(f"[ ! ]", e)
            if Show_Info == True:
                inputs = params
            params = "".join(params)[:-1]
            if params == "":
                continue
            links = list(map(lambda link: link["href"], soup.findAll('a', attrs={'href': re.compile("^http://")})))
            actions = list(map(lambda form: form["action"], soup.findAll('form')))
            for action in actions:
                for l in links:
                    i = urljoin(action, params)
                    try:
                        # l + params
                        DNS1 = urljoin(l, params)
                        if Show_Urls == True:
                            print(DNS1)
                    except Exception as e:
                        if Show_Errors == True:
                            print(f"[ ! ]", e)
                    try:
                        DNS2 = urljoin(l, i)
                        if Show_Urls == True:
                            print(DNS2)
                    except Exception as e:
                        if Show_Errors == True:
                            print(f"[ ! ]", e)
                    if Write_To_Output == True:
                        try:
                            with open(OutputPath, "a") as f:
                                try:
                                    f.writelines(f"{DNS1}\n")
                                except: pass
                                try:
                                    f.writelines(f"{DNS2}\n")
                                except: pass
                        except Exception as e:
                            if Show_Errors == True:
                                print(f"[ ! ]", e)
                    if Show_Info == True:
                        print(
                        "\n####################\n"+
                        "[ OK ]", len(inputs), "Inputs detected\n"+
                        "[ OK ]", len(links), "hyperlinks detected\n"+
                        "[ OK ]", len(actions), "forms actions detected\n"+
                        "####################\n"
                        )
        except Exception as e:
            if Show_Errors == True:
                print(f"[ ! ]", e)
main()
