import json
import itertools
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def wczytaj_rozwiazania(plik):
    with open(plik, 'r') as f:
        return json.load(f)


def licz_pary_w_cyklu(cykl):
    return set(frozenset(pair) for pair in itertools.combinations(cykl, 2))


def licz_krawedzie(cykl):
    return set(frozenset([cykl[i], cykl[(i + 1) % len(cykl)]]) for i in range(len(cykl)))


def podobienstwo_pary_wierzcholkow(r1, r2):
    p1 = licz_pary_w_cyklu(r1['cykl1']).union(licz_pary_w_cyklu(r1['cykl2']))
    p2 = licz_pary_w_cyklu(r2['cykl1']).union(licz_pary_w_cyklu(r2['cykl2']))
    return len(p1.intersection(p2))


def podobienstwo_krawedzi(r1, r2):
    k1 = licz_krawedzie(r1['cykl1']).union(licz_krawedzie(r1['cykl2']))
    k2 = licz_krawedzie(r2['cykl1']).union(licz_krawedzie(r2['cykl2']))
    return len(k1.intersection(k2))


def badanie_wypuklosci_do_najlepszego(plik_optimow, plik_najlepszego):
    optimy = wczytaj_rozwiazania(plik_optimow)
    najlepszy = wczytaj_rozwiazania(plik_najlepszego)[0]

    wyniki_do_naj_pary = []
    wyniki_do_naj_krawedzie = []

    for i, opt in enumerate(optimy):
        koszt = opt['koszt']
        p_do_naj = podobienstwo_pary_wierzcholkow(opt, najlepszy)
        k_do_naj = podobienstwo_krawedzi(opt, najlepszy)

        wyniki_do_naj_pary.append((koszt, p_do_naj))
        wyniki_do_naj_krawedzie.append((koszt, k_do_naj))

        if i % 100 == 0:
            print(f"Zakończono {i} / {len(optimy)}")

    return wyniki_do_naj_pary, wyniki_do_naj_krawedzie


def rysuj_wykres(wyniki, tytul, etykieta_y, nazwa_pliku=None):
    x, y = zip(*wyniki)
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.6)
    plt.xlabel('Wartość funkcji celu (koszt)')
    plt.ylabel(etykieta_y)
    plt.title(tytul)

    r, _ = pearsonr(x, y)
    plt.text(min(x), max(y), f'Wsp. korelacji: {r:.4f}', fontsize=12, color='blue')
    plt.grid(True)
    plt.tight_layout()

    if nazwa_pliku:
        plt.savefig(nazwa_pliku)
        print(f"Zapisano wykres do pliku: {nazwa_pliku}")

    plt.show()


if __name__ == "__main__":
    plik_optimow = "lokalne_optimy_kroB.json"
    plik_najlepszego = "LNS_najlepsze_rozwiazanie_kroB.json"

    wyniki_do_naj_pary, wyniki_do_naj_krawedzie = badanie_wypuklosci_do_najlepszego(
        plik_optimow, plik_najlepszego
    )

    rysuj_wykres(
        wyniki_do_naj_pary,
        "Podobieństwo do najlepszego – pary wierzchołków",
        "Podobieństwo do najlepszego (pary)",
        "../wypuklosci/wykres_podobienstwo_pary_kroB.png"
    )

    rysuj_wykres(
        wyniki_do_naj_krawedzie,
        "Podobieństwo do najlepszego – krawędzie",
        "Podobieństwo do najlepszego (krawędzie)",
        "../wypuklosci/wykres_podobienstwo_krawedzie_kroB.png"
    )

