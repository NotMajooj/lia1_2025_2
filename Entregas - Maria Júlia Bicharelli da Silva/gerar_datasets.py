import os

# Define o nome do diretório de datasets
DATASET_DIR = "datasets"

# Conteúdo completo para o arquivo da pessoa
pessoa_csv_data = """data,tipo,categoria,descricao,valor
2024-01-05 10:00:00,ganho,Salário,Pagamento mensal,4500.00
2024-01-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-01-09 19:00:00,gasto,Alimentação,Supermercado do mês,710.30
2024-01-12 20:15:00,gasto,Lazer,Cinema com amigos,85.50
2024-01-15 08:00:00,gasto,Transporte,Gasolina,180.20
2024-01-18 13:00:00,gasto,Alimentação,iFood,52.80
2024-01-22 18:00:00,ganho,Freelance,Job design,950.00
2024-01-25 11:00:00,gasto,Assinaturas,Netflix e Spotify,65.80
2024-01-28 15:00:00,gasto,Compras,Roupa nova,280.00
2024-01-30 09:00:00,gasto,Transporte,Uber para reunião,31.50
2024-02-05 10:00:00,ganho,Salário,Pagamento mensal,4500.00
2024-02-07 14:00:00,gasto,Saúde,Consulta médica,250.00
2024-02-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-02-10 19:30:00,gasto,Alimentação,Jantar fora,180.00
2024-02-13 09:00:00,gasto,Transporte,Manutenção carro,320.00
2024-02-16 11:00:00,gasto,Educação,Livro técnico,120.70
2024-02-20 16:00:00,gasto,Compras,Presente de aniversário,150.00
2024-02-25 21:00:00,gasto,Lazer,Show,220.00
2024-02-28 10:00:00,ganho,Presente,Presente da avó,200.00
2024-03-05 10:00:00,ganho,Salário,Pagamento mensal,4500.00
2024-03-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-03-10 18:00:00,gasto,Alimentação,Supermercado,680.40
2024-03-12 09:00:00,gasto,Transporte,Uber,28.90
2024-03-15 15:00:00,gasto,Saúde,Farmácia,95.60
2024-03-19 17:00:00,ganho,Freelance,Projeto de redação,700.00
2024-03-23 20:00:00,gasto,Lazer,Bar com amigos,130.00
2024-03-27 11:00:00,gasto,Assinaturas,Amazon Prime,19.90
2024-03-30 14:00:00,gasto,Compras,Tênis de corrida,450.00
2024-04-05 10:00:00,ganho,Salário,Pagamento mensal,4500.00
2024-04-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-04-11 19:00:00,gasto,Alimentação,Feira,150.80
2024-04-14 08:30:00,gasto,Transporte,Gasolina,190.00
2024-04-18 13:00:00,gasto,Alimentação,Almoço trabalho,35.00
2024-04-22 16:00:00,gasto,Saúde,Dentista,300.00
2024-04-26 18:00:00,gasto,Lazer,Viagem de fim de semana,800.00
2024-04-30 20:00:00,gasto,Alimentação,Delivery,60.20
2024-05-05 10:00:00,ganho,Salário,Pagamento mensal,4500.00
2024-05-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-05-10 19:00:00,gasto,Alimentação,Supermercado,750.00
2024-05-13 09:00:00,gasto,Transporte,Uber,22.50
2024-05-17 14:00:00,ganho,Investimentos,Dividendos,350.00
2024-05-21 17:00:00,gasto,Compras,Eletrônico,900.00
2024-05-25 21:00:00,gasto,Lazer,Festa,180.00
2024-05-29 11:00:00,gasto,Assinaturas,Globoplay,24.90
2024-06-05 10:00:00,ganho,Salário,Pagamento mensal,4650.00
2024-06-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-06-11 18:30:00,gasto,Alimentação,Restaurante,220.00
2024-06-14 08:00:00,gasto,Transporte,Gasolina,200.50
2024-06-18 15:00:00,gasto,Saúde,Exame de rotina,400.00
2024-06-22 19:00:00,ganho,Freelance,Consultoria,1200.00
2024-06-26 10:00:00,gasto,Educação,Curso online,350.00
2024-06-30 16:00:00,gasto,Compras,Decoração para casa,180.00
2024-07-05 10:00:00,ganho,Salário,Pagamento mensal,4650.00
2024-07-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-07-10 20:00:00,gasto,Alimentação,Supermercado,720.90
2024-07-13 09:00:00,gasto,Transporte,Uber,33.00
2024-07-17 14:00:00,gasto,Saúde,Remédios,75.20
2024-07-21 17:00:00,gasto,Lazer,Passeio no parque,50.00
2024-07-25 21:00:00,gasto,Assinaturas,HBO Max,29.90
2024-07-29 11:00:00,gasto,Compras,Videogame,350.00
2024-08-05 10:00:00,ganho,Salário,Pagamento mensal,4650.00
2024-08-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-08-11 18:30:00,gasto,Alimentação,Açougue,180.60
2024-08-14 08:00:00,gasto,Transporte,Gasolina,210.00
2024-08-18 15:00:00,ganho,Investimentos,Venda de ações,600.00
2024-08-22 19:00:00,gasto,Lazer,Happy hour,90.00
2024-08-26 10:00:00,gasto,Saúde,Fisioterapia,150.00
2024-08-30 16:00:00,gasto,Compras,Material de escritório,110.00
2024-09-05 10:00:00,ganho,Salário,Pagamento mensal,4650.00
2024-09-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-09-10 20:00:00,gasto,Alimentação,Supermercado,800.10
2024-09-13 09:00:00,gasto,Transporte,Uber,27.80
2024-09-17 14:00:00,ganho,Freelance,Revisão de texto,450.00
2024-09-21 17:00:00,gasto,Educação,Workshop,280.00
2024-09-25 21:00:00,gasto,Lazer,Teatro,160.00
2024-09-29 11:00:00,gasto,Assinaturas,Disney+,27.90
2024-10-01 15:00:00,gasto,Compras,Sapatos,320.00
2024-10-03 09:00:00,gasto,Transporte,Passagem de ônibus,55.40
2024-10-05 10:00:00,ganho,Salário,Pagamento mensal,4650.00
2024-10-06 13:00:00,gasto,Alimentação,Padaria,45.60
2024-10-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-10-10 18:00:00,gasto,Alimentação,Supermercado,690.00
2024-10-12 11:00:00,gasto,Lazer,Feriado na praia,550.00
2024-10-15 08:30:00,gasto,Transporte,Gasolina,205.00
2024-10-18 16:00:00,gasto,Saúde,Oculista,350.00
2024-10-22 20:00:00,gasto,Alimentação,Pizza,70.00
2024-10-25 10:00:00,ganho,Presente,Bônus da empresa,1000.00
2024-10-28 14:00:00,gasto,Compras,Presente para mãe,200.00
2024-10-31 09:00:00,gasto,Transporte,Uber,29.10
2024-11-05 10:00:00,ganho,Salário,Pagamento mensal,4650.00
2024-11-08 12:30:00,gasto,Moradia,Aluguel,1200.00
2024-11-10 19:30:00,gasto,Alimentação,Supermercado,730.25
2024-11-14 20:00:00,gasto,Lazer,Jantar romântico,300.00
2024-11-18 08:00:00,gasto,Transporte,Revisão do carro,500.00
2024-11-22 13:00:00,gasto,Alimentação,Almoço com cliente,80.00
2024-11-26 17:00:00,gasto,Saúde,Vacina,180.00
2024-11-30 15:00:00,gasto,Compras,Black Friday,1100.00
"""

# Conteúdo completo para o arquivo da empresa
empresa_csv_data = """data,tipo,categoria,descricao,valor
2024-01-10 15:00:00,gasto,Moradia,Aluguel do escritório,2500.00
2024-01-12 10:00:00,gasto,Outro,Pagamento fornecedor A,3800.00
2024-01-15 16:30:00,ganho,Outro,Venda de produtos,9500.00
2024-01-20 11:00:00,ganho,Outro,Prestação de serviço B,5200.00
2024-01-25 14:00:00,gasto,Educação,Marketing e publicidade,1250.00
2024-01-31 09:00:00,gasto,Outro,Salários funcionários,12500.00
2024-02-02 17:00:00,gasto,Outro,Conta de luz e internet,880.00
2024-02-08 10:00:00,ganho,Outro,Venda de produtos,6300.00
2024-02-14 11:30:00,gasto,Outro,Material de escritório,450.70
2024-02-18 09:00:00,gasto,Outro,Pagamento fornecedor C,2100.00
2024-02-22 14:00:00,ganho,Outro,Serviço de consultoria,4000.00
2024-02-28 09:00:00,gasto,Outro,Salários funcionários,12500.00
2024-03-05 15:00:00,gasto,Moradia,Aluguel do escritório,2500.00
2024-03-07 16:00:00,gasto,Educação,Campanha Google Ads,800.00
2024-03-11 10:00:00,ganho,Outro,Venda de produtos,11500.00
2024-03-15 09:30:00,gasto,Outro,Pagamento fornecedor B,3250.00
2024-03-20 13:00:00,ganho,Outro,Prestação de serviço A,6800.00
2024-03-25 17:00:00,gasto,Outro,Manutenção de equipamentos,750.00
2024-03-31 09:00:00,gasto,Outro,Salários funcionários,12500.00
2024-04-03 11:00:00,gasto,Outro,Conta de água,350.00
2024-04-09 14:00:00,ganho,Outro,Venda de produtos,8900.00
2024-04-12 10:00:00,gasto,Outro,Pagamento fornecedor A,3800.00
2024-04-18 16:00:00,ganho,Outro,Serviço de desenvolvimento,15000.00
2024-04-24 09:00:00,gasto,Educação,Patrocínio de evento,2000.00
2024-04-30 09:00:00,gasto,Outro,Salários funcionários,13000.00
2024-05-05 15:00:00,gasto,Moradia,Aluguel do escritório,2500.00
2024-05-08 10:30:00,gasto,Outro,Compra de matéria-prima,5500.00
2024-05-14 11:00:00,ganho,Outro,Venda de produtos,12800.00
2024-05-19 15:00:00,gasto,Outro,Transportadora,980.00
2024-05-23 10:00:00,ganho,Outro,Prestação de serviço C,4500.00
2024-05-28 17:00:00,gasto,Outro,Impostos,4200.00
2024-05-31 09:00:00,gasto,Outro,Salários funcionários,13000.00
2024-06-04 14:00:00,gasto,Outro,Serviços de contabilidade,1200.00
2024-06-10 16:00:00,ganho,Outro,Venda de produtos,9200.00
2024-06-13 11:00:00,gasto,Outro,Pagamento fornecedor B,3250.00
2024-06-18 10:00:00,ganho,Outro,Serviço de manutenção,3000.00
2024-06-25 13:00:00,gasto,Educação,Treinamento de equipe,1500.00
2024-06-30 09:00:00,gasto,Outro,Salários funcionários,13000.00
2024-07-05 15:00:00,gasto,Moradia,Aluguel do escritório,2500.00
2024-07-09 10:00:00,gasto,Outro,Pagamento fornecedor C,2100.00
2024-07-15 11:30:00,ganho,Outro,Venda de produtos,14000.00
2024-07-20 14:00:00,ganho,Outro,Prestação de serviço A,7200.00
2024-07-26 16:00:00,gasto,Outro,Software e licenças,890.00
2024-07-31 09:00:00,gasto,Outro,Salários funcionários,13000.00
2024-08-02 17:00:00,gasto,Outro,Conta de telefone,420.00
2024-08-08 10:00:00,ganho,Outro,Venda de produtos,11200.00
2024-08-12 11:00:00,gasto,Outro,Pagamento fornecedor A,3800.00
2024-08-18 15:00:00,ganho,Outro,Serviço de consultoria,5500.00
2024-08-24 10:00:00,gasto,Educação,Marketing digital,1800.00
2024-08-31 09:00:00,gasto,Outro,Salários funcionários,13500.00
2024-09-05 15:00:00,gasto,Moradia,Aluguel do escritório,2500.00
2024-09-09 14:00:00,gasto,Outro,Compra de equipamentos,4500.00
2024-09-15 16:00:00,ganho,Outro,Venda de produtos,16500.00
2024-09-20 10:00:00,gasto,Outro,Pagamento fornecedor B,3250.00
2024-09-26 11:00:00,ganho,Outro,Prestação de serviço B,6000.00
2024-09-30 09:00:00,gasto,Outro,Salários funcionários,13500.00
2024-10-03 17:00:00,gasto,Outro,Despesas de viagem,1300.00
2024-10-07 10:00:00,ganho,Outro,Venda de produtos,9800.00
2024-10-11 11:00:00,gasto,Outro,Pagamento fornecedor C,2100.00
2024-10-17 14:00:00,ganho,Outro,Serviço de desenvolvimento,18000.00
2024-10-23 10:00:00,gasto,Educação,Feira de negócios,2500.00
2024-10-31 09:00:00,gasto,Outro,Salários funcionários,13500.00
2024-11-05 15:00:00,gasto,Moradia,Aluguel do escritório,2500.00
2024-11-08 10:00:00,gasto,Outro,Bônus de fim de ano,5000.00
2024-11-14 11:00:00,ganho,Outro,Venda de produtos,13200.00
2024-11-19 15:00:00,gasto,Outro,Pagamento fornecedor A,3800.00
2024-11-24 10:00:00,ganho,Outro,Prestação de serviço A,8000.00
2024-11-30 09:00:00,gasto,Outro,Salários funcionários,13500.00
2024-12-03 17:00:00,gasto,Outro,Confraternização da empresa,1800.00
2024-12-09 10:00:00,ganho,Outro,Venda de produtos de Natal,22000.00
2024-12-12 11:00:00,gasto,Outro,Impostos de fim de ano,6800.00
2024-12-18 14:00:00,ganho,Outro,Serviço de consultoria,6500.00
2024-12-20 10:00:00,gasto,Outro,13º Salário,13500.00
2025-01-05 15:00:00,gasto,Moradia,Aluguel do escritório,2600.00
2025-01-10 10:00:00,ganho,Outro,Venda de produtos,11000.00
2025-01-15 11:00:00,gasto,Outro,Pagamento fornecedor B,3400.00
2025-01-20 14:00:00,ganho,Outro,Prestação de serviço B,5800.00
2025-01-25 10:00:00,gasto,Educação,Marketing 2025,2000.00
2025-01-31 09:00:00,gasto,Outro,Salários funcionários,14000.00
2025-02-03 17:00:00,gasto,Outro,Contas de início de ano,1100.00
2025-02-09 10:00:00,ganho,Outro,Venda de produtos,9500.00
2025-02-13 11:00:00,gasto,Outro,Renovação de licenças,1200.00
2025-02-19 14:00:00,ganho,Outro,Serviço de manutenção,3500.00
2025-02-28 09:00:00,gasto,Outro,Salários funcionários,14000.00
2025-03-05 15:00:00,gasto,Moradia,Aluguel do escritório,2600.00
2025-03-10 10:00:00,gasto,Outro,Pagamento fornecedor C,2300.00
2025-03-15 11:00:00,ganho,Outro,Venda de produtos,13500.00
2025-03-20 14:00:00,ganho,Outro,Prestação de serviço A,7800.00
2025-03-25 10:00:00,gasto,Outro,Compra de insumos,4800.00
2025-03-31 09:00:00,gasto,Outro,Salários funcionários,14000.00
"""

def create_csv_file(filename, csv_content):
    """Função para criar um arquivo CSV a partir de uma string."""
    # Garante que o diretório 'datasets' exista
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        print(f"Diretório '{DATASET_DIR}' criado.")

    filepath = os.path.join(DATASET_DIR, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            # O método strip() remove espaços/linhas em branco do início e do fim
            f.write(csv_content.strip())
        print(f"Arquivo '{filepath}' criado com sucesso!")
    except IOError as e:
        print(f"Erro ao escrever o arquivo '{filepath}': {e}")

# Bloco principal que executa o script
if __name__ == "__main__":
    print("Iniciando a criação dos datasets de exemplo...")
    create_csv_file("pessoa_exemplo.csv", pessoa_csv_data)
    create_csv_file("empresa_exemplo.csv", empresa_csv_data)
    print("\nProcesso concluído!")
    print("Os arquivos estão prontos na sua pasta 'datasets'.")