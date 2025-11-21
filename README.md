## ✅ Commit Rules (Read Before Committing)
https://www.conventionalcommits.org/en/v1.0.0/

# Table of Contents
- **References:** [References](./references.md)
- **Setup:** [Setup](./Setup.md)

 --- 

This project follows **Conventional Commits**.  
Your commit message must clearly explain *what* changed and *why*.  
If your commit message says things like "fix stuff", rewrite it.

### Format
<type>[optional scope]: <description>


### Allowed types

| Type | When to use it |
|------|----------------|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug or broken behavior |
| `docs` | Changing documentation (README, comments, etc.) |
| `refactor` | Improving code structure without changing functionality |
| `chore` | Maintenance tasks (dependency update, config change, etc.) |
| `test` | Adding or modifying tests |

### Rules

1. **One logical change per commit.**  
   If you fixed a bug and updated docs, that's **two commits**, not one.

2. **Write in the imperative form.**  
   ✅ `feat: add scraping for match data`  
   ❌ `added scraping for match data`

3. **Be specific.**  
   “Better scraping” is useless. What changed?

4. **No essay commits.**
   The message should explain the change, not tell a life story.

---

### Examples

✅ Good:

feat(scraper): extract player age from detailed table
fix(parser): correct market value selector after DOM change
docs: add commit rules to README

❌ Bad:

final fixes
stuff works now
update file

---
# Merge Approval

This repo uses a teammate approval process to keep code quality high and avoid broken changes. Follow the steps below whenever you open a pull request.

## 1. Create Your Pull Request
- Push your changes to a feature branch.
- Open a PR into the main branch.
- Provide a clear title and a short description of **what** you changed and **why** you changed it.

## 2. Request a Review
- Assign at least **one teammate** as a reviewer.
- Make sure your PR is small enough to review quickly. Large PRs slow everyone down.

## 3. What Reviewers Check
A teammate must verify that:
- The code runs and doesn’t break existing functionality.
- The logic is clean and maintainable.
- The changes match the project’s style and structure.


## 4. Approval
A merge is allowed only when:
- The reviewer has marked the PR as **Approved**.
- All comments that require action are resolved.


## 5. Merge
Once approved, the PR can be merged using the standard **Merge** button.  
Avoid merging your own PR without approval unless it’s an emergency.

---

Keeping the process simple makes reviews fast and the project stable.```


---

### TL;DR  
If someone needs to read the diff to understand your commit message,  
your commit message sucks. Be better.

