Wynik oznacza to, że model sklasyfikował 6 próbek z danych testowych, z czego 3 zostały sklasyfikowane poprawnie (precision 0.50). 
Z tego, co model uważa za prawidłowe odpowiedzi (recall 0.50), tylko 3 faktycznie były prawidłowe. 
Wskaźnik f1-score to średnia harmoniczna pomiędzy precision i recall i jest używana do oceny jakości klasyfikatora. 
Wskaźnik support oznacza liczbę próbek dla każdej klasy. 
W tym przypadku model nie został nauczony na próbkach z klas "Personality Info" i "Personality information", 
dlatego są one wyświetlane jako 0.

Możesz sprawdzić, czy model działa poprawnie, wprowadzając różne pytania i sprawdzając, 
czy zwraca odpowiednie kategorie. Należy również zwrócić uwagę na to, 
czy model jest w stanie generalizować do nowych danych (czyli czy dobrze radzi sobie z pytaniami, 
których nie widział podczas nauki). 
Jeśli chcesz poprawić jakość modelu, możesz spróbować dodać więcej danych treningowych lub zmienić hiperparametry (np. typ straty w klasyfikatorze SGDClassifier).


Następnie tworzony jest "pipeline" złożony z dwóch kroków:

TfidfVectorizer, który służy do przekształcenia tekstu na wektor cech (czyli macierz "bag of words")
Konwersja kolekcji surowych dokumentów na macierz cech TF-IDF.
Równoważne z CountVectorizer, po którym następuje TfidfTransformer.


SGDClassifier, który jest implementacją klasyfikatora SGD (stochastyczny spadek gradientu)
Klasyfikatory liniowe (SVM, regresja logistyczna itp.) z treningiem SGD.

Estymator ten implementuje liniowe modele z regularyzacją i uczeniem SGD (stochastic gradient descent): gradient straty jest szacowany dla każdej próbki po kolei, a model jest aktualizowany po drodze z malejącym rozkładem sił (aka learning rate). SGD pozwala na uczenie minibatch (online/out-of-core) za pomocą metody partial_fit. Aby uzyskać najlepsze wyniki przy użyciu domyślnego harmonogramu uczenia, dane powinny mieć zerową średnią i jednostkową wariancję.

Ta implementacja działa z danymi reprezentowanymi jako gęste lub rzadkie tablice wartości zmiennoprzecinkowych dla cech. Model, do którego jest dopasowywany, może być kontrolowany za pomocą parametru straty; domyślnie dopasowuje liniową maszynę wektorów wsparcia (SVM).

Regularyzator jest karą dodaną do funkcji straty, która zmniejsza parametry modelu w kierunku wektora zerowego przy użyciu kwadratowej normy euklidesowej L2 lub normy bezwzględnej L1 lub kombinacji obu (Elastic Net). Jeśli aktualizacja parametrów przekroczy wartość 0.0 z powodu regularyzatora, aktualizacja jest obcinana do 0.0, aby umożliwić uczenie rzadkich modeli i osiągnąć selekcję cech online.



Model jest trenowany na danych treningowych i następnie stosowany do przewidywania etykiet dla danych treningowych (co ma służyć do sprawdzenia jego poprawności).

Na końcu użytkownik jest pytany o pytanie, które chce zadać, a następnie model jest używany do przewidzenia etykiety dla tego pytania. Ostatecznie, przewidziana etykieta jest wyświetlana.

Ten kod tworzy model uczący się ze zbioru danych i przeprowadza testowanie jego dokładności.

Pierwsza część kodu importuje niezbędne biblioteki i funkcje. Następnie zdefiniowana jest funkcja "text_cleaner", która przyjmuje jako argument tekst i język, i zwraca tekst, który został przetworzony przez redukcję słów do ich rdzenia i zamianę wszystkich liter na małe.

Następnie plik "model.txt" jest otwierany i przeczytany, a jego zawartość jest przekształcana do formatu JSON i zapisywana do pliku "model.json".

Funkcja "train_test_split" dzieli podane dane na zbiór uczący i zbiór testowy z określonym współczynnikiem podziału (domyślnie 20% danych jest używana jako zbiór testowy).

Funkcja "openai" otwiera plik "model.json", wczytuje dane i dzieli je na zbiór uczący i testowy za pomocą funkcji "train_test_split". Następnie tworzy sekwencję kroków (pipeline) używającą TfidfVectorizer i SGDClassifier, która jest stosowana do danych uczących. Model jest oceniany na zbiorze testowym i wynik jest wyświetlany. Następnie model jest trenowany na całym zbiorze danych uczących i używany do przewidywania etykiet dla danych uczących i testowych. Raport klasyfikacji jest wyświetlany, a następnie użytkownik jest proszony o wprowadzenie pytania, a model jest używany do przewidzenia etykiety dla tego pytania.


Pipiline :
Potok transformat z estymatorem końcowym.

Sekwencyjnie zastosować listę transformat i ostateczny estymator. Pośrednie kroki potoku muszą być "transformami", to znaczy muszą implementować metody fit i transform. Estymator końcowy musi jedynie implementować fit. Transformatory w potoku mogą być buforowane przy użyciu argumentu pamięci.

Celem potoku jest złożenie kilku kroków, które mogą być walidowane krzyżowo razem przy ustawieniu różnych parametrów. W tym celu umożliwia on ustawienie parametrów poszczególnych kroków przy użyciu ich nazw oraz nazwy parametru oddzielonej znakiem '__', jak w poniższym przykładzie. Estymator kroku może być całkowicie zastąpiony przez ustawienie parametru z jego nazwą na inny estymator, lub transformator usunięty przez ustawienie go na 'passthrough' lub None.
