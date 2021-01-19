import pandas as pd
import numpy as np
import regex as re

# Các thư viện liên quan tới ngôn ngữ và NLP
from pyvi import ViTokenizer # Thư viện NLP tiếng Việt

# Thư viện liên quan của Scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import feature_selection

# Tạo pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer, make_column_selector

# Import thư viện riêng của nhóm/thư viện tham khảo
from .nlp_utils import covert_unicode, chuan_hoa_dau_tu_tieng_viet

def class_extract(df):
    selected_class = ["xã hội", "thế giới", "thể thao", "kinh doanh", "văn hóa", "pháp luật", "sức khỏe", "nhịp sống trẻ",
                      "giáo dục", "thời sự", "nhịp sống số", "tuyển sinh", "du lịch", "phóng sự", "nhà đất", "yêu",
                      "điện ảnh", "tài chính", "âm nhạc", "khoa học", "giải trí", "tv show", "công nghệ", "xe",
                      "thời trang", "smarthome", "đi chơi", "câu chuyện giáo dục", "hồ sơ", "thời sự quốc tế", "ăn gì"]
    processed_df = df[df["class"].isin(selected_class)].copy()
    processed_df.loc[processed_df["class"].isin(["thế giới", "hồ sơ"]), "class"] = "thời sự quốc tế"
    processed_df.loc[processed_df["class"].isin(["xã hội", "thời sự", "phóng sự"]), "class"] = "thời sự trong nước"
    processed_df.loc[processed_df["class"] == "đi chơi", "class"] = "du lịch"
    processed_df.loc[processed_df["class"].isin(["tài chính", "doanh nghiệp"]), "class"] = "kinh doanh"
    processed_df.loc[processed_df["class"] == "nhịp sống số", "class"] = "công nghệ"
    processed_df.loc[processed_df["class"].isin(["âm nhạc", "tv show", "điện ảnh"]), "class"] = "giải trí"
    processed_df.loc[processed_df["class"] == "smarthome", "class"] = "nhà đất"
    processed_df.loc[processed_df["class"].isin(["phòng mạch", "biết để khỏe"]), "class"] = "sức khỏe"
    processed_df.loc[processed_df["class"].isin(["tuyển sinh", "học đường", "câu chuyện giáo dục"]), "class"] = "giáo dục"
    return processed_df

# Xoá ký tự thừa
def remove_unnecessary(paragraph):
    temp=re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',paragraph)
    return re.sub(r'\s+', ' ', temp).strip()

def tokenize(sentence):
    return ViTokenizer.tokenize(sentence)

# Đọc dữ liệu stopword từ file
# (nguồn: https://github.com/stopwords/vietnamese-stopwords)
with open('src/vietnamese-stopwords-dash.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
    
# Danh sách stopword
stopword = set(lines)

def remove_stopwords(line):
    words = []
    for word in line.strip().split():
        if word not in stopword:
            words.append(word)
    return ' '.join(words)

def lower_str(string):
    return string.lower()

# --------------- Tạo pipeline ----------------------------------------------------

unicode_std = FunctionTransformer(covert_unicode)
lowercase_conv = FunctionTransformer(lower_str)
vn_std = FunctionTransformer(covert_unicode)
rm_unescesary = FunctionTransformer(remove_unnecessary)
word_tokenize = FunctionTransformer(tokenize)
rm_stopwords = FunctionTransformer(remove_stopwords)

preprocess_pipe_str = Pipeline([
    ("unicode_standardize", unicode_std),
    ("lowercase_conv", lowercase_conv),
    ("vn_standardize", vn_std),
    ("rm_unescesary", rm_unescesary),
    ("word_tokenize", word_tokenize),
    ("rm_stopwords", rm_stopwords)
])

# Tạo function transformer áp dụng tiền xử lý lên từng phần tử trong dãy
preprocess_list_str = FunctionTransformer(np.vectorize(preprocess_pipe_str.transform))

# Tạo prepreprocess pipeline để xử lý riêng cho class (do class không có tokenize và bỏ stopword)
prepreprocess_pipe_str = Pipeline([
    ("unicode_standardize", unicode_std),
    ("lowercase_conv", lowercase_conv),
    ("vn_standardize", vn_std)
])

prepreprocess_list_str = FunctionTransformer(np.vectorize(prepreprocess_pipe_str.transform))

# Khai báo các hàm cho function transformer
def drop_col(data_df):
    return data_df.drop(['links', 'title', 'description'],axis=1)

def drop_na(data_df):
    return data_df.dropna(axis=0, how="any")

def copy_df(data_df):
    return data_df.copy()

# Khai báo các hàm cho function transformer dành riêng cho từng lớp
def class_preprocess(data_df):
    data_df["class"] = prepreprocess_list_str.transform(data_df["class"])
    data_df = class_extract(data_df)
    return data_df

def content_preproc(data_df):
    data_df["content"] = preprocess_list_str.transform(data_df["content"])
    return data_df

preprocess_pipe_df = Pipeline([
    ("copy_df", FunctionTransformer(copy_df)),
    ("drop_na", FunctionTransformer(drop_na)),
    ("class_extract", FunctionTransformer(class_preprocess)),
    ("drop_columns", FunctionTransformer(drop_col)),
    ("content_preproc", FunctionTransformer(content_preproc)),
    ("drop_na_fin", FunctionTransformer(drop_na))
])