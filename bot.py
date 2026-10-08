import telebot
from telebot import types
import requests

TOKEN = "*******"
bot = telebot.TeleBot(TOKEN)

# آدرس کیف‌پول برای پرداخت اشتراک VIP (آدرس تتر خودت رو جایگزین کن)
USDT_TRC20_WALLET = "YOUR_USDT_TRC20_WALLET_ADDRESS_HERE"MY_WALLET = "0xf104a07d8a87f4aa98ea28baf19d727a00666fd1"
MY_WALLET = "0xf104a07d8a87f4aa98ea28baf19d727a00666fd1"


def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,toncoin&vs_currencies=usd&include_24hr_change=true"
        data = requests.get(url, timeout=10).json()
        
        msg = "📊 **قیمت‌های لحظه‌ای بازار:**\n\n"
        coins = {
            "bitcoin": ("🪙 بیت‌کوین (BTC)", "usd", "usd_24h_change"),
            "ethereum": ("🔹 اتریوم (ETH)", "usd", "usd_24h_change"),
            "solana": ("🟣 سولانا (SOL)", "usd", "usd_24h_change"),
            "binancecoin": ("🟡 بایننس‌کوین (BNB)", "usd", "usd_24h_change"),
            "toncoin": ("💎 تون‌کوین (TON)", "usd", "usd_24h_change"),
        }
        
        for key, val in coins.items():
            if key in data:
                price = data[key]['usd']
                chg = data[key].get('usd_24h_change', 0)
                emoji = "🟢" if chg >= 0 else "🔴"
                msg += f"{val[0]}: **${price:,.2f}** ({emoji} {chg:+.2f}%)\n"
        return msg
    except Exception:
        return "❌ خطا در دریافت داده‌های بازار. لطفاً کمی بعد دوباره تلاش کنید."
def check_token_security(address):
    try:
        url = f"https://api.honeypot.is/v2/IsHoneypot?address={address}"
        res = requests.get(url, timeout=10).json()
        
        if "honeypotResult" in res:
            is_hp = res["honeypotResult"].get("isHoneypot", False)
            buy_tax = res.get("simulationResult", {}).get("buyTax", 0)
            sell_tax = res.get("simulationResult", {}).get("sellTax", 0)
            
            status = "🚨 **خطرناک (هانی‌پات / غیرقابل فروش)**" if is_hp else "✅ **امن به نظر می‌رسد (هانی‌پات نیست)**"
            
            return (
                f"🔍 **نتیجه اسکن توکن:**\n\n"
                f"📌 وضعیت: {status}\n"
                f"📥 مالیات خرید: `{buy_tax}%`\n"
                f"📤 مالیات فروش: `{sell_tax}%`\n"
                f"⚠️ نکته: قبل از هر خریدی همیشه نقدینگی را بررسی کنید."
            )
        else:
            return "⚠️ آدرس نامعتبر است یا در شبکه‌های تحت پوشش یافت نشد."
    except Exception:
        return "❌ خطا در اسکن توکن."

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_prices = types.KeyboardButton("📊 قیمت لحظه‌ای")
    btn_scan = types.KeyboardButton("🛡 اسکن امنیت توکن")
    btn_vip = types.KeyboardButton("⭐ عضویت ویژه (VIP)")
    btn_help = types.KeyboardButton("ℹ️ راهنما و پشتیبانی")
    markup.add(btn_prices, btn_scan, btn_vip, btn_help)
    return markup
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"سلام {message.from_user.first_name} عزیز! 👋\n\n"
        "به **UniFast DeFi Bot** خوش آمدید. ⚡️\n"
        "دستیار هوشمند تحلیل، اسکن امنیت توکن‌ها و رصد لحظه‌ای بازار.\n\n"
        "از دکمه‌های زیر برای دسترسی سریع استفاده کنید:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "📊 قیمت لحظه‌ای")
def prices_handler(message):
    bot.send_chat_action(message.chat.id, 'typing')
    prices = get_crypto_prices()
    bot.send_message(message.chat.id, prices, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🛡 اسکن امنیت توکن")
def scan_prompt(message):
    msg = bot.send_message(
        message.chat.id,
        "🔍 لطفاً **آدرس کانترکت (Smart Contract)** توکن مورد نظر را ارسال کنید:"
    )
    bot.register_next_step_handler(msg, process_scan_step)

def process_scan_step(message):
    contract = message.text.strip()
    if contract.startswith("0x") and len(contract) == 42:
        bot.send_chat_action(message.chat.id, 'typing')
        res = check_token_security(contract)
        bot.send_message(message.chat.id, res, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ فرمت آدرس نامعتبر است. آدرس باید با 0x شروع شود و ۴۲ کاراکتر باشد.", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "⭐ عضویت ویژه (VIP)")
def vip_handler(message):
    vip_text = (
        "👑 **پلن‌های عضویت UniFast VIP:**\n\n"
        "⚡️ سیگنال‌های سریع پامپ و حجم‌های مشکوک\n"
        "🐋 رصد آنی کیف‌پول نهنگ‌ها و صرافی‌ها\n"
        "🤖 هشدار پیش‌خرید سریع توکن‌ها (Sniper Alerts)\n\n"
        "💳 **هزینه اشتراک:**\n"
        "• ۱ ماهه: ۲۰ تتر (USDT)\n"
        "• دائمی: ۵۰ تتر (USDT)\n\n"
        f"آدرس واریز (TRC20):\n`{USDT_TRC20_WALLET}`\n\n"
        "پس از پرداخت، شناسه تراکنش (TXID) را برای پشتیبانی ارسال کنید."
    )
    bot.send_message(message.chat.id, vip_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "ℹ️ راهنما و پشتیبانی")
def help_handler(message):
    help_text = (
        "🤖 **UniFast Bot v1.0**\n\n"
        "این ربات برای تحلیل سریع و محافظت از سرمایه شما در بازار کریپتو طراحی شده است.\n"
        "برای ثبت تبلیغات، پیشنهادها یا پشتیبانی با ادمین در ارتباط باشید."
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("ربات UniFast با موفقیت فعال شد...")
    bot.infinity_polling()
