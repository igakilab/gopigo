# 事前学習スケジュールについて
## 土曜日：9:40~12:40@ITセミナー室
- 土曜日については，最初30分程度でその日の全内容を説明し，残りは自習というスタンスで進める．
- 4/14,4/21:Assemble Gopigo and Run
- 5/12:Image Processing
- 5/26: Vision System
- 6/16: 予備日

## 水曜日：13:30~17:00@ITセミナー室
- 水曜日に関しては，都度学生の出席希望状況を確認して，開講/不開講を決定する．
- 基本的にはSA＋空いている教員で自習的に実施する
- 4/25,5/9
- 5/16,5/23
- 6/6,6/13

## 事前学習におけるSA実施内容
土曜 or 水曜に来てもらい，学生のフォロー及び事前学習内容の確認・実施及びWindows PCの設定をしてもらう．
水曜日については鍵の開け締め（IS科事務室）をしてもらいたいができるかどうか要確認．
8台分のGopigoは参加学生にAssembleしてもらえるが，残り3台分新品があるため，SAらに組み立ててもらう必要あり．そのまま貸与して事前学習中に習熟して貰う予定．

# 教員による準備
## PC
- eclipse,jdkのインストール
- vision systemフォルダのコピー
- Ultra VNCのインストール
- scpクライアント（gopigo-pc間のファイル受け渡し用．なくても良いかも）
- MS Office(最終プレゼン用)

## Gopigo SDカード
- 参考： https://www.dexterindustries.com/howto/install-raspbian-for-robots-image-on-an-sd-card/
- Raspbian for RobotsをDLする)(2017/10月のものをソースフォージから落とした)
- GoPiGoのSDカードをPCのUSBにさし，Etcherを利用してDLしたRaspbian for RobotsのzipファイルをSDにインストールする．
- 有線LAN
  - 192.168.0.2 固定 (255.255.255.0)
- Wifiセットアップ
  - 内蔵Wifiをkillし，Dexterのwifiドングルのほうのみactiveにしておく
- WiFi接続後，DI Software Updateを実行．下記をやってから再起動．
  - Update Dexter 
    - License系はqで抜けて
    - updateするか残すかの質問（デフォルトはNo）についてはNoとしておく
  - Update Robot(Gopigo3)
    - Software update後にUpdate Robotしておいたほうがいいかも(ファームのバージョンが1になる）
- aptのupgradeとupdate(これも最初にやっておくべき)
  - ``sudo apt-get upgrade``
  - ``sudo apt-get update``
- 時計の同期がおかしいので修正
  - https://www.raspberrypi.org/forums/viewtopic.php?t=195691
   - これを参考にtimedatectlの設定を変更してみたが・・．なんか3時間くらいずれたまま＞＜
   - 何もしなくても同期がちゃんと取れてる場合もあった．謎．
- ラズパイ設定を変更しておく（最初にやっておくべき）
  - ``sudo raspi-config``
  - 起動設定をDesktop Autologinにし，timezoneをAsia/Tokyoにする．あと，Expand filesystemも実施すると容量に余裕ができる
    - Boot Options => Desktop / CLI => Desktop Autologin
    - Advanced Options->Expand Filesystem
- TighgVNC
  - killするかtightに接続した場合とx11に接続した場合で壁紙を変更できれば良い
- x11vncをインストール及びセットアップ
  - https://raspberrypi.akaneiro.jp/archives/463
  - ``sudo apt-get install x11vnc``
  - 自動起動設定と解像度設定もやっておく
  - 自動起動設定``~/.config/autostart/x11vnc.desktop``
```
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=X11VNC
Comment=X11VNC
Exec=x11vnc -usepw -forever
StartupNotify=false
Terminal=false
Hidden=false
```
- /boot/config.txt の framebuffer_width, framebuffer_height で解像度を指定してから再起動．
- x11vncには有線LANの場合はだいたい``169.254.27.204:2``でUltraVNCから接続できた．
- tightvncの永続的な落とし方がわからない＞＜
- geanyのFontの設定は[Edit]->[Preferences]->[Interface]->[Fonts]で変更できる
  - フォントサイズを大きめにしておいたほうが良いかも（ノートPC次第？）
- geanyの設定変更（ビルドコマンドとインデントの設定）
  - ``/home/pi/.config/geany/filedefs/filetypes.python``
  - Working Directryがdefaultでは``/home/pi/Dexter/tmp/`` になっているので修正しておく
    - ``EX_00_WD=/home/pi/Dexter/tmp``を``EX_00_WD=``に変更する
  - indentの設定
    - [indentation]セクションのwidth=4, type=0の各行のコメントアウトを外す
- Pythonライブラリのインストール
  - ``sudo pip install py-getch``
    - 不要かも
  - ``sudo apt-get install python-opencv``
  - Video設定
```
$ cd ~/Desktop/GoPiGo3/Projects/RemoteCameraRobot
$ sudo bash install.sh
```
- リブート
  - これで　/dev/video0 も入るとのこと

## 追加（2018/03/23）
- 固定IP：192.168.0.2
  - https://hombre-nuevo.com/raspberrypi/raspberrypi0017/
  - /etc/dhcpcd.conf 末尾に追記
  - interface eth0
  - static ip_address=192.168.0.2/24
  - PC側有線LANを 192.168.0.3 などに
- 内蔵無線LANを無効
  - https://qiita.com/yyano/items/802da53ad8a4a00d00e1
  - /boot/config.txt に
    - ``#turn wifi and bluetooth off``
    - dtoverlay=pi3-disable-wifi
- TightVNC 自動起動無効化
  - https://qiita.com/a_yasui/items/f2d8b57aa616e523ede4
  - sudo systemctl disable novnc.service
  - （sudo systemctl enable novnc.service で戻せる）
- v4l2 ドライバ有効化．uv4l2 ではWaterMarkが入る問題
  - https://qiita.com/rukihena/items/95da3860f9ca86c39f8d
  - /etc/modules に bcm2835-v4l2 を追記
  - /boot/config.txt の編集の必要はなさそう．
- emacs のウィンドウ分割防止
  - emacs -nw ~/.emacs.d/init.el で内容は
  - (setq inhibit-startup-message t)


# 実施内容
## Gopigo Setup
- 組み立てる
  - カメラの設置
  - USBケーブルの接続
  - 電池の充電
- 設定
  - vnc関連の設定，ultravncの接続
  - 有線での接続と無線での接続

## Run Gopigo
- main関数の利用
- API http://gopigo3.readthedocs.io/en/master/api-basic.html#easygopigo3
- run10cm.pyを動かす
  - geanyの使い方
- set_speed():0~500 (実際の上限は1000だが，このPBLでは500を上限とする)
- forward.py(速度5程度)を動かし，そのあとstop.pyを動かす
- blocking method/non-blocking method
  - blocking/non-blokingの説明を行う
  - run10cm.py + turn_degrees(blocking)
  - forward + sleep + right + sleep + stop
- non-blocking key input(curses)
  - up down right left
  - wasd+reset_encoders()+read_encoders()+target_reached()
- python class implementation
  - gopigo control class
    - 一定距離直進，180度左に回転，一定距離直進
    - 一定距離直進，90度右に回転，一定距離直進，135度右に回転，一定距離直進
    - すべてblockingで実装
  - gopigo control + status class
    - すべてnon-blockingで実装
    - forward, back,stop
    - status.flg=1,status.encoder=[],checkはencoderの値に到達するとflgを加算する．moveメソッドはstatus.flgが1の間は直進し，2になると後進，3になると停止する．
    - 一定距離直進，90度右に回転，一定距離直進，135度右に回転，一定距離直進 をnon-blockingで実装する

## Image Processing
- cv_control class, capture streamをする方向で検討
  - continuous captureは辞めたほうが良いかも
- opencv00.py
  - 何か表示する
  - numpyの説明
  - waitKeyの説明
- opencv01.py
  - picamera api https://picamera.readthedocs.io/en/release-1.10/recipes1.html
  - captureして表示
  - 最低限のcamera初期化
- opencv02.py
  - cv_controlクラスの作成
  - capture_frame, detect_colorの追加
  - detect skin regionの説明
    - BGR2HSV
- opencv03.py
  - detect contourの追加
  - detect contours of skin color region
- opencv04.py
  - detect center and the size for each contour
- opencv05.py
  - 一定サイズ以上のskin colorがcaptureされたときにその画像を保存する
  - gpicviewの使い方
- configure pi camera
  - awbとかagとかの設定について説明する
- color_picker
- 青とか緑でcolor_detect
- 一定サイズ以上の青画像を保存
- 一定位置で一定サイズ以上の緑画像を保存
- 青と緑両方について，中心点が一定位置で一定サイズ以上の画像に青あるいは緑の名前をつけて保存する

## opencv+gopigo
- gopigo_controlとcv_controlクラスを作成する
- keycontrolで移動し，pでキャプチャして保存する
  - cv2.waitkey版
- keycontrolで移動し，青画像が見つかったら自動的に保存する
- 青画像の中心がgopigoの正面に来るように回転する
  - status利用．右・左のどちらかをチェックし，statusのflgflg(l/r/s)に代入．flgの内容にもとづいて回転．定期的に中心座標をチェックし，一定の範囲に入るとflgをsにし，gopigoもstopする

## Vision System
- socket clientのサンプル実装
- https://torina.top/detail/253/
  - multithread clientの実装
- vs_and_gocv01.py
  - vs_controlクラスの追加
  - vs文字列のparse処理
  - Vision Systemとopencvの連携
  - captureして画像表示+座標情報の表示
- vs_and_gocv02.py
  - targetマーカーの向きを向かせる
  - statusクラスを利用する．flg=l/r/s, checkはgopigoの向きと2点間の向きが一致したらsにする
    - 指定した角度だけ回転させて停止するプログラムができないか検討する．多分blockingで呼び出して，呼び出した瞬間にflgをs(あるいは0)にして，終了時に別のフラグをたてるようにしたらいける気がする
- vs_and_gocv03.py
  - 座標を指定すると，そちらを向いてから移動するプログラムを作成する
- vs_and_gocv04.py
  - 座標を指定すると，一度そこに移動してからスタート位置（vs-Markerあり）に戻ってくるプログラムを作成する
- vs_and_gocv05.py
  - ターゲットマーカーがあり，そこに移動して撮影してからスタート地点に戻ってくるプログラムを作成する．
- vs_and_gocv06.py
  - 05に追加して，撮影したマーカーが特定の評価基準を満たしているかをチェックして，満たしていない場合は満たすように向きを変えて撮影し直してから戻ってくるプログラムを作成する
