## Herokuアプリケーションの作り方

1. Herokuアプリケーションを作成
```
$ heroku create <app-name>
```

2. リモートリポジトリの追加 & push
```
$ heroku git:remote -a <app-name>
$ git push heroku main
```

3. 環境変数の設定
```
$ heroku config:set ENV_VAR=VALUE
# heroku config:unset ENV_VARで設定削除
```

4. Herokuアプリケーションサーバへ接続
```
$ heroku run bash --app <app-name>
```

5. Herokuアプリケーションのログをtail
```
$ heroku logs --tail --app <app-name>
```

6. Herokuアプリケーションを再起動
```
$ heroku restart --app <app-name>
```

