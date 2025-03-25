# 📊 API - PIA Empresa (IBGE)

**Desenvolvido para o Desafio Técnico Backend - Observatório da Indústria (FIEC)**

Esta API fornece acesso performático e seguro aos dados da **Pesquisa Industrial Anual - Empresa (PIA Empresa)** do IBGE, com suporte a filtros dinâmicos, análises estatísticas, autenticação segura, cache inteligente e CI/CD automatizado.

---

## 🚀 Tecnologias Utilizadas

| Camada          | Tecnologia                   |
| --------------- | ---------------------------- |
| Backend         | FastAPI                      |
| Banco de Dados  | PostgreSQL                   |
| ORM             | SQLAlchemy (async) + Alembic |
| Autenticação    | OAuth2 + JWT (`python-jose`) |
| Cache           | Redis (`aioredis`)           |
| Containerização | Docker + Docker Compose      |
| Testes          | Pytest + HTTPX               |
| CI/CD           | GitHub Actions               |
| Deploy          | VPS Linux + PM2 + Nginx      |

---

## 📦 Estrutura do Projeto

```bash
app/
├── core/           # Configurações, banco, cache
├── modules/
│   ├── auth/       # Cadastro, login, JWT
│   ├── users/      # CRUD de usuários
│   ├── pia/        # Consulta de dados da Tabela 1842
│   ├── analytics/  # Análises agregadas (top setores, evolução, comparação UF)
│   └── admin/      # /status e /health
├── scripts/        # Seed de dados
├── tests/          # Testes unitários e integração
```

---

## 🔐 Funcionalidades

- ✅ Cadastro e login de usuários com senha criptografada
- ✅ Proteção de rotas com JWT
- ✅ Consulta filtrável por ano, UF, variável e setor (CNAE)
- ✅ Endpoints de análise:
  - Top 5 setores por ano
  - Evolução histórica por variável
  - Comparação entre UFs
- ✅ Cache automático com Redis para requisições frequentes
- ✅ Testes automatizados (auth, users, pia, analytics)
- ✅ Status/health da API
- ✅ Documentação via Swagger e Redoc

---

## 📈 Performance e Escalabilidade

- Banco relacional: **PostgreSQL** pela robustez, integridade e performance.
- Conexão assíncrona com `asyncpg`.
- **Redis** para cache de respostas filtradas.
- Arquitetura modular com separação clara de camadas.

---

## 🧪 Testes

Execute os testes com:

```bash
pytest
```

---

## 🐳 Rodando com Docker

```bash
# Build e subida dos serviços (API + banco + redis)
docker-compose up --build

# Após subir o container:
docker exec -it nome_da_api bash
alembic upgrade head
```

---

## 🧬 Executando localmente (sem Docker)

1. Crie o banco manualmente:

```bash
psql -U postgres -c "CREATE DATABASE pia;"
```

2. Instale as dependências:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure o `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/pia
SECRET_KEY=super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30
REDIS_URL=redis://localhost:6379
```

4. Aplique as migrations:

```bash
alembic upgrade head
```

5. Popule os dados:

```bash
PYTHONPATH=. python app/scripts/seed_pia.py
```

6. Rode a API:

```bash
uvicorn app.main:app --reload
```

7. Acesse a documentação:

- http://localhost:8000/docs
- http://localhost:8000/redoc

---

## 📌 Autor

> Desenvolvido por **Wylder Menezes**  
> Engenheiro de Software | Backend Specialist  
> [linkedin.com/in/wyldersilva](https://www.linkedin.com/in/wylder-menezes/)
