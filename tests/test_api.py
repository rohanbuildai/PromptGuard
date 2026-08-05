import json
import requests
from collections import defaultdict

API_URL = "http://127.0.0.1:5000/analyze"


def run_tests():

    with open("tests/test_prompts.json", "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    total_tests = len(test_cases)
    total_passed = 0

    category_stats = defaultdict(lambda: {"passed": 0, "total": 0})

    print("=" * 90)
    print("PromptGuard API Test Suite")
    print("=" * 90)

    for index, test in enumerate(test_cases, start=1):

        category = test["category"]
        expected = test["expected"]
        prompt = test["prompt"]

        category_stats[category]["total"] += 1

        try:

            response = requests.post(
                API_URL,
                json={
                    "prompt": prompt
                },
                timeout=10
            )

            if response.status_code != 200:

                print(f"\n[{index}] ❌ HTTP {response.status_code}")
                print(f"Prompt   : {prompt}")
                print(f"Response : {response.text}")
                continue

            result = response.json()

            actual = result["overall_risk"]

            if isinstance(expected, list):
                passed = actual in expected
            else:
                passed = actual == expected

            if passed:
                total_passed += 1
                category_stats[category]["passed"] += 1

            print("-" * 90)
            print(f"Test #{index}")
            print(f"Category : {category}")
            print(f"Prompt   : {prompt}")
            print(f"Expected : {expected}")
            print(f"Actual   : {actual}")
            print(f"Result   : {'✅ PASS' if passed else '❌ FAIL'}")

        except requests.exceptions.RequestException as error:

            print("-" * 90)
            print(f"Test #{index}")
            print("❌ Connection Error")
            print(error)

    print("\n")
    print("=" * 90)
    print("CATEGORY SUMMARY")
    print("=" * 90)

    for category, stats in category_stats.items():

        accuracy = (stats["passed"] / stats["total"]) * 100

        print(
            f"{category:<20}"
            f"{stats['passed']:>2}/{stats['total']:<2}"
            f"   {accuracy:.2f}%"
        )

    overall_accuracy = (total_passed / total_tests) * 100

    print("\n")
    print("=" * 90)
    print("FINAL SUMMARY")
    print("=" * 90)
    print(f"Total Tests      : {total_tests}")
    print(f"Passed           : {total_passed}")
    print(f"Failed           : {total_tests - total_passed}")
    print(f"Overall Accuracy : {overall_accuracy:.2f}%")
    print("=" * 90)


if __name__ == "__main__":
    run_tests()