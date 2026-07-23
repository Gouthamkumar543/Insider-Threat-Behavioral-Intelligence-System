import pandas as pd
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.models import FileAccess

FILE_PATH = "datasets/file.csv"


def import_file_access():

    db: Session = SessionLocal()

    try:

        df = pd.read_csv(FILE_PATH)

        print(f"Total file records found: {len(df)}")

        batch_size = 5000
        records = []

        for _, row in df.iterrows():

            record = FileAccess(
                id=str(row["id"]),
                date=str(row["date"]),
                user=str(row["user"]),
                pc=str(row["pc"]),
                filename=str(row["filename"])
            )

            records.append(record)

            if len(records) >= batch_size:

                db.bulk_save_objects(records)
                db.commit()

                print(f"Inserted {batch_size} records")

                records = []

        if records:

            db.bulk_save_objects(records)
            db.commit()

            print(f"Inserted {len(records)} records")

        print("File access data imported successfully")

    except Exception as e:

        db.rollback()

        print("Import failed:")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":

    import_file_access()