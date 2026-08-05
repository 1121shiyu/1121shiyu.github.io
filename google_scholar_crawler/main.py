from scholarly import scholarly
import json
from datetime import datetime
import os
import sys
import traceback


def main():

    print("===================================")
    print("Google Scholar crawler started")
    print("===================================")
    sys.stdout.flush()


    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID")


    if not scholar_id:
        raise Exception(
            "GOOGLE_SCHOLAR_ID is missing. "
            "Please check GitHub Actions Secrets."
        )


    print(f"Google Scholar ID loaded: {scholar_id}")
    sys.stdout.flush()


    # Search author
    print("Searching Google Scholar author...")
    sys.stdout.flush()


    author = scholarly.search_author_id(
        scholar_id
    )


    print("Author found:")
    print(author.get("name", "Unknown"))
    sys.stdout.flush()



    # Fill author information
    print("Fetching author details...")
    sys.stdout.flush()


    scholarly.fill(
        author,
        sections=[
            "basics",
            "indices",
            "counts",
            "publications"
        ]
    )


    print("Author information fetched.")
    sys.stdout.flush()



    author["updated"] = str(datetime.now())


    if "publications" in author:
        author["publications"] = {
            v["author_pub_id"]: v
            for v in author["publications"]
        }


    print("Generating JSON data...")
    sys.stdout.flush()



    os.makedirs(
        "results",
        exist_ok=True
    )


    # Full data
    with open(
        "results/gs_data.json",
        "w",
        encoding="utf-8"
    ) as outfile:

        json.dump(
            author,
            outfile,
            ensure_ascii=False,
            indent=2
        )



    # Shields.io badge data

    shieldio_data = {

        "schemaVersion": 1,

        "label": "citations",

        "message": str(
            author.get(
                "citedby",
                0
            )
        ),

    }


    with open(
        "results/gs_data_shieldsio.json",
        "w",
        encoding="utf-8"
    ) as outfile:

        json.dump(
            shieldio_data,
            outfile,
            ensure_ascii=False,
            indent=2
        )


    print("===================================")
    print("Google Scholar crawler finished")
    print(
        f"Citations: {author.get('citedby',0)}"
    )
    print("===================================")

    sys.stdout.flush()



if __name__ == "__main__":

    try:

        main()


    except Exception as e:

        print("===================================")
        print("Crawler failed")
        print(str(e))
        print("===================================")

        traceback.print_exc()

        sys.stdout.flush()

        raise
