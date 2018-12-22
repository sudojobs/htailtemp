feed_time= []
feed_wght=[] 
auto_feed=[]

with open('feed.json') as json_data:
    data = json.load(json_data)

for i in xrange(0,len(data)):
  feed_time.append(data[i]['feedTime'])
  auto_feed.append(data[i]['autoFeed'])
  feed_wght.append(data[i]['feedWeight'])

def update_for_next_feed(val):
    time=feed_time[val]
    fhour=time[0]
    fmins=time[1]
    print("Next Time: %s and %s" % (fhour,fmins))

length=len(data) -1 
time=feed_time[length]
fhour=time[0]
fmins=time[1]

while True:
    hours=datetime.now().hour
    mins=datetime.now().minute
    if hours==fhour and mins == fmins:
        length-=1
        update_for_next_feed(length)
        print ("Food Drop Actual time %s:%s" % (fmins,fmins))
