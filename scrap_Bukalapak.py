import requests
import pandas as pd 
import progressbar
import re

url_init = 'https://www.bukalapak.com'
url = 'https://api.bukalapak.com/multistrategy-products'
key = input('Masukkan keyword :')

r = requests.get(url_init)
access_token = r.text.split('"access_token":"')[1].split('","created_at"')[0]
columns=['nama', 'harga', 'deskripsi', 'berat', 'spesifikasi', 'kondisi', 'stok', 'dilihat', 'tertarik', 'terjual', 'rating', 'nama_toko', 'lokasi', 'kurir_pengiriman', 'tag', 'gambar', 'link']
rows = []
bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

for page in range(1,101):    
    try:
        parameter = { 
            'prambanan_override': True,
            'keywords': key,
            'top_seller': True,
            'brand': True,
            'offset': 0,
            'page': page,
            'limit': 50,
            'facet': True,        
            'filter_non_popular_section': True,
            'type': 'trend',
            'access_token': access_token
        }

        r = requests.get(url, params=parameter)
        r = r.json()
        products = r['data']
        if len(products) == 0: break
            
        for i, p in enumerate(products):   
            nama = p['name']
            harga = p['price']
            deskripsi = re.sub('<[a-z0-9/]*>', '', p['description'])
            berat = p['weight']
            spesifikasi = p['specs']
            kondisi = p['condition']
            stok = p['stock']
            dilihat = p['stats']['view_count']
            tertarik = p['stats']['interest_count']
            terjual = p['stats']['sold_count']
            rating = p['rating']['average_rate']
            nama_toko = p['store']['name']
            lokasi = p['store']['address']['city']
            kurir_pengiriman = re.sub('[\[\]\']*', '', str(p['store']['carriers']))
            tag = re.sub('[\[\]\{\}\':]*|name|(url[-_/\.\{\}\':,\sa-z0-9]*)', '', str(p['tag_pages']))
            gambar = p['images']['large_urls'][0]
            link = p['url']

            row = [nama, harga, deskripsi, berat, spesifikasi, kondisi, stok, dilihat, tertarik, terjual, rating, nama_toko, lokasi, kurir_pengiriman, tag, gambar, link]
            rows.append(row) 
        bar.update(page)            
    except Exception:
        pass
bar.finish()     
df = pd.DataFrame(rows, columns=columns)
df = df.sort_values(['harga','terjual','rating'], ascending=[False,False,False])
df = df.reset_index(drop=True)
df.to_csv('hasil/{}.csv'.format(key),sep=",")
print(str(len(df)) + ' Produk Ditemukan')
print(df)