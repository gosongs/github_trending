python 抓取 github trending

## Dev
安装 `requests` 和 `pyquery`.

```bash
pip install requests pyquery
```

```bash
git clone https://github.com/gosongs/github_trending.git
cd github_trending
pip install -r requirements.txt
python start.py
```

注意: 默认会抓取所有语言的趋势, 可以通过修改 `LANG_LIST` 变量只抓取自己喜欢的.

