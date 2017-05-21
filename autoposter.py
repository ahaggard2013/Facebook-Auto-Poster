import schedule
import os
import praw
import pickle
import facebook
import time

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getPost():
    postQueue = []
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    postQueue.append([])
    # 0 - name 1 - link 2 - caption 3 - description 4 - picture
    postNum = 0
    r = praw.Reddit(user_agent = 'Top_video_post_Grabber_by_ahaggard')
    submissions = r.get_subreddit('videos').get_top(limit = 12)
    for post in submissions:
            # title of post
            postQueue[postNum].insert(0, str(post)[8:])
            # link to the post
            postQueue[postNum].insert(1, post.url)
            # caption
            postQueue[postNum].insert(2, post.comments[0].body.encode('ascii', 'ignore'))
            # no description
            postQueue[postNum].insert(3, str(post)[8:])
            # link to thumbnail
            postQueue[postNum].insert(4, 'http://img.youtube.com/vi/' + post.url[post.url.find('v=') + 2:] + '/0.jpg')
            postNum += 1
    inFile = open(os.path.join(__location__, 'postQueue.txt'), 'wb')
    pickle.dump(postQueue,inFile, pickle.HIGHEST_PROTOCOL)
    inFile.close() 
    return
    reader = pickle.load(inFile)
   

def postToFacebook():
   #FaceBook page Access Token goes here
   #https://developers.facebook.com/docs/facebook-login/access-tokens
   api = facebook.GraphAPI('AccessTokenHere')
   inFile = open(os.path.join(__location__, 'postQueue.txt'), 'r+')
   catched = False
   try:
       reader = pickle.load(inFile)
   except EOFError:
       getPost()
       inFile.close()
       inFile = open(os.path.join(__location__, 'postQueue.txt'), 'r+')
       reader = pickle.load(inFile)
       catched = True
   if not reader and catched == False:
       getPost()
       inFile.close()
       inFile = open(os.path.join(__location__, 'postQueue.txt'), 'r+')
       reader = pickle.load(inFile)
   catched = False
   post = {
       'name'        : reader[0][0],
       'link'        : reader[0][1],
       'caption'     : reader[0][2],
       'description' : reader[0][3],
       'picture'     : reader[0][4]
   }
   if not_posted(post):
       del reader[0]
       # used to save pickle changes
       inFile2 = open(os.path.join(__location__, 'postQueue.txt'), 'r+')
       pickle.dump(reader,inFile2, pickle.HIGHEST_PROTOCOL)
       inFile.close()
       inFile2.close()
       print (post['link'] + ' posted to facebook !'+ '\n')
       api.put_wall_post(message = post['caption'], attachment = post)
   else:
       del reader[0]
       # used to save pickle changes
       inFile2 =  open(os.path.join(__location__, 'postQueue.txt'), 'r+')
       pickle.dump(reader,inFile2, pickle.HIGHEST_PROTOCOL)
       inFile.close()
       inFile2.close()
       print 'Trying to repost!! \n'
       postToFacebook()
   return

def not_posted(post):
    file = open(os.path.join(__location__, 'posted.txt'), 'r+')
    for line in file:
        if post['link'] in line:
            file.close()
            return False
    file.write(post['link'] + '\n')
    file.close()
    return True

def main():
    schedule.every(2).hours.do(postToFacebook)
    while True:
        schedule.run_pending()
        time.sleep(60)

postToFacebook()
if __name__ == "__main__":
      main()
