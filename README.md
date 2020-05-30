# Marketplace-Python3
Multiple Producer Multiple Consumer based marketplace implementation using threads in python3

Languages [ROMANIAN] :

In implementarea aplicatiei am folosit in principiu dictionare pentru stocare si diversele operatii
necesare deoarece operatiile pe dictionare sunt thread safe.

Consumer - pentru consumer parsez lista de comenzi ale fiecarui consumator si verific daca este o
		   comanda de tipul "add" sau "remove". Consumatorul va astepta la esuarea incercarii
		   efectuarii unei comenzi pana cand aceasta va reusi, adica implicit pana cand producatorul
		   pune destule produse in marketplace ca un consumator sa le utilizeze.
		   In momentul in care lista de comenzi s-a terminat se face o lista (buy_list) de produse
		   cumparate, iar folosind  functia format_order acestea sunt formatate si printate unul
		   cate unul.

Producer - producatorul produce incontinuu, iar in cazul in care apelul functiei publish intoarce
		   False acestea asteapta (timpul dat pentru fiecare produs) pana cand poate incerca din
		   nou, iar pentru republicare el asteapta timpul dat ca parametru.

Marketplace - reprezinta partea centrala a aplicatiei in care sunt implementate metodele utilizate
			  in mod concurent de catre produceri si consumeri. In marketplace am utilizat
			  dictionare pentru a stoca produsele si pentru a stoca informatiile fiecarui cart
			  utilizat de catre consumator. Publish adauga produsul creat in dictionar, iar daca
			  produsul este deja in marketplace creste doar nr de produse de acel tip din
			  magazin. Metoda add_to_cart adauga un nr de produse din magazin in cart-ul 
			  consumatorului respectiv rezervandu-l. Metoda remove_from_cart scoate un nr de produse
			  din cart si le pune inapoi in magazin. Metoda place_order intoarce o lista cu
			  produsele din cart.

