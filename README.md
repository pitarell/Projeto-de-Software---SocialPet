# SocialPet

MVP acadêmico desenvolvido para a LivrePet. O sistema registra doações e saídas, controla saldos, preserva o histórico e sinaliza itens que atingiram o estoque mínimo. O projeto contribui para o ODS 12, meta 12.5.

## Recursos

- Autenticação Django com perfis de gestor e voluntário;
- bloqueio por 15 minutos após cinco tentativas de login inválidas;
- manutenção de categorias e produtos por gestores;
- movimentações transacionais, sem permissão de estoque negativo;
- filtros de estoque, histórico e alertas de reposição;
- interface responsiva, navegação por teclado e foco visível;
- sessão encerrada após 30 minutos de inatividade;
- doze testes automatizados.

## Requisitos

Python 3.12, Django 5.2 LTS e SQLite. Em produção, o projeto utiliza Gunicorn e WhiteNoise.

## Instalação local

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Acesse `http://127.0.0.1:8000`. Os dados de demonstração são fictícios: usuário `carlos` e senha `SocialPet#2026`. Troque a senha se o ambiente for compartilhado.

## Testes

```bash
python manage.py check
python manage.py test
```

## Implantação Linux

Defina as variáveis de `.env.example` no serviço de hospedagem, mantendo `DEBUG=False`, uma `SECRET_KEY` exclusiva, HTTPS e armazenamento persistente para `db.sqlite3`. Execute as migrações e a coleta de estáticos antes de iniciar o servidor:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn socialpet.wsgi:application --bind 0.0.0.0:8000
```

O SQLite é adequado ao MVP e exige volume persistente. Para maior concorrência em evolução futura, recomenda-se migrar para PostgreSQL. Execute auditoria periódica com `pip-audit -r requirements.txt` e mantenha as dependências atualizadas.

## Perfis e segurança

Gestores administram categorias e produtos. Gestores e voluntários registram movimentações e consultam estoque e histórico. O Django fornece hash PBKDF2-SHA256, proteção CSRF, escape contra XSS e consultas parametrizadas pelo ORM. Em produção são habilitados cookies seguros, redirecionamento HTTPS, HSTS e `DEBUG=False`.

## Estrutura

A aplicação segue arquitetura monolítica MVT: `core/models.py` contém o domínio, `core/services.py` concentra a movimentação transacional, `core/views.py` trata os fluxos e `templates/`/`core/static/` compõem a interface.
