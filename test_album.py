from projetoAlbumCopa import retornaFigurinhasRepetidas, retornaFaltantes, testConnection, retornaFigurinhas


class TestConnection():
    def test_01(self):
        con = testConnection()
        assert isinstance(con, bool)
        assert con == True

class TestRetornaFigurinhas():
    def test_01(self):
        sublista = retornaFigurinhas()
        assert isinstance(sublista, list)
        assert len(sublista) == 73
        assert isinstance(sublista[0], int)
        assert sublista[11] == 123

class TestRetornaFigurinhasRepetidas():
    def test_02(self):
        sublista = retornaFigurinhasRepetidas()
        assert isinstance(sublista, list)
        assert len(sublista) == 2
        assert isinstance(sublista[1], int)
        assert sublista[0] == 370
        assert sublista[1] == 523

class TestRetornaFaltantes():
    def test_03(self):
        sublista = retornaFaltantes()
        assert isinstance(sublista, list)
        assert len(sublista) == 597
        assert isinstance(sublista[1], int)
        assert sublista[5] == 6
