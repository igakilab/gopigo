## はじめに
- 国際PBLの単位は30時間以上のサポート実態があれば認められます．
- 事前学習期間(4/14~6/16)，PBLweek(6/18~23)両方に参加し，ロボット開発，開発指導，異文化交流の経験を積んでいってください．

# スケジュール
## 土曜日：9:40~12:40@知能情報システム研究センター(6F演習室手前)
- 土曜日については，最初30分程度でその日の全内容を説明し，残りは自習というスタンスで進める．
- 4/14,4/21:Assemble Gopigo and Run
- 5/12:Image Processing
- 5/26: Vision System
- 6/16: 予備日

## 水曜日：13:30~17:00@知能情報システム研究センター(6F演習室手前)
- 水曜日に関しては， 基本的にはTA＋空いている教員で対応する．
- 自習なので原則としては参加学生の自主性に任せる
- 必要な準備等もこの時間帯に行う予定
- 4/25,5/9
- 5/16,5/23
- 6/6,6/13

# 器材管理
- Gopigo+PiCamera+金具
  - HRC:12
- 単3充電池
  - HRC:
- 充電器
  - HRC:12
- エネロイド充電器
  - HRC:4(予定)
- 無線LANルータ＋ACアダプタ
  - HRC:1
- マルチタップ
  - 知能センターのものを利用する
- カッターマット
  - 鎌倉研:A2 1枚
- カッターナイフ
  - IS科事務:1
  - 井垣研:1
  - HRC:1
- はさみ
  - 井垣研:1
  - HRC:1
- 定規
  - 金属定規 HRC:1
  - アクリル定規 IS科 :2
- ノートPC
  - HRC:9
  - 鎌倉研:5
- オートポール
  - HRC:8+2追加予定
  - 西口研:?
- オートポールクランプ
  - 西口研:12
- USB-Webカメラ(Logicool 920C)
  - 鎌倉研:10
- USB-Webカメラ固定具（アングルと固定するやつ）
  - HRC:10予定
- USB-Webカメラ延長ケーブル(5m)
  - HRC:10予定
- アングル
  - HRC:5予定
- 付箋（井垣研からそれなりの量）
- テプラ：IS科事務室
- USBメモリ
  - IS基礎:2
- SDカードリーダー
  - HRC:2

# SA実施タスク
## 概要
- 鍵の開閉．4/21以降，教員が各回の主/副リーダーを決めます．リーダーは鍵の開閉や参加学生，TA全体の出欠管理をお願いします．
- gopigo開発．4/14以降，2~3人一組でPBL参加学生と同じロボ開発を参加学生よりも先回りしてやってもらいます．資料の不備等がないかを確認してもらうことと参加学生からの質問に対応できるようになってもらうことが目的です．
- gopigo開発のための環境設定．SDカードのコピーやWindows PCの各種セットアップ等．
- ゲームフィールド作成．PBL本番では，ロボットによる対戦ゲームが行われます．そこで必要となるいくつかの小物等を開発して貰う予定です．
- 学生対応．質問対応や進捗管理（進捗管理は事前学習時のみでOK）等のフォローをしてあげてください．
  - 特に自習時等で1人で取り組もうとしている参加学生がいた場合は，できる限りサポートについてあげてください．

## 主/副リーダーのタスク
- 鍵の開閉．事前学習土曜日の鍵の開閉は教員がやりますが，水曜日（自習日）のリーダーの人は1F防災センターに行って，知能情報システム研究センター（旧ITセミナー室）の鍵（部屋後方扉）を借りて13:30~17:00までいるようにしてください．
- 以下のシートを開き，参加学生，TAの出欠（o,連絡なしx,連絡ありx）を書いておいてください．
  - https://docs.google.com/spreadsheets/d/1E-czYvc6KT6kiTASxVSMuYIYfNHYy3kQCB5nJWzyoCc/edit#gid=0

## テプラ **(4/14)**
- gopigo, ノートPC等の小物にどこの研究室から来たものかを示すテプラシールを作成し，貼り付ける

## gopigo SDカードセットアップ **(4/14)**
- USBメモリに入っているEtcher-Setup-....exeファイルをTA用PC（あるいは空きPC）にインストールし，下記URLに従って，同じくUSBメモリに入っている`180331_Raspbian_custom.img`というOSイメージをgopigoに付随するSDカードにコピーしていく
  - https://www.dexterindustries.com/howto/install-raspbian-for-robots-image-on-an-sd-card/
- 自分のPCにアプリがインストールされるのが嫌な場合は↓のツールでもイメージをコピーできる
  - WinDD http://www.si-linux.co.jp/techinfo/index.php?DD%20for%20Windows
  - こちらはレジストリをいじらないので，イメージのコピーが終わったらフォルダごと消せばOK．

## 学生WindowsPCセットアップ **(4/14)**
- ログインID：admin/passなし(HRCノートPC)，Satlab/satlab(鎌倉研ノートPC)
  - 各種インストールに管理者権限が必要
  - 両方とも授業開始前にpbl18アカウントに統一するかも
- 必要であればWindows Updateを行う．
- 有線LANのネットワーク設定を行う．**(4/14)**
  - IPv4:192.168.0.10, ネットマスク:255.255.255.0
  - 参考：http://faq.buffalo.jp/app/answers/detail/a_id/15775
- 無線LANの接続設定を行う **(4/14)**
  - HRC無線LANルータの設定を確認する
- eclipse, UltraVNC, RLogin, MS Officeを学生が利用するWindows PCにセットアップする
  - 各インストーラをコピーしたUSBメモリを渡すので，学生PCにコピーしていくこと
  - 4/14時点では利用されているノートPCについてはファイルのコピーとUltraVNCのセットアップのみ行う．残りのソフトについては水曜日に空いているPCから順に実施していくこと．
    - 裏で5台程度最低限のセットアップ(ultravncのみインストールするとか)を行っておき，途中で交換するのでも良いかも．
  - UltraVNC_1_2_...Setup.exe インストール（クライアントが使えればOK）
  - eclipse
    - eclipse.zipをc:\に解凍する（`c:\eclipse\eclipse.exe`となるように解凍する）
    - JDK8のjreフォルダをc:\eclipseにコピー済み
    - vision systeのために， ``dsj.dll`` を ``C:\eclipse\jre\bin`` にコピー済み
  - RLogin
    - `c:\RLogin\Rlogin.exe` になるように配置する
  - sakura_install....exe インストール
  - Office2016インストール
    - Word/Excel/Powerpoint
    - ライセンス認証(PDF参照)
- Windowsの表示を英語にする
  - https://support.microsoft.com/ja-jp/help/4027670/windows-add-and-switch-input-and-display-language-preferences-in-windo
- Officeの表示を英語にする
  - https://www.capa.co.jp/archives/8998
- Logicool Webカメラのドライバとユーティリティをインストールし，フォーカスの変更（無限遠）ができることを確認する．
- vision systemのセットアップ
  - 細かいパラメータの確認（今後実施予定）を行ってから，zipを作成し，学生環境にコピーする予定
  - ダウンロードフォルダにvision system.zipを置いておく

## gopigo開発
- 開発されたgopigoのどこかにテプラか何かで番号を貼り付ける．
- 以下のページから3つの教材ページに飛べます(事前に確認したGoogleアカウントにログインすること)．こちらを見て，予備のgopigoを使って実際に演習ができるかを，学部生より早く確認してください．教材不備等についてはslackの#roskobuki あたりで言ってもらえれば修正します．
  - https://sites.google.com/site/ipbloit/private/2018

## ゲームフィールド等作成
### 有線LANケーブル **(4/14)**
- @Hiroto KAJIHARA @Misaka Kento @shotaro_ishigami @masaya_suetomi の4名は4/14の早い段階でLANケーブルを作成(長さ5m*10本)をお願いします(各種機材は奥野先生手配)

### vs-marker作成(40枚)
- vs-marker(vision systemで撮影し，vs-markerが貼られたロボット等の位置情報を特定するためのマーカー)をA4に印刷した紙を持っていくので，それをハサミやカッターで切り離し，両面テープで白プラダンに貼り付ける
  - 貼り付ける前にvs-markerと同じサイズ(12cm*12cm)になるように白プラダンを切っておくこと
- gopigoにvs-markerをマジックテープで貼り付けられるようにする

### Target作成(15セット)
- gopigoがカメラで撮影するターゲット
- 40 * 45の白プラダン
- 10 * 15の緑 or 青 or 黃プラダン
- 床から20cm程度のところに置けるよう発泡スチロールの台を固定する

### Guard作成(10枚)
- gopigo前面に両面テープ or マジックテープで貼り付ける赤プラダン
- サイズ:20cm*30cm
- ↓こんな感じで貼り付けるので，PiカメラとLANケーブルに干渉しないように貼り付ける
  - LANケーブルの可動範囲を見てプラダンの切り方を考える

<a href="https://sites.google.com/site/ipbloit/private/2018/ta/guard1.jpg"><img src="/site/ipbloit/private/2018/ta/guard1.jpg" border="0" width="200"></a><a href="https://sites.google.com/site/ipbloit/private/2018/ta/guard2.jpg"><img src="/site/ipbloit/private/2018/ta/guard2.jpg" border="0" width="200"></a>

### オートポール，Webカメラ設置テスト
- オートポール，クランプ，アングル，USB-Webカメラ，延長ケーブル，Webカメラ固定具を設置し，vision systemで動かしてテストする
- テスト項目
  - フィールドサイズ150cm*250cmが確保できるか
  - Targetをどこまでフィールド外に配置できるか
  - vision systemのパラメータ確認(vs-markerの認識が安定しそうな値をさぐる)
