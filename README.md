# knowledge-base
A personal repository for organizing diverse technical knowledge, tips, and best practices across various domains.

## Repository Structure

### Main Categories

- **[deep-learning/](deep-learning/)** - Deep learning theory, implementations, and applications
  - [theory/](deep-learning/theory/) - Theoretical knowledge and mathematical foundations
  - [coding/](deep-learning/coding/) - Code implementations and examples
  - [applications/](deep-learning/applications/) - Real-world applications and use cases
  - [resources/](deep-learning/resources/) - Additional references and learning materials

- **[programming/](programming/)** - General programming knowledge and tips
  - Algorithms and data structures
  - Design patterns
  - Code quality and best practices
  - Language-specific tips

- **[web-development/](web-development/)** - Web development knowledge
  - Frontend technologies (HTML, CSS, JavaScript)
  - Backend frameworks
  - DevOps and deployment
  - Performance optimization

- **[data-science/](data-science/)** - Data science and analytics
  - Data analysis techniques
  - Statistical methods
  - Data visualization
  - Tools and libraries

- **[general-tips/](general-tips/)** - General development tips and tricks
  - Productivity tools
  - Development environment setup
  - Debugging techniques
  - Version control best practices

### Tooling
- **[tools/](tools/)** - Automation scripts and utilities
  - `ckn/` - "Create Knowledge Note" CLI tool for generating markdown templates.

## Workflow

To maintain consistency and ease of use, this repository uses a custom CLI tool called `ckn` (Create Knowledge Note) to generate new entries.

### How to Add New Knowledge

1. **Run the command:**
   ```bash
   ckn
   ```

2. **Select a Category:**
   Choose the appropriate directory from the interactive list (e.g., `deep-learning/theory`).

3. **Enter Title:**
   Provide a concise title for the note. The filename will be automatically generated with the date (e.g., `YYYY-MM-DD-title.md`).

4. **Select a Template:**
   Choose the template that best fits the content:

   | ID | Template Name | Best For |
   |----|---------------|----------|
   | **1** | **Standard** | General knowledge, summaries, and tips. |
   | **2** | **Coding** | Implementation logs, bug fixes, troubleshooting, and code snippets. |
   | **3** | **Theory** | Mathematical concepts, paper summaries, and deep learning theory (includes LaTeX support). |

## Setup

To enable the `ckn` command, install the local package located in the `tools` directory:

```bash
# Install the script in editable mode
pip install -e ./tools
```

Once installed, you can run `ckn` from anywhere in your terminal.

## About

This repository serves as a comprehensive knowledge base for technical topics, organized to facilitate learning and quick reference. Each directory contains markdown files documenting various aspects of software development and related fields.

## How to Use

1. Browse categories to find topics of interest.
2. Each directory contains a README.md with an overview and index.
3. Individual markdown files contain detailed explanations, code examples, and references.
4. Use search functionality (or grep) to find specific topics quickly.

## Contributing

This is a personal knowledge base, but feel free to use it as inspiration for organizing your own knowledge repository.
