#ライブラリのインポート
from fileinput import filename
from posixpath import basename
import tkinter as tk
import tkinter.filedialog
import cv2
from PIL import Image, ImageTk
import os
import shutil

#フォーマット変換の関数
def format(image_bgr):
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk  = ImageTk.PhotoImage(image_pil)
    return image_tk

#リサイズ関数
def resize(img):
    size = int(en.get())
    h, w = img.shape[:2]
    cvh = size*h/w
    image_bgr = cv2.resize(img, (size,int(cvh)))
    return image_bgr

def imread(path):
    tmp_dir = os.getcwd()
    # 1. 対象ファイルがあるディレクトリに移動
    if len(path.split("/")) > 1:
        file_dir = "/".join(path.split("/")[:-1])
        os.chdir(file_dir)
    # 2. 対象ファイルの名前を変更
    tmp_name = "tmp_name"
    os.rename(path.split("/")[-1], tmp_name)
    # 3. 対象ファイルを読み取る
    img = cv2.imread(tmp_name , 0)
    # 4. 対象ファイルの名前を戻す
    os.rename(tmp_name, path.split("/")[-1])
    # カレントディレクトリをもとに戻す
    os.chdir(tmp_dir)
    return img


#画像選択、表示する関数
def getfile():
    global image_tk
    global img
    global image_bgr
    global f_paths
    f_paths = tk.filedialog.askopenfilenames(title="ファイル選択", initialdir="ディレクトリを入力", filetypes=[("Image file", ".png .jpg .jpeg")])
    str_file_path = str(f_paths[0])
    #OpenCVで画像を読み込む
    img = imread(str_file_path)
    image_bgr = resize(img)
    image_tk = format(image_bgr)
    canvas.create_image(0, 0, image=image_tk, anchor=tk.NW)

#2値化関数    
def scale(event=None):
    global image_tk
    global image_th
    global th
    th  = val1.get()
    ret, image_th = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)
    image_bgr = resize(image_th)
    image_tk = format(image_bgr)
    canvas.create_image(0, 0, image=image_tk, anchor=tk.NW)

#オリジナル画像表示
def org():
    global image_tk
    image_bgr = resize(img)
    image_tk = format(image_bgr)
    canvas.create_image(0, 0, image=image_tk, anchor=tk.NW)

#画像保存    
def save():
    def imwrite(filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)

            if result:
                with open(filename, mode='w+b') as f:
                    n.tofile(f)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    os.makedirs('bw_figs/', exist_ok=True)
    for f in f_paths:
        fileName = os.path.basename(str(f))
        _img = imread(str(f))
        ret, _image_th = cv2.threshold(_img, th, 255, cv2.THRESH_BINARY)
        imwrite("bw_figs/bw_" + fileName, _image_th)

#ウインドウの作成
root = tk.Tk()
#ウインドウのタイトル
root.title("2値化アプリ")
#ウインドウサイズと位置指定 幅,高さ,x座標,y座標 
root.geometry("800x600+50+50")

#フレームの作成
frame = tk.Frame(root, width=780, height=570, padx=10, pady=10, bg="#D9D9D9")
frame.place(x=10, y=10)

frame_menu = tk.Frame(frame, relief=tk.FLAT, bg="#E6E6E6", bd=2)
frame_menu.place(x=10, y=10, width=150, height=450)

frame_img = tk.Frame(frame, relief=tk.FLAT, bg="#E6E6E6", bd=2)
frame_img.place(x=170, y=10, width=580, height=450)

frame_scale = tk.Frame(frame, relief=tk.FLAT, bg="#E6E6E6", bd=2)
frame_scale.place(x=10, y=480, width=740, height=60)

#テキストボックスの作成
en = tk.Entry(frame_menu)
en.insert(0, int(400))
en.place(x=10, y=80, width = 80)

#ボタン作成
button = tk.Button(frame_menu, text="ファイル選択", command=getfile)
button.place(x=10,y=10)

#Labelの生成
l = tk.Label(frame_menu,text="表示サイズ", relief="flat")
l.place(x=10, y=50)

button_org = tk.Button(frame_menu, text="オリジナルに戻す", command=org)
button_org.place(x=10, y=120)

button_save = tk.Button(frame_menu, text="一括保存", command=save)
button_save.place(x=10, y=160)

#Scaleの値格納用変数
val1 = tk.IntVar()
val1.set(0)



#スケールの作成
sc = tk.Scale(frame_scale, variable=val1, orient='horizontal',length=720, from_=0, to=255, resolution=0.1, command=scale)
sc.place(x=10, y=7)

#キャンバス作成・配置
canvas = tk.Canvas(frame_img, width=550, height=420)
canvas.place(x=10, y=10)

#イベントループ
root.mainloop()