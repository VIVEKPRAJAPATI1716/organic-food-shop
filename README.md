# 🛒 Organic Food Shop - E-Commerce Website

## 🚀 Quick Start (सबसे आसान तरीका)

### Windows Users के लिए:

1. **START_HERE.bat** file पर **double-click** करें
2. कुछ seconds wait करें
3. Browser में automatically website खुल जाएगी

**बस इतना ही!** 🎉

---

## 📋 Manual Setup (अगर script काम न करे)

### Step 1: Dependencies Install करें
```bash
pip install -r requirements.txt
```

### Step 2: Database Setup करें
```bash
python manage.py migrate
```

### Step 3: Admin User बनाएं (Optional)
```bash
python manage.py createsuperuser
```
- Username: `admin`
- Password: `admin` (या अपना password)

### Step 4: Server Start करें
```bash
python manage.py runserver
```

### Step 5: Browser में खोलें
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🎯 Features (सुविधाएं)

✅ **User Registration & Login**
- Easy registration process
- Secure login system
- User account management

✅ **Product Browsing**
- Browse all products
- View product details
- Category-wise filtering

✅ **Shopping Cart**
- Add products to cart
- Update quantities
- Remove items
- View cart total

✅ **Checkout & Payment**
- Add shipping address
- Select saved addresses
- Paytm payment integration
- Order tracking

✅ **Order Management**
- View order history
- Track order status
- Order details

---

## 👤 Admin Panel Access

**URL**: http://127.0.0.1:8000/admin/

**Default Credentials:**
- **Username**: `admin`
- **Password**: `admin`

**Admin Panel में आप कर सकते हैं:**
- Products add/edit/delete
- Categories manage करें
- Orders देखें
- Users manage करें
- Contact messages देखें

---

## 🛍️ How to Use (कैसे Use करें)

### 1. **Register/Login**
- Home page पर "Register" या "Login" पर click करें
- Account बनाएं या login करें

### 2. **Browse Products**
- "Shop" page पर जाएं
- Products देखें और select करें
- Product details देखने के लिए click करें

### 3. **Add to Cart**
- Product page पर "Add to Cart" button click करें
- Cart में items add हो जाएंगे

### 4. **Checkout**
- Cart page पर "Checkout" button click करें
- Shipping address add करें
- Address select करें
- "Place Order" button click करें

### 5. **Payment**
- Paytm payment gateway पर redirect होगा
- Payment complete करें
- Order confirm हो जाएगा

### 6. **View Orders**
- "My Orders" page पर अपने orders देखें
- Order status track करें

---

## 🔧 Troubleshooting (समस्याएं और समाधान)

### ❌ Port Already in Use
**Problem**: Port 8000 already use हो रहा है

**Solution**:
```bash
python manage.py runserver 8001
```
फिर browser में: http://127.0.0.1:8001/

### ❌ Module Not Found
**Problem**: Python packages install नहीं हुए

**Solution**:
```bash
pip install -r requirements.txt
```

### ❌ Database Error
**Problem**: Database setup नहीं हुआ

**Solution**:
```bash
python manage.py migrate
```

### ❌ Static Files Not Found
**Problem**: Static files warning आ रही है

**Solution**: 
- Static directory automatically create हो जाती है
- Server restart करें

### ❌ Admin Login नहीं हो रहा
**Problem**: Admin user नहीं बना

**Solution**:
```bash
python manage.py createsuperuser
```

---

## 📱 Important URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Shop | http://127.0.0.1:8000/shop/ |
| Login | http://127.0.0.1:8000/login/ |
| Register | http://127.0.0.1:8000/register/ |
| Cart | http://127.0.0.1:8000/cart/ |
| Checkout | http://127.0.0.1:8000/checkout/ |
| My Orders | http://127.0.0.1:8000/myorder/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |

---

## 📦 Requirements

- Python 3.7+
- Django 3.1.1+
- All packages from `requirements.txt`

---

## 🌐 Deployment Instructions (Production)

### Step 1: Prepare Environment
- Create a `.env` file from `.env.example`.
- Update `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS`.

### Step 2: Install Production Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 4: Run with Gunicorn
```bash
gunicorn organicfoodshop.wsgi
```

---

## 🎨 Project Structure

```
organicfoodshop/
├── START_HERE.bat      # Easy setup script (Double-click to run)
├── manage.py           # Django management
├── requirements.txt    # Python dependencies
├── myapp/              # Main application
│   ├── models.py      # Database models
│   ├── views.py       # Business logic
│   ├── templates/     # HTML templates
│   └── static/        # CSS, JS, Images
└── organicfoodshop/    # Project settings
    ├── settings.py    # Configuration
    └── urls.py        # URL routing
```

---

## 💡 Tips for Best Experience

1. **First Time Setup**: `START_HERE.bat` run करें
2. **Admin Panel**: Products add करने के लिए admin panel use करें
3. **Test Payment**: Paytm staging environment use हो रहा है (testing के लिए)
4. **Browser**: Chrome या Firefox recommended
5. **Internet**: Payment के लिए internet connection जरूरी है

---

## 🆘 Need Help?

अगर कोई problem आए:
1. Error message को carefully पढ़ें
2. Troubleshooting section देखें
3. Server restart करें
4. Database migrate करें: `python manage.py migrate`

---

## ✅ All Features Working

- ✅ User Registration & Login
- ✅ Product Browsing
- ✅ Shopping Cart
- ✅ Checkout Process
- ✅ Address Management
- ✅ Payment Integration (Paytm)
- ✅ Order Placement
- ✅ Order Tracking
- ✅ Admin Panel
- ✅ Error Handling

---

## 🎉 Ready to Use!

**सब कुछ ready है!** बस `START_HERE.bat` file पर double-click करें और enjoy करें! 🚀

---

**Made with ❤️ for easy e-commerce experience**
