import unittest
from conciliador import Conciliador, Transacao

class TestConciliador(unittest.TestCase):

    def test_conciliacao_sem_divergencias(self):
        """Garante que se os dados forem iguais, nenhuma divergência é retornada."""
        sistema = [Transacao("101", 100.0, "2026-05-28")]
        banco = [Transacao("101", 100.0, "2026-05-28")]
        
        conciliador = Conciliador(sistema, banco)
        resultado = conciliador.conciliar()
        
        self.assertEqual(len(resultado), 0)

    def test_divergencia_de_valor(self):
        """Garante que valores diferentes geram um alerta do tipo correto."""
        sistema = [Transacao("102", 150.0, "2026-05-28")]
        banco = [Transacao("102", 145.0, "2026-05-28")]  # 5 reais a menos
        
        conciliador = Conciliador(sistema, banco)
        resultado = conciliador.conciliar()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['tipo_erro'], "Divergência de Valor")
        self.assertEqual(resultado[0]['valor_banco'], 145.0)

    def test_pedido_ausente_no_banco(self):
        """Garante que pedidos que sumiram do banco são detectados."""
        sistema = [Transacao("103", 200.0, "2026-05-28")]
        banco = []  # Banco não registrou nada
        
        conciliador = Conciliador(sistema, banco)
        resultado = conciliador.conciliar()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['tipo_erro'], "Não encontrado no banco")


if __name__ == "__main__":
    unittest.main()