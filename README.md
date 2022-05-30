# video-api

Built with `FastAPI` and `cornac`.

## How to run (for development)

My environment is Python 3.9.

```powershell
pip install fastapi[all]
pip install cornac
```

You can also use `conda` to install these.

And then, open the terminal, enter the folder of this project and run

```powershell
uvicorn main:app --reload
```

Now open http://127.0.0.1:8000/docs in your browser.

## How to add a video

Send a POST request to http://127.0.0.1:8000/add_video/ with the body

```json
{
  "title": "yurucamp movie",
  "cover": "https://i.vgy.me/PfcUgS.jpg", // Upload the cover to a image hosting site
  "url": "https://streamable.com/75b8hw", // Upload the video to a video hosting site
  "length_str": "1:23", // Please calculate that manually
  "category": "yuri"
}
```

You can write a script to do these automatically.

## Current implementation did not consider…

- Security. No authentication. No password.
- Possible needs to delete users or videos. You’ll need to do that manually.
- Performance. No `async` appeared. Used `sqlite`.
