from sqlalchemy import create_engine, text 

engine = create_engine("postgresql+psycopg2://postgres.mhumhvlaihdfgegupqeu:yazanYAZAN2003@aws-0-ap-south-1.pooler.supabase.com:6543/postgres")

with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    print(result.all())