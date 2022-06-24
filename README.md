# video-api

Built with `FastAPI` and `cornac`.

## How to run (for development only)

My environment is Python 3.9 so make sure you’ve installed that.

> 1. Go to https://www.python.org/downloads/, find the release version beginning with 3.9 in the “Looking for a specific release” section and click “Download”.
> 2. Scroll down to the “Files” section, click “Windows installer (64-bit)” (if you’re using Windows).

Install the needed Python packages. Open a terminal ([how to open one in Windows](https://www.wikihow.com/Open-Terminal-in-Windows)) and enter:

```bash
pip install fastapi[all]
pip install cornac
```

You can also use `conda` to install these.

And then, open the terminal in the folder of this project and run

> If you’re in Windows: open the folder (like `D:\Downloads\video-api-main`), Shift + Right click, and find “Open window here” or “Open PowerShell window here” or something similar. For our purpose, we don’t need to differentiate between Command Prompt and PowerShell — both of them works.

```bash
uvicorn main:app --reload
```

Now open http://127.0.0.1:8000/docs in your browser.

> I prepared some test data. You can use them by send a GET request to http://127.0.0.1:8000/test/ (and see the response for generated ids — three user ids and three video ids). You can do this through http://127.0.0.1:8000/docs or by `curl`.

## How to add a video

Send a POST request to http://127.0.0.1:8000/add_video/ with the body

> The easiest way is to open http://127.0.0.1:8000/docs in a browser and follow these steps:
>
> ![](https://i.vgy.me/Z6msUN.png)
>
> ![](https://i.vgy.me/9Fe0Lf.png)
>
> ![](https://i.vgy.me/oitfZQ.png)

```json
{
  "title": "yurucamp movie",
  "cover": "https://i.vgy.me/PfcUgS.jpg",
  "url": "https://streamable.com/75b8hw",
  "length_str": "1:23", // Please calculate that manually
  "category": "yuri"
}
```

> Notes: 
>
> 1. Upload the cover to a image hosting site (like [vgy.me](https://vgy.me/)),  to get the URL.
> 2. Upload the video to a video hosting site (like [Streamable](https://streamable.com/)) to get the URL.

You can write a script to do these automatically.

## Current implementation did not consider…

- **CORS was not handled correctly.** That doesn’t matter if you run both `video-api` and `video-site` locally though.
- Security. No authentication. No password.
- Possible needs to delete users or videos. You’ll need to do that manually.
- Performance. No `async` appeared. Used `sqlite`.
