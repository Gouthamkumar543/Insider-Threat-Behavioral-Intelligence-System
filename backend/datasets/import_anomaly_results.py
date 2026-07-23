import os
import sys
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.database.database import (
    engine,
    SessionLocal,
    Base
)

from app.models.models import AnomalyResult


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "processed",
    "anomaly_results.csv"
)


print("Creating database tables...")

Base.metadata.create_all(
    bind=engine
)

print("Loading anomaly results...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Records found: {len(df)}"
)

db = SessionLocal()

try:

    db.query(AnomalyResult).delete()

    for _, row in df.iterrows():

        result = AnomalyResult(
            user=str(row["user"]),
            login_count=int(
                row["login_count"]
            ),
            unique_devices=int(
                row["unique_devices"]
            ),
            after_hours_logins=int(
                row["after_hours_logins"]
            ),
            weekend_logins=int(
                row["weekend_logins"]
            ),
            after_hours_ratio=float(
                row["after_hours_ratio"]
            ),
            weekend_ratio=float(
                row["weekend_ratio"]
            ),
            anomaly_prediction=int(
                row["anomaly_prediction"]
            ),
            anomaly_score=float(
                row["anomaly_score"]
            ),
            anomaly=int(
                row["anomaly"]
            ),
            risk_score=float(
                row["risk_score"]
            ),
            risk_level=str(
                row["risk_level"]
            )
        )

        db.add(result)

    db.commit()

    print(
        "Anomaly results imported successfully."
    )

    total = db.query(
        AnomalyResult
    ).count()

    print(
        f"Database records: {total}"
    )

except Exception as error:

    db.rollback()

    print(
        f"Import failed: {error}"
    )

finally:

    db.close()