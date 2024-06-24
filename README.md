# blind_vote

## Usage

```python
# app.py에 있는 roles, names 수정
roles = ["회장", "부회장", "총무"]
names = [
    "Alice",
    "Bob",
    "Charlie",
]
```

```console
$ pip install -r requirements.txt
$ python create_test_account.py # 테스트 계정 생성 (Optional)
$ python app.py or python app.py --reset-votes
```

## URL

`http://127.0.0.1:5000/login`

`http://127.0.0.1:5000/logout`

`http://127.0.0.1:5000/vote`

`http://127.0.0.1:5000/result`
