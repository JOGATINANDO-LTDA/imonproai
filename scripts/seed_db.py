import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import AsyncSessionLocal, engine
from app.core.security import hash_password
from app.models.base import Agent, Contact, Base, Property, Tenant, User


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        tenant = Tenant(
            name="Imobiliária Modelo",
            slug="imob-modelo",
            plan="professional",
            commercial_rules="1. Não oferecer descontos > 5%\n2. Agendar visitas manhã/tarde\n3. Priorizar imóveis com vista",
        )
        db.add(tenant)
        await db.flush()

        admin = User(
            tenant_id=tenant.id,
            email="admin@imobpro.ai",
            hashed_password=hash_password("admin123"),
            full_name="Administrador",
            role="admin",
        )
        db.add(admin)

        agent = Agent(
            tenant_id=tenant.id,
            name="Ana - Assistente Virtual",
            voice_id="nova",
            llm_model="gpt-4o",
            phone_number="+5511999999999",
            whatsapp_instance="imob-modelo",
        )
        db.add(agent)

        contacts_data = [
            {"name": "Maria Silva", "whatsapp": "+5511987654321", "email": "maria@email.com", "status": "qualified", "score": 85},
            {"name": "João Santos", "whatsapp": "+5511976543210", "email": "joao@email.com", "status": "new", "score": 40},
            {"name": "Ana Oliveira", "phone": "+5511965432109", "email": "ana@email.com", "status": "proposal", "score": 70},
            {"name": "Pedro Costa", "whatsapp": "+5511954321098", "status": "won", "score": 95},
            {"name": "Lucia Ferreira", "email": "lucia@email.com", "status": "lost", "score": 20},
        ]

        for c in contacts_data:
            contact = Contact(tenant_id=tenant.id, **c)
            db.add(contact)

        properties_data = [
            {"title": "Apartamento 2 quartos - Vila Mariana", "price": 450000, "address": "Rua dos Jardins, 123", "bedrooms": 2, "bathrooms": 1, "area_m2": 65, "property_type": "apartment"},
            {"title": "Casa 3 quartos - Pinheiros", "price": 850000, "address": "Rua Funchal, 456", "bedrooms": 3, "bathrooms": 2, "area_m2": 180, "property_type": "house"},
            {"title": "Studio - Consolação", "price": 280000, "address": "Rua Augusta, 789", "bedrooms": 1, "bathrooms": 1, "area_m2": 35, "property_type": "apartment"},
            {"title": "Cobertura 4 quartos - Itaim Bibi", "price": 2500000, "address": "Rua João Cachoeira, 321", "bedrooms": 4, "bathrooms": 4, "area_m2": 350, "property_type": "apartment"},
            {"title": "Terreno 500m² - Alphaville", "price": 600000, "address": "Alameda dos Anapurus, 654", "bedrooms": 0, "bathrooms": 0, "area_m2": 500, "property_type": "land"},
        ]

        for p in properties_data:
            prop = Property(tenant_id=tenant.id, **p)
            db.add(prop)

        await db.commit()
        print("Seed executado com sucesso!")
        print(f"  Tenant: {tenant.name} (ID: {tenant.id})")
        print(f"  Admin: admin@imobpro.ai / admin123")
        print(f"  Agentes: 1 | Contatos: 5 | Imóveis: 5")


if __name__ == "__main__":
    asyncio.run(seed())
