import tkinter

from bs4 import BeautifulSoup
import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def is_valid_url(url1):
    if (url1 is None or len(url1) < 2 or url1.find('.php') != -1 or url1.find('javascript') != -1
            or url1.find('#') != -1 or url1.find('.jpg') != -1 or url1.find('.mp3') != -1):
        return 0
    else:
        return 1


def refine_str(str):
    global start_page
    if is_valid_url(str) == 0:
        return '0'
    if str.find('http:') != -1 or str.find('https:') != -1:
        pass
    else:
        if str.find(start_page) != -1:
            pass
        else:
            return start_page + str
    return str


def start_analysis():
    global start_page
    start_page = site_page.get()
    links_with_text = []
    links_count = 0

    soup = BeautifulSoup(requests.get(start_page).content, "html.parser")

    for line in soup.find_all('a'):
        href = line.get('href')
        links_with_text.append([start_page, href])

    for iteration in range(3):
        for i in range(links_count, len(links_with_text)):
            limit = 3
            if not refine_str(links_with_text[i][1]).__eq__("0"):
                soup = BeautifulSoup(requests.get(refine_str(links_with_text[i][1])).content, "html.parser")

                count = 0
                for line in soup.find_all('a'):
                    if count < limit:
                        href = line.get('href')
                        if not href is None:
                            links_with_text.append([refine_str(links_with_text[i][1]), href])
                            count += 1

                print(links_with_text)
            links_count += 1

    df = pd.DataFrame(links_with_text, columns=["from", "to"])
    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph(length=50))
    ranks = dict(sorted(nx.pagerank(G).items(), key=lambda item: item[1], reverse=True))
    most_ranked_pages_string = ''
    for page in list(ranks.items())[:10]:
        most_ranked_pages_string += str(page)[1:-1] + "\n"
    most_ranked_pages_label.config(text=most_ranked_pages_string)
    print(list(ranks.items())[:10])
    d = dict(G.degree)
    nx.draw(G, with_labels=False, node_size=[d[k] * 10 for k in d], node_color="red", alpha=0.4, arrows=True, pos=nx.spring_layout(G))
    plt.show()


master = tkinter.Tk()
start_page = ''
tkinter.Label(master, text='Enter a site').grid(row=0, column=0)
most_ranked_pages_label = tkinter.Label(master)
most_ranked_pages_label.grid(row=1, column=1)
site_page = tkinter.Entry(master, width=50)
site_page.grid(row=0, column=1)
button_for_analyzing = tkinter.Button(master, text='Start', command=start_analysis)
button_for_analyzing.grid(row=0, column=2)

master.mainloop()
