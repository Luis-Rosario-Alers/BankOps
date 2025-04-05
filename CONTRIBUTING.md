# Contributing to the BankOps project

Thank you for your interest in contributing to the BankOps project!
We welcome contributions from everyone.
This guide explains how you can help improve the project.

## Ways to Contribute 🤝

There are many ways you can contribute to the project:

1. **Report Bugs**
   - Use the GitHub issue tracker
   - Include detailed steps to reproduce
   - Describe expected vs. actual behavior
   - Include system information

2. **Suggest Enhancements**
   - Use the GitHub issue tracker
   - Describe the enhancement in detail
   - Explain why this would be useful
   - Tag with "enhancement"

3. **Submit Pull Requests**
   - Fork the repository
   - Create a new branch for your work
   - Make your changes
   - Submit a pull request
   - Link related issues

4. **Improve Documentation**
   - Fix typos or unclear instructions
   - Add examples where helpful
   - Update outdated information
   - Translate documentation

5. **Review Pull Requests**
   - Help review other's contributions
   - Test proposed changes
   - Provide constructive feedback

## Contribution Process

1. **Before Starting Work**
   - Check existing issues and PRs
   - Discuss major changes in an issue first
   - Get assigned to an issue
   - Fork the repository

2. **Making Changes**
   - Create a new branch from `develop`
   - Make focused, specific changes
   - Test your changes thoroughly
   - Update documentation if needed

3. **Submitting Changes**
   - Push changes to your fork
   - Create a pull request
   - Fill out the PR template
   - Request review
   - Respond to feedback

4. **After Submission**
   - Be patient waiting for review
   - Make requested changes
   - Keep your PR up to date
   - Help review other PRs

## Issue Guidelines

When creating an issue, please:

1. **Check Existing Issues**
   - Search open and closed issues
   - Avoid duplicates
   - Reference related issues

2. **Use Issue Templates**
   - Bug report template
   - Feature request template
   - Follow the template structure

3. **Provide Information**
   - Clear, descriptive title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected behavior
   - Screenshots if applicable

We will do our best to review your issue as soon as possible.

## Pull Request Guidelines

When submitting a PR:

1. **PR Title and Description**
   - Clear, descriptive title
   - Reference related issues
   - Explain your changes
   - List testing done

2. **Keep PRs Focused**
   - One feature/fix per PR
   - Small, manageable changes
   - Split large changes into multiple PRs

3. **Review Process**
   - Request review from maintainers
   - Address feedback promptly
   - Be open to suggestions
   - Update PR as needed

## Commit Message Guidelines

We use Conventional Commits with emojis to add visual context to our commit messages. Here's how to format your commits:

```env
<emoji>: <subject>

[optional body]
[optional footer(s)]
```

### Type

Should be part of gitmoji:

- `feat`: ✨ A new feature
- `fix`: 🐛 A bug fix
- `docs`: 📝 Documentation only changes
- `style`: 💄 Changes that do not affect the meaning of the code
- `refactor`: ♻️ A code change that neither fixes a bug nor adds a feature
- `perf`: ⚡️ A code change that improves performance
- `test`: ✅ Adding missing tests or correcting existing tests
- `build`: 📦 Changes that affect the build system or external dependencies
- `ci`: 👷 Changes to our CI configuration files and scripts
- `chore`: 🔧 Other changes that don't modify src or test files
- `revert`: ⏪️ Reverts a previous commit

### Subject

The subject contains a succinct description of the change:

- use the imperative, present tense: "change" not "changed" nor "changes"
- don't capitalize the first letter
- no dot (.) at the end

### Examples

```
✨: add temperature adjustment feature
🐛: resolve input validation error
📝: update installation steps
♻️: simplify emissions calculation logic
✅: add integration tests for weather service
🔧: update dependency versions
⚡️: optimize database queries
🚀: add automated release workflow
```

### Full Example

```
✨ feat(calculator): add CO2 calculation feature

Add new feature to calculate CO2 emissions based on fuel consumption.
The calculation takes into account:
- Fuel type
- Amount used
- Temperature adjustment

Closes #123
```

### Emoji Quick Reference

Common emojis used in our commits:

| Emoji | Code           | Description                        |
|-------|----------------|------------------------------------|
| ✨    | `:sparkles:`   | New feature                        |
| 🐛    | `:bug:`        | Fix a bug                          |
| 📝    | `:memo:`       | Add or update documentation        |
| ♻️    | `:recycle:`    | Refactor code                      |
| ✅    | `:white_check_mark:` | Add or update tests         |
| 💄    | `:lipstick:`   | Add or update UI and styles       |
| ⚡️    | `:zap:`        | Improve performance                |
| 🔧    | `:wrench:`     | Add or update configuration       |
| 🚀    | `:rocket:`     | Deploy changes                    |
| 👷    | `:construction_worker:` | Add or update CI build   |
| 📦    | `:package:`    | Add or update compiled files      |
| ⏪️    | `:rewind:`     | Revert changes                    |

### Breaking Changes

When making breaking changes, add `BREAKING CHANGE:` in the commit body or footer:

```
💥 remove deprecated endpoints

BREAKING CHANGE: The following endpoints have been removed:
- /v1/calculate
- /v1/export

Migration guide: Use /v2/calculate and /v2/export instead.
```


### VS Code Extension

For VS Code users,
we recommend
installing the [Gitmoji Commits](https://marketplace.visualstudio.com/items?itemName=seatonjiang.gitmoji-vscode) extension to help format commit messages according to these conventions.

For more information on the project, please refer to the [DEVELOPER](./docs/DEVELOPER.md) file.

## Code of Conduct⚖️

Please note that this project is governed by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Security Code of Conduct🔒

If any security vulnerabilities are found in this project, please refer to the [Security Code of Conduct🔒](SECURITY.md) for more information on how to handle notifying us.

## Getting Help🤚

Make an issue or create a discussion. We are glad to help anyone that needs it.
