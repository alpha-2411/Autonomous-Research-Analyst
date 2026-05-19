import os
from datetime import datetime


def save_report(query, report):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"reports/report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:

        f.write("QUERY:\n")
        f.write(query)

        f.write("\n\n")

        f.write("REPORT:\n")
        f.write(report)

    return filename