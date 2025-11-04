import tkinter as tk
import threading
try:
    import requests
except Exception:
    requests = None
import html

API_URL = "https://api.chucknorris.io/jokes/random"


def fetch_joke_thread():
    if requests is None:
        joke = "依赖缺失：请先运行 `pip install requests`"
        root.after(0, lambda: finish_update(joke))
        return
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        joke = data.get("value")
        if not joke:
            joke = "未能从 API 获取笑话（格式异常）"
        joke = html.unescape(joke)
    except requests.exceptions.RequestException as e:
        joke = f"请求失败：{e}"
    except Exception as e:
        joke = f"解析失败：{e}"
    root.after(0, lambda: finish_update(joke))


def on_fetch_clicked():
    joke_button.config(state="disabled")
    joke_label.config(text="加载中...")
    threading.Thread(target=fetch_joke_thread, daemon=True).start()


def finish_update(text):
    joke_label.config(text=text)
    joke_button.config(state="normal")


def main():
    global root, joke_label, joke_button
    root = tk.Tk()
    root.title("Chuck Norris Joke Fetcher")

    joke_label = tk.Label(root, text="点击按钮获取 Chuck Norris 笑话", wraplength=400)
    joke_label.pack(padx=20, pady=20)

    joke_button = tk.Button(root, text="获取笑话", command=on_fetch_clicked)
    joke_button.pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
