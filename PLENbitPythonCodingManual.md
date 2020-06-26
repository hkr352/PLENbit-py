# PLENbit Python Coding Manual

19/12/09

## Let's coding !!

## 環境構築

- 1.micro:bitのPythonでのプログラミングには 「Mu」というエディターを使います。
まずはこれをインターネットからダウンロードしてインストールしましょう
- 2.URLにアクセス
https://codewith.mu/

- 3.[Download] ボタンをクリック  
お使いのOSのダウンロードボタンを選択  
Windowsの場合は [32-bit] or [64-bit] ボタン

- 4.ボタンをクリックするとインストーラーのダウンロードが始まります。  
ダウンロードができたらインストーラーを起動します。   
インストールします。
- 5.アプリ一覧からMuのアイコンをクリックして起動してください。
- 6.起動すると、モード選択メニューがでます。
- 7.[BBC micro:bit]を選択してください。

参考URL
https://sanuki-tech.net/micro-bit/micropython/install-mu-editor/

## PCのセキュリティーにより、インストールできない場合

オンラインのPythonエディターもあります。  
https://python.microbit.org/v/2.0

<div style="page-break-before:always"></div>

##  コーディング！

早速プログラミングしてみましょう。  
文字を入力してプログラミングすることをコーディングといいます。

参考URL
https://microbit-micropython.readthedocs.io/ja/latest/

上記URLサイトにmicro:bitをつかったPythonのサンプルコードがたくさんあります。  
プログラムの基礎の勉強の参考になります。

Muエディタでプログラミング

## 1. Hello, World!

    from microbit import *
    display.scroll("Hello, World!")

- 1.まずは上記のコードをエディタに記入してみましょう。

- 2.micro:bitをPCと接続
  
  接続するとMuのステータスバー（画面内の下部分）に
  「BBC micro:bit デバイスを検出しました。」
  と表示されます。

- 3.プログラムをmicro:bitに転送
 転送ボタンを押してください。
 プログラムが実行されます。

<div style="page-break-before:always"></div>

### ここからはPLEN:bit向けの内容です。

## 2. PLEN:bit

PLEN:bitをつかったmicro:bitのボタンを押すと動くプログラム

    plenbit_firmware.py
    または
    plenbit_firmware

というファイルをMuエディタの「開く」から開いてください。

転送して動かしてみよう。


注目する部分

    while 1:
        if button_a.is_pressed():
            plenbit.motion(int( b"46",16))
        elif button_b.is_pressed():
            plenbit.motion(int( b"29",16))

数字を変えるとモーションが変わるよ。
モーションリストは後述

このプログラムでif文を覚えよう！

<div style="page-break-before:always"></div>

## 3. 目のLEDでLチカ

サンプルコード

    plenbit_firmware_L-chika.py


関数を作ってみよう！

    def L_chika():
        for _val in range(0, 4):
            pin16.write_digital(0)
            sleep(100)
            pin16.write_digital(1)
            sleep(100)

メインループの中を書き換えよう！

    while 1:
        if button_a.is_pressed():
            L_chika()

「while 1:」と書かれている部分がメインループです。


このプログラムでメインループ、関数、for文、sleep文を覚えよう！

<div style="page-break-before:always"></div>

## 4. サーボモータを動かそう

サンプルコード

    plenbit_firmware_Servo.py

サーボモータの動かし方

plenbit.servoWrite(サーボ番号,角度)

左腕を動かすプログラム
Aボタンを押すとサーボモータが動き1秒後また動きます。

    while 1:
        if button_a.is_pressed():
            plenbit.servoWrite(2,90)
            sleep(1000)
            plenbit.servoWrite(2,30)
            sleep(1000)

サーボモータ初期角度

番号:角度

0:100.0, 1:63.0, 2:30.0, 3:60.0, 4:24.0, 5:60.0, 6:100.0, 7:72.0

<div style="page-break-before:always"></div>

## 5. センサを使ったプログラム

サンプルコード

    plenbit_firmware_Sensor.py

加速度センサを使ったプログラム
加速度センサはmicro:bitの中にあるよ
PLEN:bitが倒れると？？？

    while 1:
        gesture = accelerometer.get_y()
        if gesture < 0 :
            display.show(Image.ANGRY)
            plenbit.motion(int( b"29",16))



距離センサを使ったプログラム
Aボタンを押してから動くようにしているよ
距離センサをPLEN:bitの正面から見た時の右側のソケットに差し込もう
PLEN:bitが壁を見つけると？？？

    Lsensor = pin0
    Rsensor = pin2

    while 1:

        if button_a.is_pressed():
            sleep(1000)
            while 1:
                plenbit.motion(int( b"46",16))
                _readAd = Rsensor.read_analog()
                print(_readAd)
                if (_readAd >= 650):
                    display.show(Image.HAPPY)
                    plenbit.motion(int( b"29",16))
                    break

<div style="page-break-before:always"></div>

## HELP

プログラムを転送した時に何かがおかしい時

- micro:bit になにか英文字が流れている
    
    メモリ不足の可能性があります。コードを減らしましょう

- PLEN:bitが動かない

    転送した後、一度USBケーブルをはずし、PLEN:bitの電源を入れ直してみよう。
    動かない場合はバッテリー切れかもしれません。充電してみてください。

- このマニュアルは今後アップデートののち下記URLサイトに掲載予定です。
    
    https://plen.jp/wp/plenbit/#manual

- ご質問等は下記URLから連絡ください
        
    PLENサポート: https://plen.jp/wp/contact/


- PLEN:bitモーションリスト


基本モーション

    Walk Forward = 0x46
    Walk Left Turn = 0x47
    Walk Right Turn = 0x48
    Walk Back = 0x49
    Left step = 0x00
    Forward step = 0x01
    Right step = 0x02
    A hem = 0x03
    Bow = 0x04
    Propose = 0x05
    Hug = 0x06
    Clap = 0x07
    Highfive = 0x08
    Arm PataPata = 0x29

ボックスモーション

    Shake A Box = 0x0a
    Pick Up High = 0x0b
    Pick Up Low = 0x0c
    Receive a Box = 0x0d
    Present a Box = 0x0e
    Pass a Box = 0x0f
    Throw a Box = 0x10
    Put Down High = 0x11
    Put Down Low = 0x12

サッカーモーション

    Defense Left Step = 0x14
    Dribble = 0x15
    Defense Right Step = 0x16
    Left Kick = 0x17
    Long Dribble = 0x18
    Right Kick = 0x19
    Pass To Left = 0x1a
    Pass It To Me = 0x1b
    Pass To Right = 0x1c


ダンスモーション

    Dance Left Step = 0x1e
    Dance Forward Step = 0x1f
    Dance Right Step = 0x20
    Dance Fisnish Pose = 0x21
    Dance Up Down = 0x22
    Wiggle Dance = 0x23
    Dance Back Step = 0x24
    Dance Bow = 0x25
    Twist Dance = 0x26
