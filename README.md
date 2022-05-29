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

## Current implementation did not consider…

- Security. No authentication. No password.
- Possible needs to delete users or videos. You’ll need to do that manually.
- Performance. No `async` appeared. Used `sqlite`.