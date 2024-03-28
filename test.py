import requests
from typing import List


def get_post(p_id:str) -> dict:
    
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{p_id}", timeout=10)
    return response.json()


def get_post_comments(post_:dict):
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post['id']}/comments", timeout=10)
    r: List[dict] = response.json()
    
    post_['comments'] = r
    


if __name__ == "__main__":
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)

    x:dict = response.json()
    
    
    post = get_post(1)
    get_post_comments(post)
    print(post['comments'])
    
    
    