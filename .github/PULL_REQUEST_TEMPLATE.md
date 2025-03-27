## Description

Please include a summary of the change and which issue is fixed. Please also include relevant context. List any dependencies that are required for this change. Ideally we avoid introducing any new third party dependencies in `pyproject.toml` unless absolutely necessary, because this makes the project more susceptible to breaking whenever a third party library is updated. At the moment it's very lightweight with only `requests` as a requirement.

#### Fixes # (issue)

## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Requires a documentation revision

## Testing

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce. Please also list any relevant details for your test configuration

- [ ] Test A
- [ ] Test B

#### Test Configuration

* Library version:
* OS:
* Toolchain:

## Checklist

- [ ] My PR is for one issue, rather than for multiple unrelated fixes.
- [ ] My code follows the style guidelines of this project. I have applied a Linter (recommended: Pycharm's code formatter) to make my whitespace consistent with the rest of the project.
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
- [ ] I have checked my code and corrected any misspellings
- [ ] The Harmony API is not broken by my change to the Harmony Python library
- [ ] I add third party dependencies only when necessary. If I changed the requirements, it changes in `pyproject.toml`
- [ ] If I introduced a new feature, I documented it ideally in the README examples so that people will know how to use it.
