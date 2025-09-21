SUMMARY_PROMPT = """
Given step data: {steps}
and sleep data: {sleep}
Write a short correlation analysis.
"""

def make_summary_prompt(steps, sleep):
    return SUMMARY_PROMPT.format(steps=steps, sleep=sleep)
