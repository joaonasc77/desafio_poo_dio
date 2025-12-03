from abc import ABC, abstractmethod
from datetime import datetime

#Classes do Cliente
class Cliente:
    """Representa um cliente genérico que pode ter uma ou mais contas."""

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []  # lista de contas vinculadas ao cliente

    def executar_transacao(self, conta, operacao):
        """Executa uma operação (depósito, saque, etc.) em uma conta específica."""
        operacao.aplicar(conta)

    def vincular_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Cliente do tipo pessoa física, com informações pessoais."""

    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


#Classes relacionadas a conta
class Conta:
    """Modelo base para contas bancárias."""

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, cliente, numero):
        """Cria uma nova instância de conta."""
        return cls(numero, cliente)

    # --- Propriedades da conta ---
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # --- Operações básicas ---
    def sacar(self, valor):
        """Realiza saque se o valor for válido e houver saldo."""
        if valor <= 0:
            print("Valor inválido para saque.")
            return False

        if valor > self._saldo:
            print("Não há saldo suficiente.")
            return False

        self._saldo -= valor
        print("Saque concluído.")
        return True

    def depositar(self, valor):
        """Realiza depósito se o valor for positivo."""
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False

        self._saldo += valor
        print("Depósito realizado.")
        return True


class ContaCorrente(Conta):
    """Conta corrente com limite e quantidade máxima de saques."""

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.max_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método de saque adicionando limites específicos."""

        # Conta quantos saques já foram realizados
        saques_realizados = [t for t in self.historico.transacoes if t["tipo"] == "Saque"]

        if len(saques_realizados) >= self.max_saques:
            print("Limite diário de saques atingido.")
            return False

        if valor > self.limite:
            print("Valor excede o limite permitido.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return (
            f"Agência: {self.agencia}\n"
            f"Conta:   {self.numero}\n"
            f"Titular: {self.cliente.nome}"
        )

#Histórico de Transações
class Historico:
    """Armazena todas as transações realizadas em uma conta."""

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar(self, transacao):
        """Registra uma transação com tipo, valor e data/hora."""
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })


#Operações de Saque e Depósito
class Transacao(ABC):
    """Classe abstrata para operações financeiras."""

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def aplicar(self, conta):
        pass


class Saque(Transacao):
    """Representa uma operação de saque."""

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def aplicar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.registrar(self)


class Deposito(Transacao):
    """Representa uma operação de depósito."""

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def aplicar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.registrar(self)

#Executando o código
if __name__ == "__main__":
    # Criar cliente pessoa física
    cliente = PessoaFisica(
        nome="João",
        nascimento="2000-01-01",
        cpf="12345678900",
        endereco="Rua Exemplo, 123"
    )

    # Criar conta para o cliente
    conta = ContaCorrente.criar_conta(cliente, numero=1)
    cliente.vincular_conta(conta)

    #Fazer um depósito
    deposito = Deposito(200)
    cliente.executar_transacao(conta, deposito)

    #Fazer um saque
    saque = Saque(50)
    cliente.executar_transacao(conta, saque)

    #Mostrar saldo final
    print("\nSaldo final:", conta.saldo)

    #Mostrar histórico de transações
    print("\nHistórico:")
    for t in conta.historico.transacoes:
        print(t)
