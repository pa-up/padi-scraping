import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException , TimeoutException , ElementClickInterceptedException
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome import service as fs
import time

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if minutes == 0 and hours == 0:
        return f"{seconds}秒"
    if hours == 0 and minutes != 0:
        return f"{minutes}分{seconds}秒"
    if hours != 0 and minutes != 0:
        return f"{hours}時間{minutes}分{seconds}秒"


item_ls = []
def browser_setup():
    """ブラウザを起動する関数"""
    #ブラウザの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #ブラウザの起動（webdriver_managerによりドライバーをインストール）
    CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()  # chromiumを使用したいので引数でchromiumを指定しておく
    service = fs.Service(CHROMEDRIVER)
    browser = webdriver.Chrome(
        options=options,
        service=service
    )
    browser.implicitly_wait(3)
    return browser


def get_url(browser , selected_country):
    url = 'https://www.padi.com/ja/dive-shops/' + selected_country + '/'
    browser.get(url)
    browser.implicitly_wait(5)


def check_SNS_exist(target: str , keyword: str):
    if keyword in target:
        return True
    else:
        return False

def find_position(target, keyword):
    social_media_list = ["Facebook", "Instagram", "Twitter", "TikTok", "YouTube"]
    position_list = []
    for social_media in social_media_list:
        if social_media in target:
            position_list.append(social_media)
    if keyword in position_list:
        return position_list.index(keyword) + 1
    else:
        return 0
    
def insert_newlines(keyword_list, target):
    for i, keyword in enumerate(keyword_list):
        if i == 0:
            continue
        target = target.replace(keyword, "\n" + keyword)
    return target


def page_padi_com(browser , name , place1 , place2 , detail_url):
    # detailのページにアクセス
    browser.get(detail_url)
    st.write("detail_url : " , detail_url)
    time.sleep(3)

    # ページのHTML要素を取得
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    pretty_soup = soup.prettify()
    # with open("output_detail" + ".html", "w", encoding="utf-8") as f:
    #     f.write(pretty_soup)

    try:
        detail = soup.select_one('#description > div > div.dive-center-details').text
        # st.write("detailの文字数 : " , len(detail))
    except (TypeError, AttributeError):
        detail = ""
        # st.write("detail : " , detail)
    try:
        Activities = soup.select_one('#description > div > div.dive-center-infobox > div.left-side > div:nth-child(1) > div > p').text
        # st.write("Activities: <br>", Activities, unsafe_allow_html=True)
    except AttributeError:
        Activities = ""
    try:
        Conservation = soup.select_one('div.info > p').text
    except AttributeError:
        Conservation = ""
    try:
        Languages = soup.select_one('#description > div > div.dive-center-infobox > div.left-side > div:nth-child(3) > div > p').text
    except AttributeError:
        Languages = ""
    try:
        Hours = soup.select_one('#description > div > div.dive-center-infobox > div.left-side > div.item-wrapper.working-hours-section > div > div').text
        Hours = Hours.replace('\n', '')
        Hours_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        Hours = insert_newlines(Hours_list, Hours)
    except AttributeError:
        Hours = ""
    try:
        WEBSITE = soup.select_one('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(1) > div > p > a')['href']
    except (TypeError, AttributeError):
        WEBSITE = ""
    # st.write("WEBSITE : ", WEBSITE)
    try:
        Social_media_text = soup.select_one('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(2) > div > p').text
    except AttributeError:
        Social_media_text = ""
    # st.write("Social_media_text: <br>", Social_media_text, unsafe_allow_html=True)
    try:
        Social_media_URL = soup.select('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(2) > div > p > a')
        Facebook_count = find_position(Social_media_text, "Facebook")
        if Facebook_count > 0 :
            fb = Social_media_URL[Facebook_count - 1]['href']
        else:
            fb = ""
        Instagram_count = find_position(Social_media_text, "Instagram")
        if Instagram_count > 0 :
            ins = Social_media_URL[Instagram_count - 1]['href']
        else:
            ins = ""
        Twitter_count = find_position(Social_media_text, "Twitter")
        if Twitter_count > 0 :
            twitter = Social_media_URL[Twitter_count - 1]['href']
        else:
            twitter = ""
        TikTok_count = find_position(Social_media_text, "TikTok")
        if TikTok_count > 0 :
            tickok = Social_media_URL[TikTok_count - 1]['href']
        else:
            tickok = ""
        YouTube_count = find_position(Social_media_text, "YouTube")
        if YouTube_count > 0 :
            youtube = Social_media_URL[YouTube_count - 1]['href']
        else:
            youtube = ""
    except (TypeError, AttributeError):
        fb , ins , twitter , tickok , youtube = "" , "" , "" , "" , ""
    try:
        mail = soup.select_one('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(3) > div > p > a')['href']
    except (TypeError, AttributeError):
        mail = ""
    # st.write("mail : " , mail)
    try:
        PHONE = soup.select_one('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(4) > div > p > a')['href']
        PHONE = PHONE.split(":")[-1].strip()
    except (TypeError, AttributeError):
        PHONE = ""
    # st.write("PHONE : <br>" , PHONE , unsafe_allow_html=True)
    try:
        ADDRESS = soup.select_one('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(5) > div > a > p').text
    except AttributeError:
        ADDRESS = ""
    # st.write("ADDRESS : " , ADDRESS)
    try:
        GMAP = soup.select_one('#description > div > div.dive-center-infobox > div.right-side > div:nth-child(5) > div > a')['href']
    except (TypeError, AttributeError):
        GMAP = ""

    data = {
            'name':name,
            'place1':place1,
            'place2':place2,
            'detail':detail,
            'Activities offered':Activities,
            'Conservation awards':Conservation,
            'Languages':Languages,
            'Hours':Hours,
            'WEBSITE':WEBSITE,
            'Social media':Social_media_text,
            'fb':fb,
            'ins':ins,
            'twitter':twitter,
            'tickok':tickok,
            'youtube':youtube,
            'メールアドレス':mail,
            'PHONE':PHONE,
            'ADDRESS':ADDRESS,
            'GMAP':GMAP,
        }
    return data


def page_shift_button(browser):
    """ ボタンを押してページを繰り返す関数 """
    # ページ切り替えボタン
    wait = WebDriverWait(browser, 10)
    next_page_is_valid = True
    scroll_6300 = True
    while True:
        try:
            page_shift_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#dsl-list > div > div.pagination--3KOqw > i.arrow--26Z62.padi-icons.padi-icons--carret-right')))
            if scroll_6300:
                browser.execute_script("window.scrollBy(0, 6300)")
            time.sleep(1)
            page_shift_button.click()
            break
        except TimeoutException:
            next_page_is_valid = False
            break
        except ElementClickInterceptedException:
            browser.execute_script("window.scrollBy(0, -500)")
            scroll_6300 = False
            time.sleep(1)
    return next_page_is_valid


def get_data(browser , selected_country , start_time):
    all_names = []
    all_places = []
    all_detail_URLs = []

    # リストページの読み込み
    next_page_is_valid = True
    page_number = 1
    while next_page_is_valid:
        if page_number == 1:
            get_url(browser , selected_country)
            time.sleep(2)
            try:
                delete_popup_button = browser.find_element(By.CSS_SELECTOR, 'body > div.ReactModalPortal > div > div > span')
                delete_popup_button.click()
            except NoSuchElementException:
                time.sleep(1)
        else:
            # ページの切り替え
            next_page_is_valid = page_shift_button(browser)
            if not next_page_is_valid:
                st.write(f"<h5>全ページの name , place , detail_URL を取得完了</h5>", unsafe_allow_html=True)
                break
        
        time.sleep(3)

        url = browser.current_url
        count_url = 'https://www.padi.com/ja/dive-shops/' + selected_country + '/' + "?page=" + str(page_number)
        if url != count_url and page_number > 1 :
            st.write(f"<h3>全ページの name , place , detail_URL を取得完了</h3>", unsafe_allow_html=True)
            break

        st.write(f"<h3>{page_number}ページ目</h3>", unsafe_allow_html=True)
        st.write("URL : " , url)

        current_time = time.time()
        elapsed_time = format_duration( round(current_time - start_time) )
        st.write("経過時間 : " , elapsed_time)

        page_html = browser.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        pretty_soup = soup.prettify()
        with open("output" + ".html", "w", encoding="utf-8") as f:
            f.write(pretty_soup)

        # 商品名
        try:
            names_elements = soup.select('p.title--28Pe7')
            names = [element.text for element in names_elements]
        except AttributeError:
            names = ["" for _ in range( len(names_elements) )]
        # 場所
        try:
            places_elements = soup.select('p.address--3qAGE')
            places = [element.text for element in places_elements]
        except AttributeError:
            places = ["" for _ in range( len(places_elements) )]
        
        st.write("len(names) : " , len(names) , " , " , "len(places) : " , len(places))

        # detailのURLを取得
        detail_a_elements = browser.find_elements(By.CSS_SELECTOR, 'div.relative > div.list--LcIm5 > a')
        detail_URLs = [element.get_attribute('href') for element in detail_a_elements]

        for k in range( len(detail_URLs) ):
            all_names.append(names[k])
            all_places.append(places[k])
            all_detail_URLs.append(detail_URLs[k])
        page_number += 1


    # 全ての detailページで情報を取得
    st.write("all_detail_URLs : ", len(all_detail_URLs) , "個")
    for loop in range( len(all_detail_URLs) ):
        st.write(loop + 1, "個目")
        st.write(f"<h4>{loop + 1}個目</h4>", unsafe_allow_html=True)

        current_time = time.time()
        elapsed_time = format_duration( round(current_time - start_time) )
        st.write("経過時間 : " , elapsed_time)

        #商品名、場所、詳細ページURLを取得
        name = all_names[loop]
        place = all_places[loop]
        place1 , place2 = place.split(", ")[1] , place.split(", ")[0]
        detail_url = all_detail_URLs[loop]
        data = page_padi_com(browser , name , place1 , place2 , detail_url)
        item_ls.append(data)


def main():
    st.write("<p></p>", unsafe_allow_html=True)
    st.title("padiページ情報を一括取得")
    st.write("<p></p>", unsafe_allow_html=True)
    country_options = ['選択されていません' , 'thailand', 'zhong-guo']
    selected_country = st.selectbox('国を選択', country_options)
    st.write("<p></p>", unsafe_allow_html=True)

    if selected_country != country_options[0]:
        # 開始時間計測
        start_time = time.time()

        browser = browser_setup()
        get_data(browser , selected_country , start_time)
        df = pd.DataFrame(item_ls)
        csv = df.to_csv(index=False)

        # CSVファイルのダウンロードボタンを表示
        st.download_button(
            label='CSVをダウンロード',
            data=csv,
            file_name='padiデータ.csv',
            mime='text/csv'
        )


if __name__ == '__main__':
    main()
