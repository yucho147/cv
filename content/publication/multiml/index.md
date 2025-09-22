---
title: Event Classification with Multi-step Machine Learning

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here 
# and it will be replaced with their full name and linked to their profile.
authors:
- Masahiko Saito
- Tomoe Kishimoto
- admin
- Taichi Itoh
- Yoshiaki Umeda
- Junichi Tanaka
- Yutaro Iiyama
- Ryu Sawada
- Koji Terashi

# Author notes (optional)

# Schedule page publish date (NOT publication's date).
publishDate: "2021-06-07T00:00:00Z"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: In *25th International Conference on Computing in High-Energy and Nuclear Physics(vCHEP 2021)*

abstract: The usefulness and value of Multi-step Machine Learning (ML), where a task is organized into connected sub-tasks with known intermediate inference goals, as opposed to a single large model learned end-to-end without intermediate sub-tasks, is presented. Pre-optimized ML models are connected and better performance is obtained by re-optimizing the connected one. The selection of an ML model from several small ML model candidates for each sub-task has been performed by using the idea based on Neural Architecture Search (NAS). In this paper, Differentiable Architecture Search (DARTS) and Single Path One-Shot NAS (SPOS-NAS) are tested, where the construction of loss functions is improved to keep all ML models smoothly learning. Using DARTS and SPOS-NAS as an optimization and selection as well as the connections for multi-step machine learning systems, we find that (1) such a system can quickly and successfully select highly performant model combinations, and (2) the selected models are consistent with baseline algorithms, such as grid search, and their outputs are well controlled.


# Summary. An optional shortened abstract.

tags: []

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

links:
  - type: pdf
    url: 'publication/multiml/2106.02301.pdf'

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: [icepp_project]
# - example

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---
