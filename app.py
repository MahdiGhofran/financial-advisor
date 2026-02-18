"""
مشاور مالی شخصی - Personal Financial Advisor v4.0
Live Data from Bonbast + GoldPrice + ECB Frankfurter
+ Dollar Real Value Analysis (inflation-based)
"""

import streamlit as st
import pandas as pd
import requests
import hashlib
from datetime import datetime, timedelta

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(page_title="مشاور مالی | طلا و ارز", page_icon="🪙",
                   layout="wide", initial_sidebar_state="expanded")

# ================================================================
# AUTHENTICATION
# ================================================================
USERS = {
    "mahdi": {
        "password_hash": hashlib.sha256("Mahdi@Fin2026!".encode()).hexdigest(),
        "uid": "USR-MHD-8A3F7E",
        "display_name": "مهدی",
        "role": "admin",
    },
    "guest": {
        "password_hash": hashlib.sha256("Guest@View2026!".encode()).hexdigest(),
        "uid": "USR-GST-4B9C2D",
        "display_name": "مهمان",
        "role": "guest",
    },
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.current_user = None

def _login_page():
    st.markdown("""<style>
    .login-box{max-width:420px;margin:80px auto;padding:40px;background:#112240;
    border:1px solid #233554;border-radius:20px;direction:rtl;text-align:center;
    box-shadow:0 8px 32px rgba(0,0,0,.4)}
    .login-box h1{color:#64ffda;font-size:28px;margin-bottom:6px}
    .login-box p{color:#8892b0;font-size:14px;margin-bottom:24px}
    .login-footer{text-align:center;color:#8892b0;font-size:11px;margin-top:18px;direction:rtl}
    </style>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""<div class="login-box">
        <h1>🪙 مشاور مالی</h1>
        <p>برای دسترسی به داشبورد وارد شوید</p>
        </div>""", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("نام کاربری", placeholder="mahdi / guest")
            password = st.text_input("رمز عبور", type="password", placeholder="رمز عبور را وارد کنید")
            submitted = st.form_submit_button("ورود", use_container_width=True)

            if submitted:
                user = USERS.get(username.lower().strip())
                if user and hashlib.sha256(password.encode()).hexdigest() == user["password_hash"]:
                    st.session_state.authenticated = True
                    st.session_state.current_user = {
                        "username": username.lower().strip(),
                        "uid": user["uid"],
                        "display_name": user["display_name"],
                        "role": user["role"],
                    }
                    st.rerun()
                else:
                    st.error("نام کاربری یا رمز عبور اشتباه است!")

        st.markdown('<div class="login-footer">فقط کاربران مجاز می‌توانند وارد شوند</div>',
                    unsafe_allow_html=True)

if not st.session_state.authenticated:
    _login_page()
    st.stop()

# ================================================================
# CSS
# ================================================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');
html,body,[class*="css"]{font-family:'Vazirmatn','Tahoma',sans-serif!important}
.sig{border-radius:16px;padding:22px;margin:8px 0;text-align:center;color:#fff;direction:rtl;box-shadow:0 4px 15px rgba(0,0,0,.2)}
.sig .icon{font-size:44px;margin-bottom:6px}.sig .label{font-size:12px;opacity:.7}
.sig .title{font-size:18px;font-weight:700;margin:6px 0}.sig .desc{font-size:13px;line-height:2;opacity:.9}
.sig .acts{background:rgba(255,255,255,.1);border-radius:10px;padding:10px 14px;margin-top:10px;text-align:right;font-size:13px;line-height:2.2}
.sig .acts strong{color:#fff}
.sb{background:linear-gradient(135deg,#0d3d2b,#1a6b42);border:2px solid #2ecc71}
.ss{background:linear-gradient(135deg,#3d0d15,#6b1a25);border:2px solid #e74c3c}
.sw{background:linear-gradient(135deg,#3d2e0d,#6b5a1a);border:2px solid #f1c40f}
.si{background:linear-gradient(135deg,#0d2a3d,#1a456b);border:2px solid #3498db}
.comb{border-radius:20px;padding:28px;margin:10px 0;text-align:center;color:#fff;direction:rtl;box-shadow:0 6px 25px rgba(0,0,0,.3)}
.comb .bi{font-size:52px}.comb .mt{font-size:22px;font-weight:900;margin:8px 0 4px}
.comb .st2{font-size:15px;opacity:.9}
.comb .steps{background:rgba(0,0,0,.2);border-radius:12px;padding:14px;margin-top:14px;text-align:right;font-size:14px;line-height:2.2}
.comb .steps .sn{display:inline-block;width:22px;height:22px;border-radius:50%;background:rgba(255,255,255,.2);text-align:center;line-height:22px;font-size:11px;font-weight:700;margin-left:6px}
.mb{background:linear-gradient(135deg,#0f1b2d,#162a45);border:1px solid #233554;border-radius:14px;padding:16px;text-align:center;margin:4px 0}
.mb .ml{font-size:11px;color:#8892b0;margin-bottom:3px}.mb .mv{font-size:18px;color:#64ffda;font-weight:700;direction:ltr}
.mb .ms{font-size:10px;color:#8892b0;margin-top:2px}
.hint{background:#112240;border-right:4px solid #64ffda;border-radius:8px;padding:12px 16px;margin:10px 0;color:#ccd6f6;direction:rtl;text-align:right;line-height:1.9;font-size:13px}
.hint a{color:#64ffda;text-decoration:none}.hint strong{color:#e6f1ff}
.formula{background:#0a192f;border:1px solid #233554;border-radius:10px;padding:12px 16px;font-family:'Courier New',monospace;color:#64ffda;direction:ltr;text-align:left;margin:10px 0;line-height:2;font-size:12px}
.rtl{direction:rtl;text-align:right;line-height:1.8}
.phase{border-radius:14px;padding:20px;margin:10px 0;color:#fff;direction:rtl;text-align:right;line-height:2}
.dtbl{width:100%;border-collapse:collapse;direction:rtl;margin:10px 0}
.dtbl th{background:#1a1a2e;padding:8px;border:1px solid #233554;color:#8892b0;font-size:12px}
.dtbl td{padding:8px;border:1px solid #233554;text-align:center;font-size:12px}
.dtbl .rb{background:#0d3320}.dtbl .rw{background:#3d2e0d}.dtbl .rs{background:#3d0d0d}
div[data-testid="stSidebar"]{direction:rtl}
div[data-testid="stSidebar"] input[type="number"]{direction:ltr;text-align:left}
.disc{background:#112240;border:1px solid #233554;border-radius:10px;padding:12px;text-align:center;color:#8892b0;direction:rtl;margin-top:16px}
.disc strong{color:#f1c40f}
</style>""", unsafe_allow_html=True)

# ================================================================
# API FETCHING
# ================================================================
@st.cache_data(ttl=300, show_spinner=False)
def fetch_bonbast():
    """Fetch live Iranian market prices from bonbast.com via bonbast package."""
    try:
        from bonbast.server import get_token_from_main_page, get_prices_from_api
        token = get_token_from_main_page()
        currencies, coins, golds = get_prices_from_api(token)
        c_dict = {c.code: {"sell": c.sell, "buy": c.buy} for c in currencies}
        coin_dict = {c.code: {"sell": c.sell, "buy": c.buy} for c in coins}
        gold_dict = {g.code: {"price": g.price} for g in golds}
        return {"currencies": c_dict, "coins": coin_dict, "golds": gold_dict, "ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@st.cache_data(ttl=300, show_spinner=False)
def fetch_gold_ounce():
    try:
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        d = r.json()["items"][0]
        return {"price": round(d["xauPrice"], 2), "chg": round(d["chgXau"], 2),
                "pct": round(d["pcXau"], 4)}
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_forex():
    try:
        r = requests.get("https://api.frankfurter.dev/v1/latest?base=USD", timeout=10)
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_forex_hist(days=7):
    try:
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        r = requests.get(f"https://api.frankfurter.dev/v1/{start}..{end}?base=USD"
                         "&symbols=EUR,GBP,CHF,TRY,AED,CAD,JPY,CNY", timeout=10)
        return r.json()
    except Exception:
        return None

# ================================================================
# LOAD DATA
# ================================================================
with st.spinner("دریافت داده‌های زنده از bonbast.com و goldprice.org ..."):
    bb = fetch_bonbast()
    gold_api = fetch_gold_ounce()
    forex_api = fetch_forex()
    forex_hist = fetch_forex_hist()

# Extract values with fallbacks
if bb["ok"]:
    _usd = bb["currencies"].get("USD", {}).get("sell", 156860)
    _usd_buy = bb["currencies"].get("USD", {}).get("buy", 156000)
    _eur_sell = bb["currencies"].get("EUR", {}).get("sell", 163000)
    _gbp_sell = bb["currencies"].get("GBP", {}).get("sell", 197000)
    _chf_sell = bb["currencies"].get("CHF", {}).get("sell", 177000)
    _try_sell = bb["currencies"].get("TRY", {}).get("sell", 4500)
    _aed_sell = bb["currencies"].get("AED", {}).get("sell", 42700)
    _aed_buy = bb["currencies"].get("AED", {}).get("buy", 42500)
    _cad_sell = bb["currencies"].get("CAD", {}).get("sell", 108000)
    _cny_sell = bb["currencies"].get("CNY", {}).get("sell", 21500)
    _emami = bb["coins"].get("emami1", {}).get("sell", 199480000)
    _nim = bb["coins"].get("azadi1_2", {}).get("sell", 101020000)
    _rob = bb["coins"].get("azadi1_4", {}).get("sell", 56010000)
    _gerami = bb["coins"].get("azadi1g", {}).get("sell", 27500000)
    _mozneh = bb["golds"].get("mithqal", {}).get("price", 87355000)
    _g18 = bb["golds"].get("gol18", {}).get("price", 19875100)
else:
    _usd=156860; _usd_buy=156000; _eur_sell=163000; _gbp_sell=197000; _chf_sell=177000
    _try_sell=4500; _aed_sell=42700; _aed_buy=42500; _cad_sell=108000; _cny_sell=21500
    _emami=199480000; _nim=101020000; _rob=56010000; _gerami=27500000
    _mozneh=87355000; _g18=19875100

# Gold ounce: primary goldprice.org, fallback bonbast direct ounce
if gold_api:
    _ounce = gold_api["price"]
    _ounce_chg = gold_api["chg"]
    _gold_source = "goldprice.org"
elif bb["ok"] and bb["golds"].get("ounce", {}).get("price"):
    _ounce = float(bb["golds"]["ounce"]["price"])
    _ounce_chg = 0.0
    _gold_source = "bonbast.com (مستقیم)"
else:
    _ounce = 2860.0
    _ounce_chg = 0.0
    _gold_source = "پیش‌فرض"
_forex = forex_api.get("rates", {}) if forex_api else {}

# ================================================================
# HELPERS
# ================================================================
def fmt(n, d=0):
    if n is None: return "---"
    try: return f"{n:,.{d}f}" if d else f"{n:,.0f}"
    except: return "---"

COINS = {
    "تمام امامی": {"w": 8.13, "key": "emami", "emoji": "🥇"},
    "نیم سکه": {"w": 4.06, "key": "nim", "emoji": "🥈"},
    "ربع سکه": {"w": 2.03, "key": "rob", "emoji": "🥉"},
    "سکه گرمی": {"w": 1.0, "key": "gerami", "emoji": "💫"},
}

def calc_intrinsic(ounce, dollar, weight, mint=7000):
    return (ounce * dollar * weight * 0.9) / 31.1 + mint
def calc_bubble(intrinsic, market):
    if intrinsic <= 0: return 0, 0
    return market - intrinsic, ((market / intrinsic) - 1) * 100
def calc_formula_a(dollar, ounce):
    return dollar * ounce * 0.1045
def calc_gold_18k(ounce, dollar):
    return (ounce * dollar) / 31.1035 * 0.75

# ================================================================
# SIGNALS
# ================================================================
def coin_sig(bpct):
    if bpct < 13: return "b", f"حباب {bpct:.1f}% — پایین"
    elif bpct < 25: return "w", f"حباب {bpct:.1f}% — عادی"
    else: return "s", f"حباب {bpct:.1f}% — بالا"

def gold_sig(diff_pct):
    """سیگنال طلای آب شده بر اساس درصد اختلاف مظنه با عدد A"""
    if diff_pct < 1: return "b", f"اختلاف {diff_pct:.1f}٪ — ارزان"
    elif diff_pct < 3: return "w", f"اختلاف {diff_pct:.1f}٪ — عادی"
    elif diff_pct < 5: return "w", f"اختلاف {diff_pct:.1f}٪ — گران"
    else: return "s", f"اختلاف {diff_pct:.1f}٪ — بسیار گران"

def combined_sig(bpct, gdiff_pct):
    """توصیه ترکیبی بر اساس حباب سکه و درصد اختلاف آب شده"""
    cs = bpct >= 25; cb = bpct < 13; cw = not cs and not cb
    gb = gdiff_pct < 1; gw = 1 <= gdiff_pct < 5; gs = gdiff_pct >= 5
    if cs and gb:
        return "b","🔄","چرخه طلایی!","سکه بفروشید، آب شده بخرید",[
            "سکه‌ها را بفروشید (حباب بالا)",
            "با پول حاصل فوراً طلای آب شده بخرید",
            "این چرخه وزن طلای شما را افزایش می‌دهد",
            "⚠️ آب شده نفروشید — ارزان است"]
    if cs and gw:
        return "w","💵","سکه بفروشید، دلار نگه دارید","آب شده هنوز ارزان نشده",[
            "سکه‌ها را بفروشید (حباب بالا)",
            "پول حاصل را به دلار تبدیل کنید",
            "⚠️ آب شده دارید؟ فعلاً نگه دارید (نه بخرید نه بفروشید)",
            "صبر تا فرمول A سیگنال خرید بدهد، سپس آب شده بخرید"]
    if cs and gs:
        return "s","🏦","همه چیز گران، نقد شوید!","دلار نگه دارید",[
            "سکه بفروشید (حباب بالا)",
            "آب شده هم بفروشید (بسیار گران‌تر از ارزش واقعی)",
            "همه را دلار نقد نگه دارید",
            "صبر تا اصلاح بازار"]
    if cb and gb:
        return "b","🎯","فرصت طلایی!","سکه و آب شده هر دو ارزان",[
            "با پول نقد/دلار سکه بخرید (اولویت — حباب پایین)",
            "آب شده هم بخرید اگر نقدینگی دارید (ارزان)",
            "⚠️ آب شده دارید؟ حتماً نگه دارید — الان ارزان است",
            "خرید پله‌ای: ۳ مرحله"]
    if cb and gw:
        return "b","🪙","سکه بخرید با پول نقد/دلار",f"آب شده عادی (اختلاف {gdiff_pct:.1f}٪ — نه بخرید نه بفروشید)",[
            "با پول نقد یا دلار سکه بخرید (حباب پایین)",
            "⚠️ آب شده نخرید — اختلاف با ارزش واقعی عادی است",
            "⚠️ آب شده دارید؟ نگه دارید — سیگنال فروش نیست",
            "صبر تا حباب سکه بالا رفت، سکه بفروشید، سپس آب شده بخرید (وقتی ارزان شد)"]
    if cb and gs:
        return "b","🪙💰","سکه بخرید + آب شده بفروشید",f"حباب سکه پایین + آب شده گران ({gdiff_pct:.1f}٪)",[
            "اگر آب شده دارید بفروشید (بالای ۵٪ گران‌تر از ارزش واقعی)",
            "با پول حاصل سکه بخرید (حباب پایین)",
            "با پول نقد/دلار هم سکه بخرید",
            "صبر تا حباب بالا رفت، سکه بفروشید، آب شده ارزان بخرید"]
    if cb:
        return "b","🪙","سکه بخرید با پول نقد/دلار","آب شده فعلاً نه",[
            "با پول نقد یا دلار سکه بخرید (حباب پایین)",
            "⚠️ آب شده نخرید (فعلاً ارزان نیست)",
            "⚠️ آب شده دارید؟ نگه دارید — سیگنال فروش نیست",
            "صبر تا حباب سکه بالا رفت، بفروشید، سپس آب شده بخرید"]
    if cw and gb:
        return "b","🥇","آب شده بخرید با پول نقد/دلار","سکه فعلاً مناسب نیست",[
            "با پول نقد یا دلار طلای آب شده بخرید (ارزان)",
            "سکه نخرید (حباب عادی — سود حباب ندارد)",
            "⚠️ سکه دارید؟ فعلاً نگه دارید"]
    if cw and gs:
        return "s","💰","آب شده بفروشید","اگر دارید — بسیار گران",[
            "اگر آب شده دارید بفروشید (بالای ۵٪ گران‌تر از ارزش واقعی)",
            "پول حاصل را دلار نقد نگه دارید",
            "⚠️ سکه دارید؟ فعلاً نگه دارید (حباب عادی)"]
    return "w","⏳","صبر کنید","شرایط عادی — رصد روزانه",[
        "خرید و فروش توصیه نمی‌شود",
        "⚠️ دارایی فعلی (سکه/آب شده) نگه دارید",
        "هر روز بازار را چک کنید"]

def render_sig(typ, title, desc, acts=None, lbl=""):
    c = {"b":"sb","s":"ss","w":"sw","i":"si"}[typ]
    ic = {"b":"🟢","s":"🔴","w":"🟡","i":"🔵"}[typ]
    lb = {"b":"سیگنال خرید","s":"سیگنال فروش","w":"سیگنال انتظار","i":"اطلاعات"}[typ]
    if lbl: lb = f"{lbl} | {lb}"
    ah = ""
    if acts:
        ah = '<div class="acts"><strong>📋 اقدام:</strong>' + "".join(f"<div>• {a}</div>" for a in acts) + "</div>"
    st.markdown(f'<div class="sig {c}"><div class="icon">{ic}</div><div class="label">{lb}</div>'
                f'<div class="title">{title}</div><div class="desc">{desc}</div>{ah}</div>',
                unsafe_allow_html=True)

def render_comb(typ, emoji, title, sub, steps):
    c = {"b":"sb","s":"ss","w":"sw"}[typ]
    sh = "".join(f'<div><span class="sn">{i+1}</span>{s}</div>' for i,s in enumerate(steps))
    st.markdown(f'<div class="comb {c}"><div class="bi">{emoji}</div><div class="mt">{title}</div>'
                f'<div class="st2">{sub}</div><div class="steps">{sh}</div></div>',
                unsafe_allow_html=True)

def render_m(label, value, sub=""):
    sh = f'<div class="ms">{sub}</div>' if sub else ""
    st.markdown(f'<div class="mb"><div class="ml">{label}</div><div class="mv">{value}</div>{sh}</div>',
                unsafe_allow_html=True)

def trend_analysis(hist, sym):
    if not hist or "rates" not in hist: return None
    r = hist["rates"]; dates = sorted(r.keys())
    if len(dates) < 2: return None
    f = r[dates[0]].get(sym); l = r[dates[-1]].get(sym)
    if not f or not l: return None
    return {"chg": ((l - f) / f) * 100, "dir": "down" if l < f else "up"}

# Jalali month names for UI
_MONTH_NAMES = {
    1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر",
    5: "مرداد", 6: "شهریور", 7: "مهر", 8: "آبان",
    9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند",
}

# Dirham-Dollar Analysis Constants
AED_USD_PEG = 3.6725   # Official UAE Central Bank peg: 1 USD = 3.6725 AED (fixed since 1997)

def get_jalali_year_month():
    """Get current Jalali (Solar Hijri) year and approximate month."""
    now = datetime.now()
    g_y, g_m, g_d = now.year, now.month, now.day
    if g_m > 3 or (g_m == 3 and g_d >= 21):
        j_y = g_y - 621
        base = datetime(g_y, 3, 21)
    else:
        j_y = g_y - 622
        base = datetime(g_y - 1, 3, 21)
    days = (now - base).days
    if days < 0:
        days += 365
    if days < 186:   # First 6 months: 31 days each
        j_m = days // 31 + 1
    else:
        j_m = (days - 186) // 30 + 7
    return j_y, max(1, min(12, j_m))

# ================================================================
# DIRHAM-DOLLAR CROSS-RATE ANALYSIS
# ================================================================
def calc_usd_from_aed(aed_price, peg_rate=AED_USD_PEG):
    """Calculate USD value in Tomans from AED price and fixed peg rate."""
    return aed_price * peg_rate if aed_price > 0 else 0

def calc_cross_rate_usd(iran_price, forex_rate):
    """Calculate implied USD value from any currency cross-rate.
    forex_rate = units of currency per 1 USD (from Frankfurter API)."""
    return iran_price * forex_rate if forex_rate > 0 and iran_price > 0 else 0

def calc_cross_rates_all(iran_prices, forex_rates, aed_price, market_usd):
    """Calculate cross-rate implied USD value from all available currencies."""
    results = {}
    # AED (special case: use fixed peg rate — highest reliability)
    if aed_price > 0:
        usd_calc = calc_usd_from_aed(aed_price)
        diff = market_usd - usd_calc
        diff_pct = (diff / usd_calc * 100) if usd_calc > 0 else 0
        results["AED"] = {
            "name": "درهم امارات", "emoji": "🇦🇪",
            "iran_price": aed_price, "rate": AED_USD_PEG, "rate_source": "پگ ثابت",
            "calc_usd": usd_calc, "diff": diff, "diff_pct": diff_pct,
            "weight": 0.50, "reliability": "بسیار بالا"
        }
    # Other currencies from Frankfurter (ECB rates)
    _weights = {"EUR": 0.20, "GBP": 0.10, "CHF": 0.10, "TRY": 0.03, "CAD": 0.05, "CNY": 0.02}
    _names_map = {
        "EUR": ("یورو", "🇪🇺"), "GBP": ("پوند", "🇬🇧"), "CHF": ("فرانک سوئیس", "🇨🇭"),
        "TRY": ("لیر ترکیه", "🇹🇷"), "CAD": ("دلار کانادا", "🇨🇦"), "CNY": ("یوآن چین", "🇨🇳")
    }
    for sym, iran_price in iran_prices.items():
        if sym == "AED":
            continue
        rate = forex_rates.get(sym)
        if rate and rate > 0 and iran_price > 0:
            usd_calc = calc_cross_rate_usd(iran_price, rate)
            diff = market_usd - usd_calc
            diff_pct = (diff / usd_calc * 100) if usd_calc > 0 else 0
            name, emoji = _names_map.get(sym, (sym, "🌐"))
            results[sym] = {
                "name": name, "emoji": emoji,
                "iran_price": iran_price, "rate": rate, "rate_source": "ECB",
                "calc_usd": usd_calc, "diff": diff, "diff_pct": diff_pct,
                "weight": _weights.get(sym, 0.02),
                "reliability": "بالا" if sym in ["EUR", "GBP", "CHF"] else "متوسط"
            }
    return results

def calc_consensus_usd(cross_rates):
    """Calculate weighted consensus USD value from all cross-rates."""
    total_weight = sum(cr["weight"] for cr in cross_rates.values())
    if total_weight <= 0:
        return 0
    weighted_sum = sum(cr["calc_usd"] * cr["weight"] for cr in cross_rates.values())
    return weighted_sum / total_weight

def dirham_dollar_signal(market_usd, aed_derived_usd, consensus_usd, n_currencies):
    """Generate professional buy/sell signal based on Dirham cross-rate analysis.

    AED is pegged to USD at a FIXED rate — even small deviations are meaningful.
    The AED spread in Iran is typically 0.1–0.3%, so thresholds are tight.

    Signal tiers:
        > +2.5%  : Strong Sell (dollar overpriced vs AED parity)
        +1.0~2.5%: Caution (dollar slightly overpriced)
        ±1.0%    : Neutral (within transaction-cost noise)
        -1.0~2.5%: Buy (dollar underpriced — real opportunity)
        < -2.5%  : Strong Buy (dollar significantly underpriced)
    """
    if aed_derived_usd <= 0:
        return "i", "داده کافی نیست", "ارزش دلار از درهم قابل محاسبه نیست", [], 0
    aed_diff = ((market_usd - aed_derived_usd) / aed_derived_usd * 100)
    cons_diff = ((market_usd - consensus_usd) / consensus_usd * 100) if consensus_usd > 0 else aed_diff
    consensus_note = f"اجماع {n_currencies} ارز: اختلاف {cons_diff:+.1f}%"
    if aed_diff > 2.5:
        return ("s",
            f"فروش — دلار آزاد {aed_diff:.1f}% گران‌تر از ارزش درهمی",
            f"بازار ({fmt(market_usd)}) بیش از ۲.۵% بالاتر از محاسباتی ({fmt(aed_derived_usd)})",
            ["فروش بخشی از دلار — قیمت بالاتر از ارزش درهمی",
             "خرید درهم مقرون‌به‌صرفه‌تر از دلار",
             "صبر تا اختلاف به محدوده عادی برگردد",
             consensus_note], aed_diff)
    if aed_diff > 1.0:
        return ("w",
            f"احتیاط — دلار {aed_diff:.1f}% بالاتر از ارزش درهمی",
            f"بازار ({fmt(market_usd)}) بالاتر از محاسباتی ({fmt(aed_derived_usd)})",
            ["خرید دلار توصیه نمی‌شود — گران‌تر از درهم",
             "اگر دلار دارید نگه دارید",
             "خرید درهم با تبدیل مستقیم مقرون‌به‌صرفه‌تر",
             consensus_note], aed_diff)
    if aed_diff > -1.0:
        return ("w",
            f"خنثی — قیمت نزدیک ارزش درهمی ({aed_diff:+.1f}%)",
            f"بازار ({fmt(market_usd)}) ≈ محاسباتی ({fmt(aed_derived_usd)}) — متعادل",
            ["بازار متعادل — اختلاف در حد هزینه تراکنش",
             "خرید/فروش بر اساس نیاز شخصی",
             consensus_note], aed_diff)
    if aed_diff > -2.5:
        return ("b",
            f"خرید — دلار {abs(aed_diff):.1f}% ارزان‌تر از ارزش درهمی",
            f"بازار ({fmt(market_usd)}) زیر محاسباتی ({fmt(aed_derived_usd)}) — فرصت خرید",
            ["خرید دلار — ارزان‌تر از ارزش درهمی",
             "خرید پله‌ای توصیه می‌شود (۳ مرحله)",
             "فروش درهم و خرید دلار مقرون‌به‌صرفه",
             consensus_note], aed_diff)
    return ("b",
        f"خرید قوی — دلار {abs(aed_diff):.1f}% زیر ارزش درهمی!",
        f"بازار ({fmt(market_usd)}) بسیار ارزان‌تر از محاسباتی ({fmt(aed_derived_usd)})",
        ["خرید فوری دلار — حداکثر حاشیه امن",
         "فروش درهم و خرید دلار بسیار سودمند",
         "خرید پله‌ای با بودجه بیشتر — فرصت را از دست ندهید",
         consensus_note], aed_diff)

# ================================================================
# SIDEBAR
# ================================================================
with st.sidebar:
    _u = st.session_state.current_user
    st.markdown(f'<div class="rtl" style="text-align:center;margin-bottom:12px;">'
                f'<span style="color:#64ffda;font-weight:700;">{_u["display_name"]}</span>'
                f' <span style="color:#8892b0;font-size:11px;">({_u["uid"]})</span></div>',
                unsafe_allow_html=True)
    if st.button("🚪 خروج", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()
    st.markdown("---")
    st.markdown('<div class="rtl"><h2>📊 داده‌های زنده بازار</h2></div>', unsafe_allow_html=True)
    with st.expander("🔗 وضعیت API", expanded=False):
        st.markdown(f"{'✅' if bb['ok'] else '❌'} **Bonbast.com** — ارز، سکه، طلا")
        _gold_icon = '✅' if gold_api else ('🔄' if _gold_source.startswith('bonbast') else '❌')
        st.markdown(f"{_gold_icon} **انس جهانی** — {_gold_source}")
        st.markdown(f"{'✅' if forex_api else '❌'} **Frankfurter (ECB)** — نرخ ارز جهانی")
        if not bb['ok']: st.caption(f"خطا: {bb.get('error','')[:80]}")
        if st.button("🔄 بروزرسانی داده‌ها", use_container_width=True):
            st.cache_data.clear(); st.rerun()

    st.markdown("---")
    st.markdown('<div class="rtl"><small>قیمت‌ها خودکار از bonbast.com — اصلاح دستی در صورت نیاز:</small></div>',
                unsafe_allow_html=True)
    dollar = st.number_input("💵 دلار (تومان)", value=_usd, step=100,
                             help="خودکار از bonbast.com")
    ounce = st.number_input("🥇 انس طلا ($)", value=_ounce, step=1.0, format="%.2f",
                            help=f"منبع: {_gold_source}")
    emami = st.number_input("🪙 سکه امامی (T)", value=_emami, step=500000)
    nim_p = st.number_input("🪙 نیم سکه (T)", value=_nim, step=500000)
    rob_p = st.number_input("🪙 ربع سکه (T)", value=_rob, step=500000)
    ger_p = st.number_input("🪙 سکه گرمی (T)", value=_gerami, step=100000)
    moz = st.number_input("⚖️ مظنه (T)", value=_mozneh, step=100000)
    g18 = st.number_input("✨ ۱۸ عیار/گرم (T)", value=_g18, step=10000)

    st.markdown("---")
    _j_year, _j_month = get_jalali_year_month()
    st.caption(f"📅 {datetime.now().strftime('%Y/%m/%d %H:%M')} | ☀️ {_j_year}/{_j_month:02d} ({_MONTH_NAMES[_j_month]})")

# Pre-calculate
CP = {"تمام امامی": emami, "نیم سکه": nim_p, "ربع سکه": rob_p, "سکه گرمی": ger_p}
CB = {}
for cn, ci in COINS.items():
    intr = calc_intrinsic(ounce, dollar, ci["w"])
    _, bp = calc_bubble(intr, CP[cn])
    CB[cn] = bp

# Iranian currency prices from bonbast
IRAN_CUR = {"EUR": _eur_sell, "GBP": _gbp_sell, "CHF": _chf_sell,
            "TRY": _try_sell, "AED": _aed_sell, "CAD": _cad_sell, "CNY": _cny_sell}

# Currency premiums for cross-asset analysis
CUR_NAMES = {"EUR": "یورو", "GBP": "پوند", "CHF": "فرانک سوئیس", "TRY": "لیر ترکیه",
             "AED": "درهم امارات", "CAD": "دلار کانادا", "CNY": "یوآن چین"}
CUR_PREMS = {}
for _s, _ip in IRAN_CUR.items():
    _r = _forex.get(_s)
    if _r and _r > 0:
        _fv = (1.0 / _r) * dollar
        CUR_PREMS[_s] = ((_ip - _fv) / _fv * 100) if _fv > 0 else 0

# Dirham-Dollar cross-rate pre-calculations
_usd_from_aed_sell = calc_usd_from_aed(_aed_sell)
_usd_from_aed_buy = calc_usd_from_aed(_aed_buy)
_cross_rates = calc_cross_rates_all(IRAN_CUR, _forex, _aed_sell, dollar)
_consensus_usd = calc_consensus_usd(_cross_rates)
_aed_diff_pct = ((dollar - _usd_from_aed_sell) / _usd_from_aed_sell * 100) if _usd_from_aed_sell > 0 else 0
_cons_diff_pct = ((dollar - _consensus_usd) / _consensus_usd * 100) if _consensus_usd > 0 else 0

# ================================================================
# HEADER
# ================================================================
st.markdown("""<div class="rtl"><h1 style="color:#e6f1ff;margin-bottom:0">🪙 مشاور مالی شخصی</h1>
<p style="color:#8892b0;font-size:14px;margin-top:2px">
    v4.0 | داده‌های زنده bonbast.com + goldprice.org + ECB + تحلیل دلار (درهم)</p></div>""", unsafe_allow_html=True)

# ================================================================
# TABS
# ================================================================
tab1, tab2, tab3, tab_d, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 داشبورد", "🪙 حباب سکه", "🥇 آب شده", "💵 تحلیل دلار",
    "🔢 ماشین‌حساب", "💱 تبدیل ارز", "💼 سبد سرمایه", "📉 خرید پله‌ای", "🗺️ نقشه راه"])

# ── TAB 1: DASHBOARD ─────────────────
with tab1:
    st.markdown('<div class="rtl"><h2>📊 داشبورد</h2></div>', unsafe_allow_html=True)
    mc = st.columns(6)
    with mc[0]: render_m("💵 دلار آزاد", f"{fmt(dollar)} T",
                         "🟢 bonbast زنده" if bb["ok"] else "⚠️ دستی")
    with mc[1]: render_m("📡 دلار از درهم", f"{fmt(_usd_from_aed_sell)} T",
                         f"{'🟢 ارزان' if _aed_diff_pct < -1 else ('🔴 گران' if _aed_diff_pct > 1 else '🟡 متعادل')} ({_aed_diff_pct:+.1f}%)")
    with mc[2]: render_m("🥇 انس طلا", f"${fmt(ounce,2)}", f"{_ounce_chg:+.2f}$")
    with mc[3]: render_m("🪙 سکه امامی", f"{fmt(emami)} T")
    with mc[4]: render_m("⚖️ مظنه", f"{fmt(moz)} T")
    with mc[5]: render_m("✨ ۱۸عیار/g", f"{fmt(g18)} T")

    st.markdown("<br>", unsafe_allow_html=True)
    intr_e = calc_intrinsic(ounce, dollar, 8.13)
    _, bpct_e = calc_bubble(intr_e, emami)
    fa = calc_formula_a(dollar, ounce); gdiff = moz - fa
    gdiff_pct = (gdiff / fa * 100) if fa > 0 else 0

    st.markdown('<div class="rtl"><h3>🎯 توصیه نهایی</h3></div>', unsafe_allow_html=True)
    cs, ce, ct, csb, cst = combined_sig(bpct_e, gdiff_pct)
    render_comb(cs, ce, ct, csb, cst)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="hint" style="font-size:12px">
        ⚠️ سیگنال‌های زیر هر بازار را <strong>جداگانه</strong> تحلیل می‌کنند →
        برای تصمیم نهایی به توصیه ترکیبی بالا مراجعه کنید.</div>""", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        cs_, cd_ = coin_sig(bpct_e)
        acts = {"b":["خرید پله‌ای سکه","۳ مرحله بخرید نه یکجا"],
                "s":["سکه بفروشید","ببینید آب شده ارزان است؟ (تب آب شده)"],
                "w":["فعلاً نخرید","رصد روزانه"]}
        render_sig(cs_, {"b":"خرید سکه","s":"فروش سکه","w":"صبر"}[cs_], cd_, acts[cs_], "🪙 سکه")
    with s2:
        gs_, gd_ = gold_sig(gdiff_pct)
        acts = {"b":["آب شده بخرید (مراکز معتبر)","فاکتور با عیار و وزن بگیرید"],
                "s":["آب شده بفروشید","به دلار نقد تبدیل کنید"],
                "w":["فعلاً نخرید","صبر تا اختلاف کم شود"]}
        render_sig(gs_, {"b":"خرید آب شده","s":"فروش آب شده","w":"صبر"}[gs_], gd_, acts[gs_], "🥇 آب شده")
    with s3:
        _da_sig_t, _da_sig_tit, _da_sig_dsc, _, _da_sig_d = dirham_dollar_signal(
            dollar, _usd_from_aed_sell, _consensus_usd, len(_cross_rates))
        _da_sig_acts = {"b":["خرید دلار — ارزان‌تر از درهم","جزئیات: تب تحلیل دلار"],
                        "s":["فروش دلار — گران‌تر از درهم","جزئیات: تب تحلیل دلار"],
                        "w":["بازار متعادل — صبر","جزئیات: تب تحلیل دلار"],
                        "i":["داده کافی نیست"]}
        render_sig(_da_sig_t, {"b":"خرید دلار","s":"فروش دلار","w":"صبر","i":"نامشخص"}[_da_sig_t],
                   _da_sig_dsc, _da_sig_acts.get(_da_sig_t, []), "💵 دلار")

    kc = st.columns(5)
    kc[0].metric("ارزش ذاتی سکه", f"{fmt(intr_e)} T")
    kc[1].metric("حباب امامی", f"{bpct_e:.1f}%")
    kc[2].metric("عدد A (تئوری مظنه)", f"{fmt(fa)} T", f"اختلاف: {gdiff_pct:.1f}%")
    kc[3].metric("۱۸ عیار تئوری", f"{fmt(calc_gold_18k(ounce, dollar))} T")
    kc[4].metric("دلار از درهم", f"{fmt(_usd_from_aed_sell)} T", f"{_aed_diff_pct:+.1f}%")

# ── TAB 2: COIN BUBBLE ───────────────
with tab2:
    st.markdown('<div class="rtl"><h2>🪙 تحلیل حباب + توصیه نوع سکه</h2></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint">حباب هر نوع سکه مقایسه شده. با وارد کردن بودجه، بهترین نوع پیشنهاد می‌شود.</div>""", unsafe_allow_html=True)

    bc = st.columns(4)
    for i, (cn, ci) in enumerate(COINS.items()):
        intr = calc_intrinsic(ounce, dollar, ci["w"])
        _, bp = calc_bubble(intr, CP[cn])
        with bc[i]:
            ic = "🟢" if bp < 13 else ("🟡" if bp < 25 else "🔴")
            render_m(f"{ci['emoji']} {cn}", f"{bp:.1f}% {ic}", f"ذاتی: {fmt(intr)} T")

    st.markdown("---")
    budget = st.number_input("💰 بودجه خرید سکه (تومان)", value=100_000_000, step=10_000_000,
                             help="مبلغی که می‌خواهید برای سکه اختصاص دهید")
    for cn, ci in COINS.items():
        price = CP[cn]; bp = CB[cn]
        if price <= 0: continue
        count = int(budget // price)
        if count == 0:
            st.markdown(f"**{ci['emoji']} {cn}:** {fmt(price)} T — بودجه کافی نیست ❌")
            continue
        gold_g = count * ci["w"]
        s = "b" if bp < 13 else ("w" if bp < 25 else "s")
        render_sig(s, f"{ci['emoji']} {cn} — حباب {bp:.1f}%",
            f"قیمت: {fmt(price)} T | خرید: {count} عدد | طلا: {gold_g:.2f}g | باقیمانده: {fmt(budget - count * price)} T",
            [{"b":"🟢 حباب پایین — فرصت خرید","w":"🟡 حباب عادی — صبر","s":"🔴 حباب بالا — نخرید"}[s],
             f"مجموع طلا: {gold_g:.2f} گرم (هر سکه {ci['w']}g)"], cn)

    with st.expander("📐 فرمول و جدول"):
        st.markdown("""<div class="formula">ارزش ذاتی = (انس × دلار × وزن × 0.9) ÷ 31.1 + ضرب<br>
حباب% = (قیمت بازار ÷ ارزش ذاتی − 1) × 100</div>""", unsafe_allow_html=True)
        st.markdown("""<table class="dtbl"><tr><th>حباب</th><th>سیگنال</th><th>اقدام</th></tr>
<tr class="rb"><td>زیر ۱۳٪</td><td>🟢</td><td>خرید پله‌ای</td></tr>
<tr class="rw"><td>۱۳ تا ۲۵٪</td><td>🟡</td><td>صبر</td></tr>
<tr class="rs"><td>بالای ۲۵٪</td><td>🔴</td><td>فروش، تبدیل به آب شده یا دلار</td></tr></table>""", unsafe_allow_html=True)

# ── TAB 3: MELTED GOLD ───────────────
with tab3:
    st.markdown('<div class="rtl"><h2>🥇 فرصت‌یابی طلای آب شده</h2></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint"><strong>فرمول A</strong> ارزش تئوری مظنه را محاسبه می‌کند.
    اختلاف مظنه واقعی با عدد A نشان‌دهنده ارزان یا گران بودن آب شده است.</div>""", unsafe_allow_html=True)

    a_v = calc_formula_a(dollar, ounce); diff = moz - a_v
    diff_pct = (diff / a_v * 100) if a_v > 0 else 0
    mc = st.columns(4)
    with mc[0]: render_m("عدد A (تئوری)", f"{fmt(a_v)} T")
    with mc[1]: render_m("مظنه بازار", f"{fmt(moz)} T")
    with mc[2]: render_m("اختلاف مطلق", f"{fmt(diff)} T")
    with mc[3]: render_m("اختلاف درصدی", f"{diff_pct:+.1f}٪",
                         "🟢 ارزان" if diff_pct < 1 else ("🟡 عادی" if diff_pct < 3 else "🔴 گران"))

    st.markdown("<br>", unsafe_allow_html=True)
    gs, gd = gold_sig(diff_pct)
    amap = {"b":["آب شده بخرید (مراکز معتبر: طلاین، آی‌گلد)","فاکتور با عیار و وزن بگیرید",
                 "خرید پله‌ای: نصف الان، نصف هفته بعد"],
            "s":["اگر آب شده دارید بفروشید","به دلار نقد تبدیل کنید"],
            "w":["فعلاً نخرید","هر روز فرمول A را چک کنید"]}
    render_sig(gs, {"b":"خرید آب شده","s":"فروش آب شده","w":"صبر"}[gs], gd, amap[gs])

    if gs == "b" and bpct_e >= 25:
        st.success("✅ **چرخه طلایی!** آب شده ارزان + حباب سکه بالا → سکه بفروش، آب شده بخر!")

    with st.expander("📐 فرمول و جدول"):
        st.markdown("""<div class="formula">A = دلار × انس × 0.1045<br>
اختلاف = مظنه − A<br>
درصد اختلاف = (اختلاف ÷ A) × 100</div>""", unsafe_allow_html=True)
        st.markdown("""<table class="dtbl"><tr><th>درصد اختلاف</th><th>سیگنال</th><th>اقدام</th></tr>
<tr class="rb"><td>زیر ۱٪</td><td>🟢</td><td>بهترین فرصت خرید</td></tr>
<tr class="rw"><td>۱٪ تا ۳٪</td><td>🟡</td><td>عادی — با احتیاط</td></tr>
<tr class="rw"><td>۳٪ تا ۵٪</td><td>🟡</td><td>گران — صبر کنید</td></tr>
<tr class="rs"><td>بالای ۵٪</td><td>🔴</td><td>بسیار گران — بفروشید</td></tr></table>""", unsafe_allow_html=True)

# ── TAB D: DOLLAR ANALYSIS (DIRHAM METHOD) ──────
with tab_d:
    st.markdown('<div class="rtl"><h2>💵 تحلیل دلار</h2></div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="hint">
        <strong>اصل کلیدی:</strong> درهم امارات با نرخ ثابت <strong>{AED_USD_PEG}</strong> به دلار آمریکا پگ شده.
        بنابراین اگر نرخ درهم در بازار آزاد ایران را بدانیم، ارزش واقعی لحظه‌ای دلار محاسبه می‌شود.<br>
        <strong>فرمول:</strong> ارزش دلار = قیمت درهم × {AED_USD_PEG}<br>
        <strong>مقایسه:</strong> دلار بازار آزاد بالاتر از محاسباتی → <strong>گران</strong> | پایین‌تر → <strong>ارزان</strong><br>
        <strong>چرا درهم؟</strong> ≈ ۸۵% مبادلات ارزی ایران از طریق امارات — درهم نقدشونده‌ترین ارز پس از دلار
    </div>""", unsafe_allow_html=True)

    # ── Metrics Row ──
    damc = st.columns(6)
    with damc[0]:
        render_m("🇦🇪 درهم (فروش)", f"{fmt(_aed_sell)} T", "bonbast.com")
    with damc[1]:
        render_m("🇦🇪 درهم (خرید)", f"{fmt(_aed_buy)} T", "bonbast.com")
    with damc[2]:
        render_m("💵 دلار محاسباتی", f"{fmt(_usd_from_aed_sell)} T",
                 f"= {fmt(_aed_sell)} × {AED_USD_PEG}")
    with damc[3]:
        render_m("💵 دلار بازار آزاد", f"{fmt(dollar)} T", "bonbast.com")
    with damc[4]:
        _da_abs_diff = dollar - _usd_from_aed_sell
        _da_abs_icon = "🔴 گران" if _da_abs_diff > 0 else ("🟢 ارزان" if _da_abs_diff < 0 else "🟡 برابر")
        render_m("⚖️ اختلاف مطلق", f"{fmt(_da_abs_diff)} T", _da_abs_icon)
    with damc[5]:
        _da_pct_icon = "🟢 ارزان" if _aed_diff_pct < -1.0 else ("🔴 گران" if _aed_diff_pct > 1.0 else "🟡 متعادل")
        render_m("📊 اختلاف درصدی", f"{_aed_diff_pct:+.2f}%", _da_pct_icon)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main Signal ──
    st.markdown('<div class="rtl"><h3>🎯 سیگنال اصلی (روش درهم)</h3></div>', unsafe_allow_html=True)
    _da_t, _da_title, _da_desc, _da_acts, _da_d = dirham_dollar_signal(
        dollar, _usd_from_aed_sell, _consensus_usd, len(_cross_rates))
    render_sig(_da_t, _da_title, _da_desc, _da_acts, "📡 تحلیل درهم-دلار")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Buy/Sell Zone Table ──
    st.markdown('<div class="rtl"><h3>💹 محدوده‌های خرید و فروش (بر اساس درهم)</h3></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint" style="font-size:12px">
        محدوده‌ها بر اساس ارزش محاسباتی دلار از درهم. وقتی قیمت بازار وارد هر محدوده شود، سیگنال مربوطه صادر می‌شود.
    </div>""", unsafe_allow_html=True)

    _az_strong_sell = int(_usd_from_aed_sell * 1.025)
    _az_sell = int(_usd_from_aed_sell * 1.01)
    _az_fair_h = int(_usd_from_aed_sell * 1.01)
    _az_fair_l = int(_usd_from_aed_sell * 0.99)
    _az_buy = int(_usd_from_aed_sell * 0.99)
    _az_strong_buy = int(_usd_from_aed_sell * 0.975)

    def _az_mark(lo, hi):
        return " ← 👈 قیمت فعلی" if lo <= dollar <= hi else ""

    st.markdown(f"""<table class="dtbl">
    <tr><th>محدوده</th><th>سیگنال</th><th>بازه قیمت (تومان)</th><th>وضعیت</th></tr>
    <tr class="rs"><td>فروش قوی (بالای +۲.۵%)</td><td>🔴🔴</td>
        <td>بالای {fmt(_az_strong_sell)}</td><td>{_az_mark(_az_strong_sell, 999_999_999)}</td></tr>
    <tr class="rs"><td>احتیاط (+۱% تا +۲.۵%)</td><td>🔴</td>
        <td>{fmt(_az_sell)} — {fmt(_az_strong_sell)}</td><td>{_az_mark(_az_sell, _az_strong_sell)}</td></tr>
    <tr class="rw"><td>متعادل (±۱%)</td><td>🟡</td>
        <td>{fmt(_az_fair_l)} — {fmt(_az_fair_h)}</td><td>{_az_mark(_az_fair_l, _az_fair_h)}</td></tr>
    <tr class="rb"><td>خرید (−۱% تا −۲.۵%)</td><td>🟢</td>
        <td>{fmt(_az_strong_buy)} — {fmt(_az_buy)}</td><td>{_az_mark(_az_strong_buy, _az_buy)}</td></tr>
    <tr class="rb"><td>خرید قوی (زیر −۲.۵%)</td><td>🟢🟢</td>
        <td>زیر {fmt(_az_strong_buy)}</td><td>{_az_mark(0, _az_strong_buy)}</td></tr>
    </table>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Cross-Rate Validation ──
    st.markdown('<div class="rtl"><h3>🌍 تأیید چند ارزی (Cross-Rate Validation)</h3></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint" style="font-size:12px">
        ارزش دلار را از مسیر ارزهای مختلف محاسبه و مقایسه می‌کنیم.
        اگر همه ارزها دلار آزاد را گران یا ارزان نشان دهند، سیگنال قوی‌تر است.
    </div>""", unsafe_allow_html=True)

    if _cross_rates:
        cr_header = '<tr><th>ارز</th><th>نرخ ایران (T)</th><th>نرخ جهانی (/$)</th><th>منبع</th><th>دلار محاسباتی (T)</th><th>اختلاف با بازار</th><th>وزن</th></tr>'
        cr_rows = ""
        for _cr_sym in ["AED", "EUR", "GBP", "CHF", "CAD", "TRY", "CNY"]:
            _cr = _cross_rates.get(_cr_sym)
            if not _cr:
                continue
            _cr_class = "rb" if _cr["diff_pct"] < -1 else ("rs" if _cr["diff_pct"] > 1 else "rw")
            _cr_icon = "🟢" if _cr["diff_pct"] < -1 else ("🔴" if _cr["diff_pct"] > 1 else "🟡")
            cr_rows += f'<tr class="{_cr_class}"><td>{_cr["emoji"]} {_cr["name"]}</td>'
            cr_rows += f'<td>{fmt(_cr["iran_price"])}</td>'
            cr_rows += f'<td>{_cr["rate"]:.4f}</td>'
            cr_rows += f'<td>{_cr["rate_source"]}</td>'
            cr_rows += f'<td>{fmt(_cr["calc_usd"])}</td>'
            cr_rows += f'<td>{_cr_icon} {_cr["diff_pct"]:+.2f}%</td>'
            cr_rows += f'<td>{_cr["weight"]*100:.0f}%</td></tr>'
        st.markdown(f'<table class="dtbl">{cr_header}{cr_rows}</table>', unsafe_allow_html=True)

        # Consensus
        st.markdown("<br>", unsafe_allow_html=True)
        cmc = st.columns(3)
        with cmc[0]:
            render_m("🎯 اجماع وزنی (Consensus)", f"{fmt(_consensus_usd)} T",
                     f"میانگین وزنی {len(_cross_rates)} ارز")
        with cmc[1]:
            render_m("💵 دلار بازار آزاد", f"{fmt(dollar)} T", "bonbast.com")
        with cmc[2]:
            _cons_icon = "🟢 ارزان" if _cons_diff_pct < -0.5 else ("🔴 گران" if _cons_diff_pct > 0.5 else "🟡 عادی")
            render_m("📊 اختلاف اجماع", f"{_cons_diff_pct:+.2f}%", _cons_icon)

        # Signal agreement — directional analysis
        _agree_buy = sum(1 for cr in _cross_rates.values() if cr["diff_pct"] < -0.3)
        _agree_sell = sum(1 for cr in _cross_rates.values() if cr["diff_pct"] > 0.3)
        _agree_neutral = len(_cross_rates) - _agree_buy - _agree_sell
        # Directional: how many show dollar below fair value (any amount)
        _dir_below = sum(1 for cr in _cross_rates.values() if cr["diff_pct"] < 0)
        _dir_above = sum(1 for cr in _cross_rates.values() if cr["diff_pct"] > 0)
        if _dir_below == len(_cross_rates):
            _agree_text = '✅ <strong>اجماع کامل خرید</strong> — تمام ارزها دلار آزاد را زیر ارزش نشان می‌دهند'
        elif _agree_buy > _agree_sell and _agree_buy >= len(_cross_rates) // 2:
            _agree_text = '✅ <strong>اجماع خرید</strong> — اکثریت ارزها دلار آزاد را ارزان نشان می‌دهند'
        elif _dir_above == len(_cross_rates):
            _agree_text = '⚠️ <strong>اجماع کامل فروش</strong> — تمام ارزها دلار آزاد را بالای ارزش نشان می‌دهند'
        elif _agree_sell > _agree_buy and _agree_sell >= len(_cross_rates) // 2:
            _agree_text = '⚠️ <strong>اجماع فروش</strong> — اکثریت ارزها دلار آزاد را گران نشان می‌دهند'
        elif _dir_below > _dir_above:
            _agree_text = f'📊 <strong>تمایل به خرید</strong> — {_dir_below} از {len(_cross_rates)} ارز دلار را زیر ارزش نشان می‌دهند'
        elif _dir_above > _dir_below:
            _agree_text = f'📊 <strong>تمایل به فروش</strong> — {_dir_above} از {len(_cross_rates)} ارز دلار را بالای ارزش نشان می‌دهند'
        else:
            _agree_text = '📊 <strong>نظرات متفاوت</strong> — ارزها توافق ندارند — احتیاط بیشتر'
        st.markdown(f"""<div class="hint">
            <strong>توافق ارزها:</strong>
            🟢 ارزان: {_agree_buy} ارز |
            🟡 خنثی: {_agree_neutral} ارز |
            🔴 گران: {_agree_sell} ارز |
            جهت: {_dir_below}↓ / {_dir_above}↑<br>
            {_agree_text}
        </div>""", unsafe_allow_html=True)
    else:
        st.warning("⚠️ داده‌های کافی برای تحلیل چند ارزی در دسترس نیست.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Spread Analysis ──
    st.markdown('<div class="rtl"><h3>📈 تحلیل اسپرد (Spread Analysis)</h3></div>', unsafe_allow_html=True)
    _aed_spread = ((_aed_sell - _aed_buy) / _aed_buy * 100) if _aed_buy > 0 else 0
    _usd_spread = ((dollar - _usd_buy) / _usd_buy * 100) if _usd_buy > 0 else 0

    smc = st.columns(4)
    with smc[0]:
        render_m("اسپرد درهم", f"{_aed_spread:.2f}%",
                 f"خرید: {fmt(_aed_buy)} | فروش: {fmt(_aed_sell)}")
    with smc[1]:
        render_m("اسپرد دلار", f"{_usd_spread:.2f}%",
                 f"خرید: {fmt(_usd_buy)} | فروش: {fmt(dollar)}")
    with smc[2]:
        render_m("محدوده دلار از درهم",
                 f"{fmt(_usd_from_aed_buy)} — {fmt(_usd_from_aed_sell)} T",
                 "از خرید/فروش درهم")
    with smc[3]:
        _spread_diff = abs(_aed_spread - _usd_spread)
        _spread_icon = "🟢 عادی" if _spread_diff < 0.5 else ("🟡 توجه" if _spread_diff < 1 else "🔴 غیرعادی")
        render_m("تفاوت اسپردها", f"{_spread_diff:.2f}%", _spread_icon)

    if _aed_spread > 1.5:
        st.markdown(f"""<div class="hint" style="border-right-color:#e74c3c">
            ⚠️ <strong>اسپرد درهم بالا ({_aed_spread:.2f}%)</strong> — نشان‌دهنده نوسان بازار یا کمبود عرضه.
            در این شرایط سیگنال‌ها ممکن است کم‌دقت باشند.
        </div>""", unsafe_allow_html=True)

    # Arbitrage detection
    if abs(_aed_diff_pct) > 2:
        _arb_type = "خرید دلار / فروش درهم" if _aed_diff_pct < 0 else "فروش دلار / خرید درهم"
        st.markdown(f"""<div class="hint" style="border-right-color:#f1c40f">
            💰 <strong>فرصت آربیتراژ:</strong> اختلاف {abs(_aed_diff_pct):.2f}% — {_arb_type}<br>
            وقتی اختلاف بین نرخ درهمی و بازار آزاد بالای ۲% باشد، فرصت آربیتراژ وجود دارد.
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Method Comparison ──
    st.markdown('<div class="rtl"><h3>🔄 مقایسه روش‌ها</h3></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint" style="font-size:12px">
        مقایسه دو روش مستقل تحلیل ارزش دلار. اگر هر دو روش سیگنال یکسان بدهند، اعتبار بالاتر.
    </div>""", unsafe_allow_html=True)

    mmc = st.columns(3)
    with mmc[0]:
        render_m("📡 روش درهم (لحظه‌ای)", f"{fmt(_usd_from_aed_sell)} T",
                 f"اختلاف: {_aed_diff_pct:+.1f}%")
    with mmc[1]:
        render_m("🌍 اجماع چند ارزی", f"{fmt(_consensus_usd)} T",
                 f"اختلاف: {_cons_diff_pct:+.1f}%" if _consensus_usd > 0 else "—")
    with mmc[2]:
        render_m("💵 قیمت بازار آزاد", f"{fmt(dollar)} T", "bonbast.com")

    # Combined multi-method recommendation
    # ═══ Tier 1: Strong individual signals (strict thresholds) ═══
    _m_buy_strong = sum([
        _aed_diff_pct < -1.0,
        _cons_diff_pct < -1.0 if _consensus_usd > 0 else False
    ])
    _m_sell_strong = sum([
        _aed_diff_pct > 1.0,
        _cons_diff_pct > 1.0 if _consensus_usd > 0 else False
    ])
    _m_total = 2 if _consensus_usd > 0 else 1

    # ═══ Tier 2: Directional consensus (both methods agree on direction) ═══
    _all_below = all([
        _aed_diff_pct < -0.2,
        (_cons_diff_pct < -0.2 if _consensus_usd > 0 else True)
    ])
    _all_above = all([
        _aed_diff_pct > 0.2,
        (_cons_diff_pct > 0.2 if _consensus_usd > 0 else True)
    ])
    _avg_dev = (_aed_diff_pct + (_cons_diff_pct if _consensus_usd > 0 else 0)) / _m_total

    # ═══ Status labels for each method ═══
    _aed_lbl = f"درهم: {_aed_diff_pct:+.1f}% {'✅' if _aed_diff_pct < -0.3 else ('⚠️' if _aed_diff_pct > 0.3 else '➖')}"
    _cons_lbl = f"اجماع: {_cons_diff_pct:+.1f}% {'✅' if _cons_diff_pct < -0.3 else ('⚠️' if _cons_diff_pct > 0.3 else '➖')}"

    if _m_buy_strong >= 2:
        render_sig("b", "خرید قوی — تأیید هر دو روش",
                   f"هر دو روش سیگنال خرید قوی می‌دهند (میانگین: {_avg_dev:+.1f}%)",
                   ["خرید پله‌ای دلار — اعتبار بسیار بالا",
                    _aed_lbl, _cons_lbl],
                   "🔀 ترکیبی")
    elif _m_sell_strong >= 2:
        render_sig("s", "فروش قوی — تأیید هر دو روش",
                   f"هر دو روش سیگنال فروش قوی می‌دهند (میانگین: {_avg_dev:+.1f}%)",
                   ["فروش بخشی از دلار — اعتبار بسیار بالا",
                    _aed_lbl, _cons_lbl],
                   "🔀 ترکیبی")
    elif _all_below and _avg_dev < -0.5:
        render_sig("b",
                   f"خرید — هر دو روش دلار را زیر ارزش نشان می‌دهند",
                   f"هر دو روش تحلیلی جهت خرید دارند (میانگین اختلاف: {_avg_dev:+.1f}%)",
                   ["اجماع جهتی: هر دو روش قیمت بازار را زیر ارزش واقعی می‌دانند",
                    "خرید پله‌ای توصیه می‌شود",
                    _aed_lbl, _cons_lbl],
                   "🔀 ترکیبی")
    elif _all_above and _avg_dev > 0.5:
        render_sig("s",
                   f"فروش — هر دو روش دلار را بالای ارزش نشان می‌دهند",
                   f"هر دو روش تحلیلی جهت فروش دارند (میانگین اختلاف: {_avg_dev:+.1f}%)",
                   ["اجماع جهتی: هر دو روش قیمت بازار را بالای ارزش واقعی می‌دانند",
                    "فروش بخشی از دلار توصیه می‌شود",
                    _aed_lbl, _cons_lbl],
                   "🔀 ترکیبی")
    elif _all_below:
        render_sig("b",
                   f"تمایل به خرید — جهت روش‌ها هم‌سو",
                   f"هر دو روش دلار را زیر ارزش نشان می‌دهند (میانگین: {_avg_dev:+.1f}%) ولی فاصله کم",
                   ["جهت مثبت ولی اختلاف جزئی — خرید با احتیاط",
                    _aed_lbl, _cons_lbl],
                   "🔀 ترکیبی")
    elif _all_above:
        render_sig("w",
                   f"تمایل به فروش — جهت روش‌ها هم‌سو",
                   f"هر دو روش دلار را بالای ارزش نشان می‌دهند (میانگین: {_avg_dev:+.1f}%) ولی فاصله کم",
                   ["جهت منفی — از خرید خودداری کنید",
                    _aed_lbl, _cons_lbl],
                   "🔀 ترکیبی")
    elif _m_buy_strong >= 1 and _avg_dev < -0.3:
        render_sig("b",
                   f"تمایل به خرید — حداقل یک روش سیگنال قوی دارد",
                   f"میانگین اختلاف {_avg_dev:+.1f}% — دلار کمی زیر ارزش",
                   [_aed_lbl, _cons_lbl,
                    "خرید با احتیاط — پله‌ای"],
                   "🔀 ترکیبی")
    elif _m_sell_strong >= 1 and _avg_dev > 0.3:
        render_sig("w",
                   f"تمایل به فروش — حداقل یک روش سیگنال قوی دارد",
                   f"میانگین اختلاف {_avg_dev:+.1f}% — دلار کمی بالای ارزش",
                   [_aed_lbl, _cons_lbl,
                    "از خرید خودداری کنید"],
                   "🔀 ترکیبی")
    else:
        render_sig("w", "خنثی — بازار متعادل",
                   f"میانگین اختلاف {_avg_dev:+.1f}% — سیگنال مشخصی وجود ندارد",
                   [_aed_lbl, _cons_lbl,
                    "رصد روزانه تا فرصت مشخص شود"],
                   "🔀 ترکیبی")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Formula & Education ──
    with st.expander("📐 فرمول‌ها و توضیحات"):
        _eur_rate_val = _forex.get('EUR', 0)
        _eur_iran_val = IRAN_CUR.get('EUR', 0)
        _eur_calc_val = calc_cross_rate_usd(_eur_iran_val, _eur_rate_val) if _eur_rate_val > 0 else 0
        st.markdown(f"""<div class="formula"><strong>روش ۱: درهم (اصلی — لحظه‌ای)</strong><br>
دلار محاسباتی = نرخ درهم × {AED_USD_PEG}<br>
مثال: {fmt(_aed_sell)} × {AED_USD_PEG} = {fmt(_usd_from_aed_sell)} T<br>
اختلاف = (دلار بازار − دلار محاسباتی) ÷ دلار محاسباتی × ۱۰۰<br>
= ({fmt(dollar)} − {fmt(_usd_from_aed_sell)}) ÷ {fmt(_usd_from_aed_sell)} × ۱۰۰ = {_aed_diff_pct:+.2f}%<br><br>

<strong>روش ۲: نرخ متقاطع (Cross-Rate)</strong><br>
دلار = نرخ ارز در ایران × نرخ جهانی (واحد ارز/دلار)<br>
مثال یورو: {fmt(_eur_iran_val)} × {_eur_rate_val:.4f} = {fmt(_eur_calc_val)} T<br><br>

<strong>روش ۳: اجماع وزنی</strong><br>
میانگین وزنی = Σ(دلار محاسباتی هر ارز × وزن) ÷ Σ(وزن)<br>
وزن‌ها: درهم ۵۰% | یورو ۲۰% | پوند ۱۰% | فرانک ۱۰% | سایر ۱۰%<br>
اجماع = {fmt(_consensus_usd)} T</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="hint">
            <strong>چرا درهم مهم‌ترین شاخص است؟</strong><br>
            ۱. درهم با نرخ ثابت {AED_USD_PEG} به دلار پگ شده — رابطه قطعی و بدون نوسان جهانی<br>
            ۲. ≈ ۸۵% مبادلات ارزی ایران از طریق امارات (دوبی) انجام می‌شود<br>
            ۳. درهم نقدشونده‌ترین ارز پس از دلار در بازار ایران<br>
            ۴. صرافی‌ها معمولاً درهم را با اسپرد کمتری معامله می‌کنند<br><br>
            <strong>اجماع چند ارزی (تقویت سیگنال):</strong><br>
            • ارزش دلار از مسیر ۷ ارز مختلف محاسبه و مقایسه می‌شود<br>
            • اگر درهم و اجماع هر دو جهت خرید یا فروش نشان دهند، اعتبار سیگنال بالاتر است<br><br>
            <strong>محدودیت‌ها:</strong><br>
            • در شرایط تحریم شدید، پگ در بازار ایران ممکن است کاملاً حفظ نشود<br>
            • هزینه حواله و کارمزد صرافی در محاسبات لحاظ نشده<br>
            • نوسانات لحظه‌ای ممکن است اختلاف موقت ایجاد کنند
        </div>""", unsafe_allow_html=True)

        st.markdown("""<table class="dtbl"><tr><th>اختلاف</th><th>سیگنال</th><th>اقدام</th></tr>
<tr class="rb"><td>زیر −۲.۵%</td><td>🟢🟢</td><td>خرید قوی دلار</td></tr>
<tr class="rb"><td>−۲.۵% تا −۱%</td><td>🟢</td><td>خرید دلار</td></tr>
<tr class="rw"><td>−۱% تا +۱%</td><td>🟡</td><td>متعادل (حد هزینه تراکنش)</td></tr>
<tr class="rs"><td>+۱% تا +۲.۵%</td><td>🔴</td><td>احتیاط — نخرید</td></tr>
<tr class="rs"><td>بالای +۲.۵%</td><td>🔴🔴</td><td>فروش دلار</td></tr></table>""", unsafe_allow_html=True)

    st.markdown("""<div class="disc">
    ⚠️ <strong>توجه:</strong> این تحلیل بر اساس نرخ لحظه‌ای بازار آزاد و پگ ثابت درهم-دلار است.
    سیگنال‌ها ابزار کمکی هستند — تصمیم نهایی بر عهده شماست.
    </div>""", unsafe_allow_html=True)

# ── TAB 4: CALCULATORS ───────────────
with tab4:
    st.markdown('<div class="rtl"><h2>🔢 ماشین‌حساب طلا</h2></div>', unsafe_allow_html=True)
    ct1, ct2, ct3 = st.tabs(["💰 طلای ۱۸ عیار", "⚖️ مظنه→گرم", "🔄 عیار متفاوت"])

    with ct1:
        theo = calc_gold_18k(ounce, dollar); d18 = g18 - theo
        p18 = (d18 / theo * 100) if theo > 0 else 0
        c1, c2, c3 = st.columns(3)
        c1.metric("قیمت تئوری (بر اساس انس و دلار)", f"{fmt(theo)} T")
        c2.metric("قیمت واقعی بازار ایران", f"{fmt(g18)} T")
        c3.metric("اختلاف بازار با ارزش واقعی", f"{p18:+.2f}%", f"{fmt(d18)} T")
        if p18 < 1:
            st.success("✅ **قیمت بازار منصفانه است** — قیمت فعلی نزدیک به ارزش واقعی جهانی طلاست. اگر قصد خرید دارید زمان مناسبی است.")
        elif p18 < 3:
            st.warning(f"⚠️ **بازار {p18:.1f}% گران‌تر از ارزش واقعی** — قیمت کمی بالاتر از ارزش جهانی. خرید قابل قبول ولی ایده‌آل نیست.")
        else:
            st.error(f"❌ **بازار {p18:.1f}% گران‌تر از ارزش واقعی** — قیمت طلا در ایران بالاتر از قیمت جهانی. بهتر است صبر کنید تا اختلاف کمتر شود.")

    with ct2:
        st.markdown('<div class="formula">۱ گرم ۱۸ عیار = مظنه ÷ 4.3318</div>', unsafe_allow_html=True)
        gram = moz / 4.3318 if moz > 0 else 0
        st.metric("قیمت ۱ گرم ۱۸ عیار", f"{fmt(gram)} تومان")

    with ct3:
        dc1, dc2 = st.columns(2)
        with dc1: kw = st.number_input("وزن (گرم)", value=10.0, min_value=0.1, step=0.5, format="%.1f")
        with dc2: kv = st.number_input("عیار", value=17.2, min_value=1.0, max_value=24.0, step=0.1, format="%.1f")
        price = (kv / 18.0) * kw * g18; eq = kw * (kv / 18.0)
        c1, c2 = st.columns(2)
        c1.metric("ارزش کل", f"{fmt(price)} تومان")
        c2.metric("معادل ۱۸ عیار", f"{eq:.2f} گرم")

# ── TAB 5: CURRENCY EXCHANGE ─────────
with tab5:
    st.markdown('<div class="rtl"><h2>💱 تحلیل تبدیل ارز</h2></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint">
        نرخ جهانی <strong>خودکار</strong> (ECB) | قیمت ایران <strong>خودکار</strong> (bonbast.com)<br>
        مقایسه ارزش واقعی با بازار ایران + روند هفتگی</div>""", unsafe_allow_html=True)

    CUR_INFO = {
        "EUR": {"name": "یورو", "em": "🇪🇺"},
        "GBP": {"name": "پوند", "em": "🇬🇧"},
        "CHF": {"name": "فرانک سوئیس", "em": "🇨🇭"},
        "TRY": {"name": "لیر ترکیه", "em": "🇹🇷"},
        "AED": {"name": "درهم امارات", "em": "🇦🇪"},
        "CAD": {"name": "دلار کانادا", "em": "🇨🇦"},
        "CNY": {"name": "یوآن چین", "em": "🇨🇳"},
    }

    for sym, ci in CUR_INFO.items():
        rate = _forex.get(sym)
        if not rate: continue
        usd_per = 1.0 / rate
        fair = usd_per * dollar
        iran_p = IRAN_CUR.get(sym, int(fair))
        iran_p = st.number_input(f"{ci['em']} {ci['name']} — بازار ایران (تومان)",
                                  value=iran_p, step=100, key=f"cur_{sym}",
                                  help="خودکار از bonbast.com — اصلاح دستی در صورت نیاز")
        prem = iran_p - fair; ppct = (prem / fair * 100) if fair > 0 else 0
        tr = trend_analysis(forex_hist, sym)

        mc = st.columns(4)
        with mc[0]: render_m("نرخ جهانی", f"1{sym}=${usd_per:.4f}")
        with mc[1]: render_m("ارزش واقعی", f"{fmt(fair)} T")
        with mc[2]: render_m("بازار ایران", f"{fmt(iran_p)} T")
        with mc[3]: render_m("پرمیوم", f"{ppct:+.1f}%", f"{fmt(prem)} T")

        acts = []
        if ppct < -2:
            sig = "b"; ttl = f"{ci['name']} در ایران ارزان‌تر از ارزش واقعی"
            acts = [f"خرید {ci['name']} سودمند ({abs(ppct):.1f}% تخفیف)", "تبدیل دلار به این ارز منطقی است"]
        elif ppct > 4:
            sig = "s"; ttl = f"{ci['name']} در ایران گران"
            acts = [f"از خرید خودداری کنید ({ppct:.1f}% گران‌تر)", "اگر دارید بفروشید و دلار بخرید"]
        elif ppct > 1.5:
            sig = "w"; ttl = f"{ci['name']} کمی گران‌تر"
            acts = ["صبر تا پرمیوم کاهش یابد"]
        else:
            sig = "i"; ttl = f"{ci['name']} قیمت عادی"
            acts = ["اختلاف ناچیز — تصمیم بر اساس نیاز شخصی"]
        if tr:
            d_fa = "تقویت 💪" if tr["dir"] == "down" else "تضعیف 📉"
            acts.append(f"روند هفتگی: دلار در برابر {ci['name']} {d_fa} ({tr['chg']:+.2f}%)")
        render_sig(sig, ttl, f"پرمیوم: {ppct:+.1f}% | 1{sym} = ${usd_per:.4f}", acts, f"💱 {sym}")
        st.markdown("---")

# ── TAB 6: PORTFOLIO ──────────────────
with tab6:
    st.markdown('<div class="rtl"><h2>💼 مدیریت سبد سرمایه</h2></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint">تمام دارایی‌هایتان را وارد کنید.
    سیستم بهترین اقدام را بر اساس سیگنال‌های فعلی پیشنهاد می‌دهد.</div>""", unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        st.markdown("##### 💵 ارزها")
        h_usd = st.number_input("دلار", value=100.0, min_value=0.0, step=10.0, format="%.2f", key="p_usd")
        h_eur = st.number_input("یورو", value=0.0, min_value=0.0, step=10.0, format="%.2f", key="p_eur")
        h_gbp = st.number_input("پوند", value=0.0, min_value=0.0, step=10.0, format="%.2f", key="p_gbp")
        h_irr = st.number_input("تومان نقد", value=0, min_value=0, step=1_000_000, key="p_irr")
    with pc2:
        st.markdown("##### 🥇 طلا")
        h_gold = st.number_input("آب شده ۱۸ عیار (گرم)", value=0.0, min_value=0.0, step=0.5, format="%.2f", key="p_gold")
        h_coin_e = st.number_input("سکه امامی (عدد)", value=0, min_value=0, step=1, key="p_ce")
        h_coin_n = st.number_input("نیم سکه (عدد)", value=0, min_value=0, step=1, key="p_cn")
        h_coin_r = st.number_input("ربع سکه (عدد)", value=0, min_value=0, step=1, key="p_cr")
        h_coin_g = st.number_input("سکه گرمی (عدد)", value=0, min_value=0, step=1, key="p_cg")
    with pc3:
        st.markdown("##### 💰 پس‌انداز")
        monthly = st.number_input("پس‌انداز ماهانه (تومان)", value=15_000_000, min_value=0, step=1_000_000, key="p_m")

    eur_usd = 1.0 / _forex.get("EUR", 0.84) if _forex.get("EUR") else 1.19
    gbp_usd = 1.0 / _forex.get("GBP", 0.73) if _forex.get("GBP") else 1.37

    vals = [
        ("💵 دلار", h_usd * dollar),
        ("💶 یورو", h_eur * eur_usd * dollar),
        ("💷 پوند", h_gbp * gbp_usd * dollar),
        ("🥇 آب شده", h_gold * g18),
        ("🪙 سکه امامی", h_coin_e * emami),
        ("🪙 نیم سکه", h_coin_n * nim_p),
        ("🪙 ربع سکه", h_coin_r * rob_p),
        ("🪙 سکه گرمی", h_coin_g * ger_p),
        ("💰 تومان نقد", h_irr),
    ]
    total = sum(v for _, v in vals)

    if total > 0:
        tusd = total / dollar
        st.markdown("---")
        st.metric("💎 ارزش کل سبد", f"{fmt(total)} تومان", f"≈ ${tusd:,.0f}")

        rows = [{"دارایی": n, "ارزش": fmt(v) + " T", "سهم": f"{v/total*100:.1f}%"}
                for n, v in vals if v > 0]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ══════════════════════════════════════════════
        # SMART ADVISOR ENGINE v2 — cross-asset signals
        # ══════════════════════════════════════════════
        st.markdown("---")
        st.markdown('<div class="rtl"><h3>🧠 توصیه‌های هوشمند — چه بفروشم، چه بخرم؟</h3></div>',
                    unsafe_allow_html=True)

        # Portfolio composition
        usd_val = h_usd * dollar
        eur_val = h_eur * eur_usd * dollar
        gbp_val = h_gbp * gbp_usd * dollar
        gold_val = h_gold * g18
        coin_val = h_coin_e * emami + h_coin_n * nim_p + h_coin_r * rob_p + h_coin_g * ger_p
        usd_pct = (usd_val / total * 100) if total > 0 else 0
        gold_all_pct = ((gold_val + coin_val) / total * 100) if total > 0 else 0
        cash_pct = (h_irr / total * 100) if total > 0 else 0
        has_coin = h_coin_e > 0 or h_coin_n > 0 or h_coin_r > 0 or h_coin_g > 0
        gs_t, _ = gold_sig(gdiff_pct)

        best_rec = None  # (typ, title, desc, acts_list)
        recs = []        # list of (typ, title, desc, acts_list)

        # ═══ 1. GOLDEN CYCLE (highest priority) ═══
        if has_coin and bpct_e >= 25 and gs_t == "b":
            gold_grams = coin_val / g18 if g18 > 0 else 0
            best_rec = ("b",
                "🔄 چرخه طلایی: سکه بفروشید، آب شده بخرید",
                f"حباب سکه {bpct_e:.1f}% (بالا) + آب شده {gdiff_pct:.1f}% (ارزان)",
                [f"سکه‌ها بفروشید (ارزش: ~{fmt(coin_val)} T)",
                 f"فوراً ~{gold_grams:.1f}g آب شده ۱۸ عیار بخرید",
                 "وزن طلای شما افزایش می‌یابد — تکرار در هر چرخه"])

        # ═══ 2. COIN SELLS → explicit destination ═══
        if not best_rec:
            for cn, bp_v, qty, pr in [
                ("سکه امامی", bpct_e, h_coin_e, emami),
                ("نیم سکه", CB.get("نیم سکه", 0), h_coin_n, nim_p),
                ("ربع سکه", CB.get("ربع سکه", 0), h_coin_r, rob_p),
                ("سکه گرمی", CB.get("سکه گرمی", 0), h_coin_g, ger_p)]:
                if qty > 0 and bp_v >= 25:
                    sell_v = qty * pr
                    if gs_t == "b":
                        grams = sell_v / g18 if g18 > 0 else 0
                        dest = f"با {fmt(sell_v)} T حاصل، ~{grams:.1f}g آب شده بخرید (ارزان)"
                    else:
                        usd_eq = sell_v / dollar if dollar > 0 else 0
                        dest = f"به ${usd_eq:,.0f} دلار تبدیل کنید (آب شده فعلاً ارزان نیست)"
                    recs.append(("s",
                        f"🪙 {cn} بفروشید — حباب {bp_v:.1f}%",
                        f"ارزش فروش: {fmt(sell_v)} T | سود حباب: ~{fmt(qty * (pr - calc_intrinsic(ounce, dollar, COINS[cn]['w'])))} T",
                        [f"{qty} عدد {cn} بفروشید", dest]))

        # ═══ 3. MELTED GOLD SELL → dollar ═══
        if h_gold > 0 and gs_t == "s":
            sell_v = h_gold * g18
            usd_eq = sell_v / dollar if dollar > 0 else 0
            recs.append(("s",
                f"🥇 آب شده بفروشید — اختلاف {gdiff_pct:.1f}% (گران)",
                f"ارزش: {fmt(sell_v)} T ≈ ${usd_eq:,.0f}",
                [f"{h_gold:.1f}g آب شده بفروشید",
                 f"به ${usd_eq:,.0f} دلار تبدیل کنید",
                 "صبر تا اختلاف زیر ۱% شد دوباره بخرید"]))

        # ═══ 4. CURRENCY SELLS → explicit (EUR/GBP expensive) ═══
        for sym, holding in [("EUR", h_eur), ("GBP", h_gbp)]:
            if holding > 0 and CUR_PREMS.get(sym, 0) > 4:
                name = CUR_NAMES.get(sym, sym)
                prem = CUR_PREMS[sym]
                if gs_t == "b":
                    dest_line = "با تومان حاصل آب شده بخرید (ارزان — دوطرفه سود)"
                else:
                    dest_line = "به دلار تبدیل کنید (ارزش بیشتر از نگه داشتن ارز)"
                recs.append(("s",
                    f"💱 {name} بفروشید — {prem:.1f}% گران‌تر از ارزش واقعی",
                    f"موجودی: {holding:.1f} {sym}",
                    [f"{name} بفروشید", dest_line]))

        # ═══ 5. USD → GOLD (gold cheap, user has dollars) ═══
        if h_usd >= 50 and gs_t == "b" and not best_rec:
            sell_usd = round(min(h_usd * 0.3, h_usd))
            gold_buy = (sell_usd * dollar) / g18 if g18 > 0 else 0
            recs.append(("b",
                f"💵 دلار بفروشید، آب شده بخرید — اختلاف فقط {gdiff_pct:.1f}%",
                f"پیشنهاد: {sell_usd}$ از {h_usd:.0f}$ (۳۰%) ≈ {gold_buy:.1f}g طلا",
                [f"{sell_usd} دلار بفروشید ({fmt(sell_usd * dollar)} T)",
                 f"با تومان حاصل {gold_buy:.1f}g آب شده ۱۸ عیار بخرید",
                 f"باقی {h_usd - sell_usd:.0f}$ نقد نگه دارید (ذخیره)"]))

        # ═══ 6. USD → COIN (coin cheap, gold not cheap) ═══
        if h_usd >= 50 and bpct_e < 13 and gs_t != "b":
            best_cn = min(CB, key=CB.get)
            best_bp = CB[best_cn]
            if best_bp < 13:
                coin_p = CP[best_cn]
                sell_usd = round(min(h_usd * 0.3, h_usd))
                count = int((sell_usd * dollar) // coin_p) if coin_p > 0 else 0
                if count > 0:
                    recs.append(("b",
                        f"💵 دلار بفروشید، {best_cn} بخرید — حباب {best_bp:.1f}%",
                        f"پیشنهاد: {sell_usd}$ ≈ {count} عدد {best_cn}",
                        [f"{sell_usd} دلار بفروشید",
                         f"{count} عدد {best_cn} بخرید (پله‌ای ۳ مرحله)",
                         "صبر تا حباب بالا رفت سپس بفروشید"]))

        # ═══ 7. TOMAN → GOLD/COIN/DOLLAR (user has toman) ═══
        if h_irr > 5_000_000:
            if gs_t == "b":
                grams = h_irr / g18 if g18 > 0 else 0
                recs.append(("b",
                    f"💰 تومان نقد → آب شده بخرید — اختلاف {gdiff_pct:.1f}% (ارزان)",
                    f"بودجه: {fmt(h_irr)} T ≈ {grams:.1f}g طلا",
                    [f"با {fmt(h_irr)} T آب شده بخرید (پله‌ای)",
                     "آب شده نزدیک ارزش جهانی — فرصت مناسب"]))
            elif bpct_e < 13:
                best_cn = min(CB, key=CB.get)
                coin_p = CP[best_cn]
                count = int(h_irr // coin_p) if coin_p > 0 else 0
                if count > 0:
                    recs.append(("b",
                        f"💰 تومان نقد → {best_cn} بخرید — حباب {CB[best_cn]:.1f}%",
                        f"{count} عدد قابل خرید",
                        [f"با {fmt(h_irr)} T {best_cn} بخرید",
                         "سکه ارزان — خرید پله‌ای"]))
            elif cash_pct > 30:
                usd_eq = h_irr / dollar if dollar > 0 else 0
                recs.append(("w",
                    f"💰 تومان نقد زیاد ({cash_pct:.0f}% سبد) → دلار بخرید",
                    f"معادل ${usd_eq:,.0f}",
                    [f"بخشی از {fmt(h_irr)} T را دلار بخرید",
                     "تورم ارزش تومان را کاهش می‌دهد",
                     "حداقل ۳۰% سبد ارز خارجی باشد"]))
        elif h_irr > 0 and cash_pct > 50:
            recs.append(("w",
                f"💰 تومان {cash_pct:.0f}% سبد — بیش از حد",
                "ریسک تورم",
                ["فوراً بخشی را دلار بخرید"]))

        # ═══ 8. USD → CHEAP FOREIGN CURRENCY (arbitrage) ═══
        if h_usd > 100:
            best_cur = None; best_disc = 0
            for sym, prem in CUR_PREMS.items():
                if prem < -2 and prem < best_disc:
                    best_cur = sym; best_disc = prem
            if best_cur:
                name = CUR_NAMES.get(best_cur, best_cur)
                recs.append(("b",
                    f"💱 دلار → {name} — {abs(best_disc):.1f}% ارزان‌تر از ارزش واقعی",
                    "فرصت آربیتراژ",
                    [f"بخشی از دلار بفروشید و {name} بخرید",
                     f"{name} در ایران {abs(best_disc):.1f}% زیر ارزش جهانی است"]))

        # ═══ 9. EUR/GBP → GOLD cross-signal (only 2-4% range, >4% handled in section 4) ═══
        for sym, holding in [("EUR", h_eur), ("GBP", h_gbp)]:
            prem = CUR_PREMS.get(sym, 0)
            if holding > 0 and 2 < prem <= 4 and gs_t == "b":
                name = CUR_NAMES.get(sym, sym)
                recs.append(("b",
                    f"💱🥇 {name} بفروشید، آب شده بخرید — دوطرفه سود",
                    f"{name} کمی گران ({prem:.1f}%) + آب شده ارزان ({gdiff_pct:.1f}%)",
                    [f"{name} بفروشید (پرمیوم {prem:.1f}%)",
                     "تومان حاصل را آب شده بخرید",
                     "هم از فروش گران سود می‌برید هم از خرید ارزان"]))

        # ═══ 10. RISK & DIVERSIFICATION ═══
        if usd_pct > 50:
            acts = ["قانون ۳۰%: حداکثر ۳۰% در یک دارایی"]
            if gs_t == "b": acts.append("بخشی به آب شده تبدیل کنید (ارزان)")
            elif bpct_e < 13: acts.append("بخشی به سکه تبدیل کنید (حباب پایین)")
            else: acts.append("فعلاً نگه دارید ولی در فرصت مناسب تنوع بدهید")
            recs.append(("i", f"⚠️ دلار {usd_pct:.0f}% سبد — تمرکز زیاد", "", acts))
        if gold_all_pct > 50:
            recs.append(("i", f"⚠️ طلا {gold_all_pct:.0f}% سبد — تمرکز زیاد", "",
                ["بخشی بفروشید و دلار نقد نگه دارید"]))
        if total > 0 and (cash_pct + usd_pct) < 10:
            recs.append(("i", "⚠️ نقدینگی اضطراری کم", "کمتر از ۱۰% نقد/دلار",
                ["حداقل ۱۰% سبد نقد (تومان یا دلار) نگه دارید"]))

        # ═══ RENDER ═══
        if best_rec:
            render_sig(best_rec[0], best_rec[1], best_rec[2], best_rec[3], "⭐ بهترین اقدام")
        if recs:
            for r in recs:
                render_sig(r[0], r[1], r[2], r[3], "💡 پیشنهاد")
        elif not best_rec:
            render_sig("w", "فعلاً اقدام خاصی توصیه نمی‌شود", "بازار را رصد کنید", lbl="💡")

        # Projection
        if monthly > 0:
            st.markdown("---")
            st.markdown('<div class="rtl"><h4>📈 پیش‌بینی ۱۲ ماه</h4></div>', unsafe_allow_html=True)
            rows = []
            for m in range(1, 13):
                proj = total + monthly * m; pusd = proj / dollar
                ms = ""
                prev = total + monthly * (m - 1)
                if pusd >= 500 and prev / dollar < 500: ms = "🎯 چرخه سکه-طلا"
                elif pusd >= 300 and prev / dollar < 300: ms = "🎯 ورود به طلا"
                elif pusd >= 200 and prev / dollar < 200: ms = "🎯 تنوع‌بخشی"
                rows.append({"ماه": m, "ارزش": fmt(proj)+" T", "≈$": f"${pusd:,.0f}",
                             "≈طلا": f"{proj/g18:.1f}g", "عطف": ms})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("دارایی‌هایتان را وارد کنید تا تحلیل نمایش داده شود.")

# ── TAB 7: DCA PLANNER ───────────────
with tab7:
    st.markdown('<div class="rtl"><h2>📉 برنامه‌ریزی خرید پله‌ای (DCA)</h2></div>', unsafe_allow_html=True)
    st.markdown("""<div class="hint">
        <strong>خرید پله‌ای (Dollar Cost Averaging)</strong> یعنی به‌جای خرید یکجا،
        سرمایه را در چند مرحله و در زمان‌های مختلف خرج کنید.
        این کار میانگین قیمت خرید را بهینه می‌کند و ریسک را کاهش می‌دهد.<br><br>
        <strong>📐 فرمول:</strong> میانگین = مجموع تومان پرداختی ÷ مجموع واحد خریداری شده
    </div>""", unsafe_allow_html=True)

    asset_type = st.selectbox("نوع دارایی برای خرید پله‌ای", [
        "💵 دلار", "💶 یورو", "💷 پوند", "🥇 طلای آب شده (گرم)",
        "🪙 سکه امامی", "🪙 نیم سکه", "🪙 ربع سکه", "🪙 سکه گرمی",
    ])

    # Current price for selected asset
    asset_prices = {
        "💵 دلار": ("دلار", dollar, "bonbast.com → US Dollar"),
        "💶 یورو": ("یورو", _eur_sell, "bonbast.com → Euro"),
        "💷 پوند": ("پوند", _gbp_sell, "bonbast.com → British Pound"),
        "🥇 طلای آب شده (گرم)": ("گرم ۱۸ عیار", g18, "tgju.org → طلای ۱۸ عیار"),
        "🪙 سکه امامی": ("سکه", emami, "tgju.org → سکه امامی"),
        "🪙 نیم سکه": ("نیم سکه", nim_p, "tgju.org → نیم سکه"),
        "🪙 ربع سکه": ("ربع سکه", rob_p, "tgju.org → ربع سکه"),
        "🪙 سکه گرمی": ("سکه گرمی", ger_p, "tgju.org → سکه گرمی"),
    }
    unit_name, current_price, price_hint = asset_prices[asset_type]
    st.markdown(f'<div class="hint" style="font-size:12px">قیمت فعلی {unit_name}: '
                f'<strong>{fmt(current_price)} تومان</strong> (منبع: {price_hint})</div>',
                unsafe_allow_html=True)

    st.markdown("---")

    dca_mode = st.radio("حالت", ["📝 ثبت خریدهای انجام شده", "📅 برنامه‌ریزی خریدهای آینده"],
                        horizontal=True)

    if dca_mode == "📝 ثبت خریدهای انجام شده":
        st.markdown(f"""<div class="hint" style="font-size:12px">
            خریدهای قبلی {unit_name} را وارد کنید تا میانگین قیمت و سود/ضرر محاسبه شود.
        </div>""", unsafe_allow_html=True)

        n_buys = st.slider("تعداد خریدها", 1, 20, 3)
        total_spent = 0; total_units = 0.0

        for i in range(n_buys):
            c1, c2, c3 = st.columns(3)
            with c1:
                amt = st.number_input(f"مبلغ پرداختی خرید {i+1} (T)", value=10_000_000,
                                      min_value=0, step=1_000_000, key=f"dca_a_{i}")
            with c2:
                default_rate = max(1, int(current_price * (1 - i * 0.03)))
                rate = st.number_input(f"نرخ خرید {i+1} (T/{unit_name})", value=default_rate,
                                       min_value=1, step=10000, key=f"dca_r_{i}",
                                       help=f"با چه قیمتی {unit_name} خریدید؟")
            with c3:
                if rate > 0:
                    units = amt / rate
                    st.metric(f"{unit_name} خریداری شده", f"{units:.4f}")
                    total_spent += amt; total_units += units

        if total_units > 0:
            st.markdown("---")
            avg = total_spent / total_units
            cur_val = total_units * current_price
            profit = cur_val - total_spent
            ppct = (profit / total_spent) * 100

            rc = st.columns(4)
            rc[0].metric(f"مجموع {unit_name}", f"{total_units:.4f}")
            rc[1].metric("میانگین قیمت خرید", f"{fmt(avg)} T")
            rc[2].metric("ارزش فعلی", f"{fmt(cur_val)} T")
            if profit >= 0:
                rc[3].metric("سود", f"{fmt(profit)} T", f"+{ppct:.1f}%")
            else:
                rc[3].metric("ضرر", f"{fmt(profit)} T", f"{ppct:.1f}%")

            # DCA benefit comparison
            if n_buys > 1:
                lump_units = total_spent / current_price if current_price > 0 else 0
                diff_u = total_units - lump_units
                if diff_u > 0:
                    st.success(f"✅ خرید پله‌ای سودمند بود! با همین بودجه یکجا فقط {lump_units:.4f} "
                               f"{unit_name} می‌گرفتید ولی شما {total_units:.4f} گرفتید (+{diff_u:.4f})")
                elif diff_u < 0:
                    st.warning(f"⚠️ اگر همه {fmt(total_spent)} T را امروز با نرخ فعلی خریده بودید: "
                               f"{lump_units:.4f} {unit_name} (شما: {total_units:.4f})")
                else:
                    st.info(f"💡 میانگین خرید شما برابر قیمت فعلی بازار است.")

    else:  # Planning mode
        st.markdown(f"""<div class="hint" style="font-size:12px">
            بودجه کل و تعداد مراحل را مشخص کنید تا برنامه خرید ساخته شود.<br>
            <strong>قانون طلایی:</strong> حداقل ۳ مرحله | فاصله هر مرحله حداقل ۱ هفته
        </div>""", unsafe_allow_html=True)

        p1, p2, p3 = st.columns(3)
        with p1:
            total_budget = st.number_input("💰 بودجه کل (تومان)", value=50_000_000,
                                           min_value=1_000_000, step=5_000_000)
        with p2:
            n_steps = st.number_input("تعداد مراحل خرید", value=3, min_value=2, max_value=12, step=1)
        with p3:
            interval = st.selectbox("فاصله بین خریدها", ["هر هفته", "هر ۲ هفته", "هر ماه"])

        per_step = total_budget / n_steps
        units_per = per_step / current_price if current_price > 0 else 0
        total_units_plan = total_budget / current_price if current_price > 0 else 0

        st.markdown("---")
        st.markdown(f'<div class="rtl"><h4>📋 برنامه خرید {unit_name}</h4></div>', unsafe_allow_html=True)

        render_m("مبلغ هر مرحله", f"{fmt(per_step)} T", f"≈ {units_per:.4f} {unit_name}")

        plan_rows = []
        for i in range(int(n_steps)):
            interval_days = {"هر هفته": 7, "هر ۲ هفته": 14, "هر ماه": 30}[interval]
            date = datetime.now() + timedelta(days=i * interval_days)
            plan_rows.append({
                "مرحله": f"{i+1}",
                "تاریخ تقریبی": date.strftime("%Y/%m/%d"),
                "مبلغ (T)": fmt(per_step),
                f"≈{unit_name}": f"{units_per:.4f}",
                "وضعیت": "⏳ آینده" if i > 0 else "📌 اولین خرید",
            })
        st.dataframe(pd.DataFrame(plan_rows), use_container_width=True, hide_index=True)

        st.markdown(f"""<div class="hint">
            <strong>خلاصه:</strong> با {fmt(total_budget)} T در {int(n_steps)} مرحله ({interval})
            ≈ <strong>{total_units_plan:.4f} {unit_name}</strong> خریداری می‌شود (با قیمت فعلی).<br>
            <strong>مزیت:</strong> اگر قیمت نوسان کند، میانگین خرید شما بهینه خواهد بود.
        </div>""", unsafe_allow_html=True)

# ── TAB 8: ROADMAP ────────────────────
with tab8:
    st.markdown('<div class="rtl"><h2>🗺️ نقشه راه</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="phase" style="background:linear-gradient(135deg,#0d3320,#1a3a2e);border-right:5px solid #2ecc71">
        <h3>🌱 فاز ۱: ساخت پایه (ماه ۱ تا ۶)</h3>
        <p><strong>هدف:</strong> رشد سرمایه از ۱۰۰ دلار به ۳۰۰ دلار</p>
        <ul>
            <li>دلار فعلی نگه دارید</li>
            <li>ماهانه ۵۰ تا ۱۰۰ دلار پس‌انداز</li>
            <li>خرید پله‌ای: ۲ تا ۳ نوبت در ماه</li>
            <li>اگر بازار بیش از ۳٪ ریزش کرد، بیشتر بخرید</li>
        </ul>
    </div>
    <div class="phase" style="background:linear-gradient(135deg,#0d2240,#1a3a5f);border-right:5px solid #3498db">
        <h3>🥇 فاز ۲: ورود به طلا (ماه ۶ تا ۱۲)</h3>
        <p><strong>هدف:</strong> خرید اولین طلای آب شده</p>
        <ul>
            <li>فرمول A را هفتگی چک کنید (تب آب شده)</li>
            <li>اگر اختلاف مظنه با عدد A زیر ۱٪ بود: ۲ تا ۳ گرم بخرید</li>
            <li>از مرکز معتبر بخرید و فاکتور بگیرید</li>
            <li>همیشه ۳۰٪ سرمایه را دلار نقد نگه دارید</li>
        </ul>
    </div>
    <div class="phase" style="background:linear-gradient(135deg,#3d2e0d,#4f3d1a);border-right:5px solid #f1c40f">
        <h3>🔄 فاز ۳: چرخه سکه و طلا (ماه ۱۲ به بعد)</h3>
        <p><strong>هدف:</strong> افزایش وزن طلا با چرخه خرید/فروش</p>
        <ul>
            <li>حباب زیر ۱۳٪ ⟵ سکه بخرید</li>
            <li>حباب بالای ۲۵٪ ⟵ سکه بفروشید</li>
            <li>فرمول A اختلاف زیر ۱٪ شد ⟵ آب شده بخرید</li>
            <li><strong>تکرار این چرخه = رشد وزن طلا</strong></li>
        </ul>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="rtl"><h3>⚠️ قوانین ریسک</h3></div>', unsafe_allow_html=True)
    for t, d in [("قانون ۳۰%","بیش از ۳۰% در یک دارایی نباشد"),
                 ("۳ سبد","تقسیم بین دلار+طلا+نقد"),("صبر","۳-۶ ماه برای تصمیم بزرگ"),
                 ("حد ضرر","۱۰% ضرر = بازنگری"),("حد سود","۱۵-۲۰% سود = نقد بخشی"),
                 ("بدون قرض","فقط پس‌انداز"),("پله‌ای","حداقل ۳ مرحله")]:
        st.markdown(f"🔴 **{t}:** {d}")

# ── FOOTER ────────────────────────────
st.markdown("---")
st.markdown("""<div class="disc">⚠️ <strong>سلب مسئولیت:</strong> ابزار آموزشی — سیگنال خرید/فروش نیست.
تصمیمات بر عهده شماست.</div>
<div style="text-align:center;color:#495670;padding:12px;font-size:11px">
🪙 مشاور مالی v4.0 | مهدی غفران | ❤️</div>""", unsafe_allow_html=True)
