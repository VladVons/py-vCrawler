from Inc.Scheme.Composer import TComposer


#File = 'sites/used/ua/1x1.com.ua/product_1.html'
File = 'sites/used/ua/acomp.com.ua/product_4.html'
#File = 'sites/used/ua/as-it.ua/product_1.html'
###File = 'sites/used/ua/cibermag.com/product_1.html'
#File = 'sites/used/ua/europc.ua/product_1.html'
#File = 'sites/used/ua/gazik.ua/product_1.html'
#File = 'sites/used/ua/h-store.in.ua/product_1.html'
#File = 'sites/used/ua/korob.com.ua/product_3.html'
#File = 'sites/used/ua/lapstore.com.ua/product_1.html'
#File = 'sites/used/ua/laptop-planet.com.ua/product_1.html'
#File = 'sites/used/ua/laptopchik.top/product_1.html'
#File = 'sites/used/ua/lux-pc.com/product_1.html'
#File = 'sites/used/ua/mt.org.ua/product_1.html'
###File = 'sites/used/ua/pc.com.ua/product_2.html' #sm1c
#File = 'sites/used/ua/setka.ua/product_1.html'
#
#File = 'sites/used/pl/cebit.pl/product_2.html'
#File = 'sites/used/pl/servecom.pl/product_1.html'


with open(File, 'r', encoding='utf8') as F:
    Data = F.read()

Composer = TComposer('https://gazik.ua', Data)
Composer.Parse()
print(Composer.Macros)
pass
