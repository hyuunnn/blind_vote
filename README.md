# blind_vote

## Usage

```python
# app.py에 있는 roles, names 상황에 맞게 수정
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
$ python app.py
RESET_PATH: 76990712f015e30d81488025301dee73874a76e1e5ebdc489fe272684f96
VOTE_STATUS_PATH: 3320f3322e07220984fbb6abfbf8cdb8e8d021b69b2d02a151d70f91614a
VOTE_EXPORT_PATH: c906d3c3e5b75e98e22135ea665a7629d7286270d59c1aa359a1f87b2585
~~~
```

> [!IMPORTANT]
> 관리자만 접속해야 하는 경로는 `app.py` 실행 시 랜덤 값으로 경로가 지정됩니다. 나중에 접속하기 위해 메모해주세요.

## URL

`http://127.0.0.1:5000/login`

`http://127.0.0.1:5000/logout`

`http://127.0.0.1:5000/vote`

`http://127.0.0.1:5000/result`

`http://127.0.0.1:5000/{RESET_PATH}`

`http://127.0.0.1:5000/{VOTE_STATUS_PATH}`

`http://127.0.0.1:5000/{EXPORT_PATH}`
