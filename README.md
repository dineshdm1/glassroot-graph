# AI Agents Work Better When You Remove the Chatty Ones

I found that removing the agent who talks the most prevents team failures 48% of the time.

This challenges how people build multi agent AI systems. Most companies add more checking when things go wrong. My data shows they should remove checking instead.

## What I Found

- Tested 126 real conversations where AI teams failed
- Teams work better without their chattiest member almost half the time
- Verification agents cause the most problems (even though their job is to catch mistakes)
- Simple rules work almost as well as complex systems

## The Numbers

- **48% improvement**: Removing chatty agents prevents this many failures
- **47% prediction accuracy**: How often teams would work better without their chattiest member
- **Only 7% behind**: Academic papers get 54% accuracy but only explain failures after they happen

## How to Test This

1. Install requirements: `pip install -r requirements.txt`
2. Get the data (instructions below)
3. Run the main test: `python benchmark.py`
4. Test removing agents: `python test_removal.py`

## Getting the Data

The Who&When dataset comes from research about AI agent failures.

git lfs install
git clone https://huggingface.co/datasets/Kevin355/Who_and_When
# Rename the folder to who_when_data

What Each File Does

benchmark.py - finds which agent types cause the most problems
test_removal.py - shows teams work better without chatty agents
requirements.txt - libraries you need to install

**Results You'll See**
When you run the code, you'll see that verification agents cause way more problems than tool agents. Teams succeed more often when you remove whoever talks the most.

**Why This Matters**
Companies spend millions building AI systems with lots of oversight. This research suggests they could get better results by using less oversight instead.



