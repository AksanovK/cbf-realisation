import hashlib
from math import log
import requests


s = ['КФУ', 'ИТИС', 'студент', 'изучение', 'круг', 'спорт', 'организация', 'активист', 'учеба', 'ДУ']


def zero_list_maker(size):
    list_of_zeros = [0] * size
    return list_of_zeros


def generating_cbf(k, list_of_objects, n):
    bloom_filter = zero_list_maker(n)
    for object in list_of_objects:
        count = 0

        index = int((hashlib.sha3_512(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.blake2s(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.shake_128(object.encode('utf-8')).hexdigest(56)), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha1(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha512(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha224(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha384(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.md5(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha3_224(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha3_256(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.blake2b(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.shake_256(object.encode('utf-8')).hexdigest(56)), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha256(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha3_384(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue
    return bloom_filter


def take_post():
    token = '2fb1c2022fb1c2022fb1c2024d2fc77b8422fb12fb1c2024ff0ccd451067a9b08b7c153',
    count = 1
    posts = []
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': 5.21,
                                'domain': 'itis_kfu',
                                'count': count
                            })
    items = response.json()['response']['items']
    for item in items:
        posts.append(item['text'])
    f = open('text.txt', 'w', encoding='UTF-8')
    words = []
    for post in posts:
        words = post.split()
    for word in words:
        f.write(word)
        f.write('\n')
    f.close()
    return words


def words_check(words, bloom_filter, count_of_hashes):
    for word in words:
        words_util = [word]
        new_cbf = generating_cbf(count_of_hashes, words_util, len(bloom_filter))
        count = 0
        for a in new_cbf:
            if a == 1:
                index = new_cbf.index(a)
                new_cbf[index] = 0
                if bloom_filter[index] > 0:
                    count += 1
        if count == count_of_hashes:
            print(word + ' - слово есть, вероятность ошибочного обнаружения = ' + str("%.5f" % (0.5 ** count_of_hashes)))
        else:
            print(word + ' - слова нет')


if __name__ == '__main__':
    precision = 0.0001
    words = take_post()
    m = len(words)
    n = int(log(precision) / log(0.5 ** (log(2) / m)))
    k = n / m * log(2)
    if k.is_integer():
        k = int(n / m * log(2))
    else:
        k = int(n / m * log(2)) + 1
    cbf = generating_cbf(k, words, n)
    words_check(s, cbf, k)
