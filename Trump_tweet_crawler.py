########################################
# 這隻程式建議 以 OS 設定自動排程 固定時間跑 #
# 才能在不用一值跑回圈的情況下定期追蹤 tweet #
# 或者可以自行加入while迴圈搭配sleep給他跑  #
########################################
import tweepy
import smtplib
from email.mime.text import MIMEText
import os.path
# 如果加入 while 迴圈，則需要sleep函數，便會用到
# import time

# 敏感資訊，Commit＆Push 前要記得刪除
consumer_key = '**'
consumer_secret = '**'
access_token = '**'
access_token_secret = '**'

email_account = 'your account'
email_pwd = 'your password'

# 提交你的Key和secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# 获取类似于内容句柄的东西
api = tweepy.API(auth)

# 新增一個TXT檔案寫入LOG，每次讀取Tweet時都來此檢查是否有更新，有更新才寄信
check_log_file = './tweet_check_log.txt'

###################################
# 要加while 迴圈可在此添加包住下面整段 #
###################################

# 爬川普推特，透過搜尋功能篩選出只有中美貿易戰的Tweets
public_tweets = api.search(q='((China AND Trade) OR (China AND Tariffs) OR (Xi) OR (Fed)) (from:realDonaldTrump)',
                           count=1)
tweet = public_tweets[0]

# 檢查 tweet_check_log.txt 的時間與當前爬到的 tweet 時間戳是否相同
if os.path.exists(check_log_file):
    file = open(check_log_file, 'r', encoding='utf-8')
    time_log = file.readline()
    file.close()
    # 時間戳相同，代表尚未更新，因此不動作
    if str(tweet.created_at) == time_log:
        pass
    # 時間戳不同，需覆寫 log 並寄 mail
    else:
        file = open(check_log_file, 'w', encoding='utf-8')
        file.writelines(str(tweet.created_at))
        file.close()

        msg = MIMEText(tweet.created_at.strftime("%b %d %Y - %H:%M:%S") + '\n' + tweet.text + '\n' + '點上方連結看全文')
        msg['Subject'] = '(注意)Trump 又再講幹話了！'
        msg['from'] = email_account
        msg['To'] = 'email'

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_account, email_pwd)
        server.send_message(msg)
        server.quit()
        # print('email is sent!')

else:
    file = open(check_log_file, 'a+', encoding='utf-8')
    file.writelines(str(public_tweets[0].created_at))
    file.close()

    msg = MIMEText(tweet.created_at.strftime("%b %d %Y - %H:%M:%S") + '\n' + tweet.text + '\n' + '點上方連結看全文')
    msg['Subject'] = '(注意)Trump 又再講幹話了！'
    msg['from'] = email_account
    msg['To'] = 'ffang55tw@gmail.com'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email_account, email_pwd)
    server.send_message(msg)
    server.quit()
    # print('email is sent!')
