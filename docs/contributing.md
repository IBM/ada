# Contributing to ADA

It's awesome to have you here! Contributions are more than welcome :) Thanks for taking the time to contribute :heart:

### How to report a bug

Bugs can be reported as a Github Issue. Make sure you're telling a story... in other words, tell us how to reproduce this bug, describe the problem you're facing and what you expected to happen.

Feel free to use images, gifs, code snippets and more to give us as much information as possible.

### How to open a Pull Request

If you want to help us to improve our codebase, you can open a Pull Request and we will gladly discuss your suggestion. By opening a PR, you can fix a bug, add or change some functionality, improve performance, or even update our documentation.

When opening a PR, please include:

1. **Motivation**: explain why you decided to make this change and how it will positively affect ADA;
2. **Description of your change**: detail exactly what your code does, step by step;
3. **Verification process**: tell us what you did to make sure your change has the desired effects, i.e., the tests scenarios you created.

### Change in the approach: Introduction of the "nonprod" branch

Recently, we implemented a change in the development approach to better align with our new CI/CD practices. Cirrus CI/CD requires that the default branch must match the production environment. To accommodate this requirement and maintain a testing environment, we have introduced a new branch called `nonprod`.

### Branch `nonprod`

From now on, all change PRs must be merged to the `nonprod` branch. This branch will serve as a testing environment, allowing changes to be reviewed and tested before being integrated into the `master` branch.

#### Recommended Workflow

1. **Create a New Branch:** Create a new branch to work on.

2. **Make Changes:** Make the necessary changes in your branch.

3. **Open a PR to `nonprod`:** Upon completing your changes, open a PR targeting the `nonprod` branch for review.

4. **Testing and Review:** The team will review your changes and, if necessary, perform additional tests on the `nonprod` branch.

5. **Integration with `master`:** After successful review and testing, your changes will be integrated into the `master` branch.
