'''
Assuming that we have an object:
class URL:
    float time
    string date
    dict keyword{ string key : int num }
    bool visited
    string address
'''
import time
import url

def check_url(url, domain_times, visited):
    '''
    Check URL to make sure that it meets all of the criteria.
    :param url: url to be checked
    :param domain_times: a dict of domain name strings and floats of the time accessed
    :param visited: a list of url strings that have already been visited
    :return: the next valid url
    '''

    ACCESS_TIME = 15 #Minimum number of seconds between website pings

    last_time = 0
    if (url.domain in domain_times):
        last_time = domain_times[url.domain]

    if (url.address in visited):
        return False

    while (time.time() - last_time) <= ACCESS_TIME:
        print('Waiting ', ACCESS_TIME - (time.time() - last_time), ' seconds for', url.domain)
        time.sleep(ACCESS_TIME - (time.time()-last_time))

    return True


#Testing
if __name__ == '__main__':
    a = url.URL(domain = "www.facebook.com",address = "www.facebook.com/Andrew")
    print(check_url(a,{"www.facebook.com":time.time()},['www.facebook.com/Joe Smith/profile']))