import csv

class Transacao:
    """Representa cada linha de dados de uma transação financeira."""
    def __init__(self, id_pedido: str, valor: float, data: str):
        self.id_pedido = id_pedido
        self.valor = valor
        self.data = data

    def __repr__(self):
        return f"Transacao(ID: {self.id_pedido}, Valor: {self.valor}, Data: {self.data})"


class LeitorCSV:
    """Classe responsável por ler, validar e tratar erros em arquivos CSV de entrada."""
    
    @staticmethod
    def carregar_transacoes(caminho_arquivo: str) -> list:
        transacoes = []
        
        try:
            with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                
                colunas_obrigatorias = {'id_pedido', 'valor', 'data'}
                if leitor.fieldnames and not colunas_obrigatorias.issubset(set(leitor.fieldnames)):
                    raise KeyError(f"Colunas obrigatórias ausentes. O arquivo precisa ter: {colunas_obrigatorias}")

                for linha in leitor:
                    try:
                        id_pedido = linha['id_pedido'].strip()
                        valor = float(linha['valor'].strip())
                        data = linha['data'].strip()
                        
                        transacoes.append(Transacao(id_pedido, valor, data))
                    except ValueError:
                        print(f"[AVISO] Linha ignorada por dados inválidos no arquivo {caminho_arquivo}: {linha}")
                        continue
                        
        except FileNotFoundError:
            print(f"[ERRO CRÍTICO] O arquivo '{caminho_arquivo}' não foi encontrado. Verifique o caminho.")
            return []
        except KeyError as e:
            print(f"[ERRO DE FORMATO] {e}")
            return []
        except Exception as e:
            print(f"[ERRO INESPERADO] Ocorreu um problema ao ler {caminho_arquivo}: {e}")
            return []

        return transacoes


class Conciliador:
    """O motor do sistema. Cruza os dados e gera o relatório de divergências."""
    def __init__(self, transacoes_sistema: list, transacoes_banco: list):
        self.sistema = transacoes_sistema
        self.banco = transacoes_banco
        self.divergencias = []

    def conciliar(self) -> list:
        if not self.sistema and not self.banco:
            print("[AVISO] Não há dados suficientes para realizar a conciliação.")
            return []

        banco_dict = {t.id_pedido: t for t in self.banco}
        
        banco_dict = {t.id_pedido: t for t in self.banco}
        
        for t_sistema in self.sistema:
            if t_sistema.id_pedido not in banco_dict:
                self.divergencias.append({
                    "id_pedido": t_sistema.id_pedido,
                    "tipo_erro": "Não encontrado no banco",
                    "valor_sistema": t_sistema.valor,
                    "valor_banco": None
                })
            else:
                t_banco = banco_dict[t_sistema.id_pedido]
                if round(t_sistema.valor, 2) != round(t_banco.valor, 2):
                    self.divergencias.append({
                        "id_pedido": t_sistema.id_pedido,
                        "tipo_erro": "Divergência de Valor",
                        "valor_sistema": t_sistema.valor,
                        "valor_banco": t_banco.valor
                    })
                    
        return self.divergencias

    def exportar_para_csv(self, caminho_saida: str = "divergencias.csv"):
        """Gera um arquivo CSV com as divergências encontradas para auditoria do financeiro."""
        if not self.divergencias:
            print("[INFO] Nenhuma divergência para exportar.")
            return

        try:
            with open(caminho_saida, mode='w', encoding='utf-8', newline='') as arquivo:
                colunas = ['id_pedido', 'tipo_erro', 'valor_sistema', 'valor_banco']
                escritor = csv.DictWriter(arquivo, fieldnames=colunas)
                
                escritor.writeheader()
                for erro in self.divergencias:
                    escritor.writerow(erro)
                    
            print(f"[SUCESSO] Relatório de divergências exportado para '{caminho_saida}'!")
        except Exception as e:
            print(f"[ERRO] Não foi possível exportar o arquivo de saída: {e}")

if __name__ == "__main__":
    print("Iniciando Motor de Conciliação Financeira...\n")
    print("Carregando os dados dos arquivos CSV...")
    
    dados_sistema = LeitorCSV.carregar_transacoes("sistema.csv")
    dados_banco = LeitorCSV.carregar_transacoes("banco.csv")

    if dados_sistema and dados_banco:
        motor = Conciliador(dados_sistema, dados_banco)
        resultados = motor.conciliar()

        print("\n=== RELATÓRIO DE DIVERGÊNCIAS ENCONTRADAS ===")
        if not resultados:
            print("Sucesso! Tudo 100% conciliado. Nenhum erro encontrado.")
        else:
            for erro in resultados:
                print(f"Pedido {erro['id_pedido']}: {erro['tipo_erro']} | "
                      f"Sistema: R${erro['valor_sistema']} vs Banco: R${erro['valor_banco']}")
            
            print("\n--------------------------------------------------")
            motor.exportar_para_csv()
