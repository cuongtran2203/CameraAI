"""
Seed script to create initial users
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.db.database import Base, settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_seed_users():
    # Create engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        # Get or create a default company
        result = await session.execute(text('SELECT id, name FROM companies LIMIT 1'))
        company = result.fetchone()

        if not company:
            company_id = "comp-main-001"
            await session.execute(
                text("INSERT INTO companies (id, name, code, address, phone) VALUES (:id, :name, :code, :address, :phone)"),
                {"id": company_id, "name": "CameraAI Company", "code": "CAM001", "address": "123 Main Street", "phone": "+1234567890"}
            )
            await session.commit()
            company = (company_id, "CameraAI Company")
            print(f"Created company: {company[1]}")

        company_id = company[0]

        # Get or create a default branch
        result = await session.execute(text('SELECT id, name FROM branches LIMIT 1'))
        branch = result.fetchone()

        if not branch:
            branch_id = "branch-main-001"
            await session.execute(
                text("INSERT INTO branches (id, company_id, name, code, address) VALUES (:id, :company_id, :name, :code, :address)"),
                {"id": branch_id, "company_id": company_id, "name": "Main Branch", "code": "BR001", "address": "123 Main Street"}
            )
            await session.commit()
            branch = (branch_id, "Main Branch")
            print(f"Created branch: {branch[1]}")

        branch_id = branch[0]

        # Create test users
        test_users = [
            {
                "email": "admin@cameraai.com",
                "password": "admin123",
                "full_name": "Admin User",
                "role": "admin"
            },
            {
                "email": "manager@cameraai.com",
                "password": "manager123",
                "full_name": "Manager User",
                "role": "manager"
            },
            {
                "email": "staff@cameraai.com",
                "password": "staff123",
                "full_name": "Staff User",
                "role": "staff"
            }
        ]

        for user_data in test_users:
            # Check if user already exists
            result = await session.execute(
                text("SELECT email FROM users WHERE email = :email"),
                {"email": user_data["email"]}
            )
            existing = result.fetchone()

            if existing:
                print(f"User {user_data['email']} already exists, skipping...")
                continue

            hashed_password = pwd_context.hash(user_data["password"])
            user_id = f"usr-{user_data['role']}-{user_data['email'].split('@')[0]}"

            await session.execute(
                text("""
                    INSERT INTO users (id, email, password_hash, full_name, role, branch_id, is_active)
                    VALUES (:id, :email, :password, :full_name, :role, :branch_id, :is_active)
                """),
                {
                    "id": user_id,
                    "email": user_data["email"],
                    "password": hashed_password,
                    "full_name": user_data["full_name"],
                    "role": user_data["role"],
                    "branch_id": branch_id,
                    "is_active": True
                }
            )
            print(f"Created user: {user_data['email']}")

        # Seed Food Items first
        print("\nSeeding Food Items...")
        food_item_ids = []
        food_names = ["Burger", "Pizza", "Pasta", "Salad", "Fried Rice", "Sandwich", "Tacos", "Sushi"]

        for i, name in enumerate(food_names):
            food_id = f"food-{i+1:03d}"
            food_item_ids.append(food_id)
            await session.execute(
                text("""
                    INSERT INTO food_items (id, name, category, branch_id, is_active)
                    VALUES (:id, :name, :category, :branch_id, true)
                    ON CONFLICT (id) DO NOTHING
                """),
                {"id": food_id, "name": name, "category": "Main Dish", "branch_id": branch_id}
            )
        print(f"Created {len(food_item_ids)} food items")

        # Seed Food QC Results
        print("Seeding Food QC Results...")
        food_items = [(fid,) for fid in food_item_ids]

        result = await session.execute(text('SELECT id FROM cameras LIMIT 1'))
        camera = result.fetchone()

        result = await session.execute(text('SELECT id FROM staff LIMIT 3'))
        staff_list = result.fetchall()

        camera_id = camera[0] if camera else None
        staff_ids = [s[0] for s in staff_list] if staff_list else [None]

        import random
        from datetime import datetime, timedelta

        qc_results = []

        for i in range(20):
            # Similarity score should be 0.xx (e.g., 0.85 = 85%)
            similarity = round(random.uniform(0.75, 0.99), 4)
            status = "passed" if similarity > 0.85 else "failed"

            checked_at = datetime.utcnow() - timedelta(minutes=random.randint(1, 120))
            food_item_id = random.choice(food_items)[0] if food_items else None

            await session.execute(
                text("""
                    INSERT INTO food_qc_results
                    (id, camera_id, food_item_id, result_status, similarity_score,
                     color_match, portion_match, topping_present, proof_image_url,
                     staff_id, checked_by, checked_at)
                    VALUES
                    (:id, :camera_id, :food_item_id, :result_status, :similarity_score,
                     :color_match, :portion_match, :topping_present, :proof_image_url,
                     :staff_id, :checked_by, :checked_at)
                    ON CONFLICT (id) DO NOTHING
                """),
                {
                    "id": f"qc-result-{i+1:03d}",
                    "camera_id": camera_id,
                    "food_item_id": food_item_id,
                    "result_status": status,
                    "similarity_score": similarity,
                    "color_match": similarity > 0.85,
                    "portion_match": similarity > 0.88,
                    "topping_present": random.choice([True, False]),
                    "proof_image_url": None,
                    "staff_id": random.choice(staff_ids),
                    "checked_by": "ai",
                    "checked_at": checked_at
                }
            )

        print(f"Created 20 food QC results (passed > 85%, failed <= 85%)")

        await session.commit()
        print("\nAll test users ready!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_seed_users())
