from graphs.workflow import app

query = input("Enter research query: ")

result = app.invoke({

    "query": query

})

print("\n\nPLANNER OUTPUT:\n")

print(result["planner_output"])

print("\n\nSEARCH RESULTS:\n")

for idx, item in enumerate(result["search_results"], start=1):

    print(f"\nResult {idx}")

    print("Title:", item["title"])

    print("Link:", item["link"])

    print("Snippet:", item["snippet"])


print("\n\nEXTRACTED CONTENT:\n")

for idx, article in enumerate(result["extracted_content"], start=1):

    print(f"\nARTICLE {idx}")

    print("TITLE:", article["title"])

    print("CONTENT:\n")

    print(article["text"][:1000])

    print("\n" + "="*50)

print("\n\nRESEARCH SUMMARY:\n")

print(result["research_summary"])

print("\n\nREFLECTION ANALYSIS:\n")

print(result["reflection"])

print("\n\nREFLECTION ANALYSIS:\n")

print(result["reflection"])