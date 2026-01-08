import csv
import json
import io

# ファイルパス（適宜変更してください）
CSV_FILE = '../horses.csv'
JSON_FILE = '../data/horses.json'

def convert():
    horses = []
    
    # encodingは適宜 'utf-8', 'shift_jis', 'cp932' など環境に合わせてください
    # ユーザーのCSVがExcel出力なら 'cp932' (Shift_JIS) の可能性が高いです
    try:
        # まずUTF-8で試す
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    except UnicodeDecodeError:
        # ダメならShift_JISで
        with open(CSV_FILE, mode='r', encoding='cp932') as f:
            reader = csv.DictReader(f)
            data = list(reader)

    for row in data:
        # CSVのカラム名に合わせてマッピング
        # 必須項目
        horse_id = row.get('血統登録番号')
        
        # IDがない行はスキップ
        if not horse_id:
            continue
            
        name = row.get('馬名')
        sire = row.get('父馬')

        # 詳細データ（空文字はNoneにする）
        detail = {}
        for k, v in row.items():
            # ID, Name, Sire 以外を詳細に入れる
            if k in ['血統登録番号', '馬名', '父馬']:
                continue
            
            # 値のクリーニング
            val = v.strip() if v else None
            if val == "":
                val = None
            
            # キーのマッピング（必要なら英語キーに変換）
            # ここではシンプルにCSVヘッダーをそのまま使うか、主要なものを変換するか
            key_map = {
                '母父': 'dam_sire',
                '性': 'sex',
                '生年月日': 'birthday',
                '厩舎': 'stable',
                'クラブ': 'club',
                '募集価格': 'price'
            }
            new_key = key_map.get(k, k) # マップになければ日本語のまま
            
            detail[new_key] = val

        # 生まれ年をIDから抽出（上4桁）できるが、今回は計算せず保持
        
        entry = {
            "id": horse_id,
            "name": name,
            "sire": sire,
            "detail": detail
        }
        horses.append(entry)

    # JSON書き出し
    with open(JSON_FILE, mode='w', encoding='utf-8') as f:
        json.dump(horses, f, ensure_ascii=False, indent=2)

    print(f"変換完了: {len(horses)}件のデータを {JSON_FILE} に書き出しました。")

if __name__ == "__main__":
    convert()