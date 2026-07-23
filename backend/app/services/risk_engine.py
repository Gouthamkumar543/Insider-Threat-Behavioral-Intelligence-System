def calculate_risk_score(login_logs, file_logs):
    score = 0

    # Login Analysis
    for log in login_logs:
        if not log.success:
            score += 20

        if log.location.lower() == "unknown":
            score += 25

    # File Activity Analysis
    for file in file_logs:

        action = file.action.lower()

        if action == "read":
            score += 10

        elif action == "write":
            score += 20

        elif action == "delete":
            score += 30

    return score