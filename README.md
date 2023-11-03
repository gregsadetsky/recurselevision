# recurselevision aka RCTV

## how to dev

### install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### run

```bash
uvicorn rctv.main:app --reload
```

## deployment

https://rctv.recurse.com

- hosted on greg's render account
- site is automatically deploye upon git pushing to this repo
