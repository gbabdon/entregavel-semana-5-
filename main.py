
import csv
import re
from datetime import datetime


class FormatoInvalidoError(Exception):
    """Exceção para dados que não atendem às regras do sistema."""
    pass


# Expressões regulares
PADRAO_EMAIL = re.compile(
    r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
)

PADRAO_CPF = re.compile(
    r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
)

PADRAO_TELEFONE = re.compile(
    r"^(?:\(\d{2}\)\s?)?9?\d{4}-?\d{4}$"
)

PADRAO_DATA = re.compile(
    r"^\d{2}/\d{2}/\d{4}$"
)

CAMPOS_OBRIGATORIOS = {
    "nome",
    "email",
    "cpf",
    "telefone",
    "data_nascimento",
}


def validar_email(email):
    return bool(PADRAO_EMAIL.fullmatch(email))


def validar_cpf(cpf):
    # Valida o formato, não os dígitos verificadores.
    return bool(PADRAO_CPF.fullmatch(cpf))


def validar_telefone(telefone):
    return bool(PADRAO_TELEFONE.fullmatch(telefone))


def validar_data(data):
    if not PADRAO_DATA.fullmatch(data):
        return False

    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_registro(registro):
    # Acesso por chave: identifica colunas ausentes.
    try:
        nome = registro["nome"].strip()
        email = registro["email"].strip()
        cpf = registro["cpf"].strip()
        telefone = registro["telefone"].strip()
        data = registro["data_nascimento"].strip()
    except KeyError as erro:
        raise KeyError(
            f"Coluna obrigatória ausente: {erro.args[0]}"
        ) from erro

    if not nome:
        raise FormatoInvalidoError("Nome não informado.")

    erros = []

    if not validar_email(email):
        erros.append("E-mail inválido")

    if not validar_cpf(cpf):
        erros.append("Formato de CPF inválido")

    if not validar_telefone(telefone):
        erros.append("Telefone inválido")

    if not validar_data(data):
        erros.append("Data inválida")

    if erros:
        raise FormatoInvalidoError("; ".join(erros))

    return {
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "telefone": telefone,
        "data_nascimento": data,
    }


def analisar_arquivo(caminho):
    validos = []
    invalidos = []
    total = 0

    arquivo = None

    try:
        arquivo = open(
            caminho,
            mode="r",
            encoding="utf-8",
            newline=""
        )

        leitor = csv.DictReader(arquivo)

        if leitor.fieldnames is None:
            raise ValueError("O arquivo CSV está vazio.")

        colunas = set(leitor.fieldnames)
        faltantes = CAMPOS_OBRIGATORIOS - colunas

        if faltantes:
            raise KeyError(
                "Colunas ausentes no CSV: "
                + ", ".join(sorted(faltantes))
            )

        for numero_linha, registro in enumerate(leitor, start=2):
            total += 1

            try:
                resultado = validar_registro(registro)
            except FormatoInvalidoError as erro:
                invalidos.append({
                    "linha": numero_linha,
                    "nome": registro.get("nome", "Não informado"),
                    "motivo": str(erro),
                })
            else:
                validos.append(resultado)

    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' não encontrado.")

    except (OSError, UnicodeError) as erro:
        print(f"Erro ao ler o arquivo: {erro}")

    except (KeyError, ValueError) as erro:
        print(f"Erro na estrutura dos dados: {erro}")

    else:
        print("Leitura e análise do arquivo concluídas.")

    finally:
        if arquivo is not None:
            arquivo.close()
        print("Processamento finalizado.")

    return total, validos, invalidos


def gerar_relatorio(total, validos, invalidos):
    aprovados = len(validos)
    reprovados = len(invalidos)

    percentual = (aprovados / total * 100) if total else 0

    linhas = [
        "=" * 55,
        "       RELATÓRIO DE ANÁLISE DE DADOS",
        "=" * 55,
        f"Total de registros: {total}",
        f"Registros válidos: {aprovados}",
        f"Registros inválidos: {reprovados}",
        f"Taxa de aprovação: {percentual:.2f}%",
        "",
        "--- REGISTROS VÁLIDOS ---",
    ]

    if validos:
        for pessoa in validos:
            linhas.append(
                f"Nome: {pessoa['nome']} | "
                f"E-mail: {pessoa['email']} | "
                f"CPF: {pessoa['cpf']}"
            )
    else:
        linhas.append("Nenhum registro válido.")

    linhas.append("")
    linhas.append("--- REGISTROS INVÁLIDOS ---")

    if invalidos:
        for pessoa in invalidos:
            linhas.append(
                f"Linha {pessoa['linha']} - "
                f"Nome: {pessoa['nome']} | "
                f"Motivo: {pessoa['motivo']}"
            )
    else:
        linhas.append("Nenhum registro inválido.")

    linhas.append("=" * 55)

    relatorio = "\n".join(linhas)
    print("\n" + relatorio)

    try:
        with open(
            "relatorio.txt", "w", encoding="utf-8"
        ) as arquivo:
            arquivo.write(relatorio + "\n")
    except OSError as erro:
        print(f"Não foi possível salvar o relatório: {erro}")
    else:
        print("Relatório salvo em relatorio.txt.")


def main():
    total, validos, invalidos = analisar_arquivo("dados.csv")
    gerar_relatorio(total, validos, invalidos)


if __name__ == "__main__":
    main()
