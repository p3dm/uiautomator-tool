import time
from google.oauth2 import service_account
import uiautomator2 as u2
from googleapiclient.discovery import build

from mail_reader import get_gmail_service, get_latest_unity_otp, get_credentials


gmail_service = get_gmail_service()

creds = service_account.Credentials.from_service_account_file( 
    "gen-lang-client-0462810464-4b04db6f2e79.json", 
    scopes=['https://www.googleapis.com/auth/spreadsheets'])

sheets_service = build('sheets', 'v4', credentials=creds)

Device_id = [
]

XPATH = {
    'app' : "io.unitynodes.unityapp",
    'start':'//*[@text="GET STARTED"]',
    'licsense_option' : '//*[@text="License Operator"]',
    'input_code' : '//*[@text="Enter Lease Code"]',
    'continue': '//*[@text="CONTINUE"]',
    'email': '//*[@text="Sign In with Email"]',
    'input_email': '//*[@text="Enter your email"]',
    'input_otp': '//*[@text="Enter OTP from email"]',
    'verify': '//*[@text="VERIFY"]',
    'allow': '//*[@text="Allow"]',
    'pop_up': '//*[@text="CANCEL"]'

}


def get_bold_phone_rows(spreadsheet_id, sheet_name):
    """
    Lấy dữ liệu từ Google Sheet
    Giả sử cấu trúc: A=Phone, B=Alias, C=?, D=Code (index 0,1,2,3)
    Bỏ 2 dòng header đầu
    """
    res = sheets_service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=[sheet_name],
        includeGridData=True
    ).execute()

    rows = res['sheets'][0]['data'][0]['rowData']
    result = []

    for row in rows[1:]:  # bỏ header
        cells = row.get('values', [])

        if len(cells) < 5:
            continue

        phone_cell = cells[4]
        phone_id = phone_cell.get('formattedValue')

        text_fmt = phone_cell.get('userEnteredFormat', {}) \
                              .get('textFormat', {})
        if not text_fmt.get('bold') or not phone_id:
            continue


        def cell(i):
            return cells[i].get('formattedValue') if i < len(cells) else None

        result.append({
            "Phone_ID": phone_id,
            "alias": cell(0),
            "license": cell(1),
            "mail": cell(2),
            "proxy": cell(3),
        })

    return result
    

def generate_mail(alias, mail):
    name, domain = mail.split('@')
    mail = f"{name}+{alias}@{domain}"
    return mail


def login(row_index):
    data_list = get_bold_phone_rows("1KLUV3_u3XS0VtdrwcvzgpRBfoud-drdKDfyYB1Y2xjM", "Sheet1")
    if not data_list:
        print("Không có dữ liệu từ Google Sheet")
        return
    # Lấy dòng đầu tiên
    if row_index >= len(data_list):
        print("❌ Không còn dòng dữ liệu trong Sheet")
        return
    data = data_list[row_index]
    alias = str(data['alias'])
    code = str(data['license'])
    Device_id = data['Phone_ID']
    email = generate_mail(alias, data['mail'])
    print(f"Đang đăng nhập với email: {email}, code: {code}, ip: {Device_id}")
    try:
        d = u2.connect(Device_id)
        d.app_start(XPATH['app'])
        time.sleep(6)
        d.xpath(XPATH['start']).click()
        time.sleep(6)
        d.xpath(XPATH['licsense_option']).click()
        time.sleep(6)
        d.xpath(XPATH['input_code']).click()
        time.sleep(6)
        d.send_keys(code)
        time.sleep(6)
        d.xpath(XPATH['continue']).click()
        time.sleep(6)
        d.xpath(XPATH['email']).click()
        time.sleep(6)
        d.xpath(XPATH['input_email']).click()
        time.sleep(2)
        d.send_keys(email)
        time.sleep(2)
        d.xpath(XPATH['continue']).click()
        time.sleep(10)

        print("\n🔍 Đang chờ email OTP từ Unity Nodes...")
        otp = None
        for attempt in range(10):
            print(f"⏳ Thử lần {attempt + 1}/10...")
            otp = get_latest_unity_otp(gmail_service)
            if otp:
                break
            time.sleep(5)

        if not otp:
            print("❌ KHÔNG TÌM THẤY OTP sau 10 lần thử (50 giây)")
            return


        print(f"✅ OTP tìm thấy: {otp}")
        d.xpath(XPATH['input_otp']).click()
        time.sleep(1)
        d.send_keys(otp)
        print("✅ Đã điền OTP vào app")
        d.xpath(XPATH['verify']).click()
        time.sleep(3)
        if d.xpath(XPATH['allow']).exists:
            d.xpath(XPATH['allow']).click()
        time.sleep(3)
        if d.xpath(XPATH['pop_up']).exists:
            d.xpath(XPATH['pop_up']).click()
        time.sleep(3)
        d.xpath(XPATH['continue']).click()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    data_list = get_bold_phone_rows("1KLUV3_u3XS0VtdrwcvzgpRBfoud-drdKDfyYB1Y2xjM", "Sheet1")
    for index in range(len(data_list)):
        login(index)
    print(f"\n✅ Hoàn thành {len(data_list)} dòng")



