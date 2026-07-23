from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case, cast, DateTime

from app.database.database import SessionLocal
from app.models.models import LoginActivity, AnomalyResult

router = APIRouter(
    prefix="/risk",
    tags=["Risk Analysis"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/users")
def get_user_risk_scores(
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # USER LOGIN BEHAVIOR
    # --------------------------------------------------

    user_activity = (

        db.query(

            LoginActivity.user,

            func.count(LoginActivity.id).label(
                "login_count"
            ),

            func.sum(

                case(

                    (

                        (

                            func.extract(
                                "hour",

                                cast(
                                    LoginActivity.date,
                                    DateTime
                                )

                            ) < 7

                        )

                        |

                        (

                            func.extract(
                                "hour",

                                cast(
                                    LoginActivity.date,
                                    DateTime
                                )

                            ) >= 19

                        )

                    ),

                    1

                ),

                else_=0

            ).label(

                "after_hours_count"

            ),

            func.sum(

                case(

                    (

                        func.extract(

                            "dow",

                            cast(

                                LoginActivity.date,

                                DateTime

                            )

                        ).in_([0, 6]),

                        1

                    ),

                    else_=0

                )

            ).label(

                "weekend_count"

            )

        )

        .filter(

            LoginActivity.user.isnot(None)

        )

        .group_by(

            LoginActivity.user

        )

        .all()

    )


    results = []


    for row in user_activity:

        login_count = row.login_count or 0

        after_hours_count = row.after_hours_count or 0

        weekend_count = row.weekend_count or 0


        if login_count > 0:

            after_hours_ratio = (

                after_hours_count /

                login_count

            )

            weekend_ratio = (

                weekend_count /

                login_count

            )

        else:

            after_hours_ratio = 0

            weekend_ratio = 0


        # --------------------------------------------------
        # RISK SCORE
        # --------------------------------------------------

        risk_score = 0


        # After-hours behavior
        risk_score += after_hours_ratio * 35


        # Weekend behavior
        risk_score += weekend_ratio * 30


        # High login activity
        if login_count > 100:

            risk_score += 20

        elif login_count > 50:

            risk_score += 10

        elif login_count > 20:

            risk_score += 5


        # --------------------------------------------------
        # RISK LEVEL
        # --------------------------------------------------

        if risk_score >= 70:

            risk_level = "Critical"

        elif risk_score >= 45:

            risk_level = "High"

        elif risk_score >= 20:

            risk_level = "Medium"

        else:

            risk_level = "Low"


        results.append(

            {

                "user": row.user,

                "login_count": login_count,

                "after_hours_count": after_hours_count,

                "weekend_count": weekend_count,

                "after_hours_ratio": round(

                    after_hours_ratio,

                    3

                ),

                "weekend_ratio": round(

                    weekend_ratio,

                    3

                ),

                "risk_score": round(

                    risk_score,

                    2

                ),

                "risk_level": risk_level

            }

        )


    # --------------------------------------------------
    # SAVE / UPDATE ANOMALY RESULTS
    # --------------------------------------------------

    for result in results:

        existing = (

            db.query(AnomalyResult)

            .filter(

                AnomalyResult.user == result["user"]

            )

            .first()

        )


        if existing:

            existing.login_count = result[

                "login_count"

            ]

            existing.after_hours_ratio = result[

                "after_hours_ratio"

            ]

            existing.weekend_ratio = result[

                "weekend_ratio"

            ]

            existing.risk_score = result[

                "risk_score"

            ]

            existing.risk_level = result[

                "risk_level"

            ]

        else:

            new_result = AnomalyResult(

                user=result["user"],

                login_count=result["login_count"],

                after_hours_ratio=result[

                    "after_hours_ratio"

                ],

                weekend_ratio=result[

                    "weekend_ratio"

                ],

                risk_score=result["risk_score"],

                risk_level=result["risk_level"],

                anomaly=0,

                anomaly_score=0,

                anomaly_prediction=1

            )

            db.add(new_result)


    db.commit()


    return {

        "total_users": len(results),

        "users": results

    }