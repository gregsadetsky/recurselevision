# THIS IS NOT THE REPO YOU ARE LOOKING FOR.

[Go here ---------->>>>>>>>>>>>>>>>>>>>>>>>>](https://github.com/gregsadetsky/rctv)

thank you.

---

## what is this

an IRL tv dashboard at the [Recurse Center](https://recurse.com/) with "tv apps" to bridge the physical-virtual schism

### hardware BOM

- a raspi
- a television

### TODO

- see [here](./TODO.md)!

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
- site is automatically deployed upon git pushing to this repo
