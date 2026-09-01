import subprocess
import sys

def run(cmd: str):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=False)
    if result.returncode != 0:
        print(f"Failed: {cmd}")
        sys.exit(1)

def main():
    print("=== ImobPro.ai - Setup de Desenvolvimento ===\n")

    print("1. Verificando Docker...")
    run("docker --version")

    print("\n2. Subindo serviços (PostgreSQL, Redis, Qdrant)...")
    run("docker-compose up -d postgres redis qdrant")

    print("\n3. Aguardando PostgreSQL...")
    import time
    time.sleep(5)

    print("\n4. Instalando dependências do backend...")
    run("cd backend && pip install -e '.[dev]'")

    print("\n5. Rodando migrações do banco...")
    run("cd backend && alembic upgrade head")

    print("\n6. Populando banco com dados de exemplo...")
    run("cd backend && python -m scripts.seed_db")

    print("\n7. Instalando dependências do frontend...")
    run("cd frontend && npm install")

    print("\n=== Setup completo! ===")
    print("\nPara iniciar o desenvolvimento:")
    print("  Terminal 1: cd backend && uvicorn app.main:app --reload --port 8000")
    print("  Terminal 2: cd frontend && npm run dev")
    print("  Terminal 3: cd backend && celery -A app.celery_app worker --loglevel=info")
    print("\nOu com Docker:")
    print("  docker-compose up")
    print("\nAcesse:")
    print("  Frontend: http://localhost:3000")
    print("  Backend API: http://localhost:8000/docs")
    print("  Qdrant: http://localhost:6333/dashboard")

if __name__ == "__main__":
    main()
