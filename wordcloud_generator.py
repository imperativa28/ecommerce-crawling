from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Data
df = pd.read_csv('tokopedia.csv', header=0, sep=';', index_col=0)
full_description = ' '.join(df['description'].apply(str))
stopwords = open('stopwords.txt', 'r').read().splitlines()
stopwords.extend(['menjual', 'dengan', 'harga',
                  'produk', 'barang', 'nan', 'dll'])

# Mask
# mask = np.array(Image.open('assets/image/shopping-cart.png'))

wordcloud = WordCloud(max_words=1000, stopwords=stopwords, width=800, height=800, background_color='white',
                      colormap='summer', font_path='assets/font/OpenSans-CondBold.ttf')
wordcloud.generate(full_description)
wordcloud.to_file('wordcloudclean.png')

wordcloud.to_image().show()
