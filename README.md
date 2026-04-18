# 🏙️ BDS TPHCM — Hướng dẫn deploy Streamlit Cloud

## Cấu trúc thư mục cần upload lên GitHub

```
your-repo/
├── app.py                      ← file app chính
├── requirements.txt            ← dependencies
├── bds_data_clean_v2.csv       ← dataset (nếu < 100MB)
└── house_price_models/
    ├── best_xgb.pkl
    ├── best_lgb.pkl
    ├── cat_m.pkl
    ├── meta_model.pkl
    ├── dist_stats.pkl
    └── features.json
```

## Các bước deploy

### Bước 1 — Export models từ Google Colab
Chạy cell này trong notebook để download về máy:
```python
from google.colab import files
import zipfile, os

# Zip toàn bộ models
with zipfile.ZipFile('models.zip', 'w') as z:
    for f in os.listdir('house_price_models'):
        z.write(f'house_price_models/{f}')

files.download('models.zip')
files.download('bds_data_clean_v2.csv')
```

### Bước 2 — Tạo GitHub repo
1. Vào https://github.com → New repository
2. Đặt tên: `bds-price-prediction` (public)
3. Upload toàn bộ file theo cấu trúc trên

### Bước 3 — Deploy lên Streamlit Cloud
1. Vào https://share.streamlit.io
2. Đăng nhập bằng GitHub
3. Click **"New app"**
4. Chọn repo → branch: `main` → file: `app.py`
5. Click **Deploy** → đợi ~3 phút

### Bước 4 — Lấy link demo
Sau khi deploy xong, bạn sẽ có link dạng:
`https://your-name-bds-price-prediction.streamlit.app`

Đây là link dùng để demo trong ngày thi **09/05/2025**!

---

## Lưu ý quan trọng

- File CSV (`bds_data_clean_v2.csv`) cần để **cùng cấp** với `app.py`
- Thư mục `house_price_models/` cần để **cùng cấp** với `app.py`  
- Nếu models quá nặng (> 100MB), dùng **Git LFS** hoặc lưu lên Google Drive rồi load qua URL
- Streamlit Cloud **miễn phí** cho repo public

## Tính năng của app

| Tab | Nội dung |
|-----|----------|
| 🔮 Dự đoán giá | Nhập thông số → ra giá + đánh giá thị trường |
| 📊 Phân tích thị trường | Biểu đồ giá theo quận, scatter, boxplot |
| 🔄 So sánh căn hộ | So sánh 3 căn hộ cạnh nhau |
