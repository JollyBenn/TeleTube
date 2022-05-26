import requests
import time
import telebot
import threading

token = 'TOKEN' # telegram bot api, read more: https://core.telegram.org/api
download_delay = 10 # delay for download video
timeout = 5 # timeout for load page
localstore = {} # data store
lang = 'eng' # set lang, default: uk - Ukrainian, eng - English
locales = {} # langs

locales['uk'] = {
    'welcome_message' : 'Ласкаво просимо в <b>TeleTube</b>!\nЗавантажуйте відео з YouTube у високій якості.',
    'staring_download_videos' : 'Починаю скачувати відео',
    'expect_may_take_time' : 'Зачекайте, будь ласка, це може зайняти деякий час',
    'video_name' : 'Назва',
    'video_quality' : 'Якість',
    'download_video' : 'Скачати відео',
    'error_with_video_downloading' : 'При завантаженні відео сталася помилка, повторіть спробу пізніше!',
    'download_limit_exceeded' : 'Вибачте але вже зараз йде завантаження іншого відео, зачекайте, поки завантаження закінчиться!',
    'select_video_quality' : 'Виберіть якість відео, яке хочете завантажити:',
    'select_video_url' : 'Введіть посилання на відео, яке хочете завантажити',
    'critical_error' : 'Вибачте, але якість відео, що запитується, не доступна, будь ласка, спробуйте знизити якість відео, якщо протягом 30 хвилин нічого не змінити напишіть адміністратору!',
}

locales['eng'] = {
    'welcome_message' : 'Welcome to <b>TeleTube</b>!\nUpload high quality YouTube videos.',
    'staring_download_videos' : 'Starting to download videos',
    'expect_may_take_time' : 'Please wait, this may take some time',
    'video_name' : 'Name',
    'video_quality' : 'Quality',
    'download_video' : 'Download Video',
    'error_with_video_downloading' : 'An error occurred while uploading the video, please try again later!',
    'download_limit_exceeded' : 'Sorry, another video is being downloaded, please wait while the download is complete!',
    'select_video_quality' : 'Select the quality of the video you want to upload:',
    'select_video_url' : 'Enter the link to the video you want to download',
    'critical_error' : 'Sorry, but the requested video quality is not available, please try lowering the video quality, if you do not change anything within 30 minutes, write to the administrator!',
}

def get_image( video_url ):
    try:

        video_id = video_url.split('?')[1].split('&')[0].split('v=')[1]
        url = 'https://img.youtube.com/vi/{}/maxresdefault.jpg'.format( video_id )
        response = requests.get( url, timeout=timeout )

        if response.status_code == 200:
            return response.url
        else:
            return None

    except Exception:
        return None

def get_video( user_id, video_url, video_format=720 ):
    try:

        keyboard = telebot.types.InlineKeyboardMarkup()
        msg = bot.send_message( user_id, '[📼] {}...'.format( locales[lang]['staring_download_videos'] ) )
        time.sleep( 1 )
        msg = bot.edit_message_text( '[⌛️] {}'.format( locales[lang]['expect_may_take_time'] ), user_id, msg.id )

        image = get_image( video_url )

        url = 'https://loader.to/ajax/download.php?format={}&url={}'.format( video_format, video_url )
        response = requests.get( url, timeout=timeout )

        if response.status_code == 200:

            data = response.json()
            video_id = data['id']

            response = requests.get( video_url )
            html_content = response.text
            title = html_content[html_content.find('<title>') + 7 : html_content.find('</title>')].strip('- YouTube')
            
            url = 'https://loader.to/ajax/progress.php?id={}'.format( video_id )

            while True:
                
                time.sleep( download_delay )
                response = requests.get( url, timeout=timeout )

                if response.status_code == 200:
                    if response.json()['success']:
                        if user_id in localstore:
                            if localstore[user_id]['status'] == 'work':
                                localstore[user_id]['status'] = 'wait'
                                localstore[user_id]['video_url'] = None
                                localstore[user_id]['video_quality'] = None

                        bot.delete_message( user_id, msg.id )
                        description = '<b>{}</b>: {}\n<b>{}</b>: {}p'.format( locales[lang]['video_name'], title, locales[lang]['video_quality'], video_format )
                        url_button = telebot.types.InlineKeyboardButton(text="📼 {}".format( locales[lang]['download_video'] ), url=response.json()['download_url'])
                        keyboard.add(url_button)
                        bot.send_photo( user_id, image, caption=description, reply_markup=keyboard )
                        break
                else:
                    return None
        
        else:
            bot.edit_message_text( '[⚠️] {}'.format( locales[lang]['error_with_video_downloading'] ), user_id, msg.id )

    except Exception:

        return None

def add_video_in_download( user_id, video_url, video_quality ):
    try:
        localstore[user_id] = {
            'status' : 'work',
            'video_url' : video_url,
            'video_quality' : video_quality
        }
    except Exception:
        pass
    
def handle_download_video( msg, payload ):
    try:

        bot = payload[0]
        user_id = payload[1]
        video_quality = payload[2]
        video_url = msg.text

        if user_id in localstore:
            if localstore[user_id]['status'] == 'wait':

               add_video_in_download( user_id, video_url, video_quality )
               th = threading.Thread( target=get_video, args=( user_id, video_url, video_quality ) )
               th.daemon = True
               th.start()

            else:
                bot.send_message( user_id, '[⚠️] {}'.format( locales[lang]['download_limit_exceeded'] ))
                
        else:
            add_video_in_download( user_id, video_url, video_quality )
            th = threading.Thread( target=get_video, args=( user_id, video_url, video_quality ) )
            th.daemon = True
            th.start()

    except Exception:
        pass

welcome_menu = telebot.types.InlineKeyboardMarkup()
welcome_menu.add( telebot.types.InlineKeyboardButton(text='📼 {}'.format( locales[lang]['download_video'] ), callback_data='download_video') )

quality_menu = telebot.types.InlineKeyboardMarkup()
quality_menu.add( telebot.types.InlineKeyboardButton(text='360p', callback_data='quality:360') )
quality_menu.add( telebot.types.InlineKeyboardButton(text='480p', callback_data='quality:480') )
quality_menu.add( telebot.types.InlineKeyboardButton(text='720p', callback_data='quality:720') )
quality_menu.add( telebot.types.InlineKeyboardButton(text='1080p', callback_data='quality:1080') )
quality_menu.add( telebot.types.InlineKeyboardButton(text='1440p', callback_data='quality:1440') )

bot = telebot.TeleBot( token, parse_mode='HTML' )

@bot.message_handler( commands=['start'] )
def handle_commands( msg ):
    try:
        user_id = msg.from_user.id
        bot.send_message( user_id, locales[lang]['welcome_message'], reply_markup=welcome_menu )
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: True)
def handler_query(call):
    try:

        user_id = call.from_user.id
        message_id = call.message.id
        data = call.data

        if ':' in data:
            if data.startswith('quality'):
                quality_default = [ 360, 480, 720, 1080, 1440 ]
                include_data = data.split(':')
                quality = int( include_data[1] )
                if quality in quality_default:
                    payload = [bot, user_id, quality]
                    msg = bot.edit_message_text( '[🔗] {}:'.format( locales[lang]['select_video_url'] ), user_id, message_id )
                    bot.register_next_step_handler( msg, handle_download_video, payload )
                else:
                    bot.send_message( user_id, locales[lang]['critical_error'] )
        else:
            if data == 'download_video':
                bot.edit_message_text( locales[lang]['select_video_quality'], user_id, message_id, reply_markup=quality_menu )

    except Exception:
        pass

bot.polling()