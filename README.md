# WindowsServiceExample
pywin32によるWindowsサービスアプリケーションのひな形です。

* Python Version:  3.7.4
* pywin32 Version: 224

pywin32のインストール後、以下のパスをシステムの環境変数「PATH」に追加します。パス中のAdministratorの部分は適宜書き換えて下さい。
~~~
C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages\win32
C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages\pywin32_system32
~~~

インストール ※サービスのアカウントとパスワードを --username, --password で指定
>python WindowsServiceExample.py --startup=auto --username .\Administrator --password admin-pass install

スタート
>python WindowsServiceExample.py start

ストップ
>python WindowsServiceExample.py stop

アンインストール
>python WindowsServiceExample.py remove
