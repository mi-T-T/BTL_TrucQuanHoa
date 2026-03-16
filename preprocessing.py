import pandas as pd

def load_and_clean_data(file_path):
    # 1. Tải dữ liệu với encoding phù hợp cho file thương mại điện tử Anh
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    
    # 2. Xử lý giá trị thiếu (Missing Values)
    # Loại bỏ các dòng không có CustomerID vì không thể phân tích khách hàng
    # Loại bỏ các dòng không có Description (mô tả sản phẩm)
    df.dropna(subset=['CustomerID', 'Description'], inplace=True)
    
    # 3. Định dạng kiểu dữ liệu
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(int).astype(str) # Chuyển về chuỗi 
    
    # 4. Xử lý dữ liệu bất thường (Outliers & Errors)
    # Chỉ giữ lại các đơn hàng có số lượng > 0 và đơn giá > 0
    # (Loại bỏ đơn hàng hủy 'C' và các giao dịch điều chỉnh hệ thống)
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    
    # 5. Feature Engineering (Tạo cột mới phục vụ Dashboard)
    # Tính tổng doanh thu cho mỗi dòng
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    # Tách thêm cột Tháng/Năm/Giờ để làm Page 2 (Xu hướng)
    df['Month_Year'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['Date'] = df['InvoiceDate'].dt.date
    df['Hour'] = df['InvoiceDate'].dt.hour
    
    # 6. Loại bỏ dữ liệu trùng lặp (Duplicates)
    df.drop_duplicates(inplace=True)
    
    return df

# Sử dụng hàm
df_clean = load_and_clean_data('data.csv')

# Lưu file dữ liệu sau tiền xử lí
df_clean.to_csv('ecommerce_cleaned.csv', index=False, encoding='utf-8-sig')