

#import

import argparse
import json
from evidence_route.fake_tool import run_fake_inspection
from evidence_route.schemas import InspectionJob

def demo() -> None:
    #argparse
    parser = argparse.ArgumentParser(description="Run a fake inspection job and generate a report.")
    parser.add_argument("--job-file", required=True, help="Path to the JSON file containing the job definition.")

    #read json file
    args = parser.parse_args()
    with open(args.job_file, "r", encoding="utf-8") as f:
        job_data = json.load(f)

    job = InspectionJob(**job_data)
    #run the job
    report = run_fake_inspection(job)

    #output the report
    print(json.dumps(report.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    demo()

