from sqlalchemy import create_engine
from HW7.models import Base

engine = create_engine('postgresql://mr.green:280992@localhost:5433/dbhw7')
Base.metadata.drop_all(engine)
