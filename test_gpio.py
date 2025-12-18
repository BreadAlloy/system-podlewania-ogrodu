import pytest

# w tym pliku prosze dopisac nastepne testy

# testy jakis modeli,... w django jezeli beda potrzebne bedziemy robic w django, narazie zostanmy przy prostych

# w pliku requirments_testy.txt prosze dodac biblioteki wymagane do uruchomienia testow


# struktura testu (po wiecej informacji zapraszam do dokumentacji pytest)
# def nazwa_testu():
#   przygotowanie danych do testu (nie zawsze potrzebne)
#   assert (juz konkretny test)

# ponizej przyklad

def test_example():
    print("hello")
    assert True == True

def test_addition():
    a = 2
    b = 3
    result = a + b
    assert result == 5


def test_string_upper():
    text = "pytest"
    assert text.upper() == "PYTEST"


def test_list_contains_element():
    data = [1, 2, 3, 4]
    assert 3 in data

def test_addition_parametrized(a, b, expected):
    assert a + b == expected


def test_exception_is_raised():
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0
