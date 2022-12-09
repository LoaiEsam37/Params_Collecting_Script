import re
import requests
from bs4 import BeautifulSoup # pip3 install bs4

def main():
    # Inputs >>>>>>>>>>
    InputPath = "./input" # FilePath for Input
    OutputPath = "./output" # FilePath for Output
    Show_Info = False # to print Infomation about every process
    Show_Urls = True # to print params to console
    Show_Errors = False # to print errors if errors occuried (This Function won`t stop the code from continue)
    # <<<<<<<<<< Inputs
    with open(InputPath, "r") as f:
        urls = re.split("\n", str(f.read()))
    # if there is an empty line
    if urls[-1] == "":
        del urls[-1]
    for url in urls:
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, "html.parser")
            inputs = soup.findAll("input") # Collect all inputs in html
            a_tags = soup.findAll('a', attrs={'href': re.compile("^http://")}) # Collect all a in html
            forms = soup.findAll('form') # Collect all forms in html
            # collect inputs
            params = []
            for input in inputs:
                try:
                    temp = "?" + input["name"] + "=" + input["value"] + "&"
                    params.append(temp)
                except: pass
            params = "".join(params)[:-1] # Put all params together and ( [:-1] is for delete & from the end of url)
            # collect hyperlinks
            links = []
            for link in a_tags:
                links.append(link['href'])
            # collect forms
            actions = []
            for form in forms:
                actions.append(form["action"])
            # put all together : params => inputs["name", "value"], links => a["href"], actions => forms["action"]
            for action in actions:
                for l in links:
                    try:
                        # l + params
                        if l[len(l)-1:] == "/" or l[len(l)-1:] == "&":
                            DNS1 = l + params
                        else:
                            DNS1 = l + "&" + params
                    except: pass
                    # RegEx >>>>>>>>>>
                    try:
                        # l + action + params
                        if l[len(l)-1:] == "/":
                            DNS2 = l + action[1:] + params
                        elif l[len(l)-1:] == "&":
                            if l[len(l)-2:] == "/":
                                DNS2 = l[:-2] + action + params
                            else:
                                DNS2 = l[:-1] + action + params
                        else:
                            DNS2 = l + action + params
                    except: pass
                    try:
                        # res.url + params
                        if res.url[len(res.url)-1:] == "/" or l[len(l)-1:] == "&":
                            DNS3 = l + params
                        else:
                            DNS3 = l + "&" + params
                    except: pass
                    try:
                        # res.url + action + params
                        if res.url[len(res.url)-1:] == "/":
                            DNS4 = res.url + action[1:] + params
                        elif res.url[len(res.url)-1:] == "&":
                            if res.url[len(res.url)-2:] == "/":
                                DNS4 = res.url[:-2] + action + params
                            else:
                                DNS4 = res.url[:-1] + action + params
                        else:
                            DNS4 = res.url + action + params
                    except: pass
                    # <<<<<<<<<< RegEx
                    # Print to Output File
                    try:
                        with open(OutputPath, "a") as f:
                            try:
                                f.writelines(DNS1)
                                f.writelines("\n")
                            except: pass
                            try:
                                f.writelines(DNS2)
                                f.writelines("\n")
                            except: pass
                            try:
                                f.writelines(DNS3)
                                f.writelines("\n")
                            except: pass
                            try:
                                f.writelines(DNS4)
                                f.writelines("\n")
                            except: pass
                    except Exception as e:
                        if Show_Errors == True:
                            print(f"[ ! ]", e)
                        else:
                            pass
                    if Show_Info == True:
                        print("#"*20)
                        print("[ OK ]", len(inputs), "Inputs detected")
                        print("[ OK ]", len(links), "hyperlinks detected")
                        print("[ OK ]", len(actions), "forms actions detected")
                        print("#"*20)
                    if Show_Urls == True:
                        print(DNS1)
                        print(DNS2)
                        print(DNS3)
                        print(DNS4)
        except Exception as e:
            if Show_Errors == True:
                print(f"[ ! ]", e)
            else:
                pass
main()
