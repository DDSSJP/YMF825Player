# YMF825Player

YMF825で曲を演奏するプログラムです。

YMF825ボードと、USBからSPIを出力できるデバイスが、SPIで接続されている環境が必要です。  
開発環境と同じ、または同等の環境であれば動作するはずです。

---------------------------------------------------------
## 動作環境(開発環境)
- Windows10 Pro 64bit 21H2
- Python Version 3.11.1 64bit (追加のライブラリは必要ありません)
- YMF825ボード
  - ウダデンシ YMF825Board http://uda.la/fm/
  - 販売：秋月電子 https://akizukidenshi.com/catalog/g/gM-12414/ (ここで買いました)
  - 販売：スイッチサイエンス https://www.switch-science.com/products/3399 (ここでも買えるみたい)
<br>
<br>
- USBからSPIを出力できるデバイス
  - FTDI FT232H https://www.ftdichip.com/old2020/Products/ICs/FT232H.htm (ICだけ)
    - Adafruit FT232H Breakout https://www.adafruit.com/product/2264 (USB接続できるボード)
    - 販売：秋月電子 https://akizukidenshi.com/catalog/g/gM-08942/ (ここでで買いました)
    - 販売：秋月電子 https://akizukidenshi.com/catalog/g/gK-06503/ (これでも大丈夫なはず)

  SPIデバイスは今のところ `FTD2xx` のみの対応になっています。  

---------------------------------------------------------
## YMF825ボードとSPIデバイスを接続する

YMF825ボードの電源は5Vだけを使用する、かつ、  
SPIデバイスから出力される5V電源を使用する場合の接続方法です。

| pin   | YMF825Board | Adafruit FT232H |
|-------|-------|-----|
| 電源  | 5V    | 5V  |
| GND   | GND   | GND |
| CLOCK | SCK   | D0  |
| MOSI  | MOSI  | D1  |
| MISO  | MISO  | D2  |
| SS    | SS    | D3  |
| RESET | RST_N | D4  |

**ここに図を貼る**

---------------------------------------------------------
## 使用するSPIデバイスを選択する

初めて曲を再生するときは使用するSPIデバイスを選択します。  
以下のようなメッセージが表示されますので、使用するSPIデバイスのindexの番号を入力してください。

情報は `spi_device.json` に保存されます。  
選択をやり直したい場合、環境が変化した場合は `spi_device.json` を削除してください。

```plane
found 1 spi devices.
  index:0  device:FTD2xx  id:FTPVNW8R  detail:{...いろいろ...}

Please input a device index number for you play song. >> 
```

---------------------------------------------------------
## 曲を演奏する

```python
python play.py song.mml
```

`song.mml`はMMLファイルのファイル名を指定してください。  
パスを含めることができます。  
パスの区切り文字はスラッシュ `/` を使用してください。

**今はドレミファソを繰り返すだけです。**

---------------------------------------------------------
## 曲を作る

**まだです**

